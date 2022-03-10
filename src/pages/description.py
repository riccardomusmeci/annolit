import streamlit as st
from PIL import Image

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
    st.markdown("----")
    st.markdown(
        f" \
            <font size='6'> \
                Annolit is an annotation tool for CV tasks in Streamlit. \
            </font>. \
        ", unsafe_allow_html=True
    )
    
    st.markdown("----")
    st.markdown("### Usage")
    
    st.markdown("#### 1. Setup Project")
    st.markdown("From the sidebar, go to the *Setup Project* page. Here you can")
    st.markdown("* Open a project: from a list of old annotations projects you can select one.")
    open_img_container = st.container()
    with open_img_container:
        _, img_col, _ = st.columns([4, 6, 4])
        open_img = Image.open("static/open_project.jpg")
        img_col.image(open_img, width=512)
    
    st.markdown("* Create a project: you can create a new annotation project, specifying project name, dataset to use, and classification categories.")
    create_img_container = st.container()
    with create_img_container:
        _, img_col, _ = st.columns([4, 6, 4])
        create_img = Image.open("static/create_project.jpg")
        img_col.image(create_img, width=512)
        
    st.markdown("#### 2. Annotate")
    st.markdown("From the sidebar, go to the *Annotate* page. Here you can start annotating each image in the dataset.")
    annotate_img_container = st.container()
    with annotate_img_container:
        _, img_col, _ = st.columns([4, 6, 4])
        annotate_img = Image.open("static/annotate.jpg")
        img_col.image(annotate_img, width=512)
    
    st.markdown("Every time you assing a label, an annotation.csv file is uploaded in the *projects/project_name* folder. Once you are done, this file represents the annotation file.")
    
    
    st.markdown("----------")
    st.markdown("### Warnings")
    st.warning("Be sure to have the images within the path *images/dataset_name/*.jpg*")
        
    
    