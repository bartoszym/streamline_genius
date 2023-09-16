import json
import os

from typing import Union

DATA_PATH = os.getenv("DATA_DIRECTORY_PATH", os.path.join("mining_songs", "data"))


def artist_dir_exists(artist_name: str) -> bool:
    if not os.path.isdir(DATA_PATH):
        print("creating dict")
        os.mkdir(DATA_PATH)
    dir_list = os.listdir(DATA_PATH)
    dir_list_lowered = [dir_name.lower() for dir_name in dir_list]
    for dir_name in dir_list_lowered:
        if artist_name.lower() == dir_name:
            return True
    return False


def create_artist_directory(artist_name: str):
    new_directory = os.path.join(DATA_PATH, artist_name)
    try:
        os.mkdir(new_directory)
    except FileExistsError:
        print("Directory for the artist already exists")


def save_lyrics_json(lyrics_dict: dict, artist_name: str):
    lyrics_json = json.dumps(lyrics_dict, indent=4)
    with open(os.path.join(DATA_PATH, artist_name, "lyrics.json"), "w") as outfile:
        outfile.write(lyrics_json)


def get_artist_lyrics(artist_name: str) -> Union[str, dict]:
    with open(os.path.join(DATA_PATH, artist_name, "lyrics.json"), "r") as inputfile:
        lyrics_dict = json.load(inputfile)
        return lyrics_dict["language"], lyrics_dict["lyrics"]
