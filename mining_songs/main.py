from .genius_api import GeniusAPI
from .data_managing import *
from .scraper import Scraper
from .user_interaction import menu, get_artist_data


def get_proposed_artist(artist_name: str, api: GeniusAPI) -> str:
    found_name, _, _ = api.find_artist(artist_name)
    return found_name


def download_lyrics_for_artist(artist_name: str, api: GeniusAPI, language: str):
    found_name, artist_api_path, artist_id = api.find_artist(artist_name)
    if not artist_dir_exists(found_name):
        print("essa")
        songs_urls_dict = api.get_artist_songs_urls(artist_api_path, artist_id)
        scraper = Scraper(songs_urls_dict, language)
        create_artist_directory(found_name)
        save_lyrics_json(scraper.get_artist_lyrics(), found_name)


def main():
    artist_name = prepare_data()
    menu(artist_name)


if __name__ == "__main__":
    main()
