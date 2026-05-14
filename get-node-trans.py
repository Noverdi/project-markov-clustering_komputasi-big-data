import csv
from pathlib import Path

output_path = Path("/mnt/data/node_layanan_transportasi_akses_publik_kab_bekasi.csv")

rows = []

def add(nama, sub_jenis, kecamatan="", desa_kelurahan="", alamat="", sumber="", catatan=""):
    rows.append({
        "node_id": f"TRN_{len(rows)+1:03d}",
        "nama_node": nama,
        "jenis_node": "layanan_transportasi_akses_publik",
        "sub_jenis": sub_jenis,
        "kecamatan": kecamatan,
        "desa_kelurahan": desa_kelurahan,
        "alamat": alamat,
        "latitude": "",
        "longitude": "",
        "sumber": sumber,
        "catatan_validasi": catatan
    })

src_dishub_ppid = "https://ppid.bekasikab.go.id/ppidpelaksana/"
src_mpp = "https://mpp.bekasikab.go.id/tenant"
src_terminal_cikarang = "https://ppid.jabarprov.go.id/public/assets/downloads/cikarang/9_GAMBAR%20PEMBANGUNAN%20TERMINAL%20CKR%20TH2%2002052024%20%281%29%20%281%29%20full.pdf"
src_terminal_info = "https://www.antarafoto.com/id/view/1069668/penataan-terminal-bus-tipe-b-cikarang"
src_bpljskb = "https://hubdat.dephub.go.id/id/bptd/bpljskb/profil/"
src_bpljskb_addr = "https://simaspetik.com/tentangKami"
src_stasiun_cikarang = "https://168railway.com/jadwal-stasiun/cikarang"
src_stasiun_tambun = "https://keretaapikita.com/jadwal-kereta-api-stasiun-tambun/"
src_twm = "https://www.traveloka.com/id-id/explore/destination/bus-trans-wibawa-mukti-rute-jadwal-jam-operasional-harga-tiket-trp/491609"
src_tol_japek = "https://auto2000.co.id/berita-dan-tips/exit-tol-cikarang-barat"
src_tol_cibatu = "https://astraotoshop.com/article/gerbang-tol-cibatu"
src_gt_gabus = "https://www.facebook.com/Jokowi/posts/dari-gerbang-tol-gabus-kabupaten-bekasi-pagi-ini-saya-meresmikan-dua-ruas-jalan-/649342476547850/"
src_osm = "https://www.openstreetmap.org/"

# Instansi/layanan transportasi pemerintahan
add("Dinas Perhubungan Kabupaten Bekasi", "dinas_perhubungan", "Cikarang Pusat", "", "",
    src_dishub_ppid, "Koordinat dan alamat perlu divalidasi.")
add("Layanan Dinas Perhubungan Kabupaten Bekasi di MPP", "layanan_dishub_mpp", "Cikarang Pusat", "", "",
    src_mpp, "Jika dipakai sebagai node, validasi apakah layanan Dishub aktif sebagai tenant MPP.")
add("UPTD Pengujian Kendaraan Bermotor Kabupaten Bekasi", "pengujian_kendaraan_bermotor", "Cikarang", "", "Jl. Raya Industri, Kabupaten Bekasi",
    "https://mediarjn.com/2025/11/20/uji-kir-dishub-bekasi-optimalisasi-layanan-upt-pkb-cikarang/",
    "Alamat umum dari pemberitaan layanan uji KIR; koordinat perlu divalidasi.")
add("Balai Pengujian Laik Jalan dan Sertifikasi Kendaraan Bermotor Bekasi", "balai_pengujian_kendaraan", "Cibitung", "Cibuntu", "Jalan Raya Setu, Cibuntu, Cibitung, Kabupaten Bekasi",
    src_bpljskb_addr, "Instansi Kemenhub; alamat dari laman informasi BPLJSKB/SIMASPETIK, koordinat perlu divalidasi.")

# Terminal
add("Terminal Cikarang / Terminal Kalijaya", "terminal_bus_tipe_b", "Cikarang Barat", "Kalijaya", "Jl. Fatahillah No.1, Cikarang Barat, Kabupaten Bekasi",
    src_terminal_cikarang, "Terminal tipe B utama; koordinat perlu divalidasi.")
add("Sub Terminal Sukatani", "terminal_lokal", "Sukatani", "", "",
    src_osm, "Node kandidat terminal/angkutan lokal; validasi nama resmi dan koordinat.")
add("Sub Terminal Pebayuran", "terminal_lokal", "Pebayuran", "", "",
    src_osm, "Node kandidat terminal/angkutan lokal; validasi nama resmi dan koordinat.")
add("Sub Terminal Cibarusah", "terminal_lokal", "Cibarusah", "", "",
    src_osm, "Node kandidat terminal/angkutan lokal; validasi nama resmi dan koordinat.")
add("Sub Terminal Babelan", "terminal_lokal", "Babelan", "", "",
    src_osm, "Node kandidat terminal/angkutan lokal; validasi nama resmi dan koordinat.")
add("Sub Terminal Tambun", "terminal_lokal", "Tambun Selatan", "", "",
    src_osm, "Node kandidat terminal/angkutan lokal; validasi nama resmi dan koordinat.")

