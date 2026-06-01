# Simulasi Genetic Algorithm untuk Optimasi Pemilihan Suplemen Kesehatan Harian Berbasis Web

Aplikasi web simulasi Genetic Algorithm (GA) untuk menemukan kombinasi
suplemen kesehatan harian yang paling optimal berdasarkan pemenuhan
kebutuhan nutrisi harian (RDA) dengan budget yang ditentukan.

Proyek ini dibuat sebagai pemenuhan tugas mata kuliah Kecerdasan Buatan
dengan topik B.3 Genetic Algorithm.

---

## Deskripsi Proyek

Aplikasi ini mengimplementasikan Genetic Algorithm untuk menyelesaikan
masalah optimasi kombinasi suplemen kesehatan harian. Pengguna cukup
memasukkan budget harian, dan algoritma akan mencari kombinasi suplemen
terbaik yang memaksimalkan pemenuhan 6 nutrisi harian (Vitamin C, D,
Zinc, Omega-3, Calcium, Iron) dalam batas budget yang diberikan.

Genetic Algorithm bekerja dengan mensimulasikan proses evolusi alam,
di mana individu terbaik dipertahankan, disilangkan, dan dimutasi
untuk menghasilkan generasi yang semakin baik dari waktu ke waktu.

---

## Fitur Utama

- Implementasi lengkap Genetic Algorithm dengan komponen:
  - Representasi kromosom biner
  - Fungsi fitness berbasis pemenuhan nutrisi RDA
  - Seleksi Tournament dan Roulette Wheel
  - Crossover Single-point dan Multi-point
  - Mutasi flip bit
  - Elitisme otomatis
- Visualisasi grafik evolusi fitness per generasi menggunakan Plotly
- Kontrol parameter algoritma oleh pengguna (populasi, generasi,
  crossover rate, mutation rate)
- Tampilan metrik: waktu eksekusi, generasi konvergen, skor fitness
- Representasi kromosom biner dari solusi terbaik
- Fitur tambah dan hapus suplemen secara dinamis
- Export grafik evolusi fitness ke PNG untuk keperluan laporan
- Antarmuka web responsif dengan tema dark professional

---

## Teknologi yang Digunakan

| Kategori     | Teknologi                    |
|--------------|------------------------------|
| Backend      | Python 3.11 + Flask          |
| Frontend     | HTML + CSS Vanilla           |
| Visualisasi  | Plotly (Python)              |
| Deployment   | Railway                      |
| Domain       | .my.id                       |

---

## Struktur Folder


---

## Cara Instalasi dan Menjalankan

### Prasyarat

- Python versi 3.10 atau lebih baru
- pip

### Langkah Instalasi

1. Clone repository ini

```bash
git clone https://github.com/USERNAME/simulasi-suplemen-ga.git
cd simulasi-suplemen-ga
```

2. Buat dan aktifkan virtual environment

```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

Mac / Linux:
```bash
source .venv/bin/activate
```

3. Install semua library yang dibutuhkan

```bash
pip install -r requirements.txt
```

4. Jalankan aplikasi

```bash
python app.py
```

5. Buka browser dan akses
http://127.0.0.1:5000

---

## Cara Penggunaan

1. Buka halaman Simulasi di navbar atas
2. Masukkan budget suplemen harian pada Langkah 1
3. Atur parameter Genetic Algorithm pada Langkah 2
   (nilai default sudah dioptimalkan, tidak wajib diubah)
4. Cek dan sesuaikan daftar suplemen pada Langkah 3
5. Klik tombol Jalankan Simulasi Genetic Algorithm
6. Lihat grafik evolusi fitness dan hasil rekomendasi suplemen
7. Klik Simpan PNG untuk menyimpan grafik ke folder static/img/

---

## Cara Kerja Genetic Algorithm

1. Inisialisasi: buat populasi awal secara acak (array biner)
2. Evaluasi: hitung nilai fitness tiap individu berdasarkan
   pemenuhan nutrisi dan batas budget
3. Seleksi: pilih individu terbaik untuk bereproduksi
4. Crossover: tukar gen antar dua parent menghasilkan offspring baru
5. Mutasi: ubah gen secara acak untuk menjaga keberagaman populasi
6. Elitisme: simpan individu terbaik ke generasi berikutnya
7. Ulangi dari langkah 2 sampai generasi maksimum tercapai

---

## Data Suplemen

Tersedia 15 data suplemen default yang umum dijual di apotek,
berdasarkan kandungan 6 nutrisi utama:

| Nutrisi   | Satuan | Kebutuhan Harian (RDA) |
|-----------|--------|------------------------|
| Vitamin C | mg     | 75                     |
| Vitamin D | IU     | 600                    |
| Zinc      | mg     | 8                      |
| Omega-3   | mg     | 1000                   |
| Calcium   | mg     | 1000                   |
| Iron      | mg     | 18                     |

Sumber: WHO Vitamin and Mineral Requirements in Human Nutrition (2004)

Pengguna dapat menambah atau menghapus suplemen secara dinamis
melalui antarmuka web.

---

## Referensi

1. Russell, S., & Norvig, P. (2020). Artificial Intelligence:
   A Modern Approach (4th ed.). Pearson.

2. Mitchell, M. (1998). An Introduction to Genetic Algorithms.
   MIT Press.

3. Goldberg, D. E. (1989). Genetic Algorithms in Search,
   Optimization and Machine Learning. Addison-Wesley.

4. Holland, J. H. (1975). Adaptation in Natural and Artificial
   Systems. University of Michigan Press.

5. WHO. (2004). Vitamin and Mineral Requirements in Human
   Nutrition (2nd ed.). World Health Organization.

---

## Demo dan Tautan

- Demo aplikasi : https://namaproject.my.id
- Repository    : https://github.com/USERNAME/simulasi-suplemen-ga
- Video demo    : https://youtube.com/watch?v=XXXXXXXXX

---

## Identitas

- Nama          : [Selsa Shafana Alfiyani]
- NIM           : [301240041]
- Mata Kuliah   : Kecerdasan Buatan
- Topik         : B.3 Genetic Algorithm
- Dosen         : Mohammad Bayu Anggara adalah S.Kom., M.Kom.
