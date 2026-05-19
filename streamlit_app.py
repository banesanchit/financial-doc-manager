import streamlit as st
import requests
import re

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="FinDoc AI",
    page_icon="📊",
    layout="wide"
)

# ─── CUSTOM CSS ────────────────────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f !important;
    color: #e8e4dc !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stAppViewContainer"] {
    background: #0a0a0f !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0f0f17 !important;
    border-right: 1px solid #1e1e2e !important;
    padding-top: 0 !important;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 2rem;
}

/* ── Selectbox ── */
[data-testid="stSelectbox"] label {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    color: #c0bdb5 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}

[data-testid="stSelectbox"] > div > div {
    background: #141420 !important;
    border: 1px solid #2a2a3e !important;
    border-radius: 8px !important;
    color: #f0ece4 !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stSelectbox"] span {
    color: #f0ece4 !important;
}

/* ── Text Inputs ── */
[data-testid="stTextInput"] label,
[data-testid="stNumberInput"] label,
[data-testid="stFileUploader"] label {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    color: #c0bdb5 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}

[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input {
    background: #141420 !important;
    border: 1px solid #2a2a3e !important;
    border-radius: 8px !important;
    color: #f0ece4 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.6rem 1rem !important;
    transition: border-color 0.2s !important;
    caret-color: #f0a500 !important;
}

[data-testid="stTextInput"] input::placeholder,
[data-testid="stNumberInput"] input::placeholder {
    color: #444460 !important;
}

[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus {
    border-color: #f0a500 !important;
    box-shadow: 0 0 0 2px rgba(240, 165, 0, 0.15) !important;
    outline: none !important;
}

[data-testid="stTextInput"] [type="password"] {
    background: #141420 !important;
    color: #f0ece4 !important;
}

/* ── Subheader ── */
[data-testid="stHeadingWithActionElements"] h2,
[data-testid="stHeadingWithActionElements"] h3 {
    font-family: 'Syne', sans-serif !important;
    color: #f0ece4 !important;
    font-weight: 700 !important;
}

/* ── Buttons ── */
[data-testid="stButton"] > button {
    background: #f0a500 !important;
    color: #0a0a0f !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
    padding: 0.55rem 1.4rem !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
    width: 100% !important;
}

[data-testid="stButton"] > button:hover {
    background: #ffc130 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(240, 165, 0, 0.3) !important;
}

[data-testid="stButton"] > button:active {
    transform: translateY(0) !important;
}

/* Logout button — ghost style */
[data-testid="stSidebar"] [data-testid="stButton"] > button {
    background: transparent !important;
    color: #aaa !important;
    border: 1px solid #2a2a3e !important;
    font-size: 0.78rem !important;
    padding: 0.4rem 1rem !important;
    width: auto !important;
}

[data-testid="stSidebar"] [data-testid="stButton"] > button:hover {
    background: #1e1e2e !important;
    color: #e8e4dc !important;
    border-color: #3a3a5e !important;
    transform: none !important;
    box-shadow: none !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: #141420 !important;
    border: 1px dashed #2a2a3e !important;
    border-radius: 12px !important;
    padding: 1rem !important;
    transition: border-color 0.2s !important;
}

[data-testid="stFileUploader"] > div {
    color: #c0bdb5 !important;
}

[data-testid="stFileUploader"]:hover {
    border-color: #f0a500 !important;
}

/* ── Containers / Cards ── */
[data-testid="stVerticalBlock"] [data-testid="stVerticalBlockBorderWrapper"] {
    background: #111119 !important;
    border: 1px solid #1e1e2e !important;
    border-radius: 12px !important;
    padding: 1.2rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}

[data-testid="stVerticalBlock"] [data-testid="stVerticalBlockBorderWrapper"]:hover {
    border-color: #2a2a4e !important;
    box-shadow: 0 4px 24px rgba(0,0,0,0.4) !important;
}

/* ── Markdown ── */
[data-testid="stMarkdownContainer"] h1 {
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
    color: #f0f0f0 !important;
    font-size: 2rem !important;
}

[data-testid="stMarkdownContainer"] h2 {
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    color: #f0ece4 !important;
    font-size: 1.3rem !important;
    border-bottom: 1px solid #1e1e2e !important;
    padding-bottom: 0.5rem !important;
    margin-bottom: 1rem !important;
}

[data-testid="stMarkdownContainer"] h3 {
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    color: #f0ece4 !important;
    font-size: 1rem !important;
}

[data-testid="stMarkdownContainer"] p {
    font-family: 'DM Sans', sans-serif !important;
    color: #9090a8 !important;
    font-size: 0.88rem !important;
    line-height: 1.6 !important;
}

[data-testid="stMarkdownContainer"] strong {
    color: #d8d5cd !important;
    font-weight: 600 !important;
}

/* ── Caption ── */
[data-testid="stCaptionContainer"] p {
    color: #555568 !important;
    font-size: 0.82rem !important;
}

/* ─────────────────────────────────────────────────
   HIDE default Streamlit alerts — we use custom ones
───────────────────────────────────────────────── */
div[data-testid="stAlert"] {
    display: none !important;
}

/* ── Custom Toast Alerts ── */
.toast-success {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    background: #071a0e;
    border: 1.5px solid #22c55e;
    border-left: 4px solid #22c55e;
    border-radius: 10px;
    padding: 0.9rem 1.2rem;
    margin: 0.75rem 0;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.95rem;
    font-weight: 500;
    color: #4ade80;
    letter-spacing: 0.01em;
}

.toast-error {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    background: #1a0808;
    border: 1.5px solid #ef4444;
    border-left: 4px solid #ef4444;
    border-radius: 10px;
    padding: 0.9rem 1.2rem;
    margin: 0.75rem 0;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.95rem;
    font-weight: 500;
    color: #f87171;
    letter-spacing: 0.01em;
}

.toast-warning {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    background: #1a1000;
    border: 1.5px solid #f59e0b;
    border-left: 4px solid #f59e0b;
    border-radius: 10px;
    padding: 0.9rem 1.2rem;
    margin: 0.75rem 0;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.95rem;
    font-weight: 500;
    color: #fbbf24;
    letter-spacing: 0.01em;
}

.toast-icon { font-size: 1.15rem; flex-shrink: 0; }

/* ── Divider ── */
hr {
    border: none !important;
    border-top: 1px solid #1e1e2e !important;
    margin: 1.5rem 0 !important;
}

/* ── Layout helpers ── */
.main-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.4rem;
    font-weight: 800;
    color: #f0f0f0;
    letter-spacing: -0.03em;
    line-height: 1.1;
    margin-bottom: 0.25rem;
}
.main-title span { color: #f0a500; }

.main-subtitle {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.9rem;
    color: #555568;
    letter-spacing: 0.04em;
}

.header-bar {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 2.5rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid #1e1e2e;
}

.header-icon {
    width: 44px;
    height: 44px;
    background: #f0a500;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
    flex-shrink: 0;
}

.section-pill {
    display: inline-block;
    background: rgba(240,165,0,0.12);
    color: #f0a500;
    font-family: 'Syne', sans-serif;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 0.25rem 0.75rem;
    border-radius: 100px;
    margin-bottom: 1rem;
}

.badge {
    display: inline-block;
    padding: 0.15rem 0.6rem;
    border-radius: 100px;
    font-size: 0.72rem;
    font-family: 'DM Sans', sans-serif;
    font-weight: 600;
}
.badge-report   { background: rgba(240,165,0,0.15);   color: #f0a500; }
.badge-invoice  { background: rgba(100,200,150,0.15); color: #64c896; }
.badge-contract { background: rgba(120,150,255,0.15); color: #7896ff; }
.badge-admin    { background: rgba(255,100,100,0.15); color: #ff6464; }
.badge-analyst  { background: rgba(100,180,255,0.15); color: #64b4ff; }
.badge-auditor  { background: rgba(200,150,255,0.15); color: #c896ff; }
.badge-client   { background: rgba(100,220,180,0.15); color: #64dcb4; }
</style>
""", unsafe_allow_html=True)


# ─── HELPER — Custom visible alert boxes ───────────────────────────────────────

def show_success(msg):
    st.markdown(f"""
    <div class="toast-success">
        <span class="toast-icon">✅</span>
        <span>{msg}</span>
    </div>""", unsafe_allow_html=True)

def show_error(msg):
    st.markdown(f"""
    <div class="toast-error">
        <span class="toast-icon">❌</span>
        <span>{msg}</span>
    </div>""", unsafe_allow_html=True)

def show_warning(msg):
    st.markdown(f"""
    <div class="toast-warning">
        <span class="toast-icon">⚠️</span>
        <span>{msg}</span>
    </div>""", unsafe_allow_html=True)


# ─── SESSION VARIABLES ─────────────────────────────────────────────────────────

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "token" not in st.session_state:
    st.session_state.token = None
if "username" not in st.session_state:
    st.session_state.username = ""
if "email" not in st.session_state:
    st.session_state.email = ""
if "role" not in st.session_state:
    st.session_state.role = ""
if "flash_message" not in st.session_state:
    st.session_state.flash_message = None
if "flash_type" not in st.session_state:
    st.session_state.flash_type = None


# ─── SIDEBAR ───────────────────────────────────────────────────────────────────

st.sidebar.markdown("""
<div style="font-family:'Syne',sans-serif; font-size:1.1rem; font-weight:800;
     color:#f0a500; letter-spacing:0.04em; text-transform:uppercase;
     padding:0 0.5rem; margin-bottom:0.5rem;">
    📁 FinDoc AI
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

if st.session_state.logged_in:
    role = st.session_state.role
    role_badge_map = {
        "Admin": "badge-admin",
        "Financial Analyst": "badge-analyst",
        "Auditor": "badge-auditor",
        "Client": "badge-client",
    }
    badge_class = role_badge_map.get(role, "badge-client")

    st.sidebar.markdown(f"""
    <div style="padding:0.75rem 0.8rem; background:#141420; border-radius:10px;
         margin-bottom:0.75rem; border:1px solid #1e1e2e;">
        <div style="font-family:'DM Sans',sans-serif; font-size:0.72rem; color:#777790;
             margin-bottom:0.3rem; text-transform:uppercase; letter-spacing:0.06em;">
             Signed in as
        </div>
        <div style="font-family:'Syne',sans-serif; font-size:1rem; font-weight:700;
             color:#f0ece4;">
             {st.session_state.username}
        </div>
        <div style="margin-top:0.4rem;">
            <span class="badge {badge_class}">{role}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.sidebar.button("Logout"):
        st.session_state.logged_in     = False
        st.session_state.token         = None
        st.session_state.username      = ""
        st.session_state.email         = ""
        st.session_state.role          = ""
        st.session_state.flash_message = "You have been logged out successfully."
        st.session_state.flash_type    = "success"
        st.rerun()

    st.sidebar.markdown("---")

# ─── MENU ──────────────────────────────────────────────────────────────────────

menu_options = ["Login", "Register"]

if st.session_state.logged_in:
    role = st.session_state.role
    if role == "Admin":
        menu_options.extend([
            "Upload Document", "View Documents",
            "Metadata Search", "Semantic Search",
            "Delete Document", "Admin Panel"
        ])
    elif role == "Financial Analyst":
        menu_options.extend([
            "Upload Document", "View Documents",
            "Metadata Search", "Semantic Search"
        ])
    elif role == "Auditor":
        menu_options.extend([
            "View Documents", "Metadata Search", "Semantic Search"
        ])
    elif role == "Client":
        menu_options.extend(["View Documents"])

menu = st.sidebar.selectbox("Navigation", menu_options)

# ─── HEADER ────────────────────────────────────────────────────────────────────

st.markdown("""
<div class="header-bar">
  <div class="header-icon">📊</div>
  <div>
    <div class="main-title">Financial<span> Doc</span> Manager</div>
    <div class="main-subtitle">AI-POWERED DOCUMENT ANALYSIS · RAG SYSTEM</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── FLASH MESSAGE (persists across rerun — e.g. after login / logout) ─────────

if st.session_state.flash_message:
    fmsg  = st.session_state.flash_message
    ftype = st.session_state.flash_type
    if ftype == "success":
        show_success(fmsg)
    elif ftype == "error":
        show_error(fmsg)
    else:
        show_warning(fmsg)
    st.session_state.flash_message = None
    st.session_state.flash_type    = None

# ─── REGISTER ──────────────────────────────────────────────────────────────────

if menu == "Register":
    st.markdown('<div class="section-pill">New Account</div>', unsafe_allow_html=True)
    st.subheader("Create Your Account")
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        username  = st.text_input("Username")
        email     = st.text_input("Email")
    with col2:
        password  = st.text_input("Password", type="password")
        role_name = st.selectbox(
            "Select Role",
            ["Admin", "Financial Analyst", "Auditor", "Client"]
        )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("✦ Create Account"):
        if len(username.strip()) < 3:
            show_error("Username must contain at least 3 characters")
        elif not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.com$", email):
            show_error("Please enter a valid email address")
        elif len(password) < 6:
            show_error("Password must contain at least 6 characters")
        else:
            response = requests.post(
                f"{API_URL}/auth/register",
                json={"username": username, "email": email, "password": password}
            )
            data = response.json()
            if "user_id" in data:
                user_id = data["user_id"]
                role_mapping = {
                    "Admin": 1, "Financial Analyst": 2,
                    "Auditor": 3, "Client": 4
                }
                role_id = role_mapping[role_name]
                requests.post(
                    f"{API_URL}/users/assign-role",
                    params={"user_id": user_id, "role_id": role_id}
                )
                show_success(f"🎉 {role_name} account registered successfully! You can now log in.")
            else:
                show_error("Registration failed. Please try again.")

# ─── LOGIN ─────────────────────────────────────────────────────────────────────

if menu == "Login":
    st.markdown('<div class="section-pill">Access</div>', unsafe_allow_html=True)
    st.subheader("Sign In to FinDoc")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        email    = st.text_input("Email")
        password = st.text_input("Password", type="password")
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("→ Sign In"):
            if not email or not password:
                show_error("Please fill in all fields")
            else:
                response = requests.post(
                    f"{API_URL}/auth/login",
                    json={"email": email, "password": password}
                )
                data = response.json()
                if "access_token" in data:
                    st.session_state.logged_in     = True
                    st.session_state.token         = data["access_token"]
                    st.session_state.username      = data["username"]
                    st.session_state.email         = data["email"]
                    st.session_state.role          = data["role"]
                    st.session_state.flash_message = f"Welcome back, {data['username']}! Login successful."
                    st.session_state.flash_type    = "success"
                    st.rerun()
                else:
                    show_error("Invalid email or password. Please try again.")

    with col2:
        st.markdown("""
        <div style="padding:1.5rem; background:#111119; border:1px solid #1e1e2e;
             border-radius:12px;">
            <div style="font-family:'Syne',sans-serif; font-size:0.8rem; font-weight:700;
                 color:#f0a500; text-transform:uppercase; letter-spacing:0.08em;
                 margin-bottom:1rem;">
                Role Permissions
            </div>
            <div style="font-family:'DM Sans',sans-serif; font-size:0.85rem;
                 color:#888; line-height:2.4;">
                <span class="badge badge-admin">Admin</span>
                <span style="color:#c0bdb5; margin-left:0.5rem;">Full access · Delete · Manage users</span><br>
                <span class="badge badge-analyst">Financial Analyst</span>
                <span style="color:#c0bdb5; margin-left:0.5rem;">Upload · Search · View</span><br>
                <span class="badge badge-auditor">Auditor</span>
                <span style="color:#c0bdb5; margin-left:0.5rem;">Search · View documents</span><br>
                <span class="badge badge-client">Client</span>
                <span style="color:#c0bdb5; margin-left:0.5rem;">View documents only</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ─── UPLOAD DOCUMENT ───────────────────────────────────────────────────────────

if menu == "Upload Document":
    if st.session_state.role not in ["Admin", "Financial Analyst"]:
        show_error("You are not authorized to upload documents")
    else:
        st.markdown('<div class="section-pill">Upload</div>', unsafe_allow_html=True)
        st.subheader("Upload Financial PDF")
        st.markdown("---")

        col1, col2 = st.columns(2)
        with col1:
            title         = st.text_input("Document Title")
            company_name  = st.text_input("Company Name")
            document_type = st.selectbox("Document Type", ["report", "invoice", "contract"])
        with col2:
            uploaded_file = st.file_uploader("Choose PDF File", type=["pdf"])

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("↑ Upload Document"):
            if not title:
                show_error("Title is required")
            elif not company_name:
                show_error("Company Name is required")
            elif uploaded_file is None:
                show_error("Please upload a PDF file")
            else:
                files = {"file": uploaded_file}
                data  = {
                    "title": title,
                    "company_name": company_name,
                    "document_type": document_type,
                    "uploaded_by": st.session_state.email
                }
                response = requests.post(
                    f"{API_URL}/documents/upload",
                    files=files, data=data
                )
                show_success(f"📄 {response.json()['message']}")

# ─── VIEW DOCUMENTS ────────────────────────────────────────────────────────────

if menu == "View Documents":
    st.markdown('<div class="section-pill">Documents</div>', unsafe_allow_html=True)
    st.subheader("All Documents")
    st.markdown("---")

    response  = requests.get(f"{API_URL}/documents/")
    documents = response.json()

    if not documents:
        show_warning("No documents found")
    else:
        cols = st.columns(2)
        for idx, doc in enumerate(documents):
            col = cols[idx % 2]
            type_badge_map = {
                "report":   "badge-report",
                "invoice":  "badge-invoice",
                "contract": "badge-contract",
            }
            badge = type_badge_map.get(doc['document_type'], "badge-report")
            with col:
                with st.container(border=True):
                    st.markdown(f"""
                    <div style="display:flex; justify-content:space-between;
                         align-items:flex-start; margin-bottom:0.6rem;">
                        <div style="font-family:'Syne',sans-serif; font-weight:700;
                             font-size:1rem; color:#f0ece4;">
                            📄 {doc['title']}
                        </div>
                        <span class="badge {badge}">{doc['document_type']}</span>
                    </div>
                    <div style="font-family:'DM Sans',sans-serif; font-size:0.83rem;
                         color:#666688; line-height:2.1;">
                        <span style="color:#888;">ID</span>&nbsp;
                        <span style="color:#c0bdb5;">#{doc['id']}</span><br>
                        <span style="color:#888;">Company</span>&nbsp;
                        <span style="color:#c0bdb5;">{doc['company_name']}</span><br>
                        <span style="color:#888;">Uploaded by</span>&nbsp;
                        <span style="color:#c0bdb5;">{doc['uploaded_by']}</span><br>
                        <span style="color:#888;">Date</span>&nbsp;
                        <span style="color:#c0bdb5;">{str(doc['created_at'])[:19].replace('T', ' · ')}</span>
                    </div>
                    """, unsafe_allow_html=True)

# ─── METADATA SEARCH ───────────────────────────────────────────────────────────

if menu == "Metadata Search":
    if st.session_state.role not in ["Admin", "Financial Analyst", "Auditor"]:
        show_error("You are not authorized for metadata search")
    else:
        st.markdown('<div class="section-pill">Search</div>', unsafe_allow_html=True)
        st.subheader("Metadata Search")
        st.markdown("---")

        col1, col2, col3 = st.columns(3)
        with col1:
            company_name  = st.text_input("Company Name")
        with col2:
            document_type = st.text_input("Document Type")
        with col3:
            title = st.text_input("Title")

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("⌕ Search Metadata"):
            response  = requests.get(
                f"{API_URL}/documents/search",
                params={
                    "company_name": company_name,
                    "document_type": document_type,
                    "title": title
                }
            )
            documents = response.json()
            if not documents:
                show_warning("No matching documents found")
            else:
                show_success(f"Found {len(documents)} matching document(s)")
                for doc in documents:
                    with st.container(border=True):
                        st.markdown(f"### 📄 {doc['title']}")
                        st.write(f"**Company:** {doc['company_name']}")
                        st.write(f"**Type:** {doc['document_type']}")

# ─── SEMANTIC SEARCH ───────────────────────────────────────────────────────────

if menu == "Semantic Search":
    if st.session_state.role not in ["Admin", "Financial Analyst", "Auditor"]:
        show_error("You are not authorized for semantic search")
    else:
        st.markdown('<div class="section-pill">AI Search</div>', unsafe_allow_html=True)
        st.subheader("Semantic Search")
        st.markdown("---")

        st.markdown("""
        <div style="font-family:'DM Sans',sans-serif; font-size:0.88rem; color:#888;
             margin-bottom:1.2rem;">
            Ask a natural language question — the AI will find relevant passages across all documents.
        </div>
        """, unsafe_allow_html=True)

        query = st.text_input(
            "Enter Search Query",
            placeholder="e.g. What are the quarterly revenue figures for Nimap?"
        )

        if st.button("⚡ Run AI Search"):
            if not query:
                show_error("Please enter a search query")
            else:
                with st.spinner("Searching with AI..."):
                    response = requests.post(
                        f"{API_URL}/rag/search",
                        json={"query": query}
                    )
                    results = response.json()["results"]

                if not results:
                    show_warning("No semantic results found")
                else:
                    show_success(f"Found {len(results)} relevant passage(s)")
                    for i, result in enumerate(results, 1):
                        with st.container(border=True):
                            st.markdown(f"""
                            <div style="display:flex; justify-content:space-between;
                                 margin-bottom:0.5rem;">
                                <div style="font-family:'Syne',sans-serif; font-weight:700;
                                     font-size:0.95rem; color:#f0ece4;">
                                    Result #{i}
                                </div>
                                <span class="badge badge-analyst">Doc #{result['document_id']}</span>
                            </div>
                            <div style="font-family:'DM Sans',sans-serif; font-size:0.87rem;
                                 color:#c0bdb5; line-height:1.7; padding:0.75rem;
                                 background:#0d0d15; border-radius:8px;
                                 border-left:3px solid #f0a500;">
                                {result['text']}
                            </div>
                            """, unsafe_allow_html=True)

# ─── DELETE DOCUMENT ───────────────────────────────────────────────────────────

if menu == "Delete Document":
    if st.session_state.role != "Admin":
        show_error("Only Admin can delete documents")
    else:
        st.markdown('<div class="section-pill">Danger Zone</div>', unsafe_allow_html=True)
        st.subheader("Delete Document")
        st.markdown("---")

        st.markdown("""
        <div style="background:rgba(255,100,100,0.06); border:1px solid rgba(255,100,100,0.2);
             border-left:4px solid #ef4444; border-radius:10px; padding:0.9rem 1rem;
             font-family:'DM Sans',sans-serif; font-size:0.88rem; color:#f87171;
             margin-bottom:1.5rem;">
            ⚠ &nbsp;This action is permanent. The document and all its indexed content will be removed.
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([1, 2])
        with col1:
            document_id = st.number_input("Document ID", min_value=1, step=1)

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("✕ Delete Document"):
            response = requests.delete(f"{API_URL}/documents/{document_id}")
            show_success(response.json()["message"])

# ─── ADMIN PANEL ───────────────────────────────────────────────────────────────

if menu == "Admin Panel":
    if st.session_state.role != "Admin":
        show_error("Only Admin can access Admin Panel")
    else:
        st.markdown('<div class="section-pill">Admin</div>', unsafe_allow_html=True)
        st.subheader("Admin Control Panel")
        st.markdown("---")

        admin_option = st.selectbox(
            "Select Action",
            ["View Users", "Delete User", "Change User Role"]
        )

        # VIEW USERS
        if admin_option == "View Users":
            response = requests.get(f"{API_URL}/users/")
            users    = response.json()
            cols = st.columns(3)
            for idx, user in enumerate(users):
                col = cols[idx % 3]
                role_badge_map = {
                    "Admin": "badge-admin",
                    "Financial Analyst": "badge-analyst",
                    "Auditor": "badge-auditor",
                    "Client": "badge-client",
                }
                badge_class = role_badge_map.get(user['role'], "badge-client")
                with col:
                    with st.container(border=True):
                        st.markdown(f"""
                        <div style="font-family:'Syne',sans-serif; font-weight:700;
                             font-size:0.95rem; color:#f0ece4; margin-bottom:0.5rem;">
                            👤 {user['username']}
                        </div>
                        <div style="font-family:'DM Sans',sans-serif; font-size:0.82rem;
                             color:#666688; line-height:1.9;">
                            <span style="color:#888;">Email</span><br>
                            <span style="color:#c0bdb5;">{user['email']}</span>
                        </div>
                        <div style="margin-top:0.5rem; display:flex;
                             justify-content:space-between; align-items:center;">
                            <span class="badge {badge_class}">{user['role']}</span>
                            <span style="font-family:'DM Sans',sans-serif; font-size:0.75rem;
                                 color:#444460;">ID #{user['id']}</span>
                        </div>
                        """, unsafe_allow_html=True)

        # DELETE USER
        elif admin_option == "Delete User":
            st.markdown("""
            <div style="background:rgba(255,100,100,0.06); border:1px solid rgba(255,100,100,0.2);
                 border-left:4px solid #ef4444; border-radius:10px; padding:0.9rem 1rem;
                 font-family:'DM Sans',sans-serif; font-size:0.88rem; color:#f87171;
                 margin-bottom:1.5rem;">
                ⚠ &nbsp;Deleting a user is irreversible.
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns([1, 2])
            with col1:
                user_id = st.number_input("Enter User ID", min_value=1, step=1)

            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("✕ Delete User"):
                response = requests.delete(f"{API_URL}/users/{user_id}")
                show_success(response.json()["message"])

        # CHANGE USER ROLE
        elif admin_option == "Change User Role":
            col1, col2 = st.columns(2)
            with col1:
                user_id   = st.number_input("User ID", min_value=1, step=1)
            with col2:
                role_name = st.selectbox(
                    "Select New Role",
                    ["Admin", "Financial Analyst", "Auditor", "Client"]
                )

            role_mapping = {
                "Admin": 1, "Financial Analyst": 2,
                "Auditor": 3, "Client": 4
            }
            role_id = role_mapping[role_name]

            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("✎ Update Role"):
                response = requests.put(
                    f"{API_URL}/users/change-role",
                    params={"user_id": user_id, "role_id": role_id}
                )
                show_success(response.json()["message"])