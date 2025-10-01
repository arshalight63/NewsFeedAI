import streamlit as st
from test_news import sentence_subjectivity

st.markdown("### 🎯 Biasometer")
st.progress(int(subjectivity * 100))
st.caption(f"Subjectivity score: {subjectivity:.2f}")

with st.expander("ℹ️ How we arrived at this score from the link"):
    st.write("""
    1) We fetched the article via the URL and extracted the main text using newspaper3k.
    2) We analyzed that text with TextBlob, which estimates how subjective the language is.
    3) The Biasometer bar reflects the overall subjectivity (0 = objective, 1 = subjective).
    """)
    st.write("Top sentences contributing to subjectivity:")
    for sent, subj in sentence_subjectivity(text, top_k=5):
        st.markdown(f"- **Subjectivity:** {subj:.2f} — {sent}")
    fetch_dropsite_links,
    extract_article_text,
    summarize_text,
    biasometer,
)

# ✅ This must be the first Streamlit command
st.set_page_config(
    page_title="NewsFeed AI",
    page_icon="📰",
    layout="wide"
)

st.title("📰 NewsFeed AI")
st.caption("Fetch, summarize, and analyze bias in news articles")

# -----------------------------
# User input
# -----------------------------
url = st.text_input(
    "Enter a news article URL",
    placeholder="https://www.bbc.com/news/world-12345678"
)

if url:
    with st.spinner("Fetching article..."):
        try:
            # Fetch links (for now just returns [url])
            links = fetch_dropsite_links(url)

            for link in links:
                st.divider()
                st.subheader(f"Article: {link}")

                # Extract text
                text = extract_article_text(link)

                # Summarize
                summary = summarize_text(text)

                # Biasometer
                subjectivity = biasometer(text)

                # -----------------------------
                # Display results
                # -----------------------------
                with st.expander("Full Article Text"):
                    st.write(text)

                st.markdown("### 📝 Summary")
                st.write(summary)

                st.markdown("### 🎯 Biasometer")
                st.progress(int(subjectivity * 100))
                st.caption(f"Subjectivity score: {subjectivity:.2f}")

        except Exception as e:
            st.error(f"Error processing article: {e}")
else:
    st.info("👆 Paste a news article URL above to get started.")