# Stasiun kereta
stations = [
    ("Stasiun Tambun", "stasiun_kereta", "Tambun Selatan", "Mekarsari", "Jalan Mekarsari, Tambun Selatan, Kabupaten Bekasi", src_stasiun_tambun),
    ("Stasiun Cibitung", "stasiun_kereta", "Cibitung", "", "", src_stasiun_cikarang),
    ("Stasiun Metland Telaga Murni", "stasiun_kereta", "Cikarang Barat", "Telaga Murni", "", src_stasiun_cikarang),
    ("Stasiun Cikarang", "stasiun_kereta", "Cikarang Utara", "", "", src_stasiun_cikarang),
    ("Stasiun Lemahabang", "stasiun_kereta", "Cikarang Timur", "", "", src_stasiun_cikarang),
    ("Stasiun Kedunggedeh", "stasiun_kereta", "Kedungwaringin", "", "", src_stasiun_cikarang),
]
for nama, sub, kec, desa, alamat, sumber in stations:
    add(nama, sub, kec, desa, alamat, sumber, "Koordinat perlu divalidasi dari Google Maps/OSM.")

# Titik layanan Biskita/Trans Wibawa Mukti
biskita_points = [
    ("Halte/Titik Layanan Biskita Trans Wibawa Mukti - Stasiun Cikarang", "halte_bus_publik", "Cikarang Utara", "", ""),
    ("Halte/Titik Layanan Biskita Trans Wibawa Mukti - SGC Cikarang", "halte_bus_publik", "Cikarang Utara", "", ""),
    ("Halte/Titik Layanan Biskita Trans Wibawa Mukti - Jababeka", "halte_bus_publik", "Cikarang Utara", "", ""),
    ("Halte/Titik Layanan Biskita Trans Wibawa Mukti - Lippo Cikarang", "halte_bus_publik", "Cikarang Selatan", "", ""),
    ("Halte/Titik Layanan Biskita Trans Wibawa Mukti - Cibitung", "halte_bus_publik", "Cibitung", "", ""),
    ("Halte/Titik Layanan Biskita Trans Wibawa Mukti - Tambun", "halte_bus_publik", "Tambun Selatan", "", ""),
]
for nama, sub, kec, desa, alamat in biskita_points:
    add(nama, sub, kec, desa, alamat, src_twm, "Nama titik masih kandidat berbasis koridor/rute; titik halte resmi perlu divalidasi.")

# Gerbang tol / akses jalan utama
toll_gates = [
    ("Gerbang Tol Tambun", "gerbang_tol", "Tambun Selatan", "", "", src_tol_japek),
    ("Gerbang Tol Cibitung", "gerbang_tol", "Cibitung", "", "", src_tol_japek),
    ("Gerbang Tol Cikarang Barat", "gerbang_tol", "Cikarang Barat", "", "", src_tol_japek),
    ("Gerbang Tol Cibatu", "gerbang_tol", "Cikarang Selatan", "Cibatu", "", src_tol_cibatu),
    ("Gerbang Tol Cikarang Timur", "gerbang_tol", "Cikarang Timur", "", "", src_tol_japek),
    ("Gerbang Tol Cikarang Pusat", "gerbang_tol", "Cikarang Pusat", "", "", src_osm),
    ("Gerbang Tol Gabus", "gerbang_tol", "Tambun Utara", "", "", src_gt_gabus),
    ("Gerbang Tol Tarumajaya", "gerbang_tol", "Tarumajaya", "", "", src_osm),
    ("Gerbang Tol Setu", "gerbang_tol", "Setu", "", "", src_osm),
    ("Gerbang Tol Cibitung-Cilincing", "gerbang_tol", "Cibitung", "", "", src_gt_gabus),
]
for nama, sub, kec, desa, alamat, sumber in toll_gates:
    add(nama, sub, kec, desa, alamat, sumber, "Koordinat perlu divalidasi dari Google Maps/OSM; pastikan masih aktif/beroperasi.")

# Titik akses publik lain
add("Kawasan Park and Ride Stasiun Cikarang", "park_and_ride", "Cikarang Utara", "", "",
    src_stasiun_cikarang, "Node kandidat akses publik; validasi ketersediaan fasilitas dan koordinat.")
add("Kawasan Park and Ride Stasiun Tambun", "park_and_ride", "Tambun Selatan", "Mekarsari", "",
    src_stasiun_tambun, "Node kandidat akses publik; validasi ketersediaan fasilitas dan koordinat.")
add("Kawasan Park and Ride Stasiun Cibitung", "park_and_ride", "Cibitung", "", "",
    src_stasiun_cikarang, "Node kandidat akses publik; validasi ketersediaan fasilitas dan koordinat.")
add("Kawasan Park and Ride Stasiun Metland Telaga Murni", "park_and_ride", "Cikarang Barat", "Telaga Murni", "",
    src_stasiun_cikarang, "Node kandidat akses publik; validasi ketersediaan fasilitas dan koordinat.")

fieldnames = [
    "node_id", "nama_node", "jenis_node", "sub_jenis", "kecamatan",
    "desa_kelurahan", "alamat", "latitude", "longitude", "sumber", "catatan_validasi"
]

with output_path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

output_path.as_posix(), len(rows)
