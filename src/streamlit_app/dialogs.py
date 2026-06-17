from dataclasses import dataclass

import streamlit as st

from babbo_natale_segreto.participants import (
    add_new_member,
)


@dataclass
class NewMember:
    name: str

    surname: str

    cant_take_list: list[str]


@st.dialog("Add New Member")
def show_registration():

    st.write("Please enter your details.")

    new_member = NewMember(
        name=st.text_input("Nome"),
        surname=st.text_input("Cognome"),
        cant_take_list=st.multiselect(
            "Can't take",
            st.session_state["participants"],
        ),
    )

    if st.button("Submit"):
        participants = st.session_state["participants_full_info"]

        add_new_member(
            participants,
            new_member.name,
            new_member.surname,
            new_member.cant_take_list,
        )

        st.session_state["participants_full_info"] = participants

        st.session_state["participants"] = [
            p["name"] for p in participants if p["participation"] == "True"
        ]

        st.success("New member added!")

        st.rerun()
