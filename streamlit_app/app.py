import streamlit as st
import pandas as pd
import re
import plotly.express as px
st.set_page_config(layout="wide")


data = pd.read_csv("/home/jack/MSU/CMSE495/msu_wellness_database/docs/msu_wd_keyword_database.csv")


def count_occurrences(text):
    if not isinstance(text, str):
        return 0
    return len(re.findall(r'Occurrence \d+:', text))


counts = data.map(count_occurrences)
column_counts = counts.sum()
top_terms = column_counts.nlargest(5)
top_5_data = top_terms.reset_index()
top_5_data.columns = ["Term", "Count"]

fig = px.bar(
    top_5_data, 
    x="Term", 
    y="Count", 
    title="Top 5 Most Common Terms",
    labels={"Term": "Terms", "Count": "Count of Observations"},
    text="Count"
)

fig.update_traces(textposition="outside", marker_color="royalblue")
fig.update_layout(
    xaxis_title="Terms",
    yaxis_title="Count of Observations",
    template="plotly_white"
)

counts = data.map(count_occurrences)
column_counts = counts.sum()
non_zero_counts = column_counts[column_counts > 0]
bottom_terms = non_zero_counts.nsmallest(5)
bottom_5_data = bottom_terms.reset_index()
bottom_5_data.columns = ["Term", "Count"]

fig2 = px.bar(
    bottom_5_data, 
    x="Term", 
    y="Count", 
    title="Bottom 5 Terms",
    labels={"Term": "Terms", "Count": "Count of Observations"},
    text="Count"
)

fig2.update_traces(textposition="outside", marker_color="royalblue")
fig2.update_layout(
    xaxis_title="Terms",
    yaxis_title="Count of Observations",
    template="plotly_white"
)

top_5_df = data.nlargest(5, "Total Mentions")

fig3 = px.bar(
    top_5_df,
    x="school_name",
    y="Total Mentions",
    title="Top 5 Highest Values",
    labels={"school_name": "School Name", "Total Mentions": "Count of Observations"},
    text="Total Mentions"
)

fig3.update_traces(textposition="outside", marker_color="royalblue")
fig3.update_layout(
    xaxis_title="School Name",
    yaxis_title="Count of Observations",
    template="plotly_white"
)

col1, col2, col3 = st.columns([.33,.33,.33])

with col1:
    st.plotly_chart(fig)

with col2: 
    st.plotly_chart(fig2)

with col3: 
    st.plotly_chart(fig3)

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

col1, col2 = st.columns([.01,.99])
#with col1: 
    #st.write("school name")
with col2: 
    st.write(selected_keyword)
for i, row in data.iterrows():
    #with col1:
        #st.write(f"{row["school_name"]}")
        
    
    with col2:
        count = len(re.findall(r'Occurrence \d+:', row[selected_keyword]))
        if count != 0:
            with st.expander(row["school_name"] + ":         " + f"{count} occurrences"):
                st.write(row[selected_keyword]) 



