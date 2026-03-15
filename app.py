import streamlit as st
from pypdf import PdfReader, PdfWriter
import io

st.set_page_config(page_title="JD PRIVATE SERVER", page_icon="🏢", layout="wide")

st.markdown("""
    <div style="background-color:#002b36;padding:20px;border-radius:10px">
    <h1 style="color:white;text-align:center;">JD CALIFORNIA </h1>
    <p style="color:#93a1a1;text-align:center;">Fast. Secure. HUB's Trusted Document Portal.</p>
    </div>
    """, unsafe_allow_html=True)

st.write("## 📄 Document Generation Portal")
uploaded_file = st.file_uploader("Upload PDF Template", type="pdf")

if uploaded_file:
    reader = PdfReader(uploaded_file)
    writer = PdfWriter()
    fields = reader.get_fields()
    
    if not fields:
        st.error("❌ This document isn't 'Smart' yet. Please contact VENDOR or JD to activate your template.")
    else:
        # We create the form for inputs
        with st.form("web_form"):
            user_inputs = {}
            col1, col2 = st.columns(2)
            for i, field_name in enumerate(fields.keys()):
                label = field_name.replace("_", " ").title()
                if i % 2 == 0:
                    user_inputs[field_name] = col1.text_input(label)
                else:
                    user_inputs[field_name] = col2.text_input(label)
            
            submit = st.form_submit_button("Prepare Document")

        # We move the download logic OUTSIDE the form
        if submit:
            writer.append(reader)
            writer.update_page_form_field_values(writer.pages[0], user_inputs)
            output = io.BytesIO()
            writer.write(output)
            data = output.getvalue()
            
            st.success("✅ Document Ready!")
            st.download_button(
                label="📥 Click to Download PDF",
                data=data,
                file_name="Filled_Legal_Doc.pdf",
                mime="application/pdf"
            )

st.markdown("---")
st.write("© 2020 JD Consulting | California | Privacy Guaranteed")
