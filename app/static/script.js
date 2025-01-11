const predictButton = document.getElementById('predictButton');
const tweetInput = document.getElementById('tweetInput');
const resultDiv = document.getElementById('result');
const labelSpan = document.getElementById('label');
const confidenceSpan = document.getElementById('confidence');
const feedbackButtons = document.getElementById('feedbackButtons');
const thumbsUpButton = document.getElementById('thumbsUp');
const thumbsDownButton = document.getElementById('thumbsDown');

let currentPrediction = null; // Store the current prediction data

predictButton.addEventListener('click', () => {
    const tweetText = tweetInput.value;

    if (tweetText.trim() === "") {
        alert("Please enter a tweet!");
        return;
    }

    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text: tweetText })
    })
    .then(response => response.json())
    .then(data => {
        labelSpan.textContent = data.label;
        confidenceSpan.textContent = data.confidence.toFixed(2);
        resultDiv.style.display = 'block';
        feedbackButtons.style.display = 'block'; // Show feedback buttons

        // Store current prediction for feedback
        currentPrediction = {
            text: tweetText,
            label: data.label,
            confidence: data.confidence
        };
    })
    .catch(error => {
        console.error('Error:', error);
        alert("An error occurred. Please try again.");
    });
});

thumbsUpButton.addEventListener('click', () => {
    sendFeedback(true); // true for thumbs-up
});

thumbsDownButton.addEventListener('click', () => {
    sendFeedback(false); // false for thumbs-down
});

function sendFeedback(isCorrect) {
    if (!currentPrediction) return;

    fetch('/feedback', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            ...currentPrediction,
            correct: isCorrect
        })
    })
    .then(response => {
        if (response.ok) {
            alert("Feedback submitted! Thank you.");
            feedbackButtons.style.display = 'none'; // Hide feedback buttons
            currentPrediction = null; // Clear current prediction
        } else {
            throw new Error("Failed to submit feedback.");
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert("Error submitting feedback.");
    });
}