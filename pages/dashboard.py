import streamlit as st

st.title("Analysis of Ofgem Innovation Projects")
st.write("This analysis provides insight into previous and current Innovation Projects funded by Ofgem.\
         Data regarding these projects, accessed using Energy Networks Association's Smarter Networks Portal,\
         is accessible through a series of different visual and graphical means, and adjustable to the users demand.\
         Information regarding the analyses conducted and methods used can be found with each plot.")

#Allow users to describe any errors they come across
with st.expander("To report any errors encountered, click here"):
  with st.form("expander_bug_form", clear_on_submit=True):
    description = st.text_area("Describe the error here:")
    submitted = st.form_submit_button("Click to submit")
    if submitted and description:
      st.success("Thanks for your feedback!")

st.write("Datafile last updated 28/09/2026")
st.write("Website last updated 11:41, 07/10/2026")