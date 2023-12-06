import yaml
from yaml.loader import SafeLoader
import os
import streamlit as st
import streamlit_authenticator as stauth

from streamlit_option_menu import option_menu
from app_pages import sean, andre, pips
import base64

from pathlib import Path
logo = "logotransparent.png"

st.set_page_config(page_title="DataChain", page_icon="📈", layout="centered", initial_sidebar_state="expanded", menu_items=None)

def create_about():
    st.code("""Welcome to the future of data science.""")
    st.code("""
            DataChain is an AI data science assistant that will help you with your data needs.\n
            """)
    
    st.write("FAQs")
    with st.expander("Data Assist"):
        st.code("An AI chatbot that can help you understand data,\nperform machine learning, and create visualizations.")
    with st.expander("SageMaker"):
        st.code("A pipeline to AWS SageMaker that can create notebooks\nfor you to send to your teammates")
    with st.expander("SQL"):
        st.code("A demo of an LLM interacting with a SQL Database\nto retrieve data with natural language.")


@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

bg_img = get_img_as_base64("group-background.png")
dash_img= get_img_as_base64("cartoony-background.png")

def home_background():
    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] > .main {{
    background-image: url("data:image/png;base64,{bg_img}");
    background-size: cover;
    background-size: 130%;
    background-position: -130px center;
    background-repeat: repeat;
    background-attachment: local;
    }}

    [data-testid="stHeader"] {{
    background-color: rgba(0, 0, 0, 0);
    }}

    [data-testid="stToolbar"] {{
    right: 2rem;
    }}
    </style"
    """

    st.markdown(page_bg_img, unsafe_allow_html=True)

def dash_background():
    page_bg_img = f"""
    <style>
    [data-testid="stSidebar"] > div:first-child {{
    background-image: url("data:image/png;base64,{bg_img}");
    background-position: center; 
    background-repeat: no-repeat;
    }}
    </style"
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

#  User Authentication #TODO: do with DB instead of local
userdb_path = Path(__file__).parent.parent / "authentication/userdb.yaml"
with userdb_path.open("rb") as file:
    config = yaml.load(file, Loader=SafeLoader)

#st.image(logo)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    home_background()
    st.error("Incorrect username/password")

if authentication_status == None:
    home_background()
    st.warning("Please enter your username and password")

if authentication_status:
    with st.sidebar:
        #st.image(logo)
        st.title(f"Welcome,  {name.split(' ', 1)[0]}")
        authenticator.logout("Logout", "sidebar")
        #st.write(os.getcwd()) # for dev

        selected = option_menu(
            menu_title = None,
            options = ["About", "Data Assist"],#, "SageMaker", "SQL", "Example"], #add your optios
            icons=["house","robot","book", "database-check"],
            menu_icon="menu_down",
            default_index=0,
            orientation="horizontal",
            styles={
                "container": {"display": "flex", "justify-content": "space-around"},
                "icon": {"color": "white", "font-size": "18px"},
                "nav-link": {
                    "font-size": "18px",
                    "text-align": "center",
                    "margin": "0px",
                    "padding": "10px 15px",
                    #"display": "flex",
                    #"align-items": "center",
                    #"justify-content": "center",
                    #"flex": "1",
                    "white-space": "nowrap",
                    "--hover-color": "#eee"
                },
                "nav-link-selected": {
                    #"background-color": "green",
                },
            }
        )

    if selected == "About":
        #dash_background()
        create_about()

    if selected =="Data Assist":
        sean.create_page()

    if selected=="SageMaker":
        andre.create_page()
    if selected=="SQL":
        pips.create_page()
    # move the logo up
    page_logo = f"""
    <style>
    [data-testid="stImage"] {{
        margin-top: -60px;
    }}
    </style
    """
    #TODO: UNHIDE
    #st.markdown(page_logo, unsafe_allow_html=True)

