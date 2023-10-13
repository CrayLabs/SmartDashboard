import streamlit as st
from PIL import Image


def local_css(file_name: str) -> None:
    """Add CSS to the dashboard

    The CSS needs to be called on every page.

    :param file_name: CSS file
    :type file_name: str
    """
    with open(file_name, encoding="utf-8") as file:
        st.markdown(f"<style>{file.read()}</style>", unsafe_allow_html=True)

    # st.markdown("""<link href="http://localhost:8501/app/static/style.css" type="text/css">""", unsafe_allow_html=True)


def set_streamlit_page_config() -> None:
    """Add Streamlit page configuration

    Sets the layout to wide, adds Smartsim
    logo and Dashboard title to browser tab.
    Also needs to be called on every page.
    """
    logo: Image.Image = Image.open("smartdashboard/static/SmartSim.png")
    st.set_page_config(layout="wide", page_title="Dashboard", page_icon=logo)
