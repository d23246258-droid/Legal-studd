import streamlit as st
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
import io

# --- 1. CONFIG & GOLD THEME ---
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
    .stTextInput>div>div>input, .stTextArea>div>div>textarea { background-color: #1A1A1A; color: white; border: 1px solid #D4AF37; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE UNIVERSAL STAMPING ENGINE ---
def create_full_overlay(name, ssn, dob, addr, crime, ssn_img, dl_img, lawyer_id, draft_mode):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    
    # TEXT SETTINGS
    can.setFont("Helvetica-Bold", 11)
    can.setFillColor(colors.black) # Change to white if your PDF is black

    # --- TEXT COORDINATES (Adjust these using Draft Mode!) ---
    # format: can.drawString(X, Y, "Text")
    can.drawString(110, 675, f"{name}")
    can.drawString(110, 655, f"{ssn}")
    can.drawString(110, 635, f"{dob}")
    can.drawString(110, 595, f"{addr}")
    can.drawString(110, 500, f"{crime}")

    # --- IMAGE ATTACHMENTS ---
    if ssn_img:
        can.drawImage(ssn_img, 50, 50, width=150, height=100)
    if dl_img:
        can.drawImage(dl_img, 220, 50, width=150, height=100)
    if lawyer_id:
        can.drawImage(lawyer_id, 390, 50, width=150, height=100)

    # --- DRAFT MODE GRID ---
    if draft_mode:
        can.setStrokeColor(colors.red)
        can.setLineWidth(0.5)
        for i in range(0, 650, 50):
            can.line(i, 0, i, 850); can.drawString(i, 10, str(i))
        for j in range(0, 850, 50):
            can.line(0, j, 650, j); can.drawString(10, j, str(j))
    
    can.save()
    packet.seek(0)
    return PdfReader(packet)

# --- 3. INTERFACE ---
st.markdown("<h1>👑 JD GOLD HUB</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ SYSTEM SETTINGS")
    draft_mode = st.checkbox("🛠️ Enable Draft Mode", value=False)

# INITIALIZE
name, ssn, dob, address, crime = "", "", "", "", ""
ssn_img, dl_img, lawyer_id = None, None, None

st.markdown("### 📥 STEP 1: UPLOAD DOCUMENT")
template_file = st.file_uploader("Upload any PDF to edit", type="pdf")

if template_file:
    st.markdown("### ✍️ STEP 2: EDIT CATEGORIES")
    t1, t2, t3 = st.tabs(["👤 CLIENT", "⚖️ CASE", "🖼️ ATTACHMENTS"])
    
    with t1:
        name = st.text_input("Full Name")
        ssn = st.text_input("SSN")
        dob = st.text_input("DOB")
        address = st.text_area("Address")
    with t2:
        crime = st.text_area("Crime / Charges")
    with t3:
        ssn_img = st.file_uploader("Upload SSN", type=['jpg','png','jpeg'])
        dl_img = st.file_uploader("Upload DL", type=['jpg','png','jpeg'])
        lawyer_id = st.file_uploader("Lawyer ID", type=['jpg','png','jpeg'])

    st.divider()
    if st.button("⚜️ GENERATE GOLD DOCUMENT"):
        reader = PdfReader(template_file)
        writer = PdfWriter()
        writer.add_page(reader.pages[0])

        # Create the overlay with all text and images
        overlay_reader = create_full_overlay(name, ssn, dob, address, crime, ssn_img, dl_img, lawyer_id, draft_mode)
        
        # Merge onto the original PDF
        writer.pages[0].merge_page(overlay_reader.pages[0])

        # Export
        final_output = io.BytesIO()
        writer.write(final_output)
        
        st.success("✅ Processed by JD GOLD HUB")
        st.download_button("📥 DOWNLOAD PDF", final_output.getvalue(), f"JD_{name}.pdf")
else:
    st.info("Waiting for Master PDF upload...")
