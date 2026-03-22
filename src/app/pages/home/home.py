import streamlit as st

with open("src/app/pages/home/home.html", "r") as html_file:
    home_html = html_file.read()

st.html(home_html)