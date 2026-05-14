import csv
from pathlib import Path

output_path = Path("/mnt/data/node_layanan_ekonomi_publik_kab_bekasi.csv")

rows = []

def add(nama, sub_jenis, kecamatan="", desa_kelurahan="", alamat="", sumber="", catatan=""):
    rows.append({
        "node_id": f"ECO_{len(rows)+1:03d}",
        "nama_node": nama,
        "jenis_node": "layanan_ekonomi_publik",
        "sub_jenis": sub_jenis,
        "kecamatan": kecamatan,
        "desa_kelurahan": desa_kelurahan,
        "alamat": alamat,
        "latitude": "",
        "longitude": "",
        "sumber": sumber,
        "catatan_validasi": catatan
    })

src_ppid = "https://ppid.bekasikab.go.id/ppidpelaksana/"
src_disdag = "https://disperdag.bekasikab.go.id/"
src_open_pasar = "https://opendata.bekasikab.go.id/dataset/data-jumlah-pasar-rakyat-di-kabupaten-bekasi-tahun-2024"
src_rkpd_2026 = "https://bappeda.bekasikab.go.id/uploadfiles/dokumen/20250731_045734_Laporan_RKPD_Kabupaten_Bekasi_Tahun_2026_Juni_2025_removed_%282%29.pdf"
src_pasar_sni = "https://www.bekasikab.go.id/pasar-tarumajaya-dan-kedung-gede-siap-menjadi-pasar-sni-jawa-barat"
src_perbup_upt = "https://peraturan.bpk.go.id/Download/267438/af%20PERBUP%20nomor%2015%20tahun%202021%20wis.pdf"
src_kukm = "https://kukm.bekasikab.go.id/UMKM_by_Kecamatansmry.php"
src_bpp = "https://www.bekasikab.go.id/bpp-pebayuran-kenalkan-dunia-pertanian-kepada-siswa-sd-lewat-edufarming"
src_bpp_2022 = "https://www.neraca.co.id/article/161677/pemkab-bekasi-bangun-dua-balai-penyuluhan-pertanian"
src_mpp = "https://mpp.bekasikab.go.id/tenant"

# Kantor/dinas ekonomi publik utama
add("Dinas Perdagangan Kabupaten Bekasi", "dinas_perdagangan", "Cikarang Pusat", "", "",
    src_ppid, "Koordinat dan alamat perlu divalidasi.")
add("Dinas Koperasi dan Usaha Kecil Menengah Kabupaten Bekasi", "dinas_koperasi_ukm", "Cikarang Pusat", "", "",
    src_ppid, "Koordinat dan alamat perlu divalidasi.")
add("Dinas Pertanian Kabupaten Bekasi", "dinas_pertanian", "Cikarang Pusat", "", "",
    src_ppid, "Koordinat dan alamat perlu divalidasi.")
add("Dinas Ketahanan Pangan Kabupaten Bekasi", "dinas_ketahanan_pangan", "Cikarang Pusat", "", "",
    src_ppid, "Koordinat dan alamat perlu divalidasi.")
add("Dinas Perikanan Kabupaten Bekasi", "dinas_perikanan", "Cikarang Pusat", "", "",
    src_ppid, "Koordinat dan alamat perlu divalidasi.")
add("Dinas Penanaman Modal dan Pelayanan Terpadu Satu Pintu Kabupaten Bekasi", "dpmptsp", "Cikarang Pusat", "", "",
    src_ppid, "Relevan untuk layanan perizinan ekonomi/investasi; koordinat perlu divalidasi.")
add("Badan Pendapatan Daerah Kabupaten Bekasi", "bapenda", "Cikarang Pusat", "", "",
    src_ppid, "Relevan untuk layanan pajak/retribusi daerah; koordinat perlu divalidasi.")
add("Layanan Perdagangan/Koperasi/UMKM di MPP Kabupaten Bekasi", "layanan_ekonomi_mpp", "Cikarang Pusat", "", "",
    src_mpp, "Titik layanan perlu divalidasi sesuai tenant aktif MPP.")

