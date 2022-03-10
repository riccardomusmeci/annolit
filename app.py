from __future__ import annotations
import streamlit as st
from src.multi_page import MultiPage
from src.pages import description, setup_project, annotate


    
st.set_page_config(layout="wide")
st.title("Annlit: annotation tool for CV")

app = MultiPage()
app.add_page(
    title="Description",
    fn=description.fn
)
app.add_page(
    title="Setup Project",
    fn=setup_project.fn
)

app.add_page(
    title="Annotate",
    fn=annotate.fn
)

app.run()






