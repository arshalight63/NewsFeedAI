import nltk
from textblob import TextBlob
from newspaper import Article
from transformers import pipeline
import requests

# -----------------------------
# Ensure TextBlob corpora
# -----------------------------
def ensure_textblob_corpora():
    try:
        _ = TextBlob("test").sentiment
    except LookupError:
        nltk.download("punkt")
        nltk.download("averaged_perceptron_tagger")
        nltk.download("wordnet")
        nltk.download("brown")

ensure_textblob_corpora()

# -----------------------------
# Summarizer loader (no Streamlit here)
# -----------------------------
_summarizer = None

def load_summarizer():
    global _summarizer
    if _summarizer is None:
        _summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    return _summarizer

# -----------------------------
# Fetch article links
# -----------------------------
def fetch_dropsite_links(url, limit=5):
    """For now, just return the given URL in a list."""
    return [url]

# -----------------------------
# Extract article text
# -----------------------------
def extract_article_text(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.text

# -----------------------------
# Summarize text
# -----------------------------
def summarize_text(text, max_length=130, min_length=30):
    if not text or len(text.split()) < 50:
        return text  # too short to summarize
    summarizer = load_summarizer()
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
    analysis = TextBlob(text)
    return analysis.sentiment.subjectivity

# -----------------------------
# Sentence-level subjectivity
# -----------------------------
def sentence_subjectivity(text, top_k=5):
    sentences = [str(s) for s in TextBlob(text).sentences]
    scored = [(s, TextBlob(s).sentiment.subjectivity) for s in sentences]
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_k]
