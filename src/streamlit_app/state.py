import streamlit as st


def initialize_session_state():

    defaults = {
        "selected_name": "",
        "reveal": False,
        "pending_delete": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
