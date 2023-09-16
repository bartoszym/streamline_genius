import os
import wordcloud
import matplotlib.pyplot as plt

from data_managing import DATA_PATH


def create_bar_plot(data: dict, artist_name: str, title: str) -> str:
    plt.barh(list(data.keys()), list(data.values()))
    plt.title(title)
    plot_path = os.path.join(DATA_PATH, artist_name, f"{title}_bar_plot.png")
    plt.savefig(plot_path)
    plt.show()
    plt.clf()
    return f"The image was save under path {os.path.relpath(plot_path)}"


def create_pie_chart(data: dict, artist_name: str, title: str) -> str:
    labels = [f"{words_length} characters" for words_length in data.keys()]
    fig, ax = plt.subplots()
    ax.pie(
        data.values(),
        labels=labels,
        autopct=lambda pct: "{:1.1f}%".format(pct) if pct > 2 else "",
    )
    fig.suptitle(title)
    chart_path = os.path.join(DATA_PATH, artist_name, f"{title}_pie_chart.png")
    fig.show()
    fig.savefig(chart_path)
    return f"The image was save under path {os.path.relpath(chart_path)}"


def create_word_cloud(frequency_dict: dict, which_lib: str, artist_name: str) -> str:
    word_cloud = wordcloud.WordCloud(width=800, height=800).generate_from_frequencies(
        frequency_dict
    )
    word_cloud_path = os.path.join(
        DATA_PATH, artist_name, f"{which_lib}_lyrics_word_cloud.png"
    )

    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(word_cloud)
    plt.axis("off")
    plt.show()
    plt.clf()

    word_cloud.to_file(word_cloud_path)
    return f"The image was save under path {os.path.realpath(word_cloud_path)}"
