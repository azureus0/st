from PIL import Image

# === FUNGSI KOVERSI TEKS KE BINER ===
def to_binary(data):
    """Konversi data (string) ke urutan bit (string)."""
    if isinstance(data, str):
        # Konversi string ke bytes, lalu ke biner
        return ''.join(format(ord(i), '08b') for i in data)
    elif isinstance(data, bytes) or isinstance(data, int):
        # Konversi bytes atau int ke biner
        return format(data, '08b')
    else:
        # Jika bukan string, langsung kembalikan format biner
        return ''.join(format(i, '08b') for i in data)
    
# === FUNGSI PENYISIPAN PESAN ===
from PIL import Image

# Delimiter biner untuk menandakan akhir pesan
DELIMITER = '1111111111111110111111111111111011111111111111101111111111111110' # 16 bits = 2 bytes

def encode_lsb(image_path, secret_message, output_path):
    """Menyisipkan pesan rahasia ke dalam gambar menggunakan Steganografi LSB."""
    
    # Buka gambar
    img = Image.open(image_path, 'r')
    
    # Pastikan mode gambar adalah RGB untuk kompatibilitas
    if img.mode != 'RGB':
        img = img.convert('RGB')
        
    width, height = img.size
    
    # Konversi pesan dan tambahkan delimiter
    data_binary = to_binary(secret_message) + DELIMITER
    data_len = len(data_binary)
    
    # Hitung kapasitas bit gambar
    # Setiap piksel (3 byte) dapat menyimpan 3 bit pesan
    max_capacity = width * height * 3
    
    # Cek kapasitas
    if data_len > max_capacity:
        return f"ERROR: Pesan terlalu panjang ({data_len} bit). Kapasitas max: {max_capacity} bit."

    data_index = 0
    
    # Proses penyisipan LSB
    for x in range(width):
        for y in range(height):
            # Ambil nilai RGB piksel saat ini
            pixel = list(img.getpixel((x, y)))
            
            # Iterasi melalui setiap channel (R, G, B)
            for i in range(3): # i=0(R), i=1(G), i=2(B)
                if data_index < data_len:
                    # Ambil bit pesan berikutnya (0 atau 1)
                    secret_bit = int(data_binary[data_index])
                    
                    # Hapus LSB piksel (dengan AND 11111110)
                    # Lalu, tambahkan bit rahasia (dengan OR)
                    pixel[i] = pixel[i] & 254 | secret_bit
                    
                    data_index += 1
            
            # Tulis kembali piksel yang sudah dimodifikasi
            img.putpixel((x, y), tuple(pixel))
            
            # Hentikan jika semua bit pesan sudah disisipkan
            if data_index >= data_len:
                break
        
        if data_index >= data_len:
            break
            
    # Simpan gambar baru dengan pesan tersembunyi
    img.save(output_path)
    return f"Pesan berhasil disisipkan. Gambar baru disimpan di: {output_path}"

# === FUNGSI EKSTRAKSI PESAN ===
def decode_lsb(image_path):
    """Mengambil pesan rahasia dari gambar menggunakan Steganografi LSB."""
    
    img = Image.open(image_path, 'r')
    img = img.convert('RGB')
    width, height = img.size
    
    binary_message = ""
    
    # Proses pengambilan LSB
    for x in range(width):
        for y in range(height):
            pixel = list(img.getpixel((x, y)))
            
            # Ambil LSB dari setiap channel (R, G, B)
            for i in range(3):
                # Ambil LSB piksel (dengan AND 00000001)
                binary_message += str(pixel[i] & 1)
                
                # Cek apakah delimiter sudah ditemukan
                if binary_message.endswith(DELIMITER):
                    # Hapus delimiter dari akhir pesan biner
                    final_binary = binary_message[:-len(DELIMITER)]
                    
                    # Konversi biner ke string (8 bit per karakter)
                    message_bytes = [final_binary[i:i+8] for i in range(0, len(final_binary), 8)]
                    secret_message = "".join([chr(int(b, 2)) for b in message_bytes])
                    
                    return secret_message.strip() # Menghilangkan spasi ekstra
                    
    # Jika loop selesai dan delimiter tidak ditemukan
    return "ERROR: Delimiter pesan tidak ditemukan. Gambar mungkin tidak mengandung pesan, atau kunci/format salah."