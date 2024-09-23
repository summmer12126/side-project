import streamlit as st
import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
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

# Streamlit UI
st.header("Try searching your best card")

value1=credit_benefits()
value2=check_benefits()
value = value1+value2

user_input_benefits = st.multiselect('benefit', value)
radio_name = st.radio(label='card type', options=['credit', 'debit'])
card_compare = st.button("search")



# function
def search_index(index_name, field_name, search_term):
    s = Search(using=client, index=index_name)
    s = s.query("terms", **{field_name: search_term})
    response = s.execute()
    return response



# result
if card_compare and radio_name:
    st.info("Click on the images to explore more details")

    # Define the search function
    if radio_name == "credit":
    # Perform the search
        index_name = 'card_data'

    elif radio_name=="debit":
        index_name = "card_data_check"

    field_name = 'Benefits'  # Adjust this to match your actual field name
    result = search_index(index_name, field_name, user_input_benefits)

    
    # Display results
    if result.hits:
        for hit in result.hits:
            st.markdown(f'<a href="{hit.Link}" target="_blank"><img src="{hit.Image}" width="200"></a>', unsafe_allow_html=True)
            st.markdown(f"Card Name: <span style='color: yellow'>** {hit.Name}**</span>", unsafe_allow_html=True)
            
            # st.write(f"Benefits: {hit.Benefits}")

            import ast
            benefits = ast.literal_eval(hit.Benefits)

            for benefit in benefits:
                if benefit in user_input_benefits:
                    st.markdown(f"<span style='color: yellow;'> ** {benefit}**</span>", unsafe_allow_html=True)
                else:
                    st.write(f"-{benefit}")

            st.write(f"="*80)
    else:
        st.write("No matching cards found.")



