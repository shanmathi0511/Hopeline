import pytesseract
from PIL import Image
from transformers import pipeline

summarizer = pipeline("summarization")

def extract_text_from_image(image_path):
    return pytesseract.image_to_string(Image.open(image_path))

def summarize_text(text):
    return summarizer(text, max_length=150, min_length=30, do_sample=False)[0]['summary_text']
