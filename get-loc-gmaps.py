import pandas as pd
import googlemaps
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

# --- 1. MEMBACA API KEY DARI FILE JSON ---
def load_api_key(filepath='gmaps-api.json'):
    try:
        with open(filepath, 'r') as file:
            config = json.load(file)
            # Mengambil nilai berdasarkan key di dalam JSON
            api_key = config.get("API_KEY")
            if not api_key:
                raise ValueError("Key 'API_KEY' tidak ditemukan dalam file JSON.")
            return api_key
    except FileNotFoundError:
        print(f"Error: File '{filepath}' tidak ditemukan.")
        exit(1)
    except json.JSONDecodeError:
        print(f"Error: Format file '{filepath}' bukan JSON yang valid.")
        exit(1)

# Inisialisasi API Key dari JSON
API_KEY = load_api_key()
# Inisialisasi Google Maps Client
gmaps = googlemaps.Client(key=API_KEY)

# --- 2. LOAD DATA ---
file_path = 'data/01_node_kantor_pemerintahan_kab_bekasi-rev.csv'
try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    print(f"Error: File '{file_path}' tidak ditemukan.")
    exit(1)

# --- 3. FUNGSI WORKER GEOCODING ---
def fetch_coords_gmaps(index, name, kecamatan):
    """Fungsi worker untuk mengambil koordinat via Google Maps"""
    try:
        # Konteks spesifik untuk Bekasi
        query = f"{name}, {kecamatan}, Kabupaten Bekasi, Jawa Barat"
        
        # Request ke Google Maps API
        geocode_result = gmaps.geocode(query)
        
        if geocode_result:
            lat = geocode_result[0]['geometry']['location']['lat']
            lng = geocode_result[0]['geometry']['location']['lng']
            return index, lat, lng
        return index, None, None
    except Exception as e:
        print(f"Error pada Index {index} ({name}): {e}")
        return index, None, None

# --- 4. EKSEKUSI MULTI-THREADING ---
# Filter baris yang latitude-nya masih kosong
missing_df = df[df['latitude'].isna()]
results = []


def main():
    print(f"Memulai Google Maps Geocoding untuk {len(missing_df)} lokasi...")

    # Anda bisa menaikkan MAX_WORKERS karena Google Maps API tahan beban tinggi
    MAX_WORKERS = 15

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Memetakan fungsi worker ke data
        futures = {executor.submit(fetch_coords_gmaps, idx, row['nama_kantor'], row['kecamatan']): idx 
                for idx, row in missing_df.iterrows()}
        
        # Menangkap hasil
        for future in as_completed(futures):
            res = future.result()
            results.append(res)
            idx, lat, lon = res
            if lat:
                print(f"[OK] {df.at[idx, 'nama_kantor']} -> Lat: {lat}, Lon: {lon}")
            else:
                print(f"[GAGAL] Koordinat tidak ditemukan untuk: {df.at[idx, 'nama_kantor']}")

    # --- 5. UPDATE DAN SIMPAN ---
    for idx, lat, lon in results:
        if lat:
            df.at[idx, 'latitude'] = lat
            df.at[idx, 'longitude'] = lon

    output_file = 'data/node_kantor_pemerintahan_kab_bekasi_gmaps.csv'
    df.to_csv(output_file, index=False)
    print(f"\nProses selesai! Data tersimpan di '{output_file}'")


if __name__=='__main__':
    main()