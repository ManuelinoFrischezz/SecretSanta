import time

import streamlit as st

from babbo_natale_segreto.assignments import get_assignment
from babbo_natale_segreto.crypto import decrypt_name
from babbo_natale_segreto.participants import (
    load_active_participants,
    load_participants_full_info,
)
from streamlit_app.components import render_footer
from streamlit_app.dialogs import show_registration
from streamlit_app.manage_participants import render_manage_participants
from streamlit_app.sidebar import render_sidebar
from streamlit_app.state import initialize_session_state

st.set_page_config(
    page_title="🎅 Babbo Natale Segreto",
    page_icon="🎄",
    layout="centered",
)


def __main__():

    initialize_session_state()

    if "participants" not in st.session_state:
        st.session_state["participants"] = load_active_participants()

    if "participants_full_info" not in st.session_state:
        st.session_state["participants_full_info"] = load_participants_full_info()

    st.title("🎅 Babbo Natale Segreto")

    st.markdown("---")

    render_sidebar()

    if st.button("Register Here"):
        show_registration()

    participants_options = [""] + st.session_state["participants"]

    selected_name = st.session_state.get(
        "selected_name",
        "",
    )

    if selected_name not in participants_options:
        selected_name = ""

        st.session_state["selected_name"] = ""

    selected_index = participants_options.index(selected_name)

    selected_name = st.selectbox(
        "Chi sei?",
        options=participants_options,
        index=selected_index,
    )

    if selected_name != st.session_state["selected_name"]:
        st.session_state["selected_name"] = selected_name

        st.session_state["reveal"] = False

    if selected_name:
        encrypted_name, encryption_key = get_assignment(selected_name)

        if encrypted_name and encryption_key:
            left, center, right = st.columns([3, 2, 3])

            with center:
                if st.button(
                    "🎁 Scopri chi hai sorteggiato!",
                    type="primary",
                    use_container_width=True,
                ):
                    st.session_state["reveal"] = True

            if st.session_state["reveal"]:
                decrypted_name = decrypt_name(
                    encrypted_name,
                    encryption_key,
                )

                st.markdown(
                    f"""
                    <div style="
                        text-align: center;
                    ">
                        <h2>
                            🎉 Hai sorteggiato:
                        </h2>
                        <h1>
                            {decrypted_name}
                        </h1>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                time.sleep(5)

                st.session_state["reveal"] = False

                st.rerun()

    render_footer()

    render_manage_participants()


if __name__ == "__main__":
    __main__()
