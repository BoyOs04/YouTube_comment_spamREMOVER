# YouTube Spam Comment Remover

Script Python ini membantu Anda menghapus komentar spam secara otomatis dari video YouTube berdasarkan pola teks yang Anda tentukan (misalnya nama bot, tautan spam, emoji tertentu, dsb).

---

## Fitur Utama

- Input langsung URL video atau ID video YouTube
- Deteksi dan penghapusan komentar spam menggunakan kata kunci atau pola
- Login via OAuth dengan akun Google pribadi
- Mendukung beberapa video sekaligus
- Output daftar komentar yang dihapus ke file `deleted_comments.txt`

---

## Instalasi

### 1. Siapkan Python & Termux (untuk Android) atau Terminal (untuk PC)

- Pastikan Python 3 sudah terinstal
- Pastikan Anda bisa menjalankan perintah `pip`

### 2. Instal dependensi yang dibutuhkan

```bash
pip install google-api-python-client oauth2client
```

### 3. Unduh file `ytspam.py` dan simpan dalam folder

---

## Cara Menjalankan

```bash
python ytspam.py
```

### Langkah penggunaan:

1. Jalankan script
2. Masukkan URL video YouTube (contoh: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`)
3. Masukkan pola teks komentar spam yang ingin dihapus (pisah dengan koma)
   Contoh 
   ```
   free diamonds, whatsapp.me, Ⓜ️ⓞⓜⓞ, visit my channel
   ```
4. Anda akan diarahkan ke halaman Google login di browser
5. Login dengan akun YouTube Anda
6. Salin kode otorisasi yang ditampilkan dan masukkan ke terminal
7. Script akan mulai memproses dan menghapus komentar spam

> Semua komentar yang berhasil dihapus akan dicatat di file `deleted_comments.txt`
```bash
```
---

## Membuat Google Cloud Project Sendiri

Agar script ini dapat digunakan dengan akun Google Anda (bukan akun developer pembuat), Anda perlu membuat project OAuth Anda sendiri. Berikut panduannya:

### Langkah 1: Masuk ke Google Cloud Console

- Buka [Google Cloud Console](https://console.cloud.google.com/)

### Langkah 2: Buat Proyek Baru

- Klik “Select Project” > “New Project”
- Beri nama proyek Anda, lalu klik **Create**

### Langkah 3: Aktifkan YouTube Data API v3

- Pilih proyek Anda
- Buka menu **APIs & Services > Library**
- Cari “YouTube Data API v3”
- Klik **Enable**

### Langkah 4: Konfigurasi OAuth Consent Screen

- Masuk ke **APIs & Services > OAuth consent screen**
- Pilih “External”
- Isi detail aplikasi (Nama app, email developer, dll.)
- Di bagian "Test users", tambahkan email Google Anda
- Klik **Save & Continue** hingga selesai

### Langkah 5: Buat OAuth Credentials

- Masuk ke menu **Credentials**
- Klik **Create Credentials > OAuth client ID**
- Pilih **Application type: Desktop App**
- Beri nama (misal: `YTSpamRemover`)
- Klik **Create**
- Klik **Download JSON** → File ini adalah `client_secrets.json` dan harus di edit namanya jadi itu 

### Langkah 6: Letakkan File `client_secrets.json`

- Simpan file tersebut di folder yang sama dengan file `ytspam.py`

### Langkah 7: Jalankan Script

```bash
python ytspam.py
```

---

## Struktur Folder yang Direkomendasikan

```
youtube-spam-remover/
│
├── ytspam.py
├── client_secrets.json   ← (download di OAuth Consent Screen)
├── deleted_comments.txt  ← (otomatis dibuat setelah digunakan)
└── README.md
```

---

## Troubleshooting

- **403 access_denied**: Pastikan akun Google Anda dimasukkan sebagai "Test User" di bagian OAuth consent screen.
- **InvalidClientSecretsError**: Pastikan file `client_secrets.json` berada di folder yang benar.
- **Token error**: Hapus file token `.oauth2.json` jika ingin login ulang.

---

## Bantuan

Untuk bantuan lebih lanjut, hubungi: [chat.com](http://chat.com)
