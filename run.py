import time
import streamlit as st
import pandas as pd
import numpy as np

from mining_songs.main import get_proposed_artist, download_lyrics_for_artist
from mining_songs.genius_api import GeniusAPI
from mining_songs.lyrics_analyze import Artist


def set_artist(artist_name: str, language: str):
    st.session_state.artist_name = artist_name
    download_lyrics_for_artist(artist_name, api, language)


api = GeniusAPI()
st.title("Text Mining for artist's lyrics")
library = "spacy"

with st.form("new_form"):
    language = st.selectbox("Please choose language of the lyrics:", ("en", "pl"))
    artist_name = st.text_input(
        "Please insert the name of the requested artist:",
    )

    artist_submitted = st.form_submit_button("Search artist")
    if artist_submitted:
        found_artist_name = get_proposed_artist(artist_name, api)
        st.write("Found artist's name is: ", found_artist_name)

        artist_matches = st.form_submit_button(
            "Click me if found name matches!",
            on_click=set_artist,
            args=(found_artist_name, language),
        )
        # if artist_matches:
        #     download_lyrics_for_artist(artist_name, api, language)

if "artist_name" in st.session_state:
    st.header(f"Currently selected artist is {st.session_state.artist_name}")
    artist = Artist(st.session_state.artist_name)
    most_frequent_words = artist.get_most_frequent_words(which_lib=library, amount=20)
    st.bar_chart(most_frequent_words)
