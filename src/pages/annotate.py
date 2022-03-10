import os
from pandas import options
import streamlit as st
from PIL import Image
from src.pages.utils import load_annotation_df

def next_image():
    if st.session_state.annotation_idx < st.session_state.max_index:
        st.session_state.annotation_idx += 1
    else:
        st.session_state.annotation_idx = 0

def previous_image():
    if st.session_state.annotation_idx > 0:
        st.session_state.annotation_idx -= 1
    else:
        st.session_state.annotation_idx = st.session_state.max_index-1


def fn():
    if st.session_state.project is None:
        st.error("Please select a project first from 'Setup Project' page")
    else:
        dataset_path = os.path.join(st.session_state.images_dir, st.session_state.dataset)
        df_path = os.path.join(st.session_state.project_dir, "annotation_df.csv")
        annotations_df = load_annotation_df(
            dataset_path=dataset_path,
            df_path=df_path
        )
        st.session_state.max_index = annotations_df.shape[0]
        
        annotation_container = st.container()
        with annotation_container:
            _, prev_col, next_col, _, goto_col = st.columns([3, 3, 3, 7, 5])
            
            prev_col.button("Previous Image", on_click=previous_image)
            next_col.button("Next Image", on_click=next_image)
            # goto_img_idx = goto_col.text_input(f'Go to image (max {st.session_state.max_index}-1)', '')
            
            annotation_row = annotations_df.iloc[st.session_state.annotation_idx, :]
            image_col, _, categories_col, _ = st.columns([7, 1, 3, 4])
            # plotting image
            img = Image.open(annotation_row["image_path"])
            already_labeled_text = f" - labelled as {annotation_row['label']}" if annotation_row["isAnnotated"] else ""
            image_text = f"Image {annotation_row['image_path'].split(os.sep)[-1]}" + already_labeled_text
            image_col.markdown(image_text)
            image_col.image(img, width=224)
            # showing categories to select one from
            categories_col.markdown("<br><br>"<br>, unsafe_allow_html=True)
            category = categories_col.selectbox(
                label="Select one category",
                options=["none"] + st.session_state.categories
            )
            # saving annotation
            if category != "none":
                annotation_row["label"] = category
                annotation_row["isAnnotated"] = True
                annotations_df.iloc[st.session_state.annotation_idx, :] = annotation_row
                annotations_df.to_csv(df_path, index=False)
                
                
            
                
                
        
                
                
            
            
            
    

    