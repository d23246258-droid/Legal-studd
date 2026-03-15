import streamlit as st
from pypdf import PdfReader, PdfWriter
import io

# 1. This makes it look like a professional website in the browser tab
st.set_page_config(page_title="Dhruvil Legal Solutions", page_icon="🏢", layout="wide")

# 2. Professional Header (The "Website" Look)
st.markdown("""
    <div style="background-color:#002b36;padding:20px;border-radius:10px">
    <h1 style="color:white;text-align:center;">Dhruvil Consulting: Legal & Police Automation</h1>
    <p style="color:#93a1a1;text-align:center;">Fast. Secure. Ahmedabad's Trusted Document Portal.</p>
    </div>
    """, unsafe_allow_html=True)

# 3. Sidebar with Website Info
with st.sidebar:
    st.title("About Us")
    st.write("We provide digital transformation for legal professionals and police departments in Gujarat.")
    st.write("---")
    st.write("📞 **Contact Support**")
    st.write("For custom templates or bulk access, contact Dhruvil.")

# 4. The Functional Part of the Site
st.write("## 📄 Document Generation Portal")
st.info("Upload your standardized template below to generate a print-ready PDF.")

uploaded_file = st.file_uploader("Upload PDF Template", type="pdf")

if uploaded_file:
    reader = PdfReader(uploaded_file)
    writer = PdfWriter()
    fields = reader.get_fields()
    
    if not fields:
        st.error("❌ This document isn't 'Smart' yet. Please contact Dhruvil to activate this template.")
    else:
        with st.form("web_form"):
            user_inputs = {}
            col1, col2 = st.columns(2)
            for i, field_name in enumerate(fields.keys()):
                label = field_name.replace("_", " ").title()
                if i % 2 == 0:
                    user_inputs[field_name] = col1.text_input(label)
                else:
                    user_inputs[field_name] = col2.text_input(label)
            
            if st.form_submit_button("Generate & Download"):
                writer.append(reader)
                writer.update_page_form_field_values(writer.pages[0], user_inputs)
                output = io.BytesIO()
                writer.write(output)
                st.success("✅ Document Ready!")
                st.download_button("📥 Click to Download PDF", output.getvalue(), "Legal_Doc.pdf")

# 5. Footer (Makes it feel like a real site)
st.markdown("---")
st.write("© 2026 Dhruvil Consulting | Ahmedabad, Gujarat | Privacy Guaranteed")
