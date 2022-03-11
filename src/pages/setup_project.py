import os
import streamlit as st
from src.pages.utils import load_metadata, save_metadata

def reset_project():
    st.session_state.project = None
    
def reset_annotation():
    st.session_state.annotation_idx = 0

def open_project(render_container):
    reset_project()
    render_container.empty()
    render_container = st.container()
    with render_container:
        projects = ["none"]
        if os.path.isdir(st.session_state.projects_dir):
            projects += [p for p in os.listdir(st.session_state.projects_dir)]
        project = st.selectbox(
            'Which project would you like to open?',
            projects
        )
        if project != "none":
            # Setting session vars
            st.session_state.project = project
            st.session_state.project_dir = os.path.join(st.session_state.projects_dir, project)
            st.session_state.can_annotate = True
            st.markdown(f"* Project name: **{project}**")
            dataset, categories = load_metadata()
            st.session_state.categories = categories
            st.session_state.dataset = dataset
            st.markdown(f"* Dataset name: **{dataset}**")
            st.markdown(f"* Categories: **{', '.join(categories)}**")
    
def new_project(render_container):
    """create new project

    Args:
        render_container (st.emtpy()): streamlit empty container
    """
    # reset graphics
    reset_annotation()
    render_container.empty()
    render_container = st.container()
    
    with render_container:
        st.markdown("### **New Annotation Project**")
        project = st.text_input('New project name', '')
        st.write(f'The new annotation project is {project}')
        if st.button(label="Create Project"):
            st.session_state.project = project
            # saving dir
            st.session_state.project_dir = os.path.join(st.session_state.projects_dir, project)
            st.session_state.categories = []
                
def add_dataset_and_categories():
    """add categories to project

    Args:
        render_container (_type_): streamlit render container
    """
    if st.session_state.project is not None:
        # scegli cartella di immagini da annotare
        datasets = ["none"] + [d for d in os.listdir(st.session_state.images_dir)]
        dataset = st.selectbox(
            'Which image folder would you like to annotate?',
            datasets
        )
        if dataset != "none":
            st.markdown(f"### **New annotation project {st.session_state.project} for dataset {dataset}**")
            st.session_state.dataset = dataset
            st.markdown("#### **Add New Categories**")
            category = st.text_input('Add a new category', '')
            # add and save buttons
            add_bttn, _, save_bttn = st.columns([2, 6, 2])
            if add_bttn.button("Add Category"):
                st.session_state.categories.append(category)
            if save_bttn.button("Save Project Metadata"):
                save_metadata()
                st.session_state.can_annotate = True
            st.markdown("**Categories**")
            for c in st.session_state.categories:
                st.markdown(f"* **{c}**")      
            
def fn():
    """calls the setup project page function
    """
    st.markdown("## **Setup Project**")
       
    render_container = st.empty()
    project_option = st.selectbox(
        label="Choose between an old annotation project or creating a new one",
        options=["none", "Open Project", "Create Project"]
    )
    
    if project_option == "Create Project":
        new_project(render_container)
        add_dataset_and_categories()
    if project_option == "Open Project":
        open_project(render_container)
    
    st.write("----")
    st.warning("Once you are done in setting up the annotation project, go to Annotate page from the sidebar")    
        
    

    
        
    
    
    
