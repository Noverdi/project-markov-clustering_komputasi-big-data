import pandas as pd
from geopy.geocoders import Nominatim
import time

# Load file
# df = pd.read_csv('node_kantor_pemerintahan_kab_bekasi.csv')
df = pd.read_csv('node_kantor_pemerintahan_kab_bekasi-rev.csv')
geolocator = Nominatim(user_agent="bekasi_geocoder")

def get_coords(name):
    try:
        # Menambahkan konteks wilayah agar lebih akurat
        query = f"{name}, Kabupaten Bekasi, Jawa Barat"
        location = geolocator.geocode(query)
        if location:
            return location.latitude, location.longitude
        return None, None
    except:
        return None, None

# Melakukan iterasi (disarankan pakai sleep agar tidak diblokir API OSM)
for index, row in df.iterrows():
    if pd.isna(row['latitude']):
        lat, lon = get_coords(row['nama_kantor'])
        df.at[index, 'latitude'] = lat
        df.at[index, 'longitude'] = lon
        print(f"Selesai: {row['nama_kantor']} -> {lat}, {lon}")
        time.sleep(1) # Delay 1 detik per request sesuai aturan OSM

# Simpan hasil
df.to_csv('node_kantor_pemerintahan_kab_bekasi_updated-rev.csv', index=False)