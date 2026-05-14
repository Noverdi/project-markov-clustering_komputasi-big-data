import re, pathlib, csv, unicodedata
raw=pathlib.Path('/mnt/data/health_raw.txt').read_text(errors='ignore').replace('\x0c','\n')
lines=raw.splitlines()
clean=[]
for l in lines:
    s=l.strip()
    if not s: continue
    if re.fullmatch(r'\d{1,3}',s):
        continue
    clean.append(s)

def infer_subjenis(name):
    n=name.upper()
    if n.startswith('RSIA') or 'RSIA' in n:
        return 'rumah_sakit_ibu_anak'
    if n.startswith('RS ') or n.startswith('RSU') or n.startswith('RSUD') or n.startswith('RUMAH SAKIT') or 'HOSPITAL' in n or n.startswith('SILOAM') or n.startswith('EKA HOSPITAL'):
        return 'rumah_sakit'
    if 'PUSKESMAS PEMBANTU' in n or 'PUSTU' in n:
        return 'puskesmas_pembantu'
    if 'PUSKESMAS' in n:
        return 'puskesmas'
    if 'KLINIK' in n or 'CLINIC' in n or 'MEDIKA' in n or 'HUSADA' in n or 'NAYAKA' in n or 'MITRASANA' in n or 'YAMET' in n or 'PRAKTEK' in n:
        return 'klinik'
    if 'APOTEK' in n or 'FARMA' in n or 'MEGAFARMA' in n:
        return 'apotek'
    if 'LAB' in n:
        return 'laboratorium_kesehatan'
    if 'BIDAN' in n:
        return 'bidan_praktik'
    return 'layanan_kesehatan'

records=[]; i=0; expected=1
while i < len(clean):
    m=re.match(rf'^{expected}\s+(.+)$', clean[i])
    if m and not re.match(r'^[0-9.\-]+\s+[0-9.\-]+$', m.group(1)):
        no=expected; name=m.group(1).strip(); expected += 1; i += 1
        block=[]
        while i < len(clean):
            nm=re.match(rf'^{expected}\s+(.+)$', clean[i]) if expected<=420 else None
            if nm and not re.match(r'^[0-9.\-]+\s+[0-9.\-]+$', nm.group(1)):
                break
            block.append(clean[i]); i += 1
        text='\n'.join(block)
        cm=re.search(r'Koordinat\s*:\s*\n?\s*([0-9.\-]+)\s+([0-9.\-]+)', text)
        kec=''
        for j,b in enumerate(block):
            if b == 'Pelayanan Kesehatan' and j>0:
                kec=' '.join(block[j-1].split()).title()
                break
        addr=[]
        for b in block:
            if b.upper()==kec.upper() or b=='Pelayanan Kesehatan' or b.startswith('Koordinat') or re.match(r'^[0-9.\-]+\s+[0-9.\-]+$',b): break
            if b!='Photo': addr.append(b)
        lon=lat=''
        if cm:
            lon=cm.group(1); lat=cm.group(2)
        records.append({
            'node_id': f'KES_{no:03d}',
            'nama_node': name,
            'jenis_node': 'layanan_kesehatan',
            'sub_jenis': infer_subjenis(name),
            'kecamatan': kec,
            'desa_kelurahan': '',
            'alamat': ' '.join(addr),
            'latitude': lat,
            'longitude': lon,
            'sumber': 'Satu Peta Kabupaten Bekasi - Data Spasial Sektoral Kesehatan'
        })
    else:
        i += 1

out='/mnt/data/node_layanan_kesehatan_kab_bekasi.csv'
with open(out,'w',newline='',encoding='utf-8') as f:
    writer=csv.DictWriter(f,fieldnames=['node_id','nama_node','jenis_node','sub_jenis','kecamatan','desa_kelurahan','alamat','latitude','longitude','sumber'])
    writer.writeheader(); writer.writerows(records)
print(out)
print(len(records))
from collections import Counter
print(Counter(r['sub_jenis'] for r in records))
print(records[:3])