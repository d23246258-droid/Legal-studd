import streamlit as st
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
import io

# --- 1. PREMIUM THEME & CONFIG ---
st.set_page_config(page_title="JD GOLD HUB | Legal Portal", page_icon="⚖️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    h1, h2, h3 { color: #D4AF37; font-family: 'serif'; text-align: center; }
    .stButton>button { 
        background: linear-gradient(45deg, #D4AF37, #F9E27D); 
        color: black; font-weight: bold; border-radius: 8px; width: 100%; height: 3.5em;
    }
    .stTabs [aria-selected="true"] { color: #D4AF37; border-bottom: 2px solid #D4AF37; }
    .stTextInput>div>div>input { background-color: #1A1A1A; color: white; border: 1px solid #D4AF37; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE IMAGE STAMPING ENGINE ---
def create_overlay(img_file, x, y, w, h, show_grid=False):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    if img_file:
        can.drawImage(img_file, x, y, width=w, height=h)
    
    if show_grid:
        can.setStrokeColor(colors.red)
        can.setLineWidth(0.5)
        for i in range(0, 650, 50):
            can.line(i, 0, i, 850); can.drawString(i, 10, str(i))
        for j in range(0, 850, 50):
            can.line(0, j, 650, j); can.drawString(10, j, str(j))
    can.save()
    packet.seek(0)
    return PdfReader(packet)

# --- 3. THE PORTAL INTERFACE ---
st.markdown("<h1>👑 JD GOLD HUB</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>Premium California Legal Document Automation</p>", unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ SYSTEM SETTINGS")
    draft_mode = st.checkbox("🛠️ Enable Draft Mode (Coordinate Grid)", value=False)
    st.info("Use Draft Mode to find X/Y positions for images.")

# INITIALIZE ALL CATEGORY VARIABLES
name, ssn, dob, address, phone, email, crime = "", "", "", "", "", "", ""
ssn_img, dl_img, lawyer_id = None, None, None

# STEP 1: UPLOAD THE DOCUMENT TO EDIT
st.markdown("### 📥 STEP 1: UPLOAD MASTER DOCUMENT")
template_file = st.file_uploader("Select the PDF template you want to edit", type="pdf")

if not template_file:
    st.warning("Please upload a PDF template to begin editing.")
else:
    st.success("✅ Template Active. Proceed to Step 2.")
    
    # STEP 2: CATEGORY-WISE EDITING
    st.markdown("### ✍️ STEP 2: EDIT CATEGORIES")
    t1, t2, t3 = st.tabs(["👤 CLIENT IDENTITY", "⚖️ CASE INFO", "🖼️ ATTACHMENTS"])

    with t1:
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Full Name")
            ssn = st.text_input("SSN (XXX-XX-XXXX)")
        with c2:
            dob = st.text_input("Date of Birth")
            address = st.text_area("Full Residential Address")

    with t2:
        crime = st.text_area("Nature of Crime / Legal Charges")
        phone = st.text_input("Contact Number")
        email = st.text_input("Email Address")

    with t3:
        st.write("Files uploaded here will be auto-attached to the PDF.")
        col_img1, col_img2 = st.columns(2)
        with col_img1:
            ssn_img = st.file_uploader("Upload SSN Image", type=['jpg', 'png', 'jpeg'])
        with col_img2:
            dl_img = st.file_uploader("Upload Driving License", type=['jpg', 'png', 'jpeg'])
        lawyer_id = st.file_uploader("Upload Identity of Lawyer", type=['jpg', 'png', 'jpeg'])

    # STEP 3: THE GOLD GENERATION
    st.divider()
    if st.button("⚜️ GENERATE & ATTACH TO DOCUMENT"):
        # READ THE UPLOADED TEMPLATE
        reader = PdfReader(template_file)
        writer = PdfWriter()
        writer.add_page(reader.pages[0]) # Start with Page 1
        
        # MAP TEXT DATA (Ensure PDF field names match these keys)
        text_data = {
            "full_name": name,
            "ssn_field": ssn,
            "address_field": address,
            "crime_field": crime
        }
        writer.update_page_form_field_values(writer.pages[0], text_data)
        
        # AUTO-ATTACH IMAGES (Stamp logic)
        # Position 1: SSN (Bottom Left example)
        if ssn_img:
            ssn_overlay = create_overlay(ssn_img, 50, 50, 150, 100, show_grid=draft_mode)
            writer.pages[0].merge_page(ssn_overlay.pages[0])
        
        # Position 2: DL (Bottom Right example)
        if dl_img:
            dl_overlay = create_overlay(dl_img, 400, 50, 150, 100, show_grid=draft_mode)
            writer.pages[0].merge_page(dl_overlay.pages[0])

        # EXPORT FINAL PRODUCT
        final_output = io.BytesIO()
        writer.write(final_output)
        
        st.balloons()
        st.success("⚜️ JD GOLD HUB: Document processing complete.")
        st.download_button(
            label="📥 DOWNLOAD EDITED PDF",
            data=final_output.getvalue(),
            file_name=f"JD_GOLD_{name}.pdf",
            mime="application/pdf"
        )
