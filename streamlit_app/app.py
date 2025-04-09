import streamlit as st
import pandas as pd
import re
import plotly.express as px

st.set_page_config(layout="wide", page_title="Wellness Keyword Dashboard")

# Load data
url = "https://raw.githubusercontent.com/butzujac/msu_wellness_database/refs/heads/main/streamlit_app/msu_wd_keyword_database.csv"
df = pd.read_csv(url)


# Precompute occurrence counts
def count_occurrences(text):
    if not isinstance(text, str):
        return 0
    return len(re.findall(r'Occurrence \d+:', text))

counts = data.map(count_occurrences)
column_counts = counts.sum()

# --- Sidebar Filters ---
st.sidebar.header("Filters")

keywords = [
    "Food Security", "Housing Stability", "Financial Assistance", "Healthcare Services", "Mental Health Support",
    "Transportation Access", "Personal Care Items", "Childcare Support", "Technology Access", "Clothing & Weather Essentials",
    "Academic Support", "Community & Belonging", "School Supplies", "Cooking Supplies", "Cleaning Supplies",
    "Nutrition Education", "Financial Literacy", "Legal Support", "Crisis Intervention", "Laundry Access",
    "Career Resources", "Substance Abuse Support", "Financial Counseling", "Emergency Housing", 
    "Immigration & International Student Support", "Communication Services", "Domestic Violence Resources"
]

selected_keyword = st.sidebar.selectbox("Select a Keyword", keywords)
selected_school = st.sidebar.selectbox("Select a School", data["school_name"].unique())

# --- Visualizations ---
st.markdown("## 🔍 Keyword Frequency Analysis")
col1, col2, col3 = st.columns(3)

# Top 5 terms
top_terms = column_counts.nlargest(5)
top_5_data = top_terms.reset_index()
top_5_data.columns = ["Term", "Count"]
fig1 = px.bar(top_5_data, x="Term", y="Count", title="Top 5 Most Common Terms", text="Count")
fig1.update_traces(textposition="outside", marker_color="royalblue")
fig1.update_layout(template="plotly_white")

# Bottom 5 terms
bottom_terms = column_counts[column_counts > 0].nsmallest(5)
bottom_5_data = bottom_terms.reset_index()
bottom_5_data.columns = ["Term", "Count"]
fig2 = px.bar(bottom_5_data, x="Term", y="Count", title="Bottom 5 Terms", text="Count")
fig2.update_traces(textposition="outside", marker_color="royalblue")
fig2.update_layout(template="plotly_white")

# Top 5 schools
top_5_df = data.nlargest(5, "Total Mentions")
fig3 = px.bar(top_5_df, x="school_name", y="Total Mentions", title="Top 5 Schools by Mentions", text="Total Mentions")
fig3.update_traces(textposition="outside", marker_color="royalblue")
fig3.update_layout(template="plotly_white")

with col1: st.plotly_chart(fig1, use_container_width=True)
with col2: st.plotly_chart(fig2, use_container_width=True)
with col3: st.plotly_chart(fig3, use_container_width=True)

# --- Keyword Viewer Section ---
st.markdown("---")
st.markdown(f"## 📌 Mentions of **{selected_keyword}**")
for i, row in data.iterrows():
    count = len(re.findall(r'Occurrence \d+:', row[selected_keyword]))
    if count != 0:
        with st.expander(f"{row['school_name']} — {count} occurrence(s)"):
            st.write(row[selected_keyword])

# --- Selected School Viewer ---
st.markdown("---")
st.markdown(f"## 🏫 Detailed View for **{selected_school}**")
school_row = data[data["school_name"] == selected_school]
if not school_row.empty:
    for kw in keywords:
        value = school_row.iloc[0][kw]
        if isinstance(value, str) and "Occurrence" in value:
            with st.expander(f"{kw}"):
                st.write(value)
