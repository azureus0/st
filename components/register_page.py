import streamlit as st
import connection as cn
import hashlib
import os

# -----------------------------
# Fungsi hashing password (BLAKE2b)
# -----------------------------
def hash_password(password: str):
    """Hash password dengan BLAKE2b dan salt acak."""
    salt = os.urandom(16)  # 16-byte salt
    hashed = hashlib.blake2b(password.encode(), salt=salt).hexdigest()
    return hashed, salt.hex()

def verify_password(password: str, hashed: str, salt_hex: str) -> bool:
    """Verifikasi password dengan hash & salt."""
    salt = bytes.fromhex(salt_hex)
    return hashlib.blake2b(password.encode(), salt=salt).hexdigest() == hashed

# -----------------------------
# Halaman Register
# -----------------------------
def register():
    st.header("Register Page 🔐")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if not username or not password:
            st.error("Username dan password tidak boleh kosong!")
            return

        try:
            # Cek apakah username sudah ada
            existing = cn.run_query("SELECT username FROM users WHERE username = %s;", (username,), fetch=True)

            if not existing.empty:
                st.error("⚠️ Username sudah terdaftar, silakan pilih username lain.")
                return

            # Hash password
            hashed_pass, salt = hash_password(password)

            # Simpan user baru ke DB
            cn.run_query(
                "INSERT INTO users (username, password, salt) VALUES (%s, %s, %s);",
                (username, hashed_pass, salt),
                fetch=False
            )

            st.success(f"✅ User **{username}** berhasil didaftarkan! Silakan login sekarang.")
        except Exception as e:
            st.error(f"Terjadi kesalahan saat registrasi: {e}")

# -----------------------------
# Jalankan halaman langsung
# -----------------------------
if __name__ == "__main__":
    register()
