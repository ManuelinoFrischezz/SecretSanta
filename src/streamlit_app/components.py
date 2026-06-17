import streamlit as st


def render_footer():

    st.markdown("---")

    st.markdown(
        """
        <div style='text-align: center;
                    color: #888;
                    font-size: 0.8em;'>
        🔥 Tradizione Crazy ZC 🔥
        </div>
        """,
        unsafe_allow_html=True,
    )
