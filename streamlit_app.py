import streamlit as st

home_page = st.Page("views/dashboard.py", title="Home", default=True)
overall_analysis_page = st.Page("views/dashboard.py", title='General Analysis')

pg = st.navigation([home_page, overall_analysis_page])
pg.run()