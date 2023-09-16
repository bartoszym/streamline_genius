from dataclasses import dataclass, field
from itertools import count


@dataclass
class MenuItem:
    id: int = field(init=False, default_factory=count().__next__)
    function_name: str
    human_readable_name: str
    library_choice: bool = False
    amount_by_user: bool = False


MENU_ITEMS = [
    MenuItem(
        function_name="get_most_frequent_words",
        human_readable_name="Show most frequent words",
        library_choice=True,
        amount_by_user=True,
    ),
    MenuItem(
        function_name="get_sentiment",
        human_readable_name="Show sentiment of artist's songs",
    ),
    MenuItem(
        function_name="get_most_significant_words",
        human_readable_name="Show the most significant words",
        amount_by_user=True,
    ),
    MenuItem(
        function_name="get_words_appearing_together",
        human_readable_name="Show words that appear together the most",
        amount_by_user=True,
    ),
    MenuItem(
        function_name="get_unique_words_amount",
        human_readable_name="Show amount of unique words",
    ),
    MenuItem(
        function_name="get_word_contexts",
        human_readable_name="Show contextes of some word",
        amount_by_user=True,
    ),
    MenuItem(
        function_name="get_percent_of_stopwords",
        human_readable_name="Show how many % of words are stopwords",
    ),
    MenuItem(
        function_name="get_named_entities",
        human_readable_name="Show the list of appearing named entities",
    ),
    MenuItem(
        function_name="get_parts_of_speech_numbers",
        human_readable_name="Show amounts of Parts of Speech",
    ),
    MenuItem(
        function_name="create_frequency_bar_plot",
        human_readable_name="Create bar plot with most frequent words",
        library_choice=True,
        amount_by_user=True,
    ),
    MenuItem(
        function_name="create_word_cloud",
        human_readable_name="Create world cloud",
        library_choice=True,
    ),
    MenuItem(
        function_name="create_words_lengths_pie_chart",
        human_readable_name="Create pie chart with word lenghts",
        amount_by_user=True,
    ),
    MenuItem(
        function_name="create_POS_pie_chart",
        human_readable_name="Create pie chart with % of Parts of Speech",
    ),
    MenuItem(
        function_name="get_percent",
        human_readable_name="Show how many % of words are stopwords Spacy",
    ),
]
