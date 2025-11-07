import streamlit as st
import connection as cn
from components.register_page import verify_password  

if "is_logged_in" not in st.session_state:
    st.session_state["is_logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = None
if "role" not in st.session_state:
    st.session_state["role"] = "user"

def login():
    st.header("Login Page")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        # Ambil data user dari DB
        query = cn.run_query("SELECT username, password, salt, role FROM users WHERE username=%s;", (username,))
        
        if query is not None and not query.empty:
            user = query.iloc[0]
            if verify_password(password, user["password"], user["salt"]):
                st.session_state["is_logged_in"] = True
                st.session_state["username"] = user["username"]
                st.session_state["role"] = user["role"] or "user"
                st.success(f"Login berhasil! Selamat datang, {user['username']}")
                st.rerun()
            else:
                st.error("Password salah.")
        else:
            st.error("Username tidak ditemukan.")

if __name__ == "__main__":
    login()
    if st.session_state["is_logged_in"]:
        st.write("Redirecting to Dashboard...")
