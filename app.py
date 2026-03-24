import streamlit as st
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
import io

# --- 1. THEME & HEADER ---
st.set_page_config(page_title="JD GOLD HUB", page_icon="⚖️", layout="wide")
st.markdown("<style>.stApp { background-color: #000; color: #fff; } h1 { color: #D4AF37; text-align: center; }</style>", unsafe_allow_html=True)

# --- 2. THE RIGHT-CORNER STAMPER ---
def create_right_overlay(name, ssn, dob, ssn_img, draft_mode):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    
    # MOVE TEXT TO RIGHT CORNER (X=420)
    can.setFont("Helvetica-Bold", 10)
    can.setFillColor(colors.black)
    can.drawString(420, 750, f"NAME: {name}")
    can.drawString(420, 735, f"SSN: {ssn}")
    can.drawString(420, 720, f"DOB: {dob}")

    # MOVE IMAGE TO RIGHT CORNER (X=420)
    if ssn_img:
        can.drawImage(ssn_img, 420, 600, width=130, height=90)

    # DRAFT GRID (For finding perfect X/Y)
    if draft_mode:
        can.setStrokeColor(colors.red)
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
    draft_mode = st.checkbox("🛠️ Enable Draft Mode", value=False)

template_file = st.file_uploader("📥 Upload 20-Page Template", type="pdf")

if template_file:
    t1, t2 = st.tabs(["👤 CLIENT INFO", "🖼️ ATTACHMENTS"])
    with t1:
        name = st.text_input("Full Name")
        ssn = st.text_input("SSN")
        dob = st.text_input("DOB")
    with t2:
        ssn_img = st.file_uploader("Upload ID Image", type=['jpg','png','jpeg'])

    if st.button("⚜️ GENERATE MULTI-PAGE DOCUMENT"):
        reader = PdfReader(template_file)
        writer = PdfWriter()
        
        # Create the overlay for the right corner
        overlay_reader = create_right_overlay(name, ssn, dob, ssn_img, draft_mode)

        # LOOP THROUGH ALL PAGES (1 to 20+)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            
            # STAMP ONLY THE FIRST PAGE
            if page_num == 0:
                page.merge_page(overlay_reader.pages[0])
            
            writer.add_page(page)

        # EXPORT
        final_pdf = io.BytesIO()
        writer.write(final_pdf)
        st.success(f"✅ Document Processed ({len(reader.pages)} Pages)")
        st.download_button("📥 DOWNLOAD PDF", final_pdf.getvalue(), f"JD_{name}.pdf")
