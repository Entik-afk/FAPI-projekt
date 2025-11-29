import requests
import xml.etree.ElementTree as ET

def get_cnb_rates():
    url = "https://www.cnb.cz/cs/financni_trhy/devizovy_trh/kurzy_devizoveho_trhu/denni_kurz.xml"
    
    try:
        res = requests.get(url)
        res.raise_for_status()
    except requests.RequestException as e:
        print("Chyba při stahování kurzů CNB:", e)
        return {'EUR': 0, 'USD': 0}  # fallback

    try:
        root = ET.fromstring(res.content)
    except ET.ParseError as e:
        print("Chyba při parsování XML:", e)
        return {'EUR': 0, 'USD': 0}

    rates = {}
    # najdeme všechny radky
    for radek in root.findall(".//radek"):
        code = radek.attrib.get("kod")
        mnozstvi = radek.attrib.get("mnozstvi")
        kurz = radek.attrib.get("kurz")

        if not (code and mnozstvi and kurz):
            continue

        try:
            amount = int(mnozstvi)
            rate = float(kurz.replace(",", "."))
        except ValueError:
            continue

        if code in ["EUR", "USD"] and amount > 0:
            rates[code] = rate / amount

    # fallback na 0, pokud kurz není nalezen
    for cur in ["EUR", "USD"]:
        if cur not in rates:
            rates[cur] = 0

    print("Načtené kurzy z XML:", rates)
    return rates
