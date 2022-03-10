import streamlit as st


def setup_session():
    st.session_state.projects_dir = "projects"
    st.session_state.project_dir = None
    st.session_state.project = None
    st.session_state.categories = []
    st.session_state.images_dir = "images"
    st.session_state.dataset = None
    st.session_state.annotation_idx = 0

def fn():
    setup_session()
    st.write("Description")