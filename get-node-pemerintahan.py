import csv, os, textwrap, json, pandas as pd
source = "https://bekasikab.go.id/profile/; https://web.pa-cikarang.go.id/wilayah-yuridiksi/; https://peraturan.bpk.go.id/Details/297773/perda-kab-bekasi-no-1-tahun-2022"

data = {
"Babelan": {"desa":["Babelan Kota","Bunibakti","Huripjaya","Kedungjaya","Kedungpengawas","Muarabakti","Pantai Hurip"], "kelurahan":["Bahagia","Kebalen"]},
"Bojongmangu": {"desa":["Bojongmangu","Karangindah","Karangmulya","Medalkrisna","Sukabungah","Sukamukti"], "kelurahan":[]},
"Cabangbungin": {"desa":["Jayabakti","Jayalaksana","Lenggahjaya","Lenggahsari","Setiajaya","Setialaksana","Sindangjaya","Sindangsari"], "kelurahan":[]},
"Cibarusah": {"desa":["Cibarusahjaya","Cibarusahkota","Ridogalih","Ridomanah","Sindangmulya","Sirnajati","Wibawamulya"], "kelurahan":[]},
"Cibitung": {"desa":["Cibuntu","Kertamukti","Muktiwari","Sarimukti","Sukajaya","Wanajaya"], "kelurahan":["Wanasari"]},
"Cikarang Barat": {"desa":["Cikedokan","Danauindah","Gandamekar","Gandasari","Jatiwangi","Kalijaya","Mekarwangi","Sukadanau","Telagamurni","Telajung"], "kelurahan":["Telaga Asih"]},
"Cikarang Pusat": {"desa":["Cicau","Hegarmukti","Jayamukti","Pasirranji","Pasirtanjung","Sukamahi"], "kelurahan":[]},
"Cikarang Selatan": {"desa":["Ciantra","Cibatu","Pasirsari","Sukadami","Sukaresmi","Sukasejati","Serang"], "kelurahan":[]},
"Cikarang Timur": {"desa":["Cipayung","Hegarmanah","Jatibaru","Jatireja","Karangsari","Labansari","Tanjungbaru"], "kelurahan":["Sertajaya"]},
"Cikarang Utara": {"desa":["Cikarang Kota","Harjamekar","Karangasih","Karangbaru","Karangraharja","Mekarmukti","Pasirgombong","Simpangan","Tanjungsari","Waluya","Wangunharja"], "kelurahan":[]},
"Karangbahagia": {"desa":["Karanganyar","Karangbahagia","Karangmukti","Karangrahayu","Karangsatu","Karangsentosa","Karangsetia","Sukaraya"], "kelurahan":[]},
"Kedungwaringin": {"desa":["Bojongsari","Karangharum","Karangmekar","Karangsambung","Kedungwaringin","Mekarjaya","Waringinjaya"], "kelurahan":[]},
"Muara Gembong": {"desa":["Jayasakti","Pantai Bahagia","Pantai Bakti","Pantai Harapanjaya","Pantai Mekar","Pantai Sederhana"], "kelurahan":[]},
"Pebayuran": {"desa":["Bantarjaya","Bantarsari","Karangharja","Karanghaur","Karangjaya","Karangreja","Karangpatri","Karangsegar","Kertajaya","Sumbereja","Sumbersari","Sumberurip"], "kelurahan":["Kertasari"]},
"Serang Baru": {"desa":["Cilangkara","Jayamulya","Jayasampurna","Nagacipta","Nagasari","Sirnajaya","Sukaragam","Sukasari"], "kelurahan":[]},
"Setu": {"desa":["Burangkeng","Cibening","Cijengkol","Cikarageman","Ciledug","Kertarahayu","Lubangbuaya","Muktijaya","Ragamanunggal","Taman Rahayu","Taman Sari"], "kelurahan":[]},
"Sukakarya": {"desa":["Sukaindah","Sukajadi","Sukakarsa","Sukakarya","Sukalaksana","Sukamakmur","Sukamurni"], "kelurahan":[]},
"Sukatani": {"desa":["Banjarsari","Sukaasih","Sukadarma","Sukahurip","Sukamanah","Sukamulya","Sukarukun"], "kelurahan":[]},
"Sukawangi": {"desa":["Sukabudi","Sukadaya","Sukakerta","Sukamekar","Sukaringin","Sukatenang","Sukawangi"], "kelurahan":[]},
"Tambelang": {"desa":["Sukabakti","Sukamaju","Sukamantri","Sukarahayu","Sukaraja","Sukarapih","Sukawijaya"], "kelurahan":[]},
"Tambun Selatan": {"desa":["Tridaya Sakti","Lambangjaya","Lambangsari","Mangunjaya","Mekarsari","Setiadarma","Setiamekar","Sumberjaya","Tambun"], "kelurahan":["Jatimulya"]},
"Tambun Utara": {"desa":["Jejalenjaya","Karangsatria","Satriajaya","Satriamekar","Sriamur","Srijaya","Srimahi","Srimukti"], "kelurahan":[]},
"Tarumajaya": {"desa":["Pahlawan Setia","Pantai Makmur","Pusaka Rakyat","Samudra Jaya","Sagara Makmur","Segarajaya","Setia Mulya"], "kelurahan":["Setia Asih"]},
}
rows=[]
node_id=1
for kec, vals in data.items():
    rows.append({
        "node_id": node_id,
        "nama_kantor": f"Kantor Kecamatan {kec}",
        "jenis_node": "kecamatan",
        "kecamatan": kec,
        "desa_kelurahan": "",
        "status_wilayah": "kecamatan",
        "latitude": "",
        "longitude": "",
        "alamat": "",
        "catatan": "Koordinat perlu diisi/dicek dari Google Maps, OSM, atau sumber resmi.",
        "sumber": source
    })
    node_id+=1
    for d in vals["desa"]:
        rows.append({
            "node_id": node_id,
            "nama_kantor": f"Kantor Desa {d}",
            "jenis_node": "desa",
            "kecamatan": kec,
            "desa_kelurahan": d,
            "status_wilayah": "desa",
            "latitude": "",
            "longitude": "",
            "alamat": "",
            "catatan": "Koordinat perlu diisi/dicek dari Google Maps, OSM, atau sumber resmi.",
            "sumber": source
        })
        node_id+=1
    for k in vals["kelurahan"]:
        rows.append({
            "node_id": node_id,
            "nama_kantor": f"Kantor Kelurahan {k}",
            "jenis_node": "kelurahan",
            "kecamatan": kec,
            "desa_kelurahan": k,
            "status_wilayah": "kelurahan",
            "latitude": "",
            "longitude": "",
            "alamat": "",
            "catatan": "Koordinat perlu diisi/dicek dari Google Maps, OSM, atau sumber resmi.",
            "sumber": source
        })
        node_id+=1
len(rows), sum(1 for r in rows if r["jenis_node"]=="kecamatan"), sum(1 for r in rows if r["jenis_node"]=="desa"), sum(1 for r in rows if r["jenis_node"]=="kelurahan")
