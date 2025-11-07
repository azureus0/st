from cryptography.fernet import Fernet
import base64

# === FUNGSI ENKRIPSI VIGENERE ===
def encrypt_vigenere(plaintext, key):
    # Pastikan key hanya terdiri dari huruf
    key = ''.join(filter(str.isalpha, key)).upper()
    
    # Inisialisasi variabel
    ciphertext = ""
    key_index = 0
    
    for char in plaintext:
        # Hanya enkripsi huruf (A-Z, a-z)
        if char.isalpha():
            # Tentukan offset dasar: A=65 untuk huruf kapital, a=97 untuk huruf kecil
            base = ord('A') if char.isupper() else ord('a')
            
            # Hitung pergeseran (shift) dari key saat ini
            key_shift = ord(key[key_index % len(key)]) - ord('A')
            
            # Enkripsi: (P + K) mod 26
            encrypted_char_val = (ord(char) - base + key_shift) % 26
            
            # Konversi kembali ke karakter
            ciphertext += chr(encrypted_char_val + base)
            
            # Pindah ke karakter key berikutnya
            key_index += 1
        else:
            # Karakter selain huruf (spasi, tanda baca) tidak diubah
            ciphertext += char
            
    return ciphertext

# === FUNGSI DEKRIPSI VIGENERE ===
def decrypt_vigenere(ciphertext, key):
    # Pastikan key hanya terdiri dari huruf
    key = ''.join(filter(str.isalpha, key)).upper()
    
    # Inisialisasi variabel
    plaintext = ""
    key_index = 0
    
    for char in ciphertext:
        # Hanya dekripsi huruf (A-Z, a-z)
        if char.isalpha():
            # Tentukan offset dasar: A=65 untuk huruf kapital, a=97 untuk huruf kecil
            base = ord('A') if char.isupper() else ord('a')
            
            # Hitung pergeseran (shift) dari key saat ini
            key_shift = ord(key[key_index % len(key)]) - ord('A')
            
            # Dekripsi: (C - K) mod 26
            # Tambahkan +26 sebelum modulo untuk memastikan hasil positif
            decrypted_char_val = (ord(char) - base - key_shift + 26) % 26
            
            # Konversi kembali ke karakter
            plaintext += chr(decrypted_char_val + base)
            
            # Pindah ke karakter key berikutnya
            key_index += 1
        else:
            # Karakter selain huruf (spasi, tanda baca) tidak diubah
            plaintext += char
            
    return plaintext

# === Fungsi Generate AES Key ===
def generate_aes_key():
    # Menghasilkan dan mengembalikan kunci Fernet baru
    # Output: bytes (Base64 URL-safe 32 byte)
    return Fernet.generate_key()

# === Fungsi Enkripsi AES ===
def encrypt_aes(data, key):
    # Input data: string (intermediate_ciphertext dari Vigenere)
    # Input key: bytes (kunci Fernet)
    f = Fernet(key)
    # Fernet.encrypt() mengembalikan token (bytes) yang sudah Base64 URL-safe
    return f.encrypt(data.encode('utf-8'))

# === Fungsi Dekripsi AES ===
def decrypt_aes(ciphertext_bytes, key):
    # Input ciphertext_bytes: bytes (token Base64 URL-safe dari Fernet)
    # Input key: bytes (kunci Fernet)
    f = Fernet(key)
    try:
        # decrypt() secara otomatis menangani Base64 decoding, IV, dan HMAC verification
        return f.decrypt(ciphertext_bytes).decode('utf-8')
    except Exception as e:
        # Tangani jika kunci salah, data rusak (HMAC gagal), atau token tidak valid
        print(f"ERROR DEKRIPSI AES: {e}")
        # Kembalikan pesan error yang jelas
        raise ValueError("ERROR DEKRIPSI AES: Kunci salah atau pesan telah dimodifikasi.")
   
# === FUNGSI SUPER ENKRIPSI === 
def super_encrypt_text(plaintext, vigenere_key, aes_key_bytes):
    # 1. Enkripsi Klasik: Vigenère Cipher (Output: string)
    intermediate_ciphertext = encrypt_vigenere(plaintext, vigenere_key)
    
    # 2. Enkripsi Modern: Fernet/AES (Output: bytes Fernet token, sudah Base64 URL-safe)
    final_ciphertext_bytes = encrypt_aes(intermediate_ciphertext, aes_key_bytes)
    
    # Konversi bytes Fernet token ke string ASCII agar mudah ditampilkan/disalin
    return final_ciphertext_bytes.decode('ascii')


# === FUNGSI SUPER DEKRIPSI ===
def super_decrypt_text(super_ciphertext_str, vigenere_key, aes_key_bytes):
    try:
        # Input dari Streamlit/textbox adalah string, harus di-encode ke bytes
        ciphertext_bytes = super_ciphertext_str.encode('ascii')
        
        # 1. Dekripsi Modern (Reverse Step): Fernet/AES (Output: intermediate_ciphertext string)
        intermediate_ciphertext = decrypt_aes(ciphertext_bytes, aes_key_bytes)
        
        # 2. Dekripsi Klasik (Reverse Step): Vigenère Cipher (Output: original_plaintext string)
        original_plaintext = decrypt_vigenere(intermediate_ciphertext, vigenere_key)
        
        return original_plaintext
    
    except ValueError as ve:
        # Menangkap error dari decrypt_aes (kunci salah/HMAC gagal)
        return f"ERROR DEKRIPSI: {ve}"
    except Exception as e:
        # Menangkap error lain 
        return f"ERROR DEKRIPSI: Format pesan salah atau token tidak valid."