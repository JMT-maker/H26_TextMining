from matplotlib import font_manager, rc
import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud

def visualize_barh_grapyh(counter, num_word=20):
    font_path = "c:/Windows/Fonts/malgun.ttf"
    font_name = font_manager.FontProperties(fname=font_path).get_name()
    rc('font', family=font_name)
    top_words = counter.most_common(num_word)
    word_list = [w for w, c in top_words]
    count_list = [c for w, c in top_words]
    fig, ax = plt.subplots()
    ax.barh(word_list[::-1], count_list[::-1])
    st.pyplot(fig)

def visualize_wordcloud(counter, num_word=50):
    # Windows: 'c:/Windows/Fonts/malgun.ttf', Mac: '/Library/Fonts/AppleGothic.ttf'
    wc = WordCloud(font_path='c:/Windows/Fonts/malgun.ttf', 
                width=800, height=600, max_words=num_word, background_color='ivory')
    wc = wc.generate_from_frequencies(counter)
    
    fig, ax = plt.subplots()
    ax.imshow(wc)
    ax.axis('off')
    st.pyplot(fig)