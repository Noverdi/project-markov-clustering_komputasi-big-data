# Project Ekstraksi Node dan Bobot Waktu Tempuh Fasilitas Pemerintahan

Project ini digunakan untuk membangun data graf berbasis fasilitas pemerintahan. Setiap fasilitas direpresentasikan sebagai **node**, sedangkan hubungan antar-node direpresentasikan sebagai **edge** dengan bobot berupa **waktu tempuh** antar lokasi.

Data yang dihasilkan akan digunakan untuk penelitian klasterisasi wilayah berbasis Markov Clustering Algorithm (MCL).

---

## Tujuan Project

Tujuan utama project ini adalah:

1. Mengumpulkan daftar fasilitas pemerintahan sebagai node.
2. Mendapatkan koordinat geografis dari setiap node.
3. Menggabungkan seluruh node ke dalam satu dataset.
4. Mengekstraksi waktu tempuh antar-node.
5. Membentuk struktur data graf dengan waktu tempuh sebagai bobot edge.
6. Clustering data graf menggunakan Markov CLustering untuk melihat wilayah mana yang ter-cluster untuk dijadiwak wilayah pemekaran

---

## Struktur File

```text
.
├── get-node*.py
├── get-loc*.py
├── combine.ipynb
├── data/
├── output/
└── README.md