# Pasar rakyat/tradisional (12 pasar rakyat yang sering muncul dalam pemberitaan/daftar Disdag)
pasar = [
    ("Pasar Cibarusah", "pasar_rakyat", "Cibarusah", "", "", src_open_pasar),
    ("Pasar Serang", "pasar_rakyat", "Cikarang Selatan", "", "Jl. Raya Serang-Cibarusah, Kabupaten Bekasi", src_open_pasar),
    ("Pasar Lemahabang", "pasar_rakyat", "Cikarang Utara", "", "", src_open_pasar),
    ("Pasar Setu", "pasar_rakyat", "Setu", "", "", src_open_pasar),
    ("Pasar Cikarang / Pasar Baru Cikarang", "pasar_rakyat", "Cikarang Utara", "", "", src_open_pasar),
    ("Pasar Cibitung", "pasar_rakyat", "Cibitung", "Wanasari", "Jl. Raya Teuku Umar, Wanasari, Cibitung, Kabupaten Bekasi", src_open_pasar),
    ("Pasar Tambun Selatan", "pasar_rakyat", "Tambun Selatan", "", "", src_open_pasar),
    ("Pasar Babelan", "pasar_rakyat", "Babelan", "", "", src_open_pasar),
    ("Pasar Tarumajaya", "pasar_rakyat", "Tarumajaya", "", "", src_pasar_sni),
    ("Pasar Kedung Gede", "pasar_rakyat", "Kedungwaringin", "Bojongsari", "Jl. Raya Kedungwaringin, Desa Bojongsari, Kecamatan Kedungwaringin", src_pasar_sni),
    ("Pasar Sukatani", "pasar_rakyat", "Sukatani", "", "", src_open_pasar),
    ("Pertokoan Cikarang", "kawasan_pertokoan_publik", "Cikarang Utara", "", "", src_open_pasar),
]
for nama, sub, kec, desa, alamat, sumber in pasar:
    add(nama, sub, kec, desa, alamat, sumber,
        "Koordinat perlu divalidasi dari Google Maps/OSM. Nama pasar mengacu daftar pasar rakyat/rujukan Disdag dan pemberitaan daerah.")

# UPTD pengelolaan pasar / kantor pasar
upt_pasar = [
    ("UPTD Pengelolaan Pasar Cibarusah", "uptd_pasar", "Cibarusah", "", ""),
    ("UPTD Pengelolaan Pasar Serang", "uptd_pasar", "Cikarang Selatan", "", ""),
    ("UPTD Pengelolaan Pasar Lemahabang", "uptd_pasar", "Cikarang Utara", "", ""),
    ("UPTD Pengelolaan Pasar Setu", "uptd_pasar", "Setu", "", ""),
    ("UPTD Pengelolaan Pasar Cikarang", "uptd_pasar", "Cikarang Utara", "", ""),
    ("UPTD Pengelolaan Pasar Cibitung", "uptd_pasar", "Cibitung", "", ""),
    ("UPTD Pengelolaan Pasar Tambun Selatan", "uptd_pasar", "Tambun Selatan", "", ""),
    ("UPTD Pengelolaan Pasar Babelan", "uptd_pasar", "Babelan", "", ""),
    ("UPTD Pengelolaan Pasar Tarumajaya", "uptd_pasar", "Tarumajaya", "", ""),
    ("UPTD Pengelolaan Pasar Kedung Gede", "uptd_pasar", "Kedungwaringin", "", ""),
    ("UPTD Pengelolaan Pasar Sukatani", "uptd_pasar", "Sukatani", "", ""),
]
for nama, sub, kec, desa, alamat in upt_pasar:
    add(nama, sub, kec, desa, alamat, src_perbup_upt,
        "Nama UPTD mengikuti pola UPTD pengelolaan pasar; alamat/koordinat perlu divalidasi sebelum analisis final.")

# BPP per kecamatan sebagai layanan ekonomi pertanian
kecamatan = [
    "Babelan", "Bojongmangu", "Cabangbungin", "Cibarusah", "Cibitung",
    "Cikarang Barat", "Cikarang Pusat", "Cikarang Selatan", "Cikarang Timur",
    "Cikarang Utara", "Karangbahagia", "Kedungwaringin", "Muara Gembong",
    "Pebayuran", "Serang Baru", "Setu", "Sukakarya", "Sukatani",
    "Sukawangi", "Tambelang", "Tambun Selatan", "Tambun Utara", "Tarumajaya"
]
for kec in kecamatan:
    sumber = src_bpp if kec == "Pebayuran" else (src_bpp_2022 if kec in ["Tambun Utara", "Cikarang Selatan"] else src_ppid)
    add(f"Balai Penyuluhan Pertanian Kecamatan {kec}", "balai_penyuluhan_pertanian", kec, "", "",
        sumber, "Node kandidat layanan ekonomi pertanian; nama/alamat/koordinat kantor BPP perlu divalidasi.")

# Titik ekonomi rakyat/UMKM level kecamatan sebagai kandidat agregat
for kec in kecamatan:
    add(f"Sentra/Koordinator UMKM Kecamatan {kec}", "sentra_umkm_kecamatan", kec, "", "",
        src_kukm, "Node agregat kandidat untuk ekonomi rakyat/UMKM; hanya dipakai jika analisis membutuhkan representasi UMKM per kecamatan.")

fieldnames = [
    "node_id", "nama_node", "jenis_node", "sub_jenis", "kecamatan",
    "desa_kelurahan", "alamat", "latitude", "longitude", "sumber", "catatan_validasi"
]

with output_path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

output_path.as_posix(), len(rows)
