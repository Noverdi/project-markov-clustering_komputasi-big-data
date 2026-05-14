import pandas as pd
import googlemaps
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# --- 1. MEMBACA API KEY ---
def load_api_key(filepath='gmaps-api.json'):
    try:
        with open(filepath, 'r') as file:
            config = json.load(file)
            api_key = config.get("API_KEY")
            if not api_key:
                raise ValueError("Key 'API_KEY' tidak ditemukan.")
            return api_key
    except Exception as e:
        print(f"Error memuat API Key: {e}")
        exit(1)

# Inisialisasi Gmaps Client
gmaps = googlemaps.Client(key=load_api_key())

# --- 2. DAFTAR FILE ---
files = [
    # "02_node_layanan_kesehatan_kab_bekasi.csv",
    "data/03_node_layanan_keamanan_ketertiban_kab_bekasi.csv",
    "data/04_node_layanan_pendidikan_publik_kab_bekasi.csv",
    "data/05_node_layanan_sosial_masyarakat_kab_bekasi.csv",
    "data/06_node_layanan_transportasi_akses_publik_kab_bekasi.csv",
    "data/07_node_layanan_ekonomi_publik_kab_bekasi.csv"
]

def clean_name(text):
    """Pembersihan string agar pencarian lebih akurat"""
    if not isinstance(text, str): return ""
    fixes = {
        'Muara Gembong': 'Muaragembong',
        'Cabang Bungin': 'Cabangbungin',
        'Kedung Waringin': 'Kedungwaringin',
        'Bojong Mangu': 'Bojongmangu',
        'Karang Bahagia': 'Karangbahagia'
    }
    for old, new in fixes.items():
        text = text.replace(old, new)
    return text.strip()

# --- 3. FUNGSI WORKER (GMAPS) ---
def fetch_coords_gmaps(idx, nama_node, kecamatan, alamat):
    try:
        nama_node = clean_name(nama_node)
        kec = clean_name(kecamatan) if pd.notna(kecamatan) else ""
        
        # Susun query pencarian.
        # Menggunakan alamat jika tersedia (karena alamat sering kali lebih akurat)
        if pd.notna(alamat) and str(alamat).strip() != "":
            query = f"{nama_node}, {alamat}"
        else:
            query = f"{nama_node}, {kec}, Kabupaten Bekasi, Jawa Barat"
            
        # Panggil Google Maps Geocoding
        result = gmaps.geocode(query)
        
        if result:
            lat = result[0]['geometry']['location']['lat']
            lng = result[0]['geometry']['location']['lng']
            return idx, lat, lng
            
        # Jika percobaan pertama gagal, coba persempit pencarian tanpa alamat spesifik
        fallback_query = f"{nama_node}, Kabupaten Bekasi, Jawa Barat"
        result_fallback = gmaps.geocode(fallback_query)
        if result_fallback:
            lat = result_fallback[0]['geometry']['location']['lat']
            lng = result_fallback[0]['geometry']['location']['lng']
            return idx, lat, lng
            
        return idx, None, None
        
    except Exception as e:
        print(f"Error di Index {idx}: {e}")
        return idx, None, None

# --- 4. PROSES UTAMA (MULTI-THREADING) ---
def process_file_gmaps(filename):
    if not os.path.exists(filename):
        print(f"\n[SKIP] File {filename} tidak ditemukan.")
        return

    print(f"\n==========================================")
    print(f"🚀 Memproses: {filename}")
    df = pd.read_csv(filename)
    
    # Filter baris yang latitude-nya kosong
    missing_mask = df['latitude'].isna() | df['longitude'].isna()
    to_process = df[missing_mask]

    if to_process.empty:
        print(f"Semua koordinat sudah terisi. Melewati file ini.")
        return
        
    print(f"Ditemukan {len(to_process)} node tanpa koordinat. Mulai Geocoding...")
    
    # Eksekusi dengan 15 Threads (Gmaps kuat menahan beban ini)
    MAX_WORKERS = 15
    results = []
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Peta future ke indeks dataframe
        futures = {
            executor.submit(
                fetch_coords_gmaps, 
                idx, 
                row['nama_node'], 
                row.get('kecamatan'), 
                row.get('alamat')
            ): idx for idx, row in to_process.iterrows()
        }
        
        for future in as_completed(futures):
            idx, lat, lon = future.result()
            if lat:
                df.at[idx, 'latitude'] = lat
                df.at[idx, 'longitude'] = lon
                print(f"[OK] {df.at[idx, 'nama_node']} -> {lat}, {lon}")
            else:
                print(f"[FAIL] Titik tidak ditemukan untuk: {df.at[idx, 'nama_node']}")

    # Simpan hasil
    output_name = filename.replace(".csv", "_gmaps.csv")
    df.to_csv(output_name, index=False)
    print(f"✅ Selesai! Data disimpan di '{output_name}'")

# --- 5. JALANKAN UNTUK SEMUA FILE ---
for f in files:
    process_file_gmaps(f)