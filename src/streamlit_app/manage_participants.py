import streamlit as st

from babbo_natale_segreto.commands import (
    run_sorteggio,
)
from babbo_natale_segreto.participants import (
    delete_participant,
    toggle_participant,
)


def render_manage_participants():

    with st.expander(
        "👥 Manage Participants",
        expanded=False,
    ):
        st.write("Enable, disable or remove participants.")

        participants = st.session_state["participants_full_info"]

        for participant in participants:
            name = participant["name"]

            active = participant["participation"] == "True"

            col1, col2, col3 = st.columns([5, 2, 2])

            with col1:
                status = "🟢" if active else "🔴"

                st.write(f"{status} {name}")

            with col2:
                if st.button(
                    ("Exclude" if active else "Include"),
                    key=f"toggle_{name}",
                    use_container_width=True,
                ):
                    toggle_participant(
                        participants,
                        name,
                    )

                    success, _ = run_sorteggio()

                    if success:
                        st.session_state["participants_full_info"] = participants

                        st.session_state["participants"] = [
                            p["name"]
                            for p in participants
                            if p["participation"] == "True"
                        ]

                    st.rerun()

            with col3:
                if st.button(
                    "Delete",
                    key=f"delete_{name}",
                    type="primary",
                    use_container_width=True,
                ):
                    updated = delete_participant(
                        participants,
                        name,
                    )

                    success, _ = run_sorteggio()

                    if success:
                        st.session_state["participants_full_info"] = updated

                        st.session_state["participants"] = [
                            p["name"] for p in updated if p["participation"] == "True"
                        ]

                    st.rerun()
