import NaverNewsCrawler as nnc
import streamlit as st

st.title("네이버 크롤링 결과")

# 1. 고유 키(key) 부여
keyword = st.text_input("검색할 키워드 : ", key="search_keyword")

if keyword:
    with st.spinner('뉴스 데이터를 가져오는 중...'):
        corpus = nnc.crawl_naver_news_all(keyword)
    
    if corpus:
        st.success(f"'{keyword}'에 대한 결과를 찾았습니다.")
        st.json(corpus[:3])
        
        # 데이터를 세션 상태에 저장하여 유지
        df = nnc.crawl_csv(corpus)
        st.session_state['result_df'] = df
        
        st.dataframe(df)
        
        # 2. 버튼 클릭 로직을 if문 안으로 배치
        if st.button("CSV 저장", key="save_button"):
            if 'result_df' in st.session_state:
                st.session_state['result_df'].to_csv("naver_news_results.csv", index=False, encoding='utf-8-sig')
                st.success("naver_news_results.csv 파일로 저장되었습니다!")
    else:
        st.warning("분석할 데이터가 없습니다.")
else:
    st.info("키워드를 입력해주세요.")