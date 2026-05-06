import pandas as pd
from collections import Counter
from konlpy.tag import Okt

def load_corpus(datafile, col_name='review'):
    data_df = pd.read_csv(datafile)
    return list(data_df[col_name])

def count_word_freq(corpus):
    t = Okt()
    my_tags = ['Noun', 'Verb', 'Adjective']
    my_stopwords = ['영화', '이', '것', '하는', '정말', '진짜', '보고', '점', '좀', '그', '수', '할', '있는', '때', '보는']
    
    all_text = " ".join(corpus)
    tokens = [word for word, tag in t.pos(all_text) 
            if tag in my_tags and len(word) > 1 and word not in my_stopwords]
    return Counter(tokens)