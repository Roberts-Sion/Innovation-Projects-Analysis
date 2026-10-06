import streamlit as st

home_page = st.Page("pages/dashboard.py", title="Home", default=True)
overall_analysis_page = st.Page("pages/dashboard1.py", title="General Analysis")
sif_funding_page = st.Page("pages/dashboard2.py", title="SIF Funding Analysis")

pg = st.navigation([home_page, overall_analysis_page, sif_funding_page])
pg.run()