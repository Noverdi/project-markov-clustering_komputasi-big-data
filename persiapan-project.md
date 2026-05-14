**Berikut adalah langkah-langkah sistematis yang dipersiapkan:**


---

### 1. Tahap Preprocessing & Konsolidasi Node (Done)

Sebelum menyentuh API apa pun, data node harus dalam kondisi "bersih".

* **Hierarki Administrasi:** Kelompokkan node berdasarkan levelnya (Desa **$\rightarrow$** Kecamatan **$\rightarrow$** Kabupaten). Ini membantu dalam menentukan strategi *Origin-Destination* (O-D) yang lebih hemat biaya. **( file node google sheets, done)**
* **Validasi Nomenklatur:** Pastikan semua nama desa/kecamatan sudah mengikuti standar terbaru (seperti penggabungan kata "Muaragembong") agar pencarian di Google Maps akurat. **( file node google sheets, done)**

### 2. Geocoding (Enrichment Data Spasial) (Done)

Langkah ini adalah untuk mengisi kolom `latitude` dan `longitude` yang masih kosong.

* **Eksekusi Skrip Python:** Gunakan skrip Multi-threading dengan `Google Maps Geocoding API`. **( file node google sheets, done)**
* **Verifikasi Manual (Sampling):** Ambil 5-10% data secara acak dan cek posisinya di peta untuk memastikan Google tidak salah memberikan titik (misalnya memberikan koordinat di kota lain dengan nama desa yang sama).

### 3. Perancangan Matriks Jarak (Graph Edge Preparation) ( **diputuskan ketika akan unduh via API waktu tempuhnya, minggu depan 15 Mei**)

Ini adalah tahap krusial untuk riset Teori Graf Anda. Anda perlu menentukan pasangan mana saja yang perlu dihitung jarak/waktunya.

* **Definisi Struktur Graf:**
  * Apakah graf *fully connected* (semua desa terhubung ke semua desa)? ( **diputuskan ketika akan unduh via API waktu tempuhnya, minggu depan 15 Mei**)
  * Atau hanya desa ke pusat kecamatan dan antar kecamatan saja?
* **Penentuan Mode Transportasi:** Gunakan mode `two_wheeler` untuk wilayah Bekasi agar estimasi waktu tempuh lebih realistis mengingat kondisi kemacetan dan akses jalan sempit.
* **Pemilihan Variabel Bobot (**$W$**):** Putuskan apakah bobot *edge* Anda adalah **Jarak (km)** atau  **Waktu (menit)** . Dalam analisis kewilayahan, waktu tempuh biasanya lebih bermakna daripada jarak absolut.

### 4. Ekstraksi Data dari Distance Matrix API (Minggu depan 15 mei)

Setelah matriks O-D siap:

* **Batching Request:** Google Maps API membatasi jumlah origin/destinasi per  *request* . Anda perlu membagi (batch) data Anda menjadi potongan kecil (misal: 10 origin x 10 destinasi).
* **Penyimpanan Hasil:** Simpan hasil API (jarak dan durasi) ke dalam format *long-format* (id_asal, id_tujuan, jarak, waktu) agar mudah diolah menjadi  *adjacency matrix* .

### 5. Pemodelan Matematika & Clustering (MInggu Depan 15 Mei atau 2 minggu)

* **Konstruksi Adjacency Matrix:** Ubah data jarak/waktu menjadi matriks persegi **$A$** dimana **$A_{ij}$** adalah waktu tempuh antar node.
* **Algoritma Markov Clustering (MCL):** Terapkan MCL untuk melihat bagaimana node-node (desa/kecamatan) secara alami membentuk klaster berdasarkan konektivitasnya.
* **Analisis Bekasi Utara:** Evaluasi apakah klaster yang terbentuk dari algoritma sesuai dengan usulan pembagian administratif Bekasi Utara.

### 6. Visualisasi & Interpretasi (MInggu Depan 15 Mei atau 2 minggu lagi)

* **Mapping:** Visualisasikan hasil klastering menggunakan pustaka seperti `Folium` atau `Geopandas` di Python.
* **Analisis Sensitivitas:** Coba ubah parameter waktu keberangkatan (jam sibuk vs jam sepi) untuk melihat apakah struktur klaster wilayah Anda berubah drastis akibat kemacetan.
