import time
import streamlit as st
import pandas as pd
import numpy as np

from mining_songs.main import get_proposed_artist, download_lyrics_for_artist
from mining_songs.genius_api import GeniusAPI


def get_artist_name(api: GeniusAPI):
    language = st.selectbox("Please choose language of the lyrics:", ("PL", "ENG"))
    artist_name = st.text_input(
        "Please insert the name of the requested artist:",
    )
    if artist_name:
        found_artist_name = get_proposed_artist(artist_name, api)
        st.write("Found artist's name is: ", found_artist_name)

        if st.button(
            "Click me if found name matches!",
        ):
            download_lyrics_for_artist(artist_name, api, language)
            st.session_state.artist_name = artist_name


def main():
    api = GeniusAPI()
    st.title("Text Mining for artist's lyrics")

    if "artist_name" in st.session_state:
        st.header(f"Currently selected artist is {st.session_state.artist_name}")
        # st.session_state.artist_name = "artist's name"

    get_artist_name(api)


main()
