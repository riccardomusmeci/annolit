
import streamlit as st
from typing import Any, Callable, Dict

class MultiPage: 
    
    def __init__(self) -> None:
        """init method
        """
        self.pages = []
        
    def add_page(self, title: str, fn: Callable) -> None: 
        """add page to multi-page webapp
        
        Args:
            title (str): The title of page which we are adding to the list of apps 
            fn (Callable): Python function to render this page in Streamlit
        """
        
        self.pages.append({
                "title": title, 
                "function": fn,
            })
        
    def run(self):
        """run a single page selected
        """
        # Dropdown to select the page to run  
        page = st.sidebar.selectbox(
            'Functionalities', 
            self.pages, 
            format_func=lambda page: page['title']
        )
            
        # run the app function 
        page['function']()
        
        
        