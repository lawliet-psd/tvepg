import requests
import re
import xml.etree.ElementTree as ET

M3U_URL = "https://raw.githubusercontent.com/atakan1983/kabloo/main/mehmet.m3u"
EPG_URL = "https://raw.githubusercontent.com/atakan1983/iptvepg/main/epg.xml"
OUTPUT_FILE = "m3u-epg.m3u"

def fetch_m3u():
    r = requests.get(M3U_URL)
    return r.text if r.status_code == 200 else None

def fetch_epg_ids():
    r = requests.get(EPG_URL)
    if r.status_code != 200:
        return {}
    epg_ids = {}
    root = ET.fromstring(r.text)
    for ch in root.findall("channel"):
        disp = ch.findtext("display-name")
        cid = ch.attrib.get("id")
        if disp and cid:
            epg_ids[disp.strip().lower()] = cid
    return epg_ids

def process_m3u(m3u_data, epg_map):
    lines = m3u_data.splitlines()
    output = []
    for i in range(len(lines)):
        line = lines[i]
        if line.startswith("#EXTINF:"):
            # Kanal adını yakala
            name_match = re.search(r',(.*)$', line)
            ch_name = name_match.group(1).strip().lower() if name_match else ""
            tvg_id = epg_map.get(ch_name, "")

            # Mevcut tvg-id sil
            line = re.sub(r'tvg-id="[^"]*"', '', line)
            # Fazla boşlukları düzelt
            line = re.sub(r'\s+', ' ', line)
            # tvg-id'yi doğru şekilde ekle
            line = line.replace("#EXTINF:-1", f'#EXTINF:-1 tvg-id="{tvg_id}"')
            output.append(line.strip())
        else:
            output.append(line)
    return "\n".join(output)

def save_output(content):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    print("🔄 M3U ve EPG verileri alınıyor...")
    m3u = fetch_m3u()
    epg_map = fetch_epg_ids()
    if not m3u or not epg_map:
        print("❌ Veri alınamadı.")
        return
    result = process_m3u(m3u, epg_map)
    save_output(result)
    print(f"✅ Yeni dosya oluşturuldu: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
