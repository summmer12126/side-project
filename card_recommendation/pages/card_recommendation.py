import streamlit as st
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import os
from dotenv import load_dotenv
import ast
from preprocessing import credit_benefits, check_benefits

# Load environment variables
load_dotenv()
user = os.getenv('ELASTIC_USER')
passwd = os.getenv('ELASTIC_PASSWD')

# Initialize Elasticsearch client
client = Elasticsearch(
    'https://localhost:9200',
    basic_auth=(user, passwd),
    verify_certs=False
)

# header
st.title("Which one is your best card? Top2") 

# main
st.header("Your picks")

# userinput benefits 

radio_name = st.radio(label='card type', options=['credit', 'debit'])
if radio_name :
    if radio_name =='credit':
        value=credit_benefits()
    elif radio_name =='debit':
        value=check_benefits()

user_input_benefits = st.multiselect('benefit', value)
card_compare = st.button("search")



# func
def search_cards(benefits):
    if radio_name == 'credit':
        s = Search(using=client, index="card_data")
    elif radio_name == 'debit':
        s = Search(using=client, index="card_data_check")

    # Create a should query for each benefit
    should_queries = [{"match": {"Benefits": benefit}} for benefit in benefits]
    
    # Use a bool query with minimum_should_match
    s = s.query("bool", should=should_queries, minimum_should_match=1)
    
    # Sort by score in descending order
    s = s.sort({"_score": {"order": "desc"}})
    
    response = s[:2].execute()  # Get top 2 results
    return response



# comparison
if card_compare and user_input_benefits:
    response = search_cards(user_input_benefits)
    hits = response.hits

    if len(hits) >= 2:
        col1, col2 = st.columns(2)

        for i, hit in enumerate([hits[0], hits[1]]):
            with col1 if i == 0 else col2:
                st.subheader(hit.Name)
                st.image(hit.Image, width=250)
                
                # Convert string representation of list to actual list
                benefits = ast.literal_eval(hit.Benefits)
                st.write(f"Card hit score:{hit.meta.score}")
                st.write(f"Benefits:")
                for benefit in benefits:
                    if benefit in user_input_benefits:
                        st.markdown(f"<span style='color: yellow;'> **- {benefit}**</span>", unsafe_allow_html=True)
                    else:
                        st.write(f"- {benefit}")
                
                st.write(f"[카드 상세 정보]({hit.Link})")
                
                # Display details if available
                if hasattr(hit, 'Detail'):
                    details = ast.literal_eval(hit.Detail)
                    with st.expander("상세 혜택 보기"):
                        for detail in details:
                            st.write(f"- {detail}")

    elif len(hits) == 1:
            hit=hits[0]
            st.subheader(hit[0].Name)
            st.image(hit[0].Image, width=250)
            benefits = ast.literal_eval(hit.Benefits)
            st.write(f"Card hit score:{hit.meta.score}")

            st.write("Benefits:")
            for benefit in benefits:
                if benefit in user_input_benefits:
                    st.markdown(f"<span style='color: yellow;'> **- {benefit}**</span>", unsafe_allow_html=True)
                else:
                    st.write(f"- {benefit}")
            st.write(f"[카드 상세 정보]({hits[0].Link})")
    else:
        st.write("검색 결과가 없습니다.")