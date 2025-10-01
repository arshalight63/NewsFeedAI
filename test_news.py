import nltk
from textblob import TextBlob
from newspaper import Article
from transformers import pipeline
import requests

# -----------------------------
# Ensure TextBlob corpora
# -----------------------------
def ensure_textblob_corpora():
    """Download required corpora if missing."""
    required = [
        "punkt",
        "averaged_perceptron_tagger",
        "wordnet",
        "brown"
    ]
    for resource in required:
        try:
            nltk.data.find(resource)
        except LookupError:
            nltk.download(resource)

ensure_textblob_corpora()

# -----------------------------
# Summarizer loader (no Streamlit here)
# -----------------------------
_summarizer = None

def load_summarizer():
    """Load and cache the Hugging Face summarizer pipeline."""
    global _summarizer
    if _summarizer is None:
        _summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    return _summarizer

# -----------------------------
# Fetch article links
# -----------------------------
def fetch_dropsite_links(url, limit=5):
    """
    For now, just return the given URL in a list.
    You can expand this to scrape RSS feeds or site HTML.
    """
    return [url]

# -----------------------------
# Extract article text
# -----------------------------
def extract_article_text(url):
    """Download and parse article text using newspaper3k."""
    article = Article(url)
    article.download()
    article.parse()
    return article.text

# -----------------------------
# Summarize text
# -----------------------------
def summarize_text(text, max_length=130, min_length=30):
    """Summarize text using Hugging Face transformers."""
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
    """Return a subjectivity score between 0 (objective) and 1 (subjective)."""
    analysis = TextBlob(text)
    return analysis.sentiment.subjectivity

# -----------------------------
# Sentence-level subjectivity
# -----------------------------
def sentence_subjectivity(text, top_k=5):
    """Return the top_k most subjective sentences from the text."""
    sentences = [str(s) for s in TextBlob(text).sentences]
    scored = [(s, TextBlob(s).sentiment.subjectivity) for s in sentences]
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_k]
