import re
import requests

from bs4 import BeautifulSoup

from .utils import ProgressBar

GENIUS_URL = "https://genius.com"


class Scraper:
    def __init__(self, songs_urls_dict: str, language: str) -> None:
        self.language = language
        self.songs_urls_dict = songs_urls_dict

    def get_artist_lyrics(self) -> dict:
        lyrics_dict = {}
        counter_progress = 0
        progress_bar = ProgressBar()
        for title, song_url in self.songs_urls_dict.items():
            lyrics_dict[title] = self.__extract_lyrics(song_url)
            counter_progress += 1
            if counter_progress % 5 == 0:
                progress_bar.show_progress_bar(
                    counter_progress, len(self.songs_urls_dict)
                )
        dict_to_save = {"language": self.language, "lyrics": lyrics_dict}
        return dict_to_save

    def __create_soup_object(self, url: str) -> BeautifulSoup:
        target_url = GENIUS_URL + url
        response = requests.get(target_url)
        soup = BeautifulSoup(response.content, "html.parser")
        return soup

    def __extract_lyrics(self, url: str) -> str:
        soup = self.__create_soup_object(url)
        found_divs = soup.find_all(
            "div",
            {
                "class": re.compile("Lyrics__Container.*"),
                "data-lyrics-container": "true",
            },
        )
        song_lyrics = "".join([div.get_text(" ") for div in found_divs])
        song_lyrics = self.remove_brackets(song_lyrics)
        return song_lyrics

    @staticmethod
    def remove_brackets(lyrics: str) -> str:
        lyrics = re.sub(r"(\[.*?\])", "", lyrics)
        lyrics = re.sub(r"((\().*?\))", "", lyrics)
        return lyrics
