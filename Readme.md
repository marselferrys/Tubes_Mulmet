# Tugas Besar Mata Kuliah Sistem / teknologi multimedia (IF4021)

### Dosen Pengampu: **Martin Clinton Tosima Manullang, S.T., M.T..**

# Suara Menentukan Nasib
---

## 🎯 Deskripsi Proyek
Suara Menentukan Nasib adalah sebuah program permainan sederhana yang dibuat menggunakan Python. Dalam permainan ini, karakter Mario akan bergerak berdasarkan intensitas suara yang dideteksi dari mikrofon. Namun, berbeda dari permainan biasa, Mario hanya bisa bergerak jika tangan dan kepala pemain terlihat di depan kamera. Deteksi gerakan dan posisi tubuh dilakukan secara real-time untuk memastikan pemain benar-benar ada dalam frame. Permainan ini terinspirasi dari elemen "Red Light, Green Light" pada serial Squid Game, di mana penembak dari Squid Game akan memantau pergerakan. Jika suara yang terdeteksi terlalu keras saat lampu merah menyala, Mario akan langsung tereliminasi. Sebaliknya, saat lampu hijau menyala dan suara cukup kuat, Mario akan bergerak maju.Permainan memiliki batas waktu untuk mencapai garis akhir. Di akhir sesi, sistem akan menampilkan notifikasi seperti "Berhasil Menang" atau "Gagal - Terdeteksi Saat Lampu Merah", tergantung pada performa pemain. 


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
| <img src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg" alt="Python Logo" width="60">            | Python         | Bahasa pemrograman utama untuk pengembangan filter.                              |
| <img src="https://upload.wikimedia.org/wikipedia/commons/9/9a/Visual_Studio_Code_1.35_icon.svg" alt="VS Code Logo" width="60"> | VS Code        | Editor teks untuk mengedit skrip secara efisien dengan dukungan ekstensi Python. |

---

##  🧩 Library yang Digunakan

Berikut adalah daftar library Python yang digunakan dalam proyek ini, beserta fungsinya:

| **Library**                | **Fungsi**                                                                                         |
| -------------------------- | -------------------------------------------------------------------------------------------------- |
| `cv2`                      | Digunakan untuk menangkap gambar dari kamera dan memproses gambar secara langsung.                 |
| `mediapipe`                | Digunakan untuk mendeteksi landmark wajah, seperti posisi hidung, untuk mendeteksi gerakan kepala. |
| `Scipy`, `numpy`           | Digunakan untuk bahan oprasi pembuatan program                                                     |

---

# ⚙️ Langkah Instalasi dan Penggunaan Program
1. Clone repository ini ke lokal anda:

    ```bash
    git clone https://github.com/marselferrys/Tubes_Mulmet.git
    cd dsp-realtime-rppg-respiration
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

4. Jalankan program:
    ```bash
    python main.py
    ```

## 🗓️ Logbook Mingguan
### 🔹 Minggu 1
### 🔹 Minggu 2
### 🔹 Minggu 3
### 🔹 Minggu 4
