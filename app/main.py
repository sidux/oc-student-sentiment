import csv
import os
from typing import Dict

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from transformers import BertTokenizer, TFBertForSequenceClassification
import tensorflow as tf

APP_DIR = os.path.dirname(os.path.abspath(__file__)) + "/"

MODEL_PATH = APP_DIR + "./my_bert_model"
FEEDBACK_FILE = APP_DIR + "feedback.csv"

# Ensure feedback file exists
if not os.path.exists(FEEDBACK_FILE):
    with open(FEEDBACK_FILE, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["text", "predicted_label", "confidence", "correct"])

# 1. Load model and tokenizer at startup (or lazily in the endpoint)
print("Loading model and tokenizer...")
tokenizer = BertTokenizer.from_pretrained(MODEL_PATH)
model = TFBertForSequenceClassification.from_pretrained(MODEL_PATH)

# 2. Your classify_tweet function goes here
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


# 3. Define FastAPI app
app = FastAPI(title="Tweet Sentiment API", version="1.0")

# Mount static files
app.mount("/static", StaticFiles(directory=APP_DIR + "static"), name="static")


# 4. Request Body Schema
class TweetInput(BaseModel):
    text: str


# 5. Prediction Endpoint
@app.post("/predict", summary="Predict sentiment of a tweet")
def predict_sentiment(input_data: TweetInput) -> Dict:
    """
    Expects {"text": "some tweet content"}
    Returns {"label": "...", "confidence": 0.95}
    """
    label, confidence = classify_tweet(input_data.text, tokenizer, model)

    # Return a JSON-friendly dict
    return {
        "label": label,
        "confidence": confidence
    }


templates = Jinja2Templates(directory=APP_DIR + "templates")


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Feedback Endpoint
class FeedbackInput(BaseModel):
    text: str
    label: str
    confidence: float
    correct: bool


@app.post("/feedback", summary="Submit feedback on prediction")
def store_feedback(feedback_data: FeedbackInput):
    with open(FEEDBACK_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            feedback_data.text,
            feedback_data.label,
            feedback_data.confidence,
            feedback_data.correct
        ])
    return {"message": "Feedback submitted successfully"}
