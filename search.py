import streamlit as st
import requests
from bs4 import BeautifulSoup
import datetime
import time

# Configure page
st.set_page_config(
    page_title="SearchHub - Your Search Engine",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Google-like styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        font-size: 4rem;
        font-weight: 300;
        color: #4285f4;
        margin-bottom: 2rem;
        font-family: 'Arial', sans-serif;
    }
    
    .search-container {
        display: flex;
        justify-content: center;
        margin: 2rem 0;
    }
    
    .search-stats {
        color: #70757a;
        font-size: 0.9rem;
        margin: 1rem 0;
    }
    
    .result-item {
        margin: 1.5rem 0;
        padding: 1rem;
        border-radius: 8px;
        background: #f8f9fa;
        border-left: 4px solid #4285f4;
    }
    
    .result-title {
        color: #1a0dab;
        font-size: 1.2rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }
    
    .result-url {
        color: #006621;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
    }
    
    .history-item {
        padding: 0.5rem;
        margin: 0.2rem 0;
        background: #f1f3f4;
        border-radius: 20px;
        display: inline-block;
        margin-right: 0.5rem;
        font-size: 0.9rem;
    }
    
    .tab-content {
        padding: 2rem 0;
    }
    
    .footer {
        text-align: center;
        color: #70757a;
        font-size: 0.8rem;
        margin-top: 3rem;
        padding: 1rem;
        border-top: 1px solid #e8eaed;
    }
</style>
""", unsafe_allow_html=True)

def duckduckgo_search(query):
    """Search function using DuckDuckGo"""
    url = "https://html.duckduckgo.com/html/"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/115.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    try:
        response = requests.post(url, headers=headers, data={"q": query}, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        results = []
        
        for link in soup.find_all("a", class_="result__a", href=True):
            title = link.get_text().strip()
            href = link['href']
            if title and href:
                results.append({"title": title, "link": href})
        
        return results
    except Exception as e:
        st.error(f"Search failed: {str(e)}")
        return []

def add_to_history(query):
    """Add search query to history"""
    if 'search_history' not in st.session_state:
        st.session_state.search_history = []
    
    # Remove if already exists to avoid duplicates
    if query in st.session_state.search_history:
        st.session_state.search_history.remove(query)
    
    # Add to beginning of list
    st.session_state.search_history.insert(0, query)
    
    # Keep only last 10 searches
    st.session_state.search_history = st.session_state.search_history[:10]

def main():
    # Initialize session state
    if 'search_history' not in st.session_state:
        st.session_state.search_history = []
    
    # Header
    st.markdown('<h1 class="main-header">🔍 Intelio</h1>', unsafe_allow_html=True)
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Search", "📰 News", "🖼️ Images", "⚙️ Settings"])
    
    with tab1:
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        
        # Search bar
        col1, col2, col3 = st.columns([1, 3, 1])
        
        with col2:
            search_query = st.text_input(
                "",
                placeholder="Search the web...",
                label_visibility="collapsed",
                key="search_input"
            )
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                search_button = st.button("🔍 Search", use_container_width=True)
            with col_btn2:
                lucky_button = st.button("🍀 I'm Feeling Lucky", use_container_width=True)
        
        # Search History
        if st.session_state.search_history:
            st.markdown("### Recent Searches")
            history_html = ""
            for query in st.session_state.search_history:
                if st.button(f"🕐 {query}", key=f"history_{query}"):
                    st.session_state.search_input = query
                    st.rerun()
        
        # Perform search
        if search_button or lucky_button:
            if search_query:
                add_to_history(search_query)
                
                with st.spinner("Searching..."):
                    results = duckduckgo_search(search_query)
                
                if results:
                    st.markdown(f'<div class="search-stats">About {len(results)} results</div>', 
                              unsafe_allow_html=True)
                    
                    # Display results
                    for i, result in enumerate(results, 1):
                        st.markdown(f"""
                        <div class="result-item">
                            <div class="result-title">{i}. {result['title']}</div>
                            <div class="result-url">🔗 {result['link']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Add clickable link
                        st.markdown(f"[Open Link]({result['link']})")
                        
                        if lucky_button:
                            st.markdown(f"**Lucky Pick!** Opening: {result['link']}")
                            break
                else:
                    st.warning("❌ No results found. Try a different search query.")
            else:
                st.warning("Please enter a search query.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        st.markdown("### 📰 News Search")
        
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            news_query = st.text_input(
                "",
                placeholder="Search for news...",
                label_visibility="collapsed",
                key="news_input"
            )
            
            if st.button("🔍 Search News", use_container_width=True):
                if news_query:
                    news_search_query = f"{news_query} news"
                    add_to_history(news_search_query)
                    
                    with st.spinner("Searching news..."):
                        results = duckduckgo_search(news_search_query)
                    
                    if results:
                        st.markdown(f'<div class="search-stats">About {len(results)} news results</div>', 
                                  unsafe_allow_html=True)
                        
                        for i, result in enumerate(results, 1):
                            st.markdown(f"""
                            <div class="result-item">
                                <div class="result-title">📰 {result['title']}</div>
                                <div class="result-url">🔗 {result['link']}</div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            st.markdown(f"[Read Article]({result['link']})")
                    else:
                        st.warning("❌ No news results found.")
                else:
                    st.warning("Please enter a news search query.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        st.markdown("### 🖼️ Image Search")
        
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            image_query = st.text_input(
                "",
                placeholder="Search for images...",
                label_visibility="collapsed",
                key="image_input"
            )
            
            if st.button("🔍 Search Images", use_container_width=True):
                if image_query:
                    image_search_query = f"{image_query} images"
                    add_to_history(image_search_query)
                    
                    with st.spinner("Searching images..."):
                        results = duckduckgo_search(image_search_query)
                    
                    if results:
                        st.markdown(f'<div class="search-stats">About {len(results)} image results</div>', 
                                  unsafe_allow_html=True)
                        
                        for i, result in enumerate(results, 1):
                            st.markdown(f"""
                            <div class="result-item">
                                <div class="result-title">🖼️ {result['title']}</div>
                                <div class="result-url">🔗 {result['link']}</div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            st.markdown(f"[View Images]({result['link']})")
                    else:
                        st.warning("❌ No image results found.")
                else:
                    st.warning("Please enter an image search query.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab4:
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        st.markdown("### ⚙️ Settings")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("#### Search Preferences")
            
            # Settings options
            safe_search = st.selectbox("Safe Search", ["Off", "Moderate", "Strict"])
            results_per_page = st.slider("Results per page", 5, 20, 10)
            
            st.markdown("#### Search History")
            if st.button("🗑️ Clear Search History", use_container_width=True):
                st.session_state.search_history = []
                st.success("Search history cleared!")
            
            if st.session_state.search_history:
                st.markdown("**Current History:**")
                for i, query in enumerate(st.session_state.search_history, 1):
                    st.markdown(f"{i}. {query}")
            else:
                st.info("No search history available.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>SearchHub - Powered by DuckDuckGo | Privacy-focused search engine</p>
        <p>© 2024 SearchHub. All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
