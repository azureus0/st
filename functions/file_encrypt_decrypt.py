from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os

def encrypt_file_gcm(input_filepath, output_filepath, key):
    """
    Enkripsi file menggunakan AES-256 GCM.
    Key harus 32 byte (AES-256).
    """
    
    if len(key) != 32:
        return "ERROR: Panjang kunci harus 32 byte (AES-256)."

    key_bytes = key 
    
    # 1. Buat Objek Cipher
    cipher = AES.new(key_bytes, AES.MODE_GCM)
    nonce = cipher.nonce # GCM menghasilkan Nonce unik (seperti IV)
    
    # 2. Baca dan Enkripsi File
    try:
        with open(input_filepath, 'rb') as infile:
            plaintext_data = infile.read()
            # Enkripsi dan buat Tag Autentikasi
            ciphertext, tag = cipher.encrypt_and_digest(plaintext_data)
        
        # 3. Tulis Output
        # Simpan Nonce, Tag, dan Ciphertext ke file output
        with open(output_filepath, 'wb') as outfile:
            # Urutan penyimpanan: Nonce (16B) + Tag (16B) + Ciphertext
            outfile.write(nonce)
            outfile.write(tag)
            outfile.write(ciphertext)
            
        return f"File berhasil dienkripsi ke: {output_filepath}"
    
    except FileNotFoundError:
        return "ERROR: File input tidak ditemukan."
    except ValueError as e:
        # Error jika kunci tidak memiliki panjang yang benar
        return f"ERROR: Kunci AES tidak valid. Pastikan panjangnya 32 byte. {e}"
    
def decrypt_file_gcm(input_filepath, output_filepath, key):
    """
    Dekripsi file menggunakan AES-256 GCM dan memverifikasi Tag autentikasi.
    """
    key_bytes = key # Asumsikan key sudah berupa bytes 32-panjang
    
    # 1. Baca Komponen dari File Terenkripsi
    try:
        with open(input_filepath, 'rb') as infile:
            # Baca Nonce (16 bytes), Tag (16 bytes), dan sisa data (Ciphertext)
            # Standar GCM menggunakan Nonce 12B, tapi PyCryptodome defaultnya 16B jika tidak dispesifikasi.
            # Kita menggunakan 16B sesuai output dari cipher.nonce sebelumnya.
            nonce = infile.read(16) 
            tag = infile.read(16)
            ciphertext = infile.read()
            
        # 2. Buat Objek Cipher
        cipher = AES.new(key_bytes, AES.MODE_GCM, nonce=nonce)
        
        # 3. Dekripsi dan Verifikasi
        # GCM akan mendekripsi dan membandingkan tag yang dihitung dengan tag yang disimpan.
        # Jika tag tidak cocok, ValueError akan muncul.
        plaintext_data = cipher.decrypt_and_verify(ciphertext, tag)
        
        # 4. Tulis Output
        with open(output_filepath, 'wb') as outfile:
            outfile.write(plaintext_data)
            
        return f"File berhasil didekripsi ke: {output_filepath}"
        
    except FileNotFoundError:
        return "ERROR: File terenkripsi tidak ditemukan."
    except ValueError as e:
        # PENTING: ValueError akan muncul jika TAG TIDAK COCOK (file diubah) atau kunci salah.
        return f"ERROR Dekripsi File: Kunci salah, atau file telah dirusak (Authentication Tag mismatch). Detail: {e}"