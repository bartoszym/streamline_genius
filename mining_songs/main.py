from genius_api import GeniusAPI
from data_managing import *
from scraper import Scraper
from user_interaction import menu, get_artist_data


def prepare_data() -> str:
    api = GeniusAPI()
    artist_name, artist_api_path, artist_id = get_artist_data(api)
    if not artist_dir_exists(artist_name):
        songs_urls_dict, language = api.get_artist_songs_urls(
            artist_api_path, artist_id
        )
        scraper = Scraper(songs_urls_dict, language)
        create_artist_directory(artist_name)
        save_lyrics_json(scraper.get_artist_lyrics(), artist_name)

    return artist_name


def main():
    artist_name = prepare_data()
    menu(artist_name)


if __name__ == "__main__":
    main()
