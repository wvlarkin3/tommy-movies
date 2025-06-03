import streamlit as st
import pandas as pd
import re

def normalize_title(title):
    title = title.lower().strip()
    title = re.sub(r'^(the|a|an)\s+', '', title)
    title = re.sub(r'[^a-z0-9\s]', '', title)
    return title

st.title("🎬 TommyMovies: Taste-Based Rec Engine")

watched_file = st.file_uploader("Upload your watched.csv", type="csv")
watchlist_file = st.file_uploader("(Optional) Upload your watchlist.csv", type="csv")
vibe = st.text_input("What are you in the mood for? (e.g. 'dark thriller', 'stylish drama', 'comfort show')")

if watched_file:
    watched_df = pd.read_csv(watched_file)
    watched_titles = set(normalize_title(t) for t in watched_df['Name'].dropna())
else:
    st.warning("Please upload your watched.csv file.")
    st.stop()

watchlist_titles = set()
if watchlist_file:
    watchlist_df = pd.read_csv(watchlist_file)
    watchlist_titles = set(normalize_title(t) for t in watchlist_df['Name'].dropna())

if vibe:
    sample_titles = list(watched_titles)[:200]  # Token-friendly
    excluded_str = ", ".join(f'"{title}"' for title in sample_titles)

    taste_hint = ""
    if watchlist_titles:
        sample_watchlist = list(watchlist_titles)[:20]
        taste_hint = f"\nThese titles are in my watchlist: {', '.join(sample_watchlist)}."

    prompt = f"""
I want you to act as a movie and TV recommendation assistant. Only recommend titles that are NOT in this list of watched titles: {excluded_str}.{taste_hint}

I’m in the mood for something like: {vibe}

Recommend 5–7 titles with:
- A one-line tone-aware description
- Streaming platform (if known)
- Ratings (IMDb, Rotten Tomatoes, Letterboxd, if available)
- No vague genre lists, no repeats, and no titles I've already seen
"""

    st.subheader("✅ Your GPT Prompt:")
    st.code(prompt, language='markdown')
    st.info("Paste this prompt into ChatGPT to get filtered, vibe-matched recs.")
else:
    st.stop()
