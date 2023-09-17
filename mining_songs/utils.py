import streamlit as st


class ProgressBar:
    def __init__(self) -> None:
        self.progress_bar = st.progress(0)

    def show_progress_bar(self, current: int, max: int):
        progress_percent = int((current / max) * 100)
        self.progress_bar.progress(
            progress_percent, text="Downloading artist's lyrics, please wait..."
        )
        if progress_percent >= 95:
            self.progress_bar.empty()


def progress_bar(current: int, max: int):
    progress_percent = int((current / max) * 100)
    st.progress(progress_percent, text="Downloading artist's lyrics, please wait...")
