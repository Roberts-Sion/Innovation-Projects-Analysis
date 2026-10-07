import streamlit as st

home_page = st.Page("pages/dashboard.py", title="Home", default=True)
overall_analysis_page = st.Page("pages/dashboard1.py", title="Key Analysis")
sif_funding_page = st.Page("pages/dashboard2.py", title="Analysis of Projects that have received SIF Funding")
research_page = st.Page("pages/dashboard3.py", title="Analysis of...")

pg = st.navigation([home_page, overall_analysis_page, sif_funding_page, research_page])
pg.run()