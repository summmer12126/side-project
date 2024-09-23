import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns



# conn = st.connection("mydb", type="sql")


# main 페이지 설정
st.set_page_config(page_title="dashboard", layout="wide")

# 제목
st.title("DA dashboard")

# 2 db csv 를 db에 넣는 기능 
st.header("data db input")
# st.info("CSV 파일을 업로드하고 DB 이름과 테이블 이름을 입력해주세요.")

input_file = st.file_uploader("db에 input 할 CSV 파일을 업로드하세요", type="csv")
db_name = st.text_input("db 명을 적으세요")
table_name = st.text_input("tb 명을 적으세요")


if st.button("input") and (input_file is not None) and (db_name is not None) and (table_name is not None):
    #file input
    import os
    from dotenv import load_dotenv
    from sqlalchemy import create_engine, text

    load_dotenv()

    user= os.getenv("DB_USER")
    passwd= os.getenv("DB_PASSWD")
    host= os.getenv("DB_HOST")
    port= os.getenv("DB_PORT")
    db=db_name
    

    try:
            # MySQL 서버에 연결
            engine = create_engine(f"mysql+pymysql://{user}:{passwd}@{host}:{port}")

            df_inputfile =pd.read_csv(input_file, encoding='utf-8') # euc-kr 안되는 file 있음
            # db 연결

            with engine.connect() as connection:
                    connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name}"))
                    connection.execute(text(f"USE {db_name}"))

            # 새로운 db 연결
            engine = create_engine(f"mysql+pymysql://{user}:{passwd}@{host}:{port}/{db_name}")
            
            # DataFrame을 SQL 테이블로 저장
            df_inputfile.to_sql(table_name, con=engine, if_exists='replace', index=False)

            st.success(f"데이터가 성공적으로 {db_name} 데이터베이스의 {table_name} 테이블에 저장되었습니다.")

    except Exception as e:
            st.error(f"오류가 발생했습니다: {str(e)}")            
else:
    st.info("file을 업로드하고, db, tb 명을 제대로 작성해주세요")



# # chatgpt
# response = client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[
#         {"role": "system", "content": "You are an assistant that generates SQL queries based on the given MySQL table definition\
#         and a natural language request. The query should start with 'SELECT' and end with a semicolon(;). You must give me a query statement without '\n'"},
#         {"role": "user", "content": f"A query to answer: {full_prompt}"}
#     ],
#     max_tokens=200, # 비용 발생하므로 시도하며 적당한 값 찾아간다. 200이면 최대 200단어까지 생성.
#                     # 영어는 한 단어가 1토큰, 한글은 한 글자가 1토큰 정도
#     temperature=1.0, # 창의성 발휘 여부. 0~2 사이. 0에 가까우면 strict하게, 2에 가까우면 자유롭게(창의성 필요)
#     stop=None  # 특정 문자열이 들어오면 멈춘다든지. None이면 없음. .이면 문장이 끝나면 멈춘다든지
#     )

# # 사이드바에 추가 옵션
# st.sidebar.header("대시보드 설정")
# st.sidebar.subheader("차트 색상 선택")
# color = st.sidebar.color_picker("색상을 선택하세요", "#00f900")
# st.sidebar.write("선택된 색상:", color)

# # 푸터
# st.markdown("---")
# st.markdown("© 2024 데이터 분석 대시보드. All rights reserved.")