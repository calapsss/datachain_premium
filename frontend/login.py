import yaml
from yaml.loader import SafeLoader
import os
import streamlit as st
import streamlit_authenticator as stauth

from streamlit_option_menu import option_menu
from app_pages import sean

from st_click_detector import click_detector
from pathlib import Path
logo = "logotransparent.png"

st.set_page_config(page_title="DataChain", page_icon="📈", layout="centered", initial_sidebar_state="expanded", menu_items=None)

#  User Authentication #TODO: do with DB instead of local
userdb_path = Path(__file__).parent.parent / "authentication/userdb.yaml"
with userdb_path.open("rb") as file:
    config = yaml.load(file, Loader=SafeLoader)

st.image(logo)
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Incorrect username/password")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status:
    with st.sidebar:
        st.image(logo)
        authenticator.logout("Logout", "sidebar")
        st.title(f"Welcome, { name.split(' ',1)[0]}")
        st.write(os.getcwd())

        selected = option_menu(
            menu_title = None,
            options = ["About", "Data Assist", "SageMaker"],
            icons=None,
            menu_icon="menu_down",
            default_index=0
        )
    if selected =="Data Assist":
        sean.create_page()

    page_logo = f"""
    <style>
    [data-testid="stImage"] {{
        margin-top: -60px;
    }}
    </style
    """
    st.markdown(page_logo, unsafe_allow_html=True)






    content = """
        <style>
            .container {
                display: flex;
                justify-content: flex-start;
                margin-bottom: 20px; 
            }
            .item {
                margin-right:300px;
            }
            img {
                max-width: 120%;
                height: auto;
            }
        </style>

        <div class="container">
            <div class="item">
                <p><a href='#' id='Link 1'>First link</a></p>
                <a href='#' id='Chat'>
                    <img src='https://t4.ftcdn.net/jpg/02/25/32/47/360_F_225324730_SdrulNWiykZ9BV00JrIOBuUaxWxg9OsR.jpg'>
                </a>
            </div>
        </div>

        <div class="container">
            <div class="item">
                <p><a href='#' id='Link 2'>Second link</a></p>
                <a href='#' id='SageMaker'>
                    <img src='https://t4.ftcdn.net/jpg/02/25/32/47/360_F_225324730_SdrulNWiykZ9BV00JrIOBuUaxWxg9OsR.jpg'>
                </a>
            </div>
        </div>

        <div class="container">
            <div class="item">
                <p><a href='#' id='Link 3'>Third link</a></p>
                <a href='#' id='Image 1'>
                    <img src='https://t4.ftcdn.net/jpg/02/25/32/47/360_F_225324730_SdrulNWiykZ9BV00JrIOBuUaxWxg9OsR.jpg'>
                </a>
            </div>
        </div>

        <div class="container">
            <div class="item">
                <p><a href='#' id='Link 4'>Fourth link</a></p>
                <a href='#' id='Image No'>
                    <img src='https://t4.ftcdn.net/jpg/02/25/32/47/360_F_225324730_SdrulNWiykZ9BV00JrIOBuUaxWxg9OsR.jpg'>
                </a>
            </div>
        </div>           
    """
    #st.markdown(content, unsafe_allow_html=True)
    #clicked = click_detector(content)