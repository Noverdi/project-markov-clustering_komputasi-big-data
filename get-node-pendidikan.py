import csv
from pathlib import Path

output_path = Path("/mnt/data/node_layanan_pendidikan_publik_kab_bekasi.csv")

rows = []

def add(nama, sub_jenis, kecamatan="", desa_kelurahan="", alamat="", sumber="", catatan=""):
    rows.append({
        "node_id": f"EDU_{len(rows)+1:03d}",
        "nama_node": nama,
        "jenis_node": "layanan_pendidikan_publik",
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
src_perbup_korwil = "https://peraturan.bpk.go.id/Download/256474/PERBUP%20NOMOR%2059%20TAHUN%202020%20TENTANG%20KOORDINATOR%20WILAYAH%20DINAS%20PENDIDIKAN%20PADA%20KECAMATAN%20DI%20LINGKUNGAN%20PEMRINTAH%20KABUPATEN%20BEKASI.pdf"
src_dapodik = "https://dapo.kemendikdasmen.go.id/sp/2/022200"
src_referensi = "https://referensi.data.kemendikdasmen.go.id/pendidikan/dikdas/022200/2/jf/5/index.html"
src_perpus = "https://www.bekasikab.go.id/genjot-dua-program-prioritas-disarpus-kabupaten-bekasi-optimalkan-penataan-arsip-perangkat-daerah-dan-layanan-perpustakaan"

# Kantor/instansi pendidikan utama
add("Dinas Pendidikan Kabupaten Bekasi", "dinas_pendidikan", "Cikarang Pusat", "", "",
    src_ppid, "Koordinat dan alamat perlu divalidasi.")
add("Cabang Dinas Pendidikan Wilayah III Provinsi Jawa Barat", "cabang_dinas_pendidikan", "", "", "",
    "https://disdik.jabarprov.go.id/", "Membawahi layanan pendidikan menengah provinsi; cakupan/alamat perlu divalidasi.")
add("Dinas Arsip dan Perpustakaan Kabupaten Bekasi", "dinas_arsip_perpustakaan", "Cikarang Pusat", "", "",
    src_ppid, "Koordinat dan alamat perlu divalidasi.")

# Korwil Dinas Pendidikan pada Kecamatan
kecamatan = [
    "Babelan", "Bojongmangu", "Cabangbungin", "Cibarusah", "Cibitung",
    "Cikarang Barat", "Cikarang Pusat", "Cikarang Selatan", "Cikarang Timur",
    "Cikarang Utara", "Karangbahagia", "Kedungwaringin", "Muara Gembong",
    "Pebayuran", "Serang Baru", "Setu", "Sukakarya", "Sukatani",
    "Sukawangi", "Tambelang", "Tambun Selatan", "Tambun Utara", "Tarumajaya"
]
for kec in kecamatan:
    add(f"Koordinator Wilayah Dinas Pendidikan Kecamatan {kec}",
        "korwil_dinas_pendidikan_kecamatan",
        kec, "", "",
        src_perbup_korwil,
        "Nama node dibuat berdasarkan struktur Korwil Dinas Pendidikan pada Kecamatan; alamat/koordinat kantor perlu divalidasi.")

# Perpustakaan publik
add("Perpustakaan Umum Kabupaten Bekasi - Cifest", "perpustakaan_umum", "Cikarang Selatan", "", "",
    src_perpus, "Disebut sebagai salah satu lokasi perpustakaan umum Kabupaten Bekasi; koordinat perlu divalidasi.")
add("Perpustakaan Umum Kabupaten Bekasi - Cikarang Utara", "perpustakaan_umum", "Cikarang Utara", "", "",
    src_perpus, "Disebut sebagai salah satu lokasi perpustakaan umum Kabupaten Bekasi; koordinat perlu divalidasi.")
add("Perpustakaan Umum Kabupaten Bekasi - Gedung Juang", "perpustakaan_umum", "Tambun Selatan", "", "",
    src_perpus, "Nama lokasi mengikuti informasi layanan perpustakaan daerah; koordinat perlu divalidasi.")

# Nonformal/pelatihan publik
add("Sanggar Kegiatan Belajar Kabupaten Bekasi", "skb_pendidikan_nonformal", "", "", "",
    src_dapodik, "SKB termasuk bentuk satuan pendidikan pada Dapodik; nama/alamat lokal perlu divalidasi.")
add("Balai Latihan Kerja Kabupaten Bekasi", "balai_latihan_kerja", "", "", "",
    src_ppid, "Koordinat dan alamat perlu divalidasi.")

# Kelompok sekolah negeri sebagai kandidat node terpisah perlu diisi dari Dapodik/referensi satuan pendidikan
add("Daftar Sekolah Dasar Negeri Kabupaten Bekasi", "placeholder_sd_negeri", "Kabupaten Bekasi", "", "",
    src_referensi, "Baris penanda: daftar sekolah negeri per satuan tersedia di Referensi Data Kemendikdasmen; perlu diekspor terpisah jika ingin semua SDN sebagai node.")
add("Daftar Sekolah Menengah Pertama Negeri Kabupaten Bekasi", "placeholder_smp_negeri", "Kabupaten Bekasi", "", "",
    src_dapodik, "Baris penanda: perlu diekspor terpisah dari Dapodik/Referensi Data jika semua SMPN dijadikan node.")
add("Daftar Sekolah Menengah Atas Negeri Kabupaten Bekasi", "placeholder_sma_negeri", "Kabupaten Bekasi", "", "",
    "https://referensi.data.kemendikdasmen.go.id/pendidikan/dikmen/022200/2/jf/13/s1",
    "Baris penanda: perlu diekspor terpisah dari Referensi Data Dikmen jika semua SMAN dijadikan node.")
add("Daftar Sekolah Menengah Kejuruan Negeri Kabupaten Bekasi", "placeholder_smk_negeri", "Kabupaten Bekasi", "", "",
    "https://referensi.data.kemendikdasmen.go.id/pendidikan/dikmen/022200/2/jf/15/s1",
    "Baris penanda: perlu diekspor terpisah dari Referensi Data Dikmen jika semua SMKN dijadikan node.")

fieldnames = [
    "node_id", "nama_node", "jenis_node", "sub_jenis", "kecamatan",
    "desa_kelurahan", "alamat", "latitude", "longitude", "sumber", "catatan_validasi"
]

with output_path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

output_path.as_posix(), len(rows)
