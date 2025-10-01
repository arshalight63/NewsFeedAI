import streamlit as st
from test_news import fetch_dropsite_links, extract_article_text, summarize_text

# --- Streamlit Page Setup ---
st.set_page_config(page_title="DropSite AI News", layout="wide")
st.title("📰 DropSite News — AI Summarized")
st.caption("Headlines from DropSite News with neutral AI summaries.")

# Sidebar control
limit = st.sidebar.slider("Number of headlines", 3, 15, 5)

# Fetch articles
articles = fetch_dropsite_links(limit=limit)

# Render UI
if not articles:
    st.warning("⚠️ No articles found — check the selector or site structure.")
else:
    for art in articles:
        with st.container():
            st.markdown(f"### {art['title']}")
            st.caption(f"🔗 {art['link']}")

            # Extract and summarize
            text = extract_article_text(art["link"])
            summary = summarize_text(text)

            st.write(summary)
            st.link_button("Read full article", art["link"], use_container_width=True)

        st.divider()