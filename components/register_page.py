import streamlit as st
import connection as cn
import hashlib
import os

def hash_password(password: str):
    salt = os.urandom(16)
    hashed = hashlib.blake2b(password.encode(), salt=salt).hexdigest()
    return hashed, salt.hex()

def verify_password(password: str, hashed: str, salt_hex: str) -> bool:
    salt = bytes.fromhex(salt_hex)
    return hashlib.blake2b(password.encode(), salt=salt).hexdigest() == hashed

def register():
    st.header("Register Page")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if not username or not password:
            st.error("Username dan password tidak boleh kosong!")
            return

        try:
            existing = cn.run_query("SELECT username FROM users WHERE username = %s;", (username,), fetch=True)

            if not existing.empty:
                st.error("Username sudah terdaftar, silakan pilih username lain.")
                return

            hashed_pass, salt = hash_password(password)

            cn.run_query(
                "INSERT INTO users (username, password, salt) VALUES (%s, %s, %s);",
                (username, hashed_pass, salt),
                fetch=False
            )

            st.success(f"User {username} berhasil didaftarkan! Silakan login sekarang.")
        except Exception as e:
            st.error(f"Terjadi kesalahan saat registrasi: {e}")

if __name__ == "__main__":
    register()
