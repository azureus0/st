import streamlit as st
import connection as cn
import os
import hashlib
import base64
import uuid

from functions.text_encrypt_decrypt import super_encrypt_text
from functions.file_encrypt_decrypt import encrypt_file_gcm
from functions.steganography import encode_lsb

# -----------------------------
# MASTER KEY & AES KEYS
# -----------------------------
MASTER_KEY = b"CEPUIN_MASTER_SECRET"

# Text AES (Fernet)
AES_KEY_TEXT = base64.urlsafe_b64encode(hashlib.sha256(MASTER_KEY + b"text").digest())

# File AES GCM (raw 32 bytes)
AES_KEY_FILE = hashlib.sha256(MASTER_KEY + b"file").digest()

# Vigenere Key
VIGENERE_KEY = "CEPUINVIGENEREKEY"

# -----------------------------
# FOLDER UPLOADS
# -----------------------------
UPLOAD_DIR_FILES = os.path.join("uploads", "files")
UPLOAD_DIR_IMAGES = os.path.join("uploads", "images")
os.makedirs(UPLOAD_DIR_FILES, exist_ok=True)
os.makedirs(UPLOAD_DIR_IMAGES, exist_ok=True)

# -----------------------------
# Fungsi submit laporan
# -----------------------------
def submit():
    st.header("Submit Report")

    with st.form("report_form", clear_on_submit=True):
        subject = st.text_input("Subject (singkat)")
        anonymous = st.checkbox("Submit as anonymous", value=True)

        tabs = st.tabs(["Biasa", "Steganografi"])

        with tabs[0]:
            description_biasa = st.text_area("Description (mode biasa)")
            files_biasa = st.file_uploader(
                "Upload file (opsional, bisa banyak jenis)",
                type=None, accept_multiple_files=True, key="files_biasa"
            )

        with tabs[1]:
            description_stego = st.text_area("Description (mode steganografi)")
            secret_message_stego = st.text_area("Pesan rahasia untuk disisipkan ke gambar")
            image_stego = st.file_uploader(
                "Upload image untuk steganografi (wajib)",
                type=["png"], key="image_stego"
            )

        submitted = st.form_submit_button("Submit")

        if not submitted:
            return

        # Validasi input
        if not subject:
            st.error("Subject wajib diisi!")
            return

        if not (description_biasa or description_stego):
            st.error("Deskripsi harus diisi!")
            return

        if description_stego and (not secret_message_stego or not image_stego):
            st.error("Pesan rahasia dan gambar wajib diisi untuk steganografi!")
            return

        # Tentukan mode
        if description_stego:
            mode = "steganografi"
            description = description_stego
        else:
            mode = "biasa"
            description = description_biasa

        # Tentukan username
        username_to_save = "Anonymous" if anonymous else st.session_state["username"]

        # -----------------------------
        # Simpan file biasa + enkripsi AES GCM
        # -----------------------------
        file_paths = []
        if mode == "biasa" and files_biasa:
            for f in files_biasa:
                unique_name = f"{uuid.uuid4().hex}_{f.name}"
                raw_file_path = os.path.join(UPLOAD_DIR_FILES, unique_name)

                with open(raw_file_path, "wb") as temp_file:
                    temp_file.write(f.getbuffer())

                encrypted_file_path = raw_file_path + ".enc"
                encrypt_file_gcm(
                    input_filepath=raw_file_path,
                    output_filepath=encrypted_file_path,
                    key=AES_KEY_FILE
                )
                os.remove(raw_file_path)
                file_paths.append(encrypted_file_path)

        if not file_paths:
            file_paths = None

        # -----------------------------
        # Simpan stego image
        # -----------------------------
        image_path = None
        if mode == "steganografi" and image_stego:
            unique_image_name = f"{uuid.uuid4().hex}_{image_stego.name}"
            raw_image_path = os.path.join(UPLOAD_DIR_IMAGES, unique_image_name)

            with open(raw_image_path, "wb") as out:
                out.write(image_stego.getbuffer())

            stego_output_path = os.path.join(UPLOAD_DIR_IMAGES, "stego_" + unique_image_name)
            encode_lsb(raw_image_path, secret_message_stego, stego_output_path)
            image_path = stego_output_path
            os.remove(raw_image_path)

        # -----------------------------
        # Enkripsi deskripsi
        # -----------------------------
        encrypted_description = (
            super_encrypt_text(description, VIGENERE_KEY, AES_KEY_TEXT)
            if description else None
        )

        # -----------------------------
        # Simpan metadata ke DB (PostgreSQL)
        # -----------------------------
        try:
            query = """
                INSERT INTO reports (username, subject, description, mode, file_path, image_path)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cn.run_query(query, params=(
                username_to_save,
                subject,
                encrypted_description,
                mode,
                ",".join(file_paths) if file_paths else None,
                image_path
            ), fetch=False)

            st.success("✅ Report berhasil dikirim dan disimpan ke database!")
        except Exception as e:
            st.error(f"Gagal menyimpan report: {e}")
