import streamlit as st

from babbo_natale_segreto.commands import (
    run_sorteggio,
)


def render_sidebar():

    with st.sidebar:
        st.header("⚙️ Settings")

        st.divider()

        st.subheader("🔄 New Draw")

        confirm = st.checkbox("Confirm new draw")

        if st.button(
            "🎲 Run Draw",
            disabled=not confirm,
            use_container_width=True,
        ):
            with st.spinner("Running draw..."):
                success, message = run_sorteggio()

                if success:
                    st.success(message)

                    st.session_state["reveal"] = False

                    st.rerun()

                else:
                    st.error(message)
