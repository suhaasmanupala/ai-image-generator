import streamlit as st

def setup_page():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title="AI Image Generator",
        page_icon="🎨",
        layout="centered",
        initial_sidebar_state="collapsed"
    )

def display_error(message: str):
    """Display formatted error message"""
    st.error(f"❌ {message}")
