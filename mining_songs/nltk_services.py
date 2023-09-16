import string
from nltk.text import Text
from nltk.tokenize import word_tokenize, WhitespaceTokenizer
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import SnowballStemmer


def tokenize_text_whitespaces(lyrics: str) -> list:
    whitespace_tokenizer = WhitespaceTokenizer()
    tokens = whitespace_tokenizer.tokenize(lyrics)
    return tokens


def tokenize_text(lyrics: str) -> list:
    return word_tokenize(lyrics)


def remove_punctuation(lyrics: str) -> str:
    return "".join([word for word in lyrics if word not in string.punctuation])


def calculate_percent_of_stopwords(lyrics: str) -> float:
    stop_words = [w for w in lyrics if w in stopwords.words("english")]
    return len(stop_words) / len(lyrics)


def most_frequent_words(lyrics: str, top_n_words: int = None) -> dict:
    tokens = tokenize_text(lyrics)
    stemmer = SnowballStemmer("english")
    tokens = [word.lower() for word in tokens if word.isalpha()]
    stemmed_words = [
        stemmer.stem(word) for word in tokens if word not in stopwords.words("english")
    ]
    fdist = FreqDist(stemmed_words)
    return dict(fdist.most_common(top_n_words))


def calculate_words_length_percent_distribution(
    lyrics: str, n_frequent_words: int
) -> FreqDist:
    tokens_lengths = [
        len(token) for token in tokenize_text(lyrics) if token not in string.punctuation
    ]
    fdist = FreqDist(tokens_lengths)
    most_common = fdist.most_common(n_frequent_words)
    distribution = {frequency[0]: fdist.freq(frequency[0]) for frequency in most_common}
    return distribution


def calculate_song_sentiment(lyrics: str) -> dict:
    sentiment_analyzer = SentimentIntensityAnalyzer()
    return sentiment_analyzer.polarity_scores(lyrics)


def collocation_words(lyrics: str, n_pairs: int) -> list:
    tokens = tokenize_text(remove_punctuation(lyrics))
    lyrics_text = Text(tokens)
    return lyrics_text.collocation_list(num=n_pairs)


def get_unique_words(lyrics: str):
    tokens = tokenize_text(lyrics)
    lyrics_text = Text(tokens)
    return lyrics_text.vocab()


def get_word_concordance(lyrics: str, word: str, lines: int, width: int):
    tokens = tokenize_text(lyrics)
    lyrics_text = Text(tokens)
    return lyrics_text.concordance(word, width=width, lines=lines)
