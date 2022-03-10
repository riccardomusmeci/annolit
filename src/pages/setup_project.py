import os
import json
import streamlit as st
from src.pages.utils import load_metadata, save_metadata

def reset_project():
    st.session_state.project = None

def set_new_project():
    st.session_state.new_project = True
    
def set_old_project():
    st.session_state.new_project = False
    
def open_project(render_container):
    reset_project()
    render_container.empty()
    render_container = st.container()
    with render_container:
        projects =  ["none"] + [p for p in os.listdir(st.session_state.projects_dir)]
        project = st.selectbox(
            'Which project would you like to open?',
            projects
        )
        if project != "none":
            # Setting session vars
            st.session_state.project = project
            st.session_state.project_dir = os.path.join(st.session_state.projects_dir, project)
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
    # reset_project()
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
            st.markdown("**Categories**")
            for c in st.session_state.categories:
                st.markdown(f"* **{c}**")          
            
def fn():
    """calls the setup project page function

    Args:
        project_dir (str): old project dirs

    Returns:
        str: selected (either new or old) project name
    """
    st.markdown("## **Setup Project**")
    st.write("Choose between an old annotation project or creating a new one")
       
    old_project_button, new_project_button, _ = st.columns([2, 2, 10])
    new_project_button.button(label="New Project", on_click=set_new_project)
    old_project_button.button(label="Open Project", on_click=set_old_project)
    
    render_container = st.empty()

    if 'new_project' in st.session_state:
        if st.session_state.new_project:
            new_project(render_container)
            add_dataset_and_categories()
        else:
            open_project(render_container)
    
    
    
