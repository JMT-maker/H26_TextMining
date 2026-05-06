import os
import sys
import urllib.request
import json
import pandas as pd
import streamlit as st

# client_id = st.secrets["NAVER_CLIENT_ID"]
# client_secret = st.secrets["NAVER_CLIENT_SECRET"]

def crawl_naver_news(url, start=0, display=10):
    client_id = "cLZXe0q2CRNgGR9GRAts"
    client_secret = "LVmCqeUOAe"
    url += f'&start={start}&display={display}' # 옵션 변경
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        news_data = json.loads(response_body.decode('utf-8'))['items']
        return news_data, None
    else:
        # print("Error Code:" + rescode)
        return None, rescode



def crawl_naver_news_all(keyword):
    encText = urllib.parse.quote(keyword)

    start = 1
    display = 10

    url = "https://openapi.naver.com/v1/search/news?query=" + encText # JSON 결과

    corpus = []

    while start <= 100:  # 원하는 갯수 설정해서 적용
        crawled_news, status = crawl_naver_news(url, start, display)
        if crawled_news: 
            corpus += crawled_news
            start += display
        else:
            print("Error Code:" + status)
            break

    return corpus

def crawl_csv(corpus):

    df = pd.DataFrame(corpus)

    return df