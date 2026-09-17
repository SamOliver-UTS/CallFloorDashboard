import streamlit as st

st.set_page_config(
    page_title="Call Floor Analysis Dashboard",
    page_icon="📞",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📞 Call Floor Analysis Dashboard")

st.markdown(
"""
Operational Dashboard for:

- Campaign Performance
- Batch Performance
- Dialer Performance
- Disposition Analysis
- Lead Conversion
"""
)
