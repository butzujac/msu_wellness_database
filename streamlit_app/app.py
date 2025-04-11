import streamlit as st
import pandas as pd
import re
import plotly.express as px
from PIL import Image
import base64
from io import BytesIO

st.set_page_config(layout="wide", page_title="MSU Wellness Dashboard")

# Load data
url = "https://raw.githubusercontent.com/butzujac/msu_wellness_database/refs/heads/main/streamlit_app/msu_wd_keyword_database.csv"
data = pd.read_csv(url)

# Load and center the logo
logo = Image.open("logo.png")
buffered = BytesIO()
logo.save(buffered, format="PNG")
logo_base64 = base64.b64encode(buffered.getvalue()).decode()

st.markdown(
    f"""
    <div style='text-align: center; padding-bottom: 10px;'>
        <img src='data:image/png;base64,{logo_base64}' width='200'/>
        <h1 style='color: #2E8B57;'>MSU Wellness Keyword Dashboard</h1>
    </div>
    """,
    unsafe_allow_html=True
)

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

# Abbreviations map for easier searching
abbreviations = {
    "University of Oregon": "UO", "University of Maryland, College Park": "UMD",
    "University of Indiana, Bloomington": "IU", "University of South Carolina": "USC",
    "University of Louisiana State": "LSU", "University of Minnesota": "UMN",
    "University of Nebraska, Lincoln": "UNL", "University of Iowa": "UI",
    "University of Kansas": "KU", "University of Oklahoma State": "OSU",
    "University of Texas Tech": "TTU", "University of Arizona": "UA",
    "University of Washington State": "WSU", "University of Oregon State": "OSU",
    "University of West Virginia": "WVU", "University of Virginia": "UVA",
    "University of Pittsburgh": "Pitt", "University of North Carolina State": "NCSU",
    "University of Colorado, Boulder": "CU Boulder", "University of Missouri": "Mizzou",
    "University of Utah": "UU", "University of Baylor": "BU",
    "University of Kansas State": "KSU", "University of Arkansas State": "AState",
    "University of Mississippi": "Ole Miss", "University of Alabama": "UA",
    "University of Tennessee, Knoxville": "UTK", "University of Nevada, Las Vegas": "UNLV",
    "University of New Mexico": "UNM", "University of Hawaii": "UH",
    "University of Alaska": "UAA", "University of Vermont": "UVM",
    "University of Rhode Island": "URI", "University of Delaware": "UD",
    "University of Houston": "UH", "University of Massachusetts Amherst": "UMass",
    "University of Cincinnati": "UC", "University of Colorado Denver": "CU Denver",
    "University of South Florida": "USF", "University of Louisville": "UofL",
    "University of Alabama at Birmingham": "UAB", "University of California, Irvine": "UCI",
    "University of California, San Diego": "UCSD"
}

# --- Visualizations ---
st.markdown("## 🔍 Keyword Frequency Analysis")
col1, col2, col3 = st.columns(3)

# Top 5 terms
top_terms = column_counts.nlargest(5)
top_5_data = top_terms.reset_index()
top_5_data.columns = ["Term", "Count"]
fig1 = px.bar(top_5_data, x="Term", y="Count", title="Top 5 Most Common Terms", text="Count", range_y = [0,170])
fig1.update_traces(textposition="outside", marker_color="green")
fig1.update_layout(template="plotly_white")

# Bottom 5 terms
bottom_terms = column_counts[column_counts > 0].nsmallest(5)
bottom_5_data = bottom_terms.reset_index()
bottom_5_data.columns = ["Term", "Count"]
fig2 = px.bar(bottom_5_data, x="Term", y="Count", title="Bottom 5 Terms", text="Count", range_y = [0,4])
fig2.update_traces(textposition="outside", marker_color="green")
fig2.update_layout(template="plotly_white")

# Top 5 schools
top_5_df = data.nlargest(5, "Total Mentions")
fig3 = px.bar(top_5_df, x="school_name", y="Total Mentions", title="Top 5 Schools by Mentions", text="Total Mentions", labels={"school_name":"School Name"}, range_y = [0,110])
fig3.update_traces(textposition="outside", marker_color="green")
fig3.update_layout(template="plotly_white")

with col1: st.plotly_chart(fig1, use_container_width=True)
with col2: st.plotly_chart(fig2, use_container_width=True)
with col3: st.plotly_chart(fig3, use_container_width=True)

# Keyword viewer
st.markdown("---")
st.markdown(f"## 📌 Mentions of **{selected_keyword}**")
for _, row in data.iterrows():
    count = count_occurrences(row[selected_keyword])
    if count > 0:
        with st.expander(f"{row['school_name']} — {count} occurrence(s)"):
            st.write(row[selected_keyword])

# School view
st.markdown("---")
st.markdown(f"## 🏢 Detailed View for **{selected_school}**")
school_row = data[data["school_name"] == selected_school]
if not school_row.empty:
    for kw in keywords:
        value = school_row.iloc[0][kw]
        if isinstance(value, str) and "Occurrence" in value:
            with st.expander(f"{kw}"):
                st.write(value)

# Search Schools by Name
st.markdown("---")
st.markdown("## 🔎 Search for a School")
school_search = st.text_input("Enter school name, abbreviation, or keyword to search:")

if school_search:
    search_lower = school_search.lower()
    matched_schools = data[data["school_name"].str.contains(search_lower, case=False, na=False) |
                           data["school_name"].map(lambda x: any(search_lower in abbr.lower() for school, abbr in abbreviations.items() if school in x))]

    if not matched_schools.empty:
        for _, row in matched_schools.iterrows():
            st.markdown(f"### {row['school_name']}")
            st.write(f"Total Mentions: {row['Total Mentions']}")
            with st.expander("View keyword details"):
                for kw in keywords:
                    value = row[kw]
                    if isinstance(value, str) and "Occurrence" in value:
                        st.markdown(f"**{kw}**")
                        st.write(value)
    else:
        st.warning("No schools matched your search.")

# Search keyword contents
st.markdown("---")
st.markdown("## 🔍 Search Keyword Mentions")
text_search = st.text_input("Search mentions for any term (e.g., 'housing', 'laptop', etc.):")

if text_search:
    found = False
    for _, row in data.iterrows():
        for kw in keywords:
            val = row[kw]
            if isinstance(val, str) and text_search.lower() in val.lower():
                if not found:
                    st.markdown("### Matching Mentions:")
                    found = True
                with st.expander(f"{row['school_name']} — {kw}"):
                    st.write(val)
    if not found:
        st.warning("No keyword mentions matched your search.")