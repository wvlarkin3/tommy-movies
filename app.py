import streamlit as st
import pandas as pd
import re

def normalize_title(title):
    title = str(title).lower().strip()
    title = re.sub(r'^(the|a|an)\s+', '', title)  # Remove leading articles
    title = re.sub(r'[^\w\s]', '', title)         # Remove punctuation
    title = re.sub(r'\s+', ' ', title)            # Normalize spacing
    return title

def load_titles(file, column_name="Name"):
    df = pd.read_csv(file)
    titles = df[column_name].dropna().astype(str).apply(normalize_title)
    return set(titles)

st.title("🎬 TommyMovies: Taste-Based Rec Engine")

watched_file = st.file_uploader("Upload your watched.csv", type=["csv"])
watchlist_file = st.file_uploader("(Optional) Upload your watchlist.csv", type=["csv"])
vibe = st.text_input("What are you in the mood for? (e.g. 'dark thriller', 'stylish drama', 'comfort show')")

if watched_file and vibe:
    watched_titles = load_titles(watched_file)

    watchlist_titles = set()
    if watchlist_file:
        watchlist_titles = load_titles(watchlist_file)

    watched_str = ', '.join(f'"{t}"' for t in sorted(watched_titles))
    watchlist_str = ', '.join(sorted(watchlist_titles)) if watchlist_titles else "(none)"

    prompt = f"""
I want you to act as a movie and TV recommendation assistant.

Only recommend titles that are NOT in this list of watched titles:
{watched_str}

These titles are in my watchlist:
{watchlist_str}

I’m in the mood for something like: {vibe}

Recommend 5–7 titles with:
- A one-line tone-aware description
- Streaming platform (if known)
- Ratings (IMDb, Rotten Tomatoes, Letterboxd, if available)
- No vague genre lists, no repeats, and no titles I've already seen
"""

    st.subheader("📋 Copy Your GPT Prompt")
    st.code(prompt, language='markdown')

else:
    st.info("Please upload your watched list and describe your desired vibe.")
