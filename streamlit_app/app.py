import streamlit as st
import pandas as pd
import re
st.set_page_config(layout="wide")


st.write("new app test! showing first keywords ")
keywords = [
    "Food Security", "Housing Stability", "Financial Assistance", "Healthcare Services", "Mental Health Support",
    "Transportation Access", "Personal Care Items", "Childcare Support", "Technology Access", "Clothing & Weather Essentials",
    "Academic Support", "Community & Belonging", "School Supplies", "Cooking Supplies", "Cleaning Supplies",
    "Nutrition Education", "Financial Literacy", "Legal Support", "Crisis Intervention", "Laundry Access",
    "Career Resources", "Substance Abuse Support", "Financial Counseling", "Emergency Housing", 
    "Immigration & International Student Support", "Communication Services", "Domestic Violence Resources"
]

selected_keyword = st.selectbox('Select a keyword', keywords)

data = pd.read_csv("/home/jack/MSU/CMSE495/msu_wellness_database/docs/msu_wd_keyword_database.csv")
col1, col2 = st.columns([.2, .8])
with col1: 
    st.write("school name")
with col2: 
    st.write(selected_keyword)
for i, row in data.iterrows():
    
    with col1:
        st.write(f"{row["school_name"]}")
        
    
    with col2:
        count = len(re.findall(r'Occurrence \d+:', row[selected_keyword])) 
        with st.expander(f"{count} occurrences"):
            st.write(row["Food Security"]) 



