from genius_api import GeniusAPI
from lyrics_analyze import Artist
from menu_items import MENU_ITEMS

from typing import Union


def get_int_from_user(message: str) -> int:
    while True:
        from_user = input(message)
        try:
            return int(from_user)
        except ValueError:
            print("It's not number!")


def select_library(LIBRARY_DICT: dict):
    while True:
        selected_library = get_int_from_user("Choose library:\n 1. NLTK \n 2. SpaCy\n")
        if selected_library in LIBRARY_DICT.keys():
            return selected_library
        print(f"Chosen value has to be {LIBRARY_DICT.keys()}")


def menu(artist_name: str):
    def print_menu():
        for i in MENU_ITEMS:
            print(f"{i.id + 1}: {i.human_readable_name}")

    LIBRARY_DICT = {1: "nltk", 2: "spacy"}
    artist = Artist(artist_name)
    while True:
        print_menu()
        while True:
            selection = get_int_from_user("Type number of the menu item: ")
            if selection in range(len(MENU_ITEMS) + 1):
                break
        chosen_item = MENU_ITEMS[selection - 1]
        if chosen_item.function_name == "get_word_contexts":
            chosen_word = input("Type word that you want to get contexts for: ")
            chosen_amount = get_int_from_user(
                "Type how many lines of contexts you want to see: "
            )

            chosen_line_length = get_int_from_user(
                "Type how long should be the lines with contexts: "
            )

            artist.get_word_contexts(chosen_word, chosen_amount, chosen_line_length)
            continue

        selected_library, amount = None, None
        if chosen_item.library_choice and artist.language == "en":
            selected_library = select_library(LIBRARY_DICT)
        if chosen_item.amount_by_user:
            amount = get_int_from_user("Choose amount of words that will be provided: ")

        selected_by_user = {
            "which_lib": LIBRARY_DICT[selected_library] if selected_library else None,
            "amount": amount,
        }
        params = {
            key: value for key, value in selected_by_user.items() if value is not None
        }
        function_result = getattr(artist, chosen_item.function_name)(**params)
        from pprint import pprint

        pprint(function_result)
        wait_for_user = input("Click enter to continue...")


def get_artist_data(api: GeniusAPI) -> Union[str, str, str]:
    while True:
        artist_name = input("Please provide artist name: ")
        found_name, api_path, artist_id = api.find_artist(artist_name)
        is_found_name_good = input(
            f"""Is found name "{found_name}" the artist you are looking for? (y or n)"""
        )
        if is_found_name_good == "y":
            return found_name, api_path, artist_id
