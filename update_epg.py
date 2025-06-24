import requests

url = "https://belgeselsemo.com.tr/tools/epg.html/jkhm4"
output_file = "epg.xml"

def update_epg():
    try:
        r = requests.get(url)
        if r.status_code == 200 and "<tv" in r.text:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(r.text)
            print("EPG dosyası güncellendi.")
        else:
            print("Hatalı veri veya bağlantı sorunu.")
    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    update_epg()
