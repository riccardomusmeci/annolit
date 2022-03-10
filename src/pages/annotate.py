import os
from pandas import options
import streamlit as st
from PIL import Image
from src.pages.utils import load_annotation_df

def set_index(idx):
    
    try:
        idx = int(idx)
    except:
        return    
    
    if idx < st.session_state.max_index and idx > 0:
        st.session_state.annotation_idx = idx
        
def next_image():
    if st.session_state.annotation_idx < st.session_state.max_index - 1:
        st.session_state.annotation_idx += 1
    else:
        st.session_state.annotation_idx = 0

def previous_image():
    if st.session_state.annotation_idx > 0:
        st.session_state.annotation_idx -= 1
    else:
        st.session_state.annotation_idx = st.session_state.max_index-1

def fn():
    
    dataset_path = os.path.join(st.session_state.images_dir, st.session_state.dataset)
    df_path = os.path.join(st.session_state.project_dir, "annotation_df.csv")
    annotations_df = load_annotation_df(
        dataset_path=dataset_path,
        df_path=df_path
    )
    st.session_state.max_index = annotations_df.shape[0]
    
    annotation_container = st.container()
    with annotation_container:
        prev_col, next_col, _, goto_col = st.columns([3, 3, 5, 5])
        
        prev_col.button("Previous Image", on_click=previous_image)
        next_col.button("Next Image", on_click=next_image)
        
        with goto_col:
            goto_idx = goto_col.text_input(f'Go to image (max {st.session_state.max_index-1})', '0')
            if st.button("Go"):
                set_index(goto_idx)
                
        
        annotation_row = annotations_df.iloc[st.session_state.annotation_idx, :]
        image_col, info_col, categories_col = st.columns([4, 4, 2])
        
        # plotting image
        img = Image.open(annotation_row["image_path"])
        image_col.image(img, width=224)
        
        # showing image info
        img_name = annotation_row['image_path'].split(os.sep)[-1]
        label = annotation_row['label'] if annotation_row['label'] != -1 else "none"
        info_col.markdown("<br><br>", unsafe_allow_html=True)
        info_col.markdown(f"* image: *{img_name}*")
        info_col.markdown(f"* label: *{label}*")
        
        # showing categories to select one from and saving new annotation
        categories_col.markdown("<br>", unsafe_allow_html=True)
        category = categories_col.radio(
            label="Select one category",
            options=st.session_state.categories
        )
        if category != "none":
            annotation_row["label"] = category
            annotation_row["isAnnotated"] = True
            annotations_df.iloc[st.session_state.annotation_idx, :] = annotation_row
            annotations_df.to_csv(df_path, index=False)
            
                
            
                
                
        
                
                
            
            
            
    

    