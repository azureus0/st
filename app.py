import streamlit as st
import connection as cn
from components import dashboard, login_page, register_page

# --------------------------
# Inisialisasi database
# --------------------------
cn.init_db()          # Users
cn.init_db_reports()  # Reports

# --------------------------
# SESSION STATE DEFAULT
# --------------------------
if 'is_logged_in' not in st.session_state:
    st.session_state['is_logged_in'] = False
if 'role' not in st.session_state:
    st.session_state['role'] = 'user'
if 'username' not in st.session_state:
    st.session_state['username'] = None
if 'page' not in st.session_state:
    st.session_state['page'] = 'login'

# --------------------------
# PAGE CONFIG
# --------------------------
st.set_page_config(page_title="CEPUIN", layout="centered")

# --------------------------
# USER SUDAH LOGIN
# --------------------------
if st.session_state['is_logged_in']:
    st.sidebar.title("Navigation")
    st.sidebar.success(f"Logged in as '{st.session_state['username']}'")

    # Pilihan menu sesuai role
    if st.session_state['role'] == 'admin':
        menu = ["Dashboard Admin"]
    else:
        menu = ["Submit Report"]

    choice = st.sidebar.radio("Go to", menu)

    # Routing halaman sesuai role & pilihan
    dashboard.route_page(choice)

    # Tombol logout
    st.sidebar.divider()
    if st.sidebar.button(":red[Logout]"):
        st.session_state['is_logged_in'] = False
        st.session_state['username'] = None
        st.session_state['role'] = 'user'
        st.session_state['page'] = 'login'
        st.rerun()

# --------------------------
# BELUM LOGIN
# --------------------------
else:
    st.sidebar.title("Navigation")
    st.sidebar.warning("Not logged in")
    choice = st.sidebar.radio("Menu", ["Login", "Register"])

    if choice == "Login":
        login_page.login()
    elif choice == "Register":
        register_page.register()

    # Redirect otomatis setelah login sukses
    if st.session_state['is_logged_in']:
        st.rerun()
