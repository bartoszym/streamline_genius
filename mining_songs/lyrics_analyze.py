import re

from . import graphics
from . import nltk_services
from . import sklearn_services
from . import spacy_services
from dataclasses import dataclass
from .data_managing import get_artist_lyrics
from .utils import progress_bar


@dataclass
class Song:
    title: str
    lyrics: str


class Artist:
    def __init__(self, artist_name: str) -> None:
        self.artist_name = artist_name
        self.language, lyrics_dict = get_artist_lyrics(artist_name)
        self.songs = []
        for title, lyrics in lyrics_dict.items():
            self.songs.append(Song(title, lyrics))

    def str_all_lyrics(self) -> str:
        return "".join([s.lyrics.lower() for s in self.songs])

    def get_most_frequent_words(
        self, which_lib: str = None, amount: int = None
    ) -> dict:
        if which_lib == "nltk":
            return nltk_services.most_frequent_words(self.str_all_lyrics(), amount)
        elif which_lib == "spacy" or which_lib == None:
            kwargs = {"language": self.language}
            return spacy_services.most_frequent_words(
                re.sub("\r\n", " ", self.str_all_lyrics()), amount, **kwargs
            )
        else:
            raise ValueError(
                "Wrong value of which_lib: possible are [nltk, spacy, None]"
            )

    def get_most_frequent_words_lengths(self, amount: int) -> list:
        return nltk_services.calculate_words_length_percent_distribution(
            self.str_all_lyrics(), amount
        )

    def create_words_lengths_pie_chart(self, amount: int = 5) -> str:
        words_lengths = self.get_most_frequent_words_lengths(amount)
        values = [percent * 100 for percent in words_lengths.values()]
        others_percent = (100 - sum(values)) / 100
        words_lengths["other"] = others_percent
        return graphics.create_pie_chart(
            words_lengths, self.artist_name, f"{self.artist_name}'s words lengths"
        )

    def create_word_cloud(self, which_lib: str = None) -> str:
        if which_lib in ["nltk", "spacy", None]:
            freq_dist = self.get_most_frequent_words(which_lib)
        else:
            raise ValueError(
                "Wrong value of which_lib: possible are [nltk, spacy, None]"
            )
        return graphics.create_word_cloud(freq_dist, which_lib, self.artist_name)

    def get_sentiment(self) -> dict:
        sentiment_dict = {
            "overall": {
                "neg": 0,
                "neu": 0,
                "pos": 0,
                "compound": 0,
            },
            "most_neg": {"score": 0, "title": "", "compound": 0},
            "most_pos": {"score": 0, "title": "", "compound": 0},
        }

        def check_highest_sentiments(
            sentiment_dict: dict, song_sentiment: dict
        ) -> dict:
            for i in ["pos", "neg"]:
                if song_sentiment[i] > sentiment_dict[f"most_{i}"]["score"]:
                    sentiment_dict[f"most_{i}"]["score"] = song_sentiment[i]
                    sentiment_dict[f"most_{i}"]["title"] = song.title
                    sentiment_dict[f"most_{i}"]["compound"] = song_sentiment["compound"]
            return sentiment_dict

        for counter, song in enumerate(self.songs):
            progress_bar(counter, len(self.songs))
            song_sentiment = nltk_services.calculate_song_sentiment(song.lyrics)
            for key in sentiment_dict["overall"].keys():
                sentiment_dict["overall"][key] += song_sentiment[key]
            sentiment_dict = check_highest_sentiments(sentiment_dict, song_sentiment)

        for key in sentiment_dict["overall"].keys():
            sentiment_dict["overall"][key] /= len(self.songs)
        print(
            f"The most positive song is {sentiment_dict['most_pos']['title']} with {sentiment_dict['most_pos']['score']} score. Compound: {sentiment_dict['most_pos']['compound']}"
        )
        print(
            f"The most negative song is {sentiment_dict['most_neg']['title']} with {sentiment_dict['most_neg']['score']} score. Compound: {sentiment_dict['most_neg']['compound']}"
        )
        print(
            f"The overall negative sentiment of the songs is {sentiment_dict['overall']['neg']}"
        )
        print(
            f"The overall neutral sentiment of the songs is {sentiment_dict['overall']['neu']}"
        )
        print(
            f"The overall positive sentiment of the songs is {sentiment_dict['overall']['pos']}"
        )
        return sentiment_dict

    def create_frequency_bar_plot(self, amount: int, which_lib: str = None) -> str:
        if which_lib in ["nltk", "spacy", None]:
            freq_dist = self.get_most_frequent_words(which_lib, amount)
        else:
            raise ValueError(
                "Wrong value of which_lib: possible are [nltk, spacy, None]"
            )
        return graphics.create_bar_plot(
            freq_dist,
            self.artist_name,
            f"{self.artist_name}'s most used words acc to {which_lib}",
        )

    def get_most_significant_words(self, amount: int = 10):
        lyrics = [song.lyrics for song in self.songs]
        return sklearn_services.get_most_significant_words(lyrics, amount)

    def get_words_appearing_together(self, amount: int = 20) -> list:
        return nltk_services.collocation_words(self.str_all_lyrics(), amount)

    def get_unique_words_amount(self) -> list:
        return len(nltk_services.get_unique_words(self.str_all_lyrics()))

    def get_word_contexts(self, word: str, n_lines: int = 25, line_length: int = 75):
        return nltk_services.get_word_concordance(
            self.str_all_lyrics(), word, n_lines, line_length
        )

    def get_percent_of_stopwords(self) -> float:
        return nltk_services.calculate_percent_of_stopwords(self.str_all_lyrics())

    def get_percent(self) -> float:
        kwargs = {"language": self.language}
        return spacy_services.percent_stopwords(self.str_all_lyrics(), **kwargs)

    def get_named_entities(self):
        kwargs = {"language": self.language}
        ners = spacy_services.get_NERS(
            re.sub("\r\n", " ", self.str_all_lyrics()), **kwargs
        )
        for key, value in ners.items():
            print(f"{key}:")
            for i, j in enumerate(value):
                print(j, end=", ")
                if i % 10 == 0:
                    print("")
            print("")
        return ners

    def get_parts_of_speech_numbers(self) -> list:
        kwargs = {"language": self.language}
        return spacy_services.get_POS(
            re.sub("\r\n", " ", self.str_all_lyrics()), **kwargs
        )

    def create_POS_pie_chart(self) -> str:
        POS_dict = dict(self.get_parts_of_speech_numbers())
        return graphics.create_pie_chart(
            POS_dict,
            self.artist_name,
            f"{self.artist_name}'s % division of Parts of Speech",
        )
