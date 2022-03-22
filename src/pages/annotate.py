import os
import cv2
import random
import streamlit as st
import matplotlib.pyplot as plt
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
            st.markdown("### **Go to image**")
            input_col, _ = st.columns([5, 8])
            goto_idx = input_col.text_input(f'Go to image (max {st.session_state.max_index-1})', '0')
            if input_col.button("Go"):
                set_index(goto_idx)
            
            st.write("------")
            
            st.markdown(f"### **Image ({st.session_state.annotation_idx}/{st.session_state.max_index-1})**")
            prev_col, next_col, _ = st.columns([3, 3, 10])
            
            st.write("-----")
            
            prev_col.button("Previous Image", on_click=previous_image)
            next_col.button("Next Image", on_click=next_image)

            annotation_row = annotations_df.iloc[st.session_state.annotation_idx, :]
            image_col, _, info_col = st.columns([8, 1, 4])
            
            # plotting image
            img = cv2.imread(annotation_row["image_path"])
            if img.shape[0] > 768:
                width = 1024
            else:
                width = 384    
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # img = Image.open(annotation_row["image_path"])
            image_col.image(img, width=width)
            
            # showing image info
            img_name = annotation_row['image_path'].split(os.sep)[-1]
            label = annotation_row['label']
            info_col.markdown("<br><br>", unsafe_allow_html=True)
            info_col.markdown("### **Image Information**")
            info_col.text(f"Image Filename: {img_name}")
            info_col.text(f"Label: {label}")
            
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

            info_col.markdown("### **Annotations Distribution**")
            _valid_label_df = annotations_df[annotations_df["label"] != "none"]
            tot_annotations = _valid_label_df["label"].shape[0]
            plot_data = {}            
            for c in st.session_state.categories:
                plot_data[c] = 100.*_valid_label_df["label"].value_counts()[c] / tot_annotations
                
            fig, ax = plt.subplots()
            names = list(plot_data.keys())
            values = list(plot_data.values())
            ax.bar(range(len(plot_data)), values, tick_label=names)
            ax.set_ylim(bottom=0, top=100)
            ax.set_ylabel("% Annotations")
            ax.set_xlabel("Label")
            info_col.pyplot(fig)
            
            
            

            
            
            
    

    