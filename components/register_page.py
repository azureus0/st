import streamlit as st
import connection as cn  
import hashlib
import os

# --- Fungsi hashing password dengan BLAKE2b ---
def hash_password(password):
    salt = os.urandom(16)  # 16 bytes salt
    hashed = hashlib.blake2b(password.encode(), salt=salt).hexdigest()
    return hashed, salt.hex()

# --- Fungsi verifikasi password ---
def verify_password(password, hashed, salt_hex):
    salt = bytes.fromhex(salt_hex)
    return hashlib.blake2b(password.encode(), salt=salt).hexdigest() == hashed

# --- Halaman Register ---
def register():
    st.header("Register Page (Blake2b Hashing)")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if not username or not password:
            st.error("Username dan password tidak boleh kosong")
            return

        # cek apakah username sudah ada
        query = cn.run_query("SELECT * FROM users WHERE username = %s;", (username,), fetch=True)
        if query.empty:
            # hash password
            hashed_pass, salt = hash_password(password)

            # simpan ke database (password + salt)
            cn.run_query(
                "INSERT INTO users (username, password, salt) VALUES (%s, %s, %s);",
                (username, hashed_pass, salt),
                fetch=False
            )
            st.success(f"User '{username}' berhasil didaftarkan. Silakan login sekarang.")  

        else:
            st.error("Username sudah terdaftar.")

if __name__ == "__main__":
    register()
