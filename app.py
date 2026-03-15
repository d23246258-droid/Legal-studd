import streamlit as st
from pypdf import PdfReader, PdfWriter
import io
import datetime

# --- CONFIGURATION & THEME ---
st.set_page_config(page_title="JD PRIVATE SERVER", page_icon="⚖️", layout="wide")

# CUSTOM CSS FOR THE "PREMIUM" LOOK
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #f63366;
        color: white;
    }
    .login-header {
        font-family: 'Helvetica Neue', sans-serif;
        color: #d4af37; /* Gold Color */
        text-align: center;
        padding-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- USER DATABASE (This is where you add members) ---
# Format: "USER_ID": "PASSWORD"
USERS = {
    "24KJP": "JP916",      # Your first member
    "ADMIN": "JD2026",     # Your master key
    "GUEST": "WELCOME26"   # Example for a trial user
}

# --- AUTHENTICATION LOGIC ---
def check_password():
    if "auth" not in st.session_state:
        st.session_state["auth"] = False

    if not st.session_state["auth"]:
        st.markdown("<h1 class='login-header'>⚖️ JD CALIFORNIA <br>PRIVATE GATEWAY</h1>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1.5, 1])
        with col2:
            with st.container(border=True):
                u_id = st.text_input("Member ID")
                u_pw = st.text_input("Security Key", type="password")
                if st.button("Access Server"):
                    if u_id in USERS and USERS[u_id] == u_pw:
                        st.session_state["auth"] = True
                        st.session_state["user"] = u_id
                        st.rerun()
                    else:
                        st.error("Invalid Credentials. Contact JD for access.")
        return False
    return True

# --- MAIN APP INTERFACE ---
if check_password():
    user = st.session_state["user"]
    
    # Branded Header
    st.markdown(f"""
        <div style="background: linear-gradient(90deg, #002b36, #073642); padding:25px; border-radius:15px; border-left: 10px solid #d4af37;">
            <h1 style="color:white; margin:0;">JD CALIFORNIA : {user}</h1>
            <p style="color:#93a1a1; margin:0;">Standardized Document Automation • Secured System</p>
        </div>
        """, unsafe_allow_html=True)

    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/1041/1041916.png", width=100) # Placeholder Logo
        st.title("Admin Panel")
        st.write(f"Logged in: **{user}**")
        st.divider()
        if st.button("Logout"):
            st.session_state["auth"] = False
            st.rerun()

    st.write("### 📂 Upload Your Template")
    uploaded_file = st.file_uploader("", type="pdf")

    if uploaded_file:
        reader = PdfReader(uploaded_file)
        writer = PdfWriter()
        fields = reader.get_fields()
        
        if not fields:
            st.warning("⚠️ This PDF is not 'Smart' yet. Please map it in PDFescape first.")
        else:
            with st.form("doc_form"):
                st.write("#### 📝 Input Required Details")
                user_inputs = {}
                cols = st.columns(2)
                for i, field_name in enumerate(fields.keys()):
                    label = field_name.replace("_", " ").title()
                    with cols[i % 2]:
                        user_inputs[field_name] = st.text_input(label)
                
                if st.form_submit_button("Generate Document"):
                    writer.append(reader)
                    writer.update_page_form_field_values(writer.pages[0], user_inputs)
                    
                    # LOGGING (For your security audits)
                    log_time = datetime.datetime.now().strftime("%H:%M:%S")
                    
                    output = io.BytesIO()
                    writer.write(output)
                    
                    st.success(f"✅ Success! Document prepared at {log_time}")
                    st.download_button(
                        label="📥 Download Final PDF",
                        data=output.getvalue(),
                        file_name=f"{user}_Generated_{datetime.date.today()}.pdf",
                        mime="application/pdf"
                    )

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>© 2026 JD Consulting | Empowering Ahmedabad Legal Professionals</p>", unsafe_allow_html=True)
