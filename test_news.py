import requests
from bs4 import BeautifulSoup
from newspaper import Article
from transformers import pipeline

# --- AI Summarizer (smaller model to save space) ---
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

import feedparser

def fetch_dropsite_links(limit=5):
    """Fetch DropSite News posts via Substack RSS feed."""
    url = "https://www.dropsitenews.com/feed"
    feed = feedparser.parse(url)

    links = []
    for entry in feed.entries[:limit]:
        links.append({
            "title": entry.title,
            "link": entry.link
        })
    return links


def extract_article_text(url):
    """Use newspaper3k to extract full article text."""
    try:
        art = Article(url)
        art.download()
        art.parse()
        return art.text
    except Exception as e:
        print(f"Failed to extract {url}: {e}")
        return ""

def summarize_text(text, max_len=130, min_len=30):
    """Summarize article text with AI."""
    if not text or len(text) < 200:
        return "⚠️ Article too short to summarize."

    try:
        # Truncate to avoid exceeding model limits
        truncated = text[:2000]  # ~2000 characters is safe for distilbart
        summary = summarizer(
            truncated,
            max_length=max_len,
            min_length=min_len,
            do_sample=False
        )
        return summary[0]["summary_text"]
    except Exception as e:
        return f"Summarization failed: {e}"


def main():
    print("Fetching DropSite News headlines...\n")
    articles = fetch_dropsite_links(limit=5)

    if not articles:
        print("⚠️ No articles found — check the selector or site structure.")
        return

    for art in articles:
        print("📰", art["title"])
        print("🔗", art["link"])
        text = extract_article_text(art["link"])
        if text:
            summary = summarize_text(text)
            print("📌 Summary:", summary)
        else:
            print("⚠️ Could not extract article text.")
        print("-" * 80)

if __name__ == "__main__":
    main()