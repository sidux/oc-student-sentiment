import os
import csv
from typing import Dict

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace
from opentelemetry.trace import get_tracer_provider, SpanKind
from opentelemetry.propagate import extract
from opentelemetry.metrics import get_meter_provider, set_meter_provider
from opentelemetry.sdk.metrics import MeterProvider
import logging
from dotenv import load_dotenv
from transformers import BertTokenizer, TFBertForSequenceClassification
import tensorflow as tf
from azure.monitor.events.extension import track_event

# Load environment variables
load_dotenv()

# Configure Application Insights
if os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING"):
    configure_azure_monitor()

# Set up OpenTelemetry tracer and logger
tracer = trace.get_tracer(__name__, tracer_provider=get_tracer_provider())
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Set up metrics
# meter_provider = MeterProvider()
# set_meter_provider(meter_provider)
# meter = meter_provider.get_meter(__name__)

# Define custom metrics
# feedback_counter = meter.create_counter(
#     name="feedback_submissions",
#     description="Counts the number of feedback submissions",
#     unit="1"
# )

APP_DIR = os.path.dirname(os.path.abspath(__file__)) + "/"
MODEL_PATH = APP_DIR + "./my_bert_model"
FEEDBACK_FILE = APP_DIR + "feedback.csv"

# Ensure feedback CSV exists
if not os.path.exists(FEEDBACK_FILE):
    with open(FEEDBACK_FILE, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["text", "predicted_label", "confidence", "correct"])

app = FastAPI(title="Tweet Sentiment API", version="1.0")
FastAPIInstrumentor.instrument_app(app)
app.mount("/static", StaticFiles(directory=APP_DIR + "static"), name="static")

# Load model and tokenizer
tokenizer = BertTokenizer.from_pretrained(MODEL_PATH)
model = TFBertForSequenceClassification.from_pretrained(MODEL_PATH)

# Define label map
label_map = {0: "Negative", 1: "Neutral", 2: "Positive"}


def classify_tweet(text: str, tokenizer, model, max_len=30):
    encoded = tokenizer.encode_plus(
        text,
        add_special_tokens=True,
        max_length=max_len,
        truncation=True,
        padding='max_length',
        return_attention_mask=True,
        return_tensors='tf'
    )
    outputs = model(encoded['input_ids'], attention_mask=encoded['attention_mask'])
    probs = tf.nn.softmax(outputs.logits, axis=-1)
    predicted_id = tf.argmax(probs, axis=1).numpy()[0]
    confidence = float(tf.reduce_max(probs, axis=1).numpy()[0])
    label_str = label_map[predicted_id]
    return label_str, confidence


class TweetInput(BaseModel):
    text: str


@app.post("/predict", summary="Predict sentiment of a tweet")
def predict_sentiment(input_data: TweetInput, request: Request) -> Dict:
    label, confidence = classify_tweet(input_data.text, tokenizer, model)

    # Log the prediction to Application Insights
    logger.info(
        "Prediction made",
        extra={
            "text": input_data.text,
            "predicted_label": label,
            "confidence": confidence,
        }
    )

    # Return a JSON-friendly dict
    return {
        "label": label,
        "confidence": confidence
    }


templates = Jinja2Templates(directory=APP_DIR + "templates")


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


class FeedbackInput(BaseModel):
    text: str
    label: str
    confidence: float
    correct: bool


@app.post("/feedback", summary="Submit feedback on prediction")
def store_feedback(feedback_data: FeedbackInput, request: Request):
    # Store feedback in CSV
    with open(FEEDBACK_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            feedback_data.text,
            feedback_data.label,
            feedback_data.confidence,
            feedback_data.correct
        ])

    # Log feedback to Application Insights
    track_event("feedback", {
        "text": feedback_data.text,
        "label": feedback_data.label,
        "correct": str(feedback_data.correct)
    })

    logger.info(
        "Feedback received",
        extra={
            "text": feedback_data.text,
            "label": feedback_data.label,
            "confidence": feedback_data.confidence,
            "correct": feedback_data.correct,
        }
    )

    # Increment feedback counter
    # feedback_counter.add(1, {"correct": feedback_data.correct})

    return {"message": "Feedback submitted successfully"}
