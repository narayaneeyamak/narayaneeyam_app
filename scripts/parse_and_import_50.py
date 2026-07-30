import zipfile
import xml.etree.ElementTree as ET
import sys
import os
import json
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

excel_path = r"C:\Users\Lenovo\Downloads\Narayaneeyam (2).xlsx"
json_path = os.path.join("src", "data", "narayaneeyam_data.json")

DASAKAM_METADATA = {
    1: {"title": "Dasakam 1: The Glory of the Supreme Being", "titleTelugu": "దశకం 1: భగవత్స్వరూప మహత్త్వము", "summary": "Focuses on the divine, all-pervading form of Lord Guruvayurappan."},
    2: {"title": "Dasakam 2: Meditation on the Divine Form", "titleTelugu": "దశకం 2: భగవత్స్వరూప ధ్యానము", "summary": "Meditation on the divine limbs and glory of the Lord."},
    3: {"title": "Dasakam 3: Characteristics of a True Devotee", "titleTelugu": "దశకం 3: భక్త లక్షణము", "summary": "Prarthana and devotion to Lord Guruvayurappan."},
    4: {"title": "Dasakam 4: Ashtanga Yoga & Sadhana", "titleTelugu": "దశకం 4: అష్టాంగ యోగము", "summary": "Yogic sadhana and intense devotion."},
    5: {"title": "Dasakam 5: Cosmic Evolution & Creation", "titleTelugu": "దశకం 5: సృష్టి క్రమము", "summary": "Description of Prakriti and cosmic evolution."},
    6: {"title": "Dasakam 6: Description of the Virat Purusha", "titleTelugu": "దశకం 6: విరాట్ పురుష వర్ణనము", "summary": "The universal form of the Lord."},
    7: {"title": "Dasakam 7: Manifestation of Lord Brahma", "titleTelugu": "దశకం 7: బ్రహ్మోత్పత్తి", "summary": "Birth of Lord Brahma and divine grace."},
    8: {"title": "Dasakam 8: Dissolution & Re-creation", "titleTelugu": "దశకం 8: ప్రళయము మరియు సృష్టి", "summary": "Pralaya and revival of creation."},
    9: {"title": "Dasakam 9: Creation of the Cosmos", "titleTelugu": "దశకం 9: జగత్సృష్టి", "summary": "Detailed account of cosmic creation."},
    10: {"title": "Dasakam 10: Diverse Worlds & Species", "titleTelugu": "దశకం 10: నానావిధ సృష్టి", "summary": "Creation of various realms and beings."},
    11: {"title": "Dasakam 11: Avatar of Lord Varaha", "titleTelugu": "దశకం 11: వరాహ అవతారము", "summary": "Appearance of Lord Varaha to uplift Mother Earth."},
    12: {"title": "Dasakam 12: Slaying of Hiranyaksha", "titleTelugu": "దశకం 12: హిరణ్యాక్ష వధ", "summary": "Lord Varaha defeating Hiranyaksha."},
    13: {"title": "Dasakam 13: Kapila Avatar & Devahuti", "titleTelugu": "దశకం 13: కపిలావతారము", "summary": "Lord Kapila teaching Sankhya philosophy to Devahuti."},
    14: {"title": "Dasakam 14: Story of Yajna Avatar", "titleTelugu": "దశకం 14: యజ్ఞ అవతారము", "summary": "Glorification of Yajna avatar and Svayambhuva Manu."},
    15: {"title": "Dasakam 15: Story of King Rishabhadeva", "titleTelugu": "దశకం 15: ఋషభదేవ చరిత్ర", "summary": "Life and teachings of King Rishabhadeva."},
    16: {"title": "Dasakam 16: King Bharata's Devotion", "titleTelugu": "దశకం 16: జడభరత చరిత్ర", "summary": "The divine story of King Bharata."},
    17: {"title": "Dasakam 17: Sacred Realms & Geography", "titleTelugu": "దశకం 17: వర్షద్వీప వర్ణనము", "summary": "Geography of Jambudvipa and sacred realms."},
    18: {"title": "Dasakam 18: Story of King Prithu", "titleTelugu": "దశకం 18: పృథు చక్రవర్తి చరిత్ర", "summary": "Avatar of King Prithu and milking of Mother Earth."},
    19: {"title": "Dasakam 19: Story of Prachetas & Narada", "titleTelugu": "దశకం 19: ప్రచేతసుల చరిత్ర", "summary": "Devotion of Prachetas and teachings of Lord Shiva & Narada."},
    20: {"title": "Dasakam 20: Dhruva's Penance & Grace", "titleTelugu": "దశకం 20: ధ్రువోపాఖ్యానము", "summary": "The steadfast devotion of child Dhruva."},
    21: {"title": "Dasakam 21: Glory of Dhruva & Story of King Vena", "titleTelugu": "దశకం 21: వేనోపాఖ్యానము", "summary": "Dhruva's ascension and story of King Vena."},
    22: {"title": "Dasakam 22: Story of King Ajamila", "titleTelugu": "దశకం 22: అజామిలోపాఖ్యానము", "summary": "Redemption of Ajamila by chanting the Name of Narayana."},
    23: {"title": "Dasakam 23: Story of Chitraketu", "titleTelugu": "దశకం 23: చిత్రకేతూపాఖ్యానము", "summary": "King Chitraketu's devotion and transformation."},
    24: {"title": "Dasakam 24: Prahlada's Devotion", "titleTelugu": "దశకం 24: ప్రహ్లాద చరిత్ర", "summary": "Unshakeable devotion of Bhakta Prahlada."},
    25: {"title": "Dasakam 25: Narasimha Avatar", "titleTelugu": "దశకం 25: నృసింహావతారము", "summary": "Appearance of Lord Narasimha and slaying of Hiranyakashipu."},
    26: {"title": "Dasakam 26: Praise of Lord Narasimha", "titleTelugu": "దశకం 26: నృసింహ స్తుతి", "summary": "Prahlada's soulful prayer to Lord Narasimha."},
    27: {"title": "Dasakam 27: Gajendra Moksham", "titleTelugu": "దశకం 27: గజేంద్ర మోక్షము", "summary": "Rescue of Gajendra the King Elephant."},
    28: {"title": "Dasakam 28: Churning of the Ocean (Samudra Manthan)", "titleTelugu": "దశకం 28: క్షీరసాగర మథనము", "summary": "The Devas and Asuras churning the Milk Ocean."},
    29: {"title": "Dasakam 29: Kurma & Mohini Avatars", "titleTelugu": "దశకం 29: కూర్మ మోహినీ అవతారములు", "summary": "Lord Kurma holding Mandara and Mohini distributing Amrita."},
    30: {"title": "Dasakam 30: Story of Vamana Avatar", "titleTelugu": "దశకం 30: వామనావతారము", "summary": "Appearance of Vamana at King Bali's sacrifice."},
    31: {"title": "Dasakam 31: Trivikrama Avatar & King Bali", "titleTelugu": "దశకం 31: త్రివిక్రమావతారము", "summary": "Lord Trivikrama measuring the three worlds."},
    32: {"title": "Dasakam 32: Matsya Avatar", "titleTelugu": "దశకం 32: మత్స్యావతారము", "summary": "Lord Matsya saving King Satyavrata and the Vedas."},
    33: {"title": "Dasakam 33: Story of Ambarisha & Durvasa", "titleTelugu": "దశకం 33: అంబరీష చరిత్ర", "summary": "King Ambarisha's Ekadashi vow and protection by Sudarshana Chakra."},
    34: {"title": "Dasakam 34: Solar Dynasty & Bhagiratha", "titleTelugu": "దశకం 34: సూర్యవంశ వర్ణనము", "summary": "Ancestors of Lord Rama and Bhagiratha bringing Ganga."},
    35: {"title": "Dasakam 35: Sri Rama Avatar - Early Life", "titleTelugu": "దశకం 35: శ్రీరామావతారము (బాలకాండ)", "summary": "Incarnation of Sri Rama and protection of Vishvamitra's yajna."},
    36: {"title": "Dasakam 36: Sri Rama Avatar - Exile & Ravana Vadha", "titleTelugu": "దశకం 36: శ్రీరామావతారము (వనవాసము & రావణవధ)", "summary": "Forest exile, Sita's abduction, and victory over Ravana."},
    37: {"title": "Dasakam 37: Parasurama Avatar", "titleTelugu": "దశకం 37: పరశురామావతారము", "summary": "Incarnation of Lord Parasurama destroying wicked kshatriyas."},
    38: {"title": "Dasakam 38: Lunar Dynasty & King Yayati", "titleTelugu": "దశకం 38: చంద్రవంశ వర్ణనము", "summary": "Soma dynasty and the story of King Yayati."},
    39: {"title": "Dasakam 39: Story of King Dushyanta & Bharata", "titleTelugu": "దశకం 39: దుష్యంత భరత చరిత్ర", "summary": "Lineage of Kuru and birth of Emperor Bharata."},
    40: {"title": "Dasakam 40: Descent of Sri Krishna - Prophecy", "titleTelugu": "దశకం 40: శ్రీకృష్ణావతార భూమిక", "summary": "Mother Earth praying to Lord Vishnu for relief."},
    41: {"title": "Dasakam 41: Birth of Bhagavan Sri Krishna", "titleTelugu": "దశకం 41: శ్రీకృష్ణ జననము", "summary": "Divine birth of Sri Krishna in Mathura prison."},
    42: {"title": "Dasakam 42: Transfer to Gokulam & Putana Moksham", "titleTelugu": "దశకం 42: పూతనా మోక్షము", "summary": "Arrival in Gokulam and liberation of demoness Putana."},
    43: {"title": "Dasakam 43: Slaying of Sakatasura & Trinavarta", "titleTelugu": "దశకం 43: శకటాసుర తృణావర్త వధ", "summary": "Child Krishna subduing Sakatasura and whirlwind demon Trinavarta."},
    44: {"title": "Dasakam 44: Namakarana & Childhood Leelas", "titleTelugu": "దశకం 44: నామకరణము & బాలలీలలు", "summary": "Naming ceremony by Sage Garga and toddler pastimes."},
    45: {"title": "Dasakam 45: Universal Vision in Krishna's Mouth", "titleTelugu": "దశకం 45: విశ్వరూప దర్శనము", "summary": "Mother Yashoda witnessing the cosmos inside Krishna's mouth."},
    46: {"title": "Dasakam 46: Damodara Leela & Yashoda's Love", "titleTelugu": "దశకం 46: దామోదర లీల", "summary": "Yashoda binding Krishna to the wooden mortar."},
    47: {"title": "Dasakam 47: Liberation of Yamalarjuna Trees", "titleTelugu": "దశకం 47: యమలార్జున భంజనము", "summary": "Felling of twin Arjuna trees liberating Nalakuvara and Manigriva."},
    48: {"title": "Dasakam 48: Move to Vrindavan & Vatsasura", "titleTelugu": "దశకం 48: బృందావన ప్రవేశము & వత్సాసుర వధ", "summary": "Journey to Vrindavan and subduing Vatsasura & Bakasura."},
    49: {"title": "Dasakam 49: Slaying of Aghasura", "titleTelugu": "దశకం 49: అఘాసుర వధ", "summary": "Liberation of serpent demon Aghasura."},
    50: {"title": "Dasakam 50: Brahma Mohan Leela", "titleTelugu": "దశకం 50: బ్రహ్మ మోహన లీల", "summary": "Lord Brahma's illusion and Krishna manifesting as all calves and cowherds."}
}

