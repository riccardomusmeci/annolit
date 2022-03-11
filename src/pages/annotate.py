import os
from pandas import options
import streamlit as st
from PIL import Image
from src.pages.utils import load_annotation_df

def set_index(idx):
    try:
        idx = int(idx)
    except:
        return 0
    
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
    
    if not st.session_state.can_annotate:
        st.error("You must setup a project first using the Setup Project page from the sidebar")
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
            st.markdown("### **Faster indexing**")
            input_col, _ = st.columns([5, 8])
            goto_idx = input_col.text_input(f'Go to image (max {st.session_state.max_index-1})', '0')
            if input_col.button("Go"):
                set_index(goto_idx)
            
            st.write("------")
            
            st.markdown("### **Slower indexing**")
            prev_col, next_col, _ = st.columns([3, 3, 10])
            
            prev_col.button("Previous Image", on_click=previous_image)
            next_col.button("Next Image", on_click=next_image)

            annotation_row = annotations_df.iloc[st.session_state.annotation_idx, :]
            image_col, info_col, categories_col = st.columns([4, 4, 2])
            
            # plotting image
            img = Image.open(annotation_row["image_path"])
            image_col.image(img, width=384)
            
            # showing image info
            img_name = annotation_row['image_path'].split(os.sep)[-1]
            label = annotation_row['label']
            info_col.markdown("<br><br>", unsafe_allow_html=True)
            info_col.markdown("### **Image Information**")
            info_col.markdown(f"* image: *{img_name}*")
            info_col.markdown(f"* label: *{label}*")
            
            # showing categories to select one from and saving new annotation
            info_col.markdown("<br>", unsafe_allow_html=True)
            info_col.markdown("### **Image Annotation**")
            category = info_col.radio(
                label="Select one category",
                options=st.session_state.categories,
            )
            
            if info_col.button("Save"):
                annotation_row["label"] = category
                annotation_row["isAnnotated"] = True
                annotations_df.iloc[st.session_state.annotation_idx, :] = annotation_row
                annotations_df.to_csv(df_path, index=False)
            

            
            
            
    

    