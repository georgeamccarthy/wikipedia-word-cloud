from wordcloud import WordCloud
import matplotlib.pyplot as plt
import wikipedia
import streamlit as st
import string


def get_wordcloud(page_name):
    wiki_page = None
    try:
        wiki_page = wikipedia.page(page_name)
    except wikipedia.DisambiguationError as e:
        wiki_page = wikipedia.page(e.options[0])
    except wikipedia.PageError as e:
        st.text(f"Page {page_name} does not match any pages. Try another.")

    if wiki_page is None:
        return None, None, None

    wiki_text = wiki_page.content
    wiki_title = wiki_page.title
    wiki_url = wiki_page.url

    allowed_chars = string.ascii_letters + string.digits + " "
    for char in wiki_text:
        if char not in allowed_chars:
            wiki_text = wiki_text.replace(char, "")
    wiki_text = wiki_text.lower()

    wiki_words = " ".join(wiki_text.split(" ")) + ""

    wordcloud = WordCloud(width=800, height=800).generate(wiki_words)
    return wordcloud, wiki_title, wiki_url


st.title("Wikipedia Word Cloud")
st.markdown(
    """[![GitHub repo](https://img.shields.io/badge/GitHub-wikipedia--word--cloud-brightgreen) ![Stars badge](https://img.shields.io/github/stars/georgeamccarthy/wikipedia-word-cloud)](https://github.com/georgeamccarthy/wikipedia-word-cloud)"""
)

query = st.text_input(label="Enter the title of a Wikipedia article")

if st.button(label="Search") or query:
    if query:
        fig = plt.figure(figsize=(8, 8), facecolor=None)
        plot = fig.add_subplot(111)
        wordcloud, wiki_title, wiki_url = get_wordcloud(query)

        if wordcloud is not None:
            plot.axis("off")
            st.markdown(f"# [{wiki_title}]({wiki_url})")
            plot.imshow(wordcloud)
            st.pyplot(fig=fig)
