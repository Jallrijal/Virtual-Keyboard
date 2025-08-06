# AI-Virtual-Keyboard

Dibuat Oleh Rijal Imamul Haq Syamsu Alam.

Referensi: https://github.com/vinit714/AI-Virtual-Keyboard

## Cara Penggunaan

### Persyaratan Sistem
- Python 3.9 atau lebih tinggi
- Kamera web
- Library yang diperlukan (lihat requirements.txt)

### Instalasi
1. Clone repository ini
2. Install dependensi: `pip install -r requirements.txt`
3. Jalankan program: `python virtual_keyboard.py`

### Cara Menggunakan Virtual Keyboard
1. **Arahkan JARI TENGAH** ke tombol yang ingin ditekan
2. **Rapatkan JARI TELUNJUK dan JARI TENGAH** untuk menekan tombol
3. **Tekan 'q'** di keyboard fisik untuk keluar

### Fitur
- ✅ Deteksi tangan real-time menggunakan MediaPipe
- ✅ Keyboard virtual responsif yang menyesuaikan ukuran layar
- ✅ Visual feedback untuk tombol yang dipilih
- ✅ Area teks untuk menampilkan hasil ketikan
- ✅ Tombol backspace untuk menghapus karakter
- ✅ Threshold jarak yang dapat disesuaikan untuk kemudahan penggunaan

### Teknologi yang Digunakan
- **OpenCV** - Pemrosesan gambar dan deteksi
- **MediaPipe** - Deteksi tangan dan landmark
- **CVZone** - Modul deteksi tangan yang mudah digunakan
- **PyNput** - Kontrol keyboard virtual
- **NumPy** - Perhitungan matematika