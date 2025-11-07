import streamlit as st
import connection as cn
from functions.text_encrypt_decrypt import super_decrypt_text
from functions.file_encrypt_decrypt import decrypt_file_gcm
from functions.steganography import decode_lsb
from .submit_report import AES_KEY_TEXT, AES_KEY_FILE, VIGENERE_KEY
import os

def dashboard_admin():
    cn.init_db_reports()

    query = """
        SELECT r.id, r.subject, r.description, r.mode, r.file_path, r.image_path 
        FROM reports r
    """
    reports = cn.run_query(query, fetch=True)

    if reports is None or reports.empty:
        st.error("Tidak ada laporan yang ditemukan.")
        return

    st.subheader("Admin Dashboard - Reports")

    for index, report in reports.iterrows():
        with st.container():
            st.markdown(f"### Report #{index + 1} — {report['subject']}")
            st.caption(f"Mode: `{report['mode']}`")

            # Encrypted description
            st.write(f"**Encrypted Description:** {report['description'] or '—'}")

            # Tombol decrypt description langsung di bawahnya
            if report['description']:
                if st.button(f"Decrypt Description #{index + 1}", key=f"desc_{index}"):
                    try:
                        decrypted_description = super_decrypt_text(
                            report['description'], VIGENERE_KEY, AES_KEY_TEXT
                        )
                        st.info(f"Decrypted Description: {decrypted_description}")
                    except Exception as e:
                        st.error(f"Error decrypting description: {e}")

            # Gambar steganografi
            if report['mode'] == "steganografi" and report['image_path']:
                if os.path.exists(report['image_path']):
                    st.image(report['image_path'], caption="Steganography Image", width=300)
                else:
                    st.warning("Gambar tidak ditemukan di path yang disimpan.")

            # File attachments
            if report['file_path']:
                st.write("**Attached Files:**")
                for fpath in report['file_path'].split(","):
                    st.code(fpath.strip())

            # ======= TOMBOL AKSI =======
            col1, col2 = st.columns([1, 1])

            # Dekripsi File
            with col1:
                if report['file_path']:
                    if st.button(f"Decrypt File(s) #{index + 1}", key=f"file_{index}"):
                        try:
                            file_list = [f.strip() for f in report['file_path'].split(",") if f.strip()]
                            for fpath in file_list:
                                if not os.path.exists(fpath):
                                    st.warning(f"File tidak ditemukan: {fpath}")
                                    continue

                                # Hilangkan ekstensi .enc dan buat nama asli
                                original_name = os.path.basename(fpath).replace(".enc", "")
                                decrypted_path = os.path.join("uploads", f"decrypted_{original_name}")

                                decrypt_file_gcm(fpath, decrypted_path, AES_KEY_FILE)
                                st.success(f"File berhasil didekripsi: {original_name}")

                                # Tombol download file asli
                                with open(decrypted_path, "rb") as f:
                                    st.download_button(
                                        label=f"Download {original_name}",
                                        data=f.read(),
                                        file_name=original_name,
                                    )
                        except Exception as e:
                            st.error(f"Error decrypting file(s): {e}")

            # Dekripsi Steganografi
            with col2:
                if report['mode'] == "steganografi" and report['image_path']:
                    if st.button(f"Decrypt Steganography #{index + 1}", key=f"stego_{index}"):
                        try:
                            message = decode_lsb(report['image_path'])
                            st.success(f"Pesan tersembunyi: {message}")
                        except Exception as e:
                            st.error(f"Error decrypting steganography image: {e}")

            st.divider()
