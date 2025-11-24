# Sistem-Rekomendasi-Prioritas-Pembangunan-Daerah-Berbasis-IPM
Rekomendasi sistem untuk prioritas pembangunan daerah di Indonesia berbasis Indeks Pembangunan Manusia (IPM)

# Sistem Rekomendasi Prioritas Pembangunan Daerah Berbasis IPM

Proyek ini adalah sebuah **Decision Support System (Sistem Pendukung Keputusan)** yang dirancang untuk membantu pemerintah daerah dalam merumuskan prioritas pembangunan yang tepat sasaran.
Sistem ini menganalisis dataset **Indeks Pembangunan Manusia (IPM)** dari 514 Kabupaten/Kota di Indonesia. Dengan menggabungkan data numerik dan kategorikal, sistem ini tidak hanya menampilkan peringkat, tetapi juga menggali **insight mendalam** melalui analisis kesenjangan (*Gap Analysis*) dan pengelompokan wilayah (*Clustering*).

## Dataset & Preprocessing

Sistem ini dibangun di atas data Index Pembangunan Manusia (`dataset IPM.csv`) yang mencakup aspek vital pembangunan manusia.

### 1. Struktur Data
Dataset terdiri dari **514 baris** dengan rincian data sebagai berikut :

| Kategori | Kolom Numerik (Input Model) | Kolom Kategorikal (Konteks Tambahan) | Deskripsi Indikator |
| :--- | :--- | :--- | :--- |
| **Wilayah** | - | `Provinsi`, `Kota` | Identitas administratif wilayah. |
| **Kesehatan** | `Jumlah AHH` | `AHH` | **Angka Harapan Hidup**: Mengukur derajat kesehatan & umur panjang. |
| **Pendidikan** | `Jumlah RLS` | `RLS` | **Rata-rata Lama Sekolah**: Mengukur tingkat pendidikan masyarakat saat ini. |
| **Pendidikan** | `Jumlah HLS` | `HLS` | **Harapan Lama Sekolah**: Mengukur potensi pendidikan masa depan. |
| **Ekonomi** | `Pengeluaran` | `PPK` | **Pengeluaran Per Kapita**: Mengukur standar hidup layak (daya beli). |
| **Komposit** | `Jumlah IPM` | `IPM` | Nilai agregat Indeks Pembangunan Manusia. |

### 2. Preprocessing
Dataset awal menggunakan format penulisan angka Indonesia yang perlu dibersihkan agar dapat diolah :
* **Pemisah Ribuan:** Kolom `Pengeluaran` menggunakan titik (contoh: `7.686,00`).
    * *Solusi:* Menghapus titik (`.`) agar terbaca sebagai ribuan.
* **Pemisah Desimal:** Kolom skor (misal `Jumlah AHH`) menggunakan koma (contoh: `69,57`).
    * *Solusi:* Mengganti koma (`,`) menjadi titik (`.`) untuk konversi ke format `float`.

## Metodologi & Insight Strategis

Sistem ini mengubah data mentah menjadi rekomendasi kebijakan melalui 3 tahap analisis:

### 1. Deteksi Dimensi Terlemah (*Weakest Link Analysis*)
Sistem menormalisasi seluruh indikator numerik ke skala 0-1 untuk perbandingan yang adil.
* **Cara Kerja:** Membandingkan skor ternormalisasi antara Kesehatan, Pendidikan, dan Ekonomi dalam satu kota.
* **Insight:** Menemukan "lubang" pembangunan. Contoh: Kota dengan IPM "Tinggi" (berdasarkan kolom kategori) ternyata memiliki skor `Pengeluaran` yang anjlok dibanding kota setara.
* **Output:** Rekomendasi otomatis difokuskan pada dimensi dengan skor terendah tersebut.

### 2. Perhitungan Gap Score (Analisis Ketimpangan)
Rumus: $Gap Score = 1 - \text{Rata-rata Skor Normalisasi}$
* **Filosofi:** Semakin tinggi skor kesenjangan, semakin jauh kota tersebut dari potensi maksimalnya.
* **Insight:** Memungkinkan Pemerintah Provinsi untuk tidak hanya melihat IPM terendah, tetapi melihat kota mana yang paling "tertinggal" secara struktural di berbagai aspek sekaligus.

### 3. Clustering Wilayah (Peer Grouping)
Menggunakan **K-Means Clustering** untuk mengelompokkan 514 kota menjadi 4 karakteristik unik.
* **Tujuan:** *Benchmarking* yang adil. Membandingkan kinerja suatu kota bukan dengan Jakarta atau Surabaya, melainkan dengan kota lain dalam klaster ekonomi-sosial yang sama.

### Fitur Utama Dashboard

Aplikasi Streamlit ini menyediakan pandangan makro dan mikro:

1.  **Dashboard Provinsi (Makro):**
    * **Dual Priority Recommendation:** Menampilkan kota prioritas berdasarkan dua sudut pandang: Ketimpangan Tertinggi (Gap Score) vs Kualitas Hidup Terendah (IPM).
    * **Peta Sebaran:** Histogram distribusi nilai IPM di provinsi terpilih.
2.  **Detail Kota (Mikro):**
    * **Profil Dimensi:** Grafik batang untuk melihat keseimbangan antar sektor (Kesehatan vs Pendidikan vs Ekonomi).
    * **Status Kategori:** Menampilkan status asli dari dataset (misal: AHH "Sedang", PPK "Rendah") sebagai konteks tambahan.
    * **Rekomendasi Kebijakan:** Teks aksi nyata berdasarkan dimensi terlemah (misal: *"Tingkatkan akses pendidikan dasar"* jika RLS terendah).

## Cara Running Program

1.  **Persiapan:**
    Pastikan Python terinstal. Install library yang diperlukan:
    ```bash
    pip install pandas scikit-learn streamlit matplotlib seaborn
    ```

2.  **File Data:**
    Pastikan file `dataset IPM.csv` berada dalam satu direktori dengan kode program.

3.  **Eksekusi:**
    Jalankan perintah berikut di terminal:
    ```bash
    streamlit run nama_file_anda.py
    ```

---
*Dikembangkan untuk optimalisasi kebijakan pembangunan daerah berbasis data.*
