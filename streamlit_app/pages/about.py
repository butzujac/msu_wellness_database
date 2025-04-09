import streamlit as st

st.set_page_config(page_title="About", layout="wide")

st.title("About the MSU Wellness Dashboard")

# Sub-navigation using sidebar
section = st.sidebar.radio(
    "About Sections",
    ["📌Mission", "📬Contact Us", "👏 Acknowledgements", "🧑‍💻Team"]
)

# Content for each sub-section
if section == "📌Mission":
    st.subheader("Our Mission")
    st.markdown("""
The goal of this dashboard is to help identify keywords across multiple universities that allow for insights
within different university wellness programs. We aimed to make the dashboard easily accessible and simple to understand. 
With an array of schools and keywords any kind of search is possible within this dashboard.
    """)

elif section == "📬Contact Us":
    st.subheader("Get in Touch")
    st.markdown("""
    Reach out to us at:

    - Email: 
    - GitHub: 
    """)

elif section == "👏 Acknowledgements":
    st.subheader("Special Thanks")
    st.markdown("""
    We would like to thank:
    - MSU Wellness Program
    - MSU CMSE Department
    - Professor Dirk
    - Yash Mandlecha
    """)

elif section == "🧑‍💻Team":
    st.subheader("Team")
    st.markdown("""
    #### Jack Butzu
    - Picture
    - Contact
    - Bio
    
    #### Ethan LaBombard
    - Picture
    - Contact
    - Bio
                
    #### Androw Shmona
    - Picture
    - Contact
    - Bio
                
    #### Anthony McCollom
    - Picture
    - Contact
    - Bio
    
    """)
