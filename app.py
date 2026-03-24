# --- INITIALIZE VARIABLES (Add this before tab1, tab2, tab3) ---
name = ""
ssn = ""
dob = ""
address = ""
phone = ""
email = ""
crime = ""
ssn_img = None
dl_img = None
lawyer_id = None

# --- NOW START YOUR TABS ---
tab1, tab2, tab3 = st.tabs(["👤 CLIENT IDENTITY", "⚖️ CASE DETAILS", "🖼️ ATTACHMENT UPLOADS"])

with tab1:
    name = st.text_input("Full Name")
    # ... rest of your inputs ...

with tab3:
    ssn_img = st.file_uploader("Image of SSN", type=['png', 'jpg', 'jpeg'])
    # ... rest of your uploads ...

# --- NOW THE GENERATION ENGINE WILL WORK ---
if st.button("⚜️ GENERATE GOLD STANDARD DOCUMENT"):
    if ssn_img: # Python now knows what ssn_img is!
        # Your overlay code here...
import streamlit as st
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
import io

# --- PREVIOUS CONFIG & THEME (Keep your existing CSS) ---
st.set_page_config(page_title="JD GOLD HUB | Legal Portal", page_icon="⚖️", layout="wide")

# --- IMPROVED OVERLAY FUNCTION ---
def create_overlay(img_file, x, y, w, h, show_grid=False):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    
    # 1. Draw the actual image
    if img_file:
        can.drawImage(img_file, x, y, width=w, height=h)
    
    # 2. DRAFT MODE: Draw a Grid and Label Coordinates
    if show_grid:
        can.setStrokeColor(colors.red)
        can.setLineWidth(0.5)
        # Draw vertical and horizontal lines every 50 pixels
        for i in range(0, 650, 50):
            can.line(i, 0, i, 800) # Vertical
            can.drawString(i, 10, str(i))
        for j in range(0, 850, 50):
            can.line(0, j, 600, j) # Horizontal
            can.drawString(10, j, str(j))
        
        # Highlight the current image box in Red
        can.setDash(3, 3)
        can.rect(x, y, w, h, stroke=1, fill=0)
        can.drawString(x, y-15, f"Target: x={x}, y={y}")

    can.save()
    packet.seek(0)
    return PdfReader(packet)

# --- SIDEBAR SETTINGS ---
with st.sidebar:
    st.markdown("## ⚙️ SYSTEM SETTINGS")
    draft_mode = st.checkbox("🛠️ Enable Draft Mode (Show Grid)", value=False)
    if draft_mode:
        st.warning("Draft Mode is ON. Red coordinates will appear on the PDF.")

# --- THE REST OF YOUR PORTAL CODE ---
st.markdown("<h1 style='text-align: center;'>👑 JD GOLD HUB</h1>", unsafe_allow_html=True)

# ... (Insert your Tabs and Inputs here from the previous code) ...

# --- GENERATION LOGIC ---
if st.button("⚜️ GENERATE GOLD STANDARD DOCUMENT"):
    # ... (Standard PDF Loading logic) ...
    
    # When calling the overlay, pass the 'draft_mode' variable
    if ssn_img:
        # Currently set to x=50, y=50. Change these numbers based on the grid!
        ov = create_overlay(ssn_img, 50, 50, 150, 100, show_grid=draft_mode)
        writer.pages[0].merge_page(ov.pages[0])
        
    if dl_img:
        # Currently set to x=400, y=50
        ov2 = create_overlay(dl_img, 400, 50, 150, 100, show_grid=draft_mode)
        writer.pages[0].merge_page(ov2.pages[0])

    # ... (Save and Download logic) ...
