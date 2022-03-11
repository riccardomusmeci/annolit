from email.mime import image
import os
import json
import pandas as pd
import streamlit as st
from typing import Tuple

def save_metadata():
    """saves dataset name and categories dict at project_folder/metadata.json
    """
    os.makedirs(st.session_state.project_dir, exist_ok=True)
    
    metadata = {
        "dataset": st.session_state.dataset,
        "categories": []
    }
    
    metadata_path = os.path.join(st.session_state.project_dir, "metadata.json")
    
    with open(metadata_path, "w") as f:
        metadata["categories"] = [{
                "category_name": cat,
                "category_id": idx
            } for idx, cat in enumerate(st.session_state.categories)
        ]
        
        json.dump(metadata, f, indent=4)
    
def load_metadata() -> Tuple[str, list]:
    """loads metadata from project metadata.json

    Returns:
        Tuple[str, list]: dataset name, categories list
    """
    metadata_path = os.path.join(st.session_state.project_dir, "metadata.json")
    with open(metadata_path, "r") as f:
        metadata = json.load(f)
    dataset = metadata["dataset"]
    categories = [cat["category_name"] for cat in metadata["categories"]]
    return dataset, categories
     
def load_annotation_df(dataset_path: str, df_path: str) -> pd.DataFrame:
    """loads annotation df, if necessary it creates the df for the first time

    Args:
        dataset_path (str): path to dataset with images
        df_path (str): path to pd.DataFrame

    Returns:
        pd.DataFrame: pd.DataFrame
    """

    images = [os.path.join(dataset_path, f) for f in os.listdir(dataset_path) if f.endswith(".jpg")]
    if os.path.isfile(df_path) is False:
        # Creating annotation_df
        _ann_data = {
            "image_path": images, 
            "isAnnotated": [False] * len(images),
            "label": ["none"] * len(images)
        }
        annotation_df = pd.DataFrame(data=_ann_data)
        annotation_df.to_csv(df_path, index=False)
    else:
        annotation_df = pd.read_csv(df_path)
    return annotation_df 
    
    