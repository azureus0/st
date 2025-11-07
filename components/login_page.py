import streamlit as st
import connection as cn
from components.register_page import verify_password  

# -----------------------------
# Default Session State
# -----------------------------
if "is_logged_in" not in st.session_state:
    st.session_state["is_logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = None
if "role" not in st.session_state:
    st.session_state["role"] = "user"

# -----------------------------
# Login Page
# -----------------------------
def login():
    st.header("Login Page 🔑")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if not username or not password:
            st.error("Username dan password wajib diisi!")
            return

        try:
            # Ambil data user dari database
            query = cn.run_query(
                "SELECT username, password, salt, role FROM users WHERE username = %s;",
                (username,),
                fetch=True
            )

            # Cek apakah user ditemukan
            if query is not None and not query.empty:
                user = query.iloc[0]

                # Verifikasi password
                if verify_password(password, user["password"], user["salt"]):
                    st.session_state["is_logged_in"] = True
                    st.session_state["username"] = user["username"]
                    st.session_state["role"] = user["role"] or "user"
                    st.success(f"✅ Login berhasil! Selamat datang, **{user['username']}** 👋")
                    st.rerun()
                else:
                    st.error("❌ Password salah.")
            else:
                st.error("⚠️ Username tidak ditemukan.")
        except Exception as e:
            st.error(f"Terjadi kesalahan saat login: {e}")

# -----------------------------
# Jalankan langsung (opsional)
# -----------------------------
if __name__ == "__main__":
    login()
    if st.session_state["is_logged_in"]:
        st.write("Redirecting to Dashboard...")
