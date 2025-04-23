import streamlit as st
import pandas as pd
import re
import plotly.express as px
from PIL import Image
import base64
from io import BytesIO
import requests

st.set_page_config(layout="wide", page_title="MSU Wellness Dashboard")

# Load data
data_url = "https://raw.githubusercontent.com/butzujac/msu_wellness_database/refs/heads/main/docs/msu_wd.csv"
data = pd.read_csv(data_url)

# Load and center the logo
logo_url = "https://raw.githubusercontent.com/butzujac/msu_wellness_database/refs/heads/main/streamlit_app/logo.png"
response = requests.get(logo_url)
logo = Image.open(BytesIO(response.content))
buffered = BytesIO()
logo.save(buffered, format="PNG")
logo_base64 = base64.b64encode(buffered.getvalue()).decode()

# Highlight keywords in occurences
def highlight_keyword(text, keyword):
    if not isinstance(text, str):
        return text

    # Highlight the keyword
    pattern = re.compile(re.escape(keyword), re.IGNORECASE)
    highlighted = pattern.sub(
        lambda match: f"<span style='background-color: yellow; font-weight: bold;'>{match.group(0)}</span>",
        text
    )

    # Convert raw URLs into clickable links
    highlighted = re.sub(
        r'(https?://[^\s]+)',
        r'<a href="\1" target="_blank">\1</a>',
        highlighted
    )

    # Split paragraphs and wrap in <p> tags
    paragraphs = highlighted.split("\n")
    formatted = "".join(f"<p>{para.strip()}</p>" for para in paragraphs if para.strip())

    return f"<div>{formatted}</div>"






st.markdown(
    f"""
    <div style='text-align: center; padding-bottom: 10px;'>
        <img src='data:image/png;base64,{logo_base64}' width='200'/>
        <h1 style='color: #2E8B57;'>MSU Wellness Keyword Dashboard</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# No match keywords
#  "Housing Stability", "Healthcare Services", "Transportation Access", "Personal Care Items","Childcare Support",
#  "Technology Access","Clothing & Weather Essentials", "Community & Belonging", "Cooking Supplies", "Legal Support",
#  "Laundry Access", "Career Resources", "Substance Abuse Support", "Immigration & International Student Support", "Communication Services", "Domestic Violence Resources"

# Keywords and abbreviations
keywords = [
    "Food Security","Financial Assistance", "Mental Health Support",
    "Academic Support", "School Supplies", "Cleaning Supplies",
    "Nutrition Education", "Financial Literacy", "Crisis Intervention", "Financial Counseling", "Emergency Housing"
]

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

# Count helper
def count_occurrences(text):
    if not isinstance(text, str):
        return 0
    return len(re.findall(r'Occurrence \d+:', text))

counts = data.map(count_occurrences)
column_counts = counts.sum()

# TABS for navigation
tab1, tab2 = st.tabs(["🔍 Keyword Search", "🏫 School Search"])

# --- TAB 1: Keyword Search ---
with tab1:
    st.header("🔍 Keyword Search")

    col1, col2, col3 = st.columns(3)

    fig1 = px.bar(column_counts.nlargest(5).reset_index().rename(columns={"index": "Term", 0: "Count"}),
                  x="Term", y="Count", text="Count", title="Top 5 Most Common Terms", range_y=[0, 25])
    fig1.update_traces(textposition="outside", marker_color="green")
    fig1.update_layout(template="plotly_white")

    fig2 = px.bar(column_counts[column_counts > 0].nsmallest(5).reset_index().rename(columns={"index": "Term", 0: "Count"}),
                  x="Term", y="Count", text="Count", title="Bottom 5 Terms", range_y=[0, 8])
    fig2.update_traces(textposition="outside", marker_color="green")
    fig2.update_layout(template="plotly_white")

    fig3 = px.bar(data.nlargest(5, "Total Mentions"), x="school_name", y="Total Mentions", text="Total Mentions",
                  title="Top 5 Schools by Mentions", range_y=[0, 20])
    fig3.update_traces(textposition="outside", marker_color="green")
    fig3.update_layout(template="plotly_white")

    with col1: st.plotly_chart(fig1, use_container_width=True)
    with col2: st.plotly_chart(fig2, use_container_width=True)
    with col3: st.plotly_chart(fig3, use_container_width=True)

    selected_keyword = st.selectbox("Select a Keyword", keywords)
    st.markdown(f"### Mentions of **{selected_keyword}**")
    for _, row in data.iterrows():
        count = count_occurrences(row[selected_keyword])
        if count > 0:
            with st.expander(f"{row['school_name']} — {count} occurrence(s)"):
                # st.write(row[selected_keyword])
                highlighted_text = highlight_keyword(row[selected_keyword], selected_keyword)
                st.markdown(highlighted_text, unsafe_allow_html=True)


    # st.markdown("---")
    # text_search = st.text_input("Search mentions for any term (e.g., 'laptop', 'food'):")
    # if text_search:
    #     found = False
    #     for _, row in data.iterrows():
    #         for kw in keywords:
    #             val = row[kw]
    #             if isinstance(val, str) and text_search.lower() in val.lower():
    #                 if not found:
    #                     st.markdown("### Matching Mentions:")
    #                     found = True
    #                 with st.expander(f"{row['school_name']} — {kw}"):
    #                     st.write(val)
    #     if not found:
    #         st.warning("No keyword mentions matched your search.")

# --- TAB 2: School Search ---
with tab2:
    st.header("🏫 School Search")

    selected_school = st.selectbox("Select a School", data["school_name"].unique())
    st.markdown(f"### Keyword Mentions for **{selected_school}**")
    school_row = data[data["school_name"] == selected_school]
    if not school_row.empty:
        for kw in keywords:
            value = school_row.iloc[0][kw]
            if isinstance(value, str) and "Occurrence" in value:
                with st.expander(f"{kw}"):
                    # st.write(value)
                    highlighted = highlight_keyword(value, kw)
                    st.markdown(highlighted, unsafe_allow_html=True)


    st.markdown("---")
    school_search = st.text_input("Search by school name or abbreviation:")
    if school_search:
        search_lower = school_search.lower()
        matched_schools = data[
            data["school_name"].str.contains(search_lower, case=False, na=False) |
            data["school_name"].map(lambda x: any(search_lower in abbr.lower() for school, abbr in abbreviations.items() if school in x))
        ]
        if not matched_schools.empty:
            for _, row in matched_schools.iterrows():
                st.markdown(f"### {row['school_name']}")
                st.write(f"Total Mentions: {row['Total Mentions']}")
                with st.expander("View keyword details"):
                    for kw in keywords:
                        value = row[kw]
                        if isinstance(value, str) and "Occurrence" in value:
                            st.markdown(f"**{kw}**")
                            # st.write(value)
                            highlighted = highlight_keyword(value, kw)
                            st.markdown(highlighted, unsafe_allow_html=True)

        else:
            st.warning("No schools matched your search.")

