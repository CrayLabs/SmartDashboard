import os
import pathlib

import streamlit as st
from PIL import Image

## Page Setup ##


# Add css
def local_css(file_name: str) -> None:
    with open(file_name, encoding="utf-8") as file:
        st.markdown(f"<style>{file.read()}</style>", unsafe_allow_html=True)


# Loading Image using PIL
def get_logo() -> Image.Image:
    curr_path = pathlib.Path(os.path.abspath(__file__)).parent.parent.parent
    return Image.open(curr_path / "assets/images/SmartSim.png")


# Set page config
def set_streamlit_page_config() -> None:
    curr_path = pathlib.Path(os.path.abspath(__file__)).parent.parent.parent
    logo: Image.Image = Image.open(curr_path / "assets/images/SmartSim.png")
    st.set_page_config(layout="wide", page_title="Dashboard", page_icon=logo)
