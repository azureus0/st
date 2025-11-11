import streamlit as st
import connection as cn
from functions.text_encrypt_decrypt import super_decrypt_text
from functions.file_encrypt_decrypt import decrypt_file_gcm
from functions.steganography import decode_lsb
import os
import io
import hashlib
import base64
from datetime import datetime
import pytz  

MASTER_KEY = st.secrets.get("MASTER_KEY", "CEPUIN_MASTER_SECRET").encode()

AES_KEY_TEXT = base64.urlsafe_b64encode(hashlib.sha256(MASTER_KEY + b"text").digest())
AES_KEY_FILE = hashlib.sha256(MASTER_KEY + b"file").digest()
VIGENERE_KEY = "CEPUINVIGENEREKEY"


def dashboard_admin():
    cn.init_db_reports()

    query = """
        SELECT id, username, subject, description, mode, file_path, image_path, timestamp
        FROM reports
        ORDER BY timestamp DESC;
    """
    reports = cn.run_query(query, fetch=True)

    if reports is None or reports.empty:
        st.warning("Tidak ada laporan yang ditemukan di database.")
        return

    st.title("Dashboard Admin - Reports")

    wib = pytz.timezone("Asia/Jakarta")  

    for index, report in reports.iterrows():
        with st.container():
            
            timestamp_obj = report["timestamp"]
            if timestamp_obj.tzinfo is None:
                timestamp_obj = timestamp_obj.replace(tzinfo=pytz.UTC)
            timestamp_wib = timestamp_obj.astimezone(wib)
            formatted_time = timestamp_wib.strftime("%d %B %Y, %H:%M")

            st.markdown(f"### Report #{report['id']} — {report['subject']}")
            st.caption(f"Pengirim: {report['username']} | {formatted_time}")
            st.caption(f"Mode: `{report['mode']}`")

            if report["description"]:
                with st.expander("Lihat / Dekripsi Deskripsi"):
                    st.code(report["description"])
                    if st.button(
                        f"Decrypt Description #{report['id']}",
                        key=f"desc_{report['id']}",
                    ):
                        try:
                            decrypted_text = super_decrypt_text(
                                report["description"], VIGENERE_KEY, AES_KEY_TEXT
                            )
                            st.success(f"Decrypted: {decrypted_text}")
                        except Exception as e:
                            st.error(f"Gagal mendekripsi: {e}")
            else:
                st.info("Deskripsi kosong.")

            if report["file_path"]:
                file_list = [
                    f.strip() for f in report["file_path"].split(",") if f.strip()
                ]
                st.write("Attached Encrypted Files:")
                for fpath in file_list:
                    st.code(fpath)

                if st.button(
                    f"Decrypt File(s) #{report['id']}", key=f"file_{report['id']}"
                ):
                    for fpath in file_list:
                        if not os.path.exists(fpath):
                            st.warning(f"File tidak ditemukan: {fpath}")
                            continue
                        try:
                            original_name = os.path.basename(fpath).replace(".enc", "")
                            decrypted_path = os.path.join(
                                "uploads", f"decrypted_{original_name}"
                            )
                            decrypt_file_gcm(fpath, decrypted_path, AES_KEY_FILE)
                            st.success(f"File berhasil didekripsi: {original_name}")

                            with open(decrypted_path, "rb") as f:
                                st.download_button(
                                    label=f"Download {original_name}",
                                    data=f.read(),
                                    file_name=original_name,
                                )
                        except Exception as e:
                            st.error(f"Error decrypting {fpath}: {e}")

            if report["mode"] == "steganografi" and report["image_path"]:
                st.write("Steganography Image:")
                if os.path.exists(report["image_path"]):
                    st.image(
                        report["image_path"],
                        caption="Image with Hidden Message",
                        width=300,
                    )
                    if st.button(
                        f"Decode Stego #{report['id']}", key=f"stego_{report['id']}"
                    ):
                        try:
                            hidden_msg = decode_lsb(report["image_path"])
                            st.success(f"Pesan tersembunyi: {hidden_msg}")
                        except Exception as e:
                            st.error(f"Error decoding image: {e}")
                else:
                    st.warning("Gambar tidak ditemukan di path yang tersimpan.")

            st.divider()
