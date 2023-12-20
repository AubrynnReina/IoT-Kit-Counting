import streamlit as st
import st_templates.templates as templates 
import style.style as style

st.set_page_config(page_title="IOT Counting System", layout="wide")
st.markdown(style.hide_menu_style, unsafe_allow_html=True)
st.markdown(templates.photo_template, unsafe_allow_html=True)
col1, col2, col3 = st.columns([1,1,1])
col1.image("img/good.png", caption="Good photo example")
col2.image("img/bad1.png", caption="Blurred photo example")
col3.image("img/bad2.png", caption="Overlappings photo example")
st.markdown(templates.process_template, unsafe_allow_html=True)
