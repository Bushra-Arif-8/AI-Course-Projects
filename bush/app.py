# app.py
import streamlit as st
import base64

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image:
        encoded_string = base64.b64encode(image.read()).decode()
        page_bg_img = f"""
    <style>
    html, body, [data-testid="stApp"] {{
        background-image: url("data:image/jpg;base64,{encoded_string}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        height: 100%;
    }}
    .title {{
        font-size: 45px;
        font-weight: bold;
        color: black;
        text-align: center;
        margin-top: 5px; 
        margin-right: 80px;
        text-shadow: 2px 2px 4px #000000;
    }}
    .quote {{
        font-size: 24px;
        font-style: italic;
        color: #f0f0f0;
        text-align: center;
        margin-top: 5px; 
        margin-right: 20px;
        margin-bottom: 40px;
        text-shadow: 1px 1px 3px #000000;
    }}
    .stButton > button {{
        background-color: purple;
        color: white;
        font-size: 20px;
        padding: 15px 40px;
        border: none;
        border-radius: 10px;
        cursor: pointer;
        display: block;
        margin: auto;
        transition: 0.3s ease-in-out;
    }}
    .stButton > button:hover {{
        background-color: pink;
        transform: scale(1.05);
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

def welcome_page():
    add_bg_from_local("fff.jpg")
    st.markdown('<div class="title">💖 AI-POWERED MatchMinds</div>', unsafe_allow_html=True)
    st.markdown('<div class="quote">"Where friendships begin with a spark of compatibility..."</div>', unsafe_allow_html=True)
    if st.button("Get Started"):
        st.session_state.page = "test"
        st.rerun()

if 'page' not in st.session_state:
    st.session_state.page = "welcome"

if st.session_state.page == "welcome":
    welcome_page()
elif st.session_state.page == "test":
    import test
    test.prediction_page()
elif st.session_state.page == "suggestion":
    import suggestion
    suggestion.suggestion_page()