def extract_file_id(drive_url):
    if not drive_url: return None
    if "/d/" in drive_url:
        return drive_url.split("/d/")[1].split("/")[0].split("?")[0]
    if "id=" in drive_url:
        return drive_url.split("id=")[1].split("&")[0]
    return None

def download_task(item):
    file_id, dest_path = item
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 1000:
        return dest_path, True
    if not file_id:
        return dest_path, False
    
    dl_url = f"https://drive.usercontent.google.com/download?id={file_id}&export=download"
    try:
        req = urllib.request.Request(
            dl_url,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req, timeout=15) as resp, open(dest_path, 'wb') as out_f:
            out_f.write(resp.read())
        size = os.path.getsize(dest_path)
        return dest_path, size > 1000
    except Exception as e:
        print(f"Failed {dest_path}: {e}")
        return dest_path, False

def fast_process_50_dasakams():
    if not os.path.exists(excel_path):
        print(f"Error: {excel_path} not found")
        sys.exit(1)

    with zipfile.ZipFile(excel_path, 'r') as z:
        shared_strings = []
        if 'xl/sharedStrings.xml' in z.namelist():
            tree = ET.parse(z.open('xl/sharedStrings.xml'))
            ns = {'main': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
            for si in tree.getroot().findall('.//main:si', ns):
                t_elems = si.findall('.//main:t', ns)
                shared_strings.append(''.join([t.text if t.text else '' for t in t_elems]))

        wb_tree = ET.parse(z.open('xl/workbook.xml'))
        ns = {'main': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main', 'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
        sheets = [(s.attrib['name'], s.attrib.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')) for s in wb_tree.getroot().findall('.//main:sheet', ns)]
        rels_tree = ET.parse(z.open('xl/_rels/workbook.xml.rels'))
        rel_map = {r.attrib['Id']: r.attrib['Target'] for r in rels_tree.getroot().findall('.//r:Relationship', {'r': 'http://schemas.openxmlformats.org/package/2006/relationships'})}

        dasakam_slokas_map = {}

        for sheet_name, rId in sheets:
            target = rel_map.get(rId)
            if not target: continue
            sheet_path = 'xl/' + target if not target.startswith('xl/') else target
            sheet_tree = ET.parse(z.open(sheet_path))
            rows = sheet_tree.getroot().findall('.//main:row', ns)
            if not rows: continue

            num_match = ''.join([ch for ch in sheet_name if ch.isdigit()])
            sheet_d_no = int(num_match) if num_match else 0

            for r in rows[1:]:
                cells = {}
                for c in r.findall('./main:c', ns):
                    ref = c.attrib.get('r')
                    col = ''.join([ch for ch in ref if ch.isalpha()])
                    t_attr = c.attrib.get('t')
                    val_elem = c.find('main:v', ns)
                    val = val_elem.text if val_elem is not None else ''
                    if t_attr == 's' and val.isdigit():
                        idx = int(val)
                        if idx < len(shared_strings): val = shared_strings[idx]
                    elif t_attr == 'inlineStr':
                        t_elem = c.find('.//main:t', ns)
                        val = t_elem.text if t_elem is not None else ''
                    cells[col] = val

                sloka_text = cells.get('C', '').strip()
                if not sloka_text: continue

                d_str = cells.get('A', '').strip()
                try:
                    d_no = int(float(d_str))
                except ValueError:
                    d_no = sheet_d_no

                if d_no == 0: continue

                s_str = cells.get('B', '').strip()
                try:
                    s_no = int(float(s_str))
                except ValueError:
                    s_no = len(dasakam_slokas_map.get(d_no, [])) + 1

                audio_link = cells.get('D', '').strip()

                if d_no not in dasakam_slokas_map:
                    dasakam_slokas_map[d_no] = []

                dasakam_slokas_map[d_no].append({
                    "slokaNo": s_no,
                    "text": sloka_text,
                    "driveUrl": audio_link
                })

    print(f"Parsed {len(dasakam_slokas_map)} Dasakams from Excel.")

    # Prepare download queue
    download_items = []
    for d_no, slokas in dasakam_slokas_map.items():
        audio_dir = os.path.join("public", "audio", f"dasakam{d_no}")
        os.makedirs(audio_dir, exist_ok=True)
        for s in slokas:
            mp3_filename = f"sloka_{s['slokaNo']}.mp3"
            mp3_path = os.path.join(audio_dir, mp3_filename)
            file_id = extract_file_id(s.get("driveUrl", ""))
            download_items.append((file_id, mp3_path))

    print(f"Downloading {len(download_items)} audio files using 12 concurrent workers...")
    completed_count = 0
    with ThreadPoolExecutor(max_workers=12) as executor:
        futures = [executor.submit(download_task, item) for item in download_items]
        for f in as_completed(futures):
            dest, success = f.result()
            completed_count += 1
            if completed_count % 50 == 0 or completed_count == len(download_items):
                print(f"Progress: {completed_count}/{len(download_items)} files processed...")

    # Build final JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    final_dasakams = []
    for d_no in sorted(dasakam_slokas_map.keys()):
        slokas_in = dasakam_slokas_map[d_no]
        meta = DASAKAM_METADATA.get(d_no, {
            "title": f"Dasakam {d_no}",
            "titleTelugu": f"దశకం {d_no}",
            "summary": f"Srimad Narayaneeyam Dasakam {d_no} slokas."
        })

        processed_slokas = []
        for s in slokas_in:
            s_no = s["slokaNo"]
            drive_url = s.get("driveUrl", "")
            mp3_filename = f"sloka_{s_no}.mp3"
            mp3_path = os.path.join("public", "audio", f"dasakam{d_no}", mp3_filename)
            rel_audio_url = f"/audio/dasakam{d_no}/{mp3_filename}"

            processed_slokas.append({
                "slokaNo": s_no,
                "text": s["text"],
                "audioUrl": rel_audio_url if os.path.exists(mp3_path) else drive_url,
                "driveUrl": drive_url
            })

        final_dasakams.append({
            "id": d_no,
            "number": d_no,
            "title": meta["title"],
            "titleTelugu": meta["titleTelugu"],
            "summary": meta["summary"],
            "slokaCount": len(processed_slokas),
            "slokas": processed_slokas
        })

    json_data["dasakams"] = final_dasakams
    json_data["totalDasakams"] = len(final_dasakams)

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)

    print(f"\nSUCCESS! Fully imported all 50 Dasakams ({len(download_items)} slokas & audio files) into {json_path}!")

if __name__ == "__main__":
    fast_process_50_dasakams()
