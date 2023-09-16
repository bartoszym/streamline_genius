from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk_services import tokenize_text_whitespaces
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer


def tf_idf(lyrics: list):
    def prepare_lyrics(lyrics):
        prepared = []
        for lyric in lyrics:
            tokenized_song = tokenize_text_whitespaces(lyric)
            lem = WordNetLemmatizer()
            prepared_lyrics = [
                lem.lemmatize(word)
                for word in tokenized_song
                if not word in stopwords.words("english") and len(word) > 2
            ]
            prepared.append(" ".join(prepared_lyrics))
        return prepared

    tfv = TfidfVectorizer()
    prepared_lyrics = prepare_lyrics(lyrics)
    vec_text = tfv.fit_transform(prepared_lyrics)

    return vec_text, tfv


def get_most_significant_words(songs: list, n_words: int):
    vec_text, tfv = tf_idf(songs)
    for idf, word in sorted(zip(tfv.idf_, tfv.get_feature_names_out()), reverse=True)[
        :n_words
    ]:
        print(f"{idf}, {word}")


def k_means(songs: list, n_clusters: int = 5):
    vec_text, tfv = tf_idf(songs)
    words = tfv.get_feature_names()
    kmeans = KMeans(n_clusters=n_clusters, n_init=17)
    kmeans.fit(vec_text)
    common_words = kmeans.cluster_centers_.argsort()[:, -1:-11:-1]
    for num, centroid in enumerate(common_words):
        print(centroid)
        print(str(num) + " : " + ", ".join(words[word] for word in centroid))
