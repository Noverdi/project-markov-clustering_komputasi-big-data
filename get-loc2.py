import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import os

# Daftar file yang akan diproses
files = [
    "02_node_layanan_kesehatan_kab_bekasi.csv",
    "03_node_layanan_keamanan_ketertiban_kab_bekasi.csv",
    "04_node_layanan_pendidikan_publik_kab_bekasi.csv",
    "05_node_layanan_sosial_masyarakat_kab_bekasi.csv",
    "06_node_layanan_transportasi_akses_publik_kab_bekasi.csv",
    "07_node_layanan_ekonomi_publik_kab_bekasi.csv"
]

# Inisialisasi Nominatim
geolocator = Nominatim(user_agent="ui_graduate_research_bekasi")


def clean_name(text):
    """Membersihkan ejaan khas Bekasi agar sesuai standar OSM"""
    if not isinstance(text, str): return text
    fixes = {
        'Muara Gembong': 'Muaragembong',
        'Cabang Bungin': 'Cabangbungin',
        'Kedung Waringin': 'Kedungwaringin',
        'Bojong Mangu': 'Bojongmangu',
        'Karang Bahagia': 'Karangbahagia'
    }
    for old, new in fixes.items():
        text = text.replace(old, new)
    return text


def get_coords_osm(name, kecamatan):
    """Fungsi worker untuk mencari koordinat"""
    try:
        # Menambahkan konteks wilayah agar hasil lebih presisi
        query = f"{name}, {kecamatan}, Kabupaten Bekasi, Jawa Barat"
        location = geolocator.geocode(query, timeout=10)
        if location:
            return location.latitude, location.longitude
        return None, None
    except:
        return None, None


def process_file(filename):
    if not os.path.exists(filename):
        print(f"File {filename} tidak ditemukan.")
        return

    print(f"\n--- Memproses: {filename} ---")
    df = pd.read_csv(filename)
    
    # 1. Pembersihan Nama
    df['nama_node'] = df['nama_node'].apply(clean_name)
    if 'kecamatan' in df.columns:
        df['kecamatan'] = df['kecamatan'].apply(clean_name)

    # 2. Filter baris yang koordinatnya kosong
    missing_mask = df['latitude'].isna() | df['longitude'].isna()
    to_process = df[missing_mask]

    if to_process.empty:
        print(f"Semua koordinat di {filename} sudah terisi.")
        return

    # 3. Eksekusi Multi-threading (max_workers=1 untuk mematuhi aturan OSM)
    # Meskipun multi-threading, kita gunakan delay agar tidak diblokir
    results = []
    with ThreadPoolExecutor(max_workers=1) as executor:
        future_to_idx = {
            executor.submit(get_coords_osm, row['nama_node'], row['kecamatan']): idx 
            for idx, row in to_process.iterrows()
        }
        
        for future in as_completed(future_to_idx):
            idx = future_to_idx[future]
            lat, lon = future.result()
            df.at[idx, 'latitude'] = lat
            df.at[idx, 'longitude'] = lon
            
            status = f"✅ {lat}, {lon}" if lat else "❌ Tidak ditemukan"
            print(f"Index {idx}: {df.at[idx, 'nama_node']} -> {status}")
            time.sleep(1) # Delay wajib 1 detik per request (Aturan OSM)

    # Simpan hasil
    output_name = filename.replace(".csv", "_updated.csv")
    df.to_csv(output_name, index=False)
    print(f"Selesai! Hasil disimpan di {output_name}")


def main():
    # Jalankan untuk semua file
    for f in files:
        filename = f'data/{f}'
        process_file(filename=filename)


if __name__=='__main__':
    main()