<div align="center">
<img src="assets/poster.png" width="100%" />

# Tugas Besar Mata Kuliah Sistem / teknologi multimedia (IF4021)

### Dosen Pengampu: **Martin C.T Manullang, S.T., M.T., PhD.**

# Suara Menentukan Nasib
---

## 🎯 Deskripsi Proyek
Suara Menentukan Nasib adalah sebuah program permainan sederhana yang dibuat menggunakan Python. Dalam permainan ini, karakter Mario akan bergerak berdasarkan intensitas suara yang dideteksi dari mikrofon. Namun, berbeda dari permainan biasa, Mario hanya bisa bergerak jika tangan dan kepala pemain terlihat di depan kamera. Deteksi gerakan dan posisi tubuh dilakukan secara real-time untuk memastikan pemain benar-benar ada dalam frame. Permainan ini terinspirasi dari elemen "Red Light, Green Light" pada serial Squid Game, di mana penembak dari Squid Game akan memantau pergerakan. Jika suara yang terdeteksi terlalu keras saat lampu merah menyala, Mario akan langsung tereliminasi. Sebaliknya, saat lampu hijau menyala dan suara cukup kuat, Mario akan bergerak maju. Permainan memiliki batas waktu untuk mencapai garis akhir. Di akhir sesi, sistem akan menampilkan notifikasi jika menang  "Selamat! Kamu Menang" atau jika kalah "Kamu Kalah: Bersuara" dan menampilkan volume dan pitch suara pemain, tergantung pada performa pemain. 


---

## 🧑‍🤝‍🧑 Anggota Tim

| Nama                    | NIM        | Username GitHub         |
|-------------------------|------------|--------------------------|
| Marchel Ferry Timoteus S           | 121140195  | marselferrys         |
| Silva Oktaria Putri       | 12214085  | Silvok      |
| Irma Amelia Novianti        | 122140128  | irmaamelia45            |

---



## 🌐 Teknologi yang Digunakan

Berikut adalah teknologi dan alat yang digunakan dalam proyek ini:

| Logo                                                                                                                           | Nama Teknologi | Fungsi                                                                           |
| ------------------------------------------------------------------------------------------------------------------------------ | -------------- | -------------------------------------------------------------------------------- |
| <img src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg" style="width:50px;" alt="Python Logo" width="60">            | Python         | Bahasa pemrograman utama untuk pengembangan filter.                              |
| <img src="https://upload.wikimedia.org/wikipedia/commons/9/9a/Visual_Studio_Code_1.35_icon.svg" style="width:50px;" alt="VS Code Logo" width="60"> | VS Code        | Editor teks untuk mengedit skrip secara efisien dengan dukungan ekstensi Python. |

---

##  🧩 Library yang Digunakan

Berikut adalah daftar library Python yang digunakan dalam proyek ini, beserta fungsinya:

| **Library**        | **Fungsi**                                                                                                                                                                                                                                                                                                                                                         |
|--------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `cv2`              | Digunakan untuk menangkap gambar dari kamera (`VideoCapture`) dan memproses gambar secara langsung, seperti memberikan efek blur.                                                                                                                                                                                                                                 |
| `mediapipe`        | Digunakan untuk mendeteksi landmark tubuh, wajah, dan tangan. Contohnya: posisi hidung (`pose_landmarks.landmark[0]`) untuk mendeteksi gerakan kepala, serta landmark tangan (`pose_landmarks.landmark[15]`, `pose_landmarks.landmark[16]`) untuk mendeteksi gerakan tangan.                                                |
| `pygame`           | Digunakan untuk membuat dan mengelola jendela game (`display`), menangani input pengguna (keyboard dan mouse melalui `event`), menampilkan grafis 2D (karakter, latar belakang, tombol, teks melalui `blit`, `draw`), serta memutar audio (`mixer`).                                                                       |
| `numpy`            | Digunakan untuk operasi numerik, terutama pada array yang mewakili gambar dan data audio.                                                                                                                                                                                                                                   |
| `scipy`            | Digunakan untuk memproses sinyal audio, misalnya dengan *band-pass filter* melalui modul `scipy.signal` untuk mendeteksi suara berdasarkan frekuensi tertentu.                                                                                                                                                              |
| `sounddevice`      | Digunakan untuk menangkap input suara dari mikrofon secara real-time. Sering digunakan bersama `numpy` untuk analisis volume dan pitch suara dalam game berbasis input audio.                                                                                                                                               |
| `PIL` (`Pillow`)   | Digunakan untuk memuat, memproses, dan menampilkan gambar (misalnya: membuka gambar tombol, background, atau ikon), serta mengubah ukuran atau format gambar sebelum ditampilkan di jendela game dengan `pygame`.                                                                                                           |


---

# ⚙️ Langkah Instalasi dan Penggunaan Program
1. Clone repository ini ke lokal anda:

    ```bash
    git clone https://github.com/marselferrys/Tubes_Mulmet.git
    ```

2. Masuk ke direktori proyek

    ```bash
    cd Tubes_Mulmet
    ```

2. Aktifkan virtual environment (opsional):

    ```bash
    uv venv
    source venv/bin/activate  # Linux/Mac
    .venv\Scripts\activate    # Windows
    ```

3. Instal dependensi:

    ```bash
    pip install -r requirements.txt # pip
    uv pip install -r requirements.txt # uv
    ```

4. Jalankan program di CMD/Terminal:
    ```bash
    python main.py
    ```

## 🗓️ Logbook Mingguan
### 🔹 Minggu 1
### 🔹 Minggu 2
### 🔹 Minggu 3
### 🔹 Minggu 4

---
Laporan: 

---
Demo Program: 
