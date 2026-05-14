import csv
from pathlib import Path

output_path = Path("/mnt/data/node_layanan_sosial_masyarakat_kab_bekasi.csv")

rows = []

def add(nama, sub_jenis, kecamatan="", desa_kelurahan="", alamat="", sumber="", catatan=""):
    rows.append({
        "node_id": f"SOC_{len(rows)+1:03d}",
        "nama_node": nama,
        "jenis_node": "layanan_sosial_masyarakat",
        "sub_jenis": sub_jenis,
        "kecamatan": kecamatan,
        "desa_kelurahan": desa_kelurahan,
        "alamat": alamat,
        "latitude": "",
        "longitude": "",
        "sumber": sumber,
        "catatan_validasi": catatan
    })

src_mpp_tenant = "https://mpp.bekasikab.go.id/tenant"
src_dinsos_mpp = "https://mpp.bekasikab.go.id/detail-tenant?id=85"
src_kemenag_alamat = "https://jabar.kemenag.go.id/alamat-satker"
src_kemenag_kab = "https://jabar.kemenag.go.id/profil/profil-kantor-kementerian-agama-kabupaten-bekasi"
src_pmi = "https://www.bekasikab.go.id/pmi-kabupaten-bekasi-siapkan-posko-siaga-mudik-dan-arus-balik-lebaran"
src_pos = "https://www.posindonesia.co.id/id/kantorPosTerdekat"
src_bpjs_kes = "https://bpjs-kesehatan.go.id/"
src_bpjs_tk = "https://www.bpjsketenagakerjaan.go.id/"
src_ppid = "https://ppid.bekasikab.go.id/ppidpelaksana/"

# Layanan sosial utama dan tenant layanan masyarakat
add("Dinas Sosial Kabupaten Bekasi", "dinas_sosial", "Cikarang Pusat", "", "", src_dinsos_mpp,
    "Terdaftar sebagai tenant MPP Kabupaten Bekasi; alamat/koordinat kantor perlu divalidasi.")
add("Mal Pelayanan Publik Kabupaten Bekasi", "mal_pelayanan_publik", "Cikarang Pusat", "", "", src_mpp_tenant,
    "Node pusat layanan masyarakat terpadu; koordinat perlu divalidasi.")
add("Kementerian Agama Kabupaten Bekasi", "kantor_kementerian_agama", "Cikarang Pusat", "", "Komplek Pemda Blok E.3 Cikarang Pusat, Kabupaten Bekasi", src_kemenag_alamat,
    "Alamat dari daftar satker Kemenag Jabar; koordinat perlu divalidasi.")
add("Palang Merah Indonesia Kabupaten Bekasi", "pmi", "", "", "", src_pmi,
    "Markas/posko PMI Kabupaten Bekasi disebut sebagai pusat pelayanan; alamat/koordinat perlu divalidasi.")
add("BPJS Kesehatan Kabupaten Bekasi / KC Cikarang", "bpjs_kesehatan", "Cikarang", "", "", src_bpjs_kes,
    "Nama kantor dan titik perlu divalidasi dari kanal resmi/Google Maps.")
add("BPJS Ketenagakerjaan Kabupaten Bekasi / KC Cikarang", "bpjs_ketenagakerjaan", "Cikarang", "", "", src_bpjs_tk,
    "Nama kantor dan titik perlu divalidasi dari kanal resmi/Google Maps.")
add("PT TASPEN (Persero) KC Bekasi - layanan MPP Kabupaten Bekasi", "taspen", "Cikarang Pusat", "", "", src_mpp_tenant,
    "Terdaftar sebagai tenant MPP Kabupaten Bekasi; titik layanan perlu divalidasi.")
add("Kantor Pos Indonesia Cabang Cikarang", "kantor_pos", "Cikarang", "", "", src_pos,
    "Nama/titik kantor pos perlu divalidasi melalui pencarian kantor pos resmi Pos Indonesia.")
add("Kantor Pos Indonesia Cabang Tambun", "kantor_pos", "Tambun Selatan", "", "", src_pos,
    "Nama/titik kantor pos perlu divalidasi melalui pencarian kantor pos resmi Pos Indonesia.")
add("Kantor Pos Indonesia Cabang Babelan", "kantor_pos", "Babelan", "", "", src_pos,
    "Nama/titik kantor pos perlu divalidasi melalui pencarian kantor pos resmi Pos Indonesia.")
add("Kantor Pos Indonesia Cabang Cibitung", "kantor_pos", "Cibitung", "", "", src_pos,
    "Nama/titik kantor pos perlu divalidasi melalui pencarian kantor pos resmi Pos Indonesia.")
add("Kantor Pos Indonesia Cabang Cibarusah", "kantor_pos", "Cibarusah", "", "", src_pos,
    "Nama/titik kantor pos perlu divalidasi melalui pencarian kantor pos resmi Pos Indonesia.")
add("Kantor Pos Indonesia Cabang Sukatani", "kantor_pos", "Sukatani", "", "", src_pos,
    "Nama/titik kantor pos perlu divalidasi melalui pencarian kantor pos resmi Pos Indonesia.")
add("Kantor Pos Indonesia Cabang Pebayuran", "kantor_pos", "Pebayuran", "", "", src_pos,
    "Nama/titik kantor pos perlu divalidasi melalui pencarian kantor pos resmi Pos Indonesia.")

# KUA per kecamatan
kecamatan = [
    "Babelan", "Bojongmangu", "Cabangbungin", "Cibarusah", "Cibitung",
    "Cikarang Barat", "Cikarang Pusat", "Cikarang Selatan", "Cikarang Timur",
    "Cikarang Utara", "Karangbahagia", "Kedungwaringin", "Muara Gembong",
    "Pebayuran", "Serang Baru", "Setu", "Sukakarya", "Sukatani",
    "Sukawangi", "Tambelang", "Tambun Selatan", "Tambun Utara", "Tarumajaya"
]
for kec in kecamatan:
    add(f"Kantor Urusan Agama Kecamatan {kec}", "kua", kec, "", "", src_kemenag_kab,
        "Nama node dibuat berdasarkan layanan KUA tingkat kecamatan; alamat/koordinat perlu divalidasi.")

# Layanan sosial/komunitas tingkat kecamatan sebagai node kontekstual yang dapat diisi jika tersedia
for kec in kecamatan:
    add(f"Pusat Kesejahteraan Sosial Kecamatan {kec}", "pusat_kesejahteraan_sosial_kecamatan", kec, "", "", src_ppid,
        "Node kandidat layanan sosial tingkat kecamatan; nama/titik aktual perlu divalidasi sebelum dipakai sebagai node final.")

fieldnames = [
    "node_id", "nama_node", "jenis_node", "sub_jenis", "kecamatan",
    "desa_kelurahan", "alamat", "latitude", "longitude", "sumber", "catatan_validasi"
]

with output_path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

output_path.as_posix(), len(rows)
