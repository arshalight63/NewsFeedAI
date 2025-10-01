# test_news.py

import requests
from newspaper import Article
from textblob import TextBlob
from transformers import pipeline
import streamlit as st

# -----------------------------
# Summarizer (cached for speed)
# -----------------------------
@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="facebook/bart-large-cnn")

summarizer = load_summarizer()

# -----------------------------
# Fetch article links from a site
# -----------------------------
def fetch_dropsite_links(url, limit=5):
    """
    Fetch a few article links from a given site.
    For now, this is a placeholder that just returns [url].
    You can expand it to scrape RSS feeds or site HTML.
    """
    return [url]

# -----------------------------
# Extract article text
# -----------------------------
def extract_article_text(url):
    """
    Download and parse article text using newspaper3k.
    """
    article = Article(url)
    article.download()
    article.parse()
    return article.text

# -----------------------------
# Summarize text
# -----------------------------
def summarize_text(text, max_length=130, min_length=30):
    """
    Summarize text using Hugging Face transformers.
    """
    if not text or len(text.split()) < 50:
        return text  # too short to summarize
    summary = summarizer(
        text,
        max_length=max_length,
        min_length=min_length,
        do_sample=False
    )
    return summary[0]['summary_text']

# -----------------------------
# Biasometer (subjectivity)
# -----------------------------
def biasometer(text):
    """
    Return a subjectivity score between 0 (objective) and 1 (subjective).
    """
    analysis = TextBlob(text)
    return analysis.sentiment.subjectivity
