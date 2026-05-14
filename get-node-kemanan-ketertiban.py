import csv
from pathlib import Path

output_path = Path("/mnt/data/node_layanan_keamanan_ketertiban_kab_bekasi.csv")

rows = []

def add(nama, jenis, sub, kecamatan="", desa_kelurahan="", alamat="", latitude="", longitude="", sumber="", catatan=""):
    rows.append({
        "node_id": f"SEC_{len(rows)+1:03d}",
        "nama_node": nama,
        "jenis_node": jenis,
        "sub_jenis": sub,
        "kecamatan": kecamatan,
        "desa_kelurahan": desa_kelurahan,
        "alamat": alamat,
        "latitude": latitude,
        "longitude": longitude,
        "sumber": sumber,
        "catatan_validasi": catatan
    })

# Sumber ringkas
src_polres = "https://tribratanews-metrobekasi.metro.polri.go.id/"
src_damkar = "https://bekasi.pojoksatu.id/kabupaten-bekasi/1136998655/nomor-kontak-kantor-damkar-kabupaten-bekasi-pastikan-simpan-untuk-siaga"
src_bappeda = "https://bappeda.bekasikab.go.id/uploadfiles/dokumen/20240718_114543_LAPORAN_EVALUASI_TERHADAP_RKPD_KABUPATEN_BEKASI_TAHUN_2023.pdf"
src_pemkab_ppid = "https://ppid.bekasikab.go.id/ppidpelaksana/"

# Kepolisian
add("Polres Metro Bekasi", "keamanan_ketertiban", "polres", "Cikarang Utara", "Simpangan",
    "Jl. Ki Hajar Dewantara No.1, Simpangan, Cikarang Utara, Kabupaten Bekasi",
    sumber=src_polres, catatan="Alamat umum tersedia; koordinat perlu divalidasi.")

polsek_data = [
    ("Polsek Tambun", "Tambun Selatan/Tambun Utara", "", ""),
    ("Polsek Cikarang", "Cikarang Utara", "", ""),
    ("Polsek Cikarang Pusat", "Cikarang Pusat", "", ""),
    ("Polsek Cikarang Barat", "Cikarang Barat", "", ""),
    ("Polsek Cikarang Selatan", "Cikarang Selatan", "", ""),
    ("Polsek Cikarang Timur", "Cikarang Timur", "", ""),
    ("Polsek Kedung Waringin", "Kedungwaringin", "", ""),
    ("Polsek Pebayuran", "Pebayuran", "Kertajaya", ""),
    ("Polsek Muaragembong", "Muara Gembong", "", ""),
    ("Polsek Sukatani", "Sukatani/Sukakarya", "", ""),
    ("Polsek Tambelang", "Tambelang", "", ""),
    ("Polsek Babelan", "Babelan", "", ""),
    ("Polsek Tarumajaya", "Tarumajaya", "", ""),
    ("Polsek Cibarusah", "Cibarusah", "", ""),
    ("Polsek Serang Baru", "Serang Baru", "", ""),
    ("Polsek Setu", "Setu", "", ""),
    ("Polsek Cabangbungin", "Cabangbungin", "", ""),
]
for nama, kec, desa, alamat in polsek_data:
    add(nama, "keamanan_ketertiban", "polsek", kec, desa, alamat,
        sumber=src_polres, catatan="Nama polsek mengacu daftar Polsek Jajaran Polres Metro Bekasi; kecamatan cakupan perlu divalidasi jika dipakai sebagai atribut resmi.")

# Satpol PP / Ketertiban umum
add("Satuan Polisi Pamong Praja Kabupaten Bekasi", "keamanan_ketertiban", "satpol_pp",
    "Cikarang Pusat", "", "", sumber=src_pemkab_ppid,
    catatan="Koordinat dan alamat perlu divalidasi.")

# BPBD
add("Badan Penanggulangan Bencana Daerah Kabupaten Bekasi", "keamanan_ketertiban", "bpbd",
    "Cikarang Pusat", "", "", sumber=src_pemkab_ppid,
    catatan="Koordinat dan alamat perlu divalidasi.")

# Damkar dan pos damkar
add("Dinas Pemadam Kebakaran Kabupaten Bekasi", "keamanan_ketertiban", "dinas_pemadam_kebakaran",
    "Cikarang Barat", "", "", sumber=src_damkar,
    catatan="Koordinat dan alamat perlu divalidasi.")

damkar_posts = [
    ("Pos Damkar Cikarang Utara", "Cikarang Utara", "021-89077000"),
    ("Pos Damkar Cikarang Selatan", "Cikarang Selatan", "021-89881900"),
    ("Pos Damkar Pemda Kabupaten Bekasi", "Cikarang Pusat", "021-89119000"),
    ("Pos Damkar Babelan", "Babelan", "021-89239900"),
    ("Pos Damkar Serang Baru", "Serang Baru", "021-89098803"),
    ("Pos Damkar Sukatani", "Sukatani", "021-89097913"),
    ("Pos Damkar Tarumajaya", "Tarumajaya", "0813-1793-2644"),
    # Tambahan dari sumber lama/berita pembangunan pos
    ("Pos/Mako Damkar Cikarang Barat", "Cikarang Barat", ""),
    ("Pos Damkar Metland Cibitung", "Cibitung", ""),
    ("Pos Damkar Cikarang Timur / Stadion Wibawa Mukti", "Cikarang Timur", ""),
]
for nama, kec, kontak in damkar_posts:
    add(nama, "keamanan_ketertiban", "pos_pemadam_kebakaran", kec, "", "",
        sumber=src_damkar, catatan=f"Kontak: {kontak}. Koordinat perlu divalidasi." if kontak else "Nama pos dari pemberitaan/rujukan damkar; koordinat perlu divalidasi.")

# Pos polisi umum - dikosongkan agar tidak mengarang titik; bisa ditambahkan manual kemudian.
# Add a note row? Better no.

fieldnames = [
    "node_id", "nama_node", "jenis_node", "sub_jenis", "kecamatan",
    "desa_kelurahan", "alamat", "latitude", "longitude", "sumber", "catatan_validasi"
]

with output_path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

output_path.as_posix(), len(rows)
