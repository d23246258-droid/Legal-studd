import os
import streamlit as st
from PIL import Image  # Add this for image handling

# --- DIRECTORY SETUP ---
# Creating separate folders for better organization
DOCS_DIR = "saved_docs"
IMAGES_DIR = "uploaded_images"

for folder in [DOCS_DIR, IMAGES_DIR]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# --- UPDATED INTERFACE ---
if check_password():
    # ... (Header Code) ...

    tab1, tab2, tab3 = st.tabs(["📄 PDF Generator", "🖼️ Image Upload", "📂 Browse Server"])

    # TAB 2: NEW IMAGE UPLOAD SECTION
    with tab2:
        st.write("### 📤 Upload Images to Server")
        img_file = st.file_uploader("Select JPG, PNG, or JPEG", type=["jpg", "png", "jpeg"])
        
        if img_file:
            # Display a small preview before saving
            img = Image.open(img_file)
            st.image(img, caption="Preview", width=300)
            
            if st.button("Confirm & Save to Server"):
                save_path = os.path.join(IMAGES_DIR, img_file.name)
                with open(save_path, "wb") as f:
                    f.write(img_file.getbuffer())
                st.success(f"✅ {img_file.name} saved successfully!")

    # TAB 3: BROWSING SECTION (PDFs + Images)
    with tab3:
        st.write("### 🗄️ Master File Repository")
        
        sub_tab_pdf, sub_tab_img = st.tabs(["Documents", "Images"])
        
        with sub_tab_pdf:
            pdf_files = os.listdir(DOCS_DIR)
            for f in pdf_files:
                st.text(f"📄 {f}")
                # ... (Add download button logic from previous step)
        
        with sub_tab_img:
            img_files = os.listdir(IMAGES_DIR)
            if not img_files:
                st.info("No images uploaded yet.")
            else:
                # Create a grid for the images
                cols = st.columns(3)
                for idx, f_name in enumerate(img_files):
                    with cols[idx % 3]:
                        img_path = os.path.join(IMAGES_DIR, f_name)
                        st.image(img_path, use_container_width=True)
                        st.caption(f_name)
                        with open(img_path, "rb") as file:
                            st.download_button("Download", file, file_name=f_name, key=f"dl_{f_name}")
      
