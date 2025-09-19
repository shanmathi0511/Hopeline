from transformers import pipeline

emotion_pipeline = pipeline("text-classification", model="bhadresh-savani/distilbert-base-uncased-emotion")

def detect_emotion(text):
    emotions = emotion_pipeline(text)
    top_emotion = max(emotions, key=lambda x: x['score'])
    return top_emotion['label'], round(top_emotion['score'], 2)
