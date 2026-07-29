import zipfile
import xml.etree.ElementTree as ET
import sys
import os
import json
import urllib.request
import time

excel_path = r"C:\Users\Lenovo\Downloads\Narayaneeyam (1).xlsx"
json_path = os.path.join("src", "data", "narayaneeyam_data.json")

# Titles in Telugu and English for Dasakams 1 to 20
DASAKAM_METADATA = {
    1: {"title": "Dasakam 1: The Glory of the Form of the Supreme Being", "titleTelugu": "దశకం 1: భగవత్స్వరూప మహత్త్వము", "summary": "Focuses on the divine, all-pervading form of Lord Guruvayurappan."},
    2: {"title": "Dasakam 2: Form of the Supreme & Devotion", "titleTelugu": "దశకం 2: భగవత్స్వరూప ధ్యానము", "summary": "Meditation on the divine limbs and glory of the Lord."},
    3: {"title": "Dasakam 3: Characteristics of a True Devotee", "titleTelugu": "దశకం 3: భక్త లక్షణము", "summary": "Prarthana and devotion to Lord Guruvayurappan."},
    4: {"title": "Dasakam 4: Ashtanga Yoga & Practice", "titleTelugu": "దశకం 4: అష్టాంగ యోగము", "summary": "Yogic sadhana and devotion."},
    5: {"title": "Dasakam 5: Cosmic Evolution & Creation", "titleTelugu": "దశకం 5: సృష్టి క్రమము", "summary": "Description of Prakriti and cosmic evolution."},
    6: {"title": "Dasakam 6: Description of the Virat Purusha", "titleTelugu": "దశకం 6: విరాట్ పురుష వర్ణనము", "summary": "The universal form of the Lord."},
    7: {"title": "Dasakam 7: Manifestation of Brahma", "titleTelugu": "దశకం 7: బ్రహ్మోత్పత్తి", "summary": "Birth of Lord Brahma and divine grace."},
    8: {"title": "Dasakam 8: Dissolution & Creation", "titleTelugu": "దశకం 8: ప్రళయము మరియు సృష్టి", "summary": "Pralaya and revival of creation."},
    9: {"title": "Dasakam 9: Creation of the Cosmos", "titleTelugu": "దశకం 9: జగత్సృష్టి", "summary": "Detailed account of cosmic creation."},
    10: {"title": "Dasakam 10: The Diverse Worlds & Species", "titleTelugu": "దశకం 10: నానావిధ సృష్టి", "summary": "Creation of various realms and beings."},
    11: {"title": "Dasakam 11: Incarnation of Lord Varaha", "titleTelugu": "దశకం 11: వరాహ అవతారము", "summary": "Appearance of Lord Varaha to uplift Mother Earth."},
    12: {"title": "Dasakam 12: Slaying of Hiranyaksha", "titleTelugu": "దశకం 12: హిరణ్యాక్ష వధ", "summary": "Lord Varaha defeating Hiranyaksha."},
    13: {"title": "Dasakam 13: Story of Kapila & Devahuti", "titleTelugu": "దశకం 13: కపిలావతారము", "summary": "Lord Kapila teaching Sankhya philosophy to Devahuti."},
    14: {"title": "Dasakam 14: Story of Yajna Avatar", "titleTelugu": "దశకం 14: యజ్ఞ అవతారము", "summary": "Glorification of Yajna avatar and Svayambhuva Manu."},
    15: {"title": "Dasakam 15: Story of Rishabhadeva", "titleTelugu": "దశకం 15: ఋషభదేవ చరిత్ర", "summary": "Life and teachings of King Rishabhadeva."},
    16: {"title": "Dasakam 16: King Bharata's Devotion", "titleTelugu": "దశకం 16: జడభరత చరిత్ర", "summary": "The divine story of King Bharata."},
    17: {"title": "Dasakam 17: Description of the Earth & Continents", "titleTelugu": "దశకం 17: భూగోళ వర్ణనము", "summary": "Geography of Jambudvipa and sacred realms."},
    18: {"title": "Dasakam 18: Story of King Prithu", "titleTelugu": "దశకం 18: పృథు చక్రవర్తి చరిత్ర", "summary": "Avatar of King Prithu and milking of Mother Earth."},
    19: {"title": "Dasakam 19: Story of Prachetas & Narada", "titleTelugu": "దశకం 19: ప్రచేతసుల చరిత్ర", "summary": "Devotion of Prachetas and teachings of Lord Shiva & Narada."},
    20: {"title": "Dasakam 20: Story of Dhruva's Penance", "titleTelugu": "దశకం 20: ధ్రువోపాఖ్యానము", "summary": "The steadfast devotion of child Dhruva."}
}

def extract_file_id(drive_url):
    if not drive_url:
        return None
    if "/d/" in drive_url:
        return drive_url.split("/d/")[1].split("/")[0].split("?")[0]
    if "id=" in drive_url:
        return drive_url.split("id=")[1].split("&")[0]
    return None

def download_audio_file(file_id, dest_path):
    if not file_id:
        return False
    dl_url = f"https://drive.usercontent.google.com/download?id={file_id}&export=download"
    try:
        req = urllib.request.Request(
            dl_url,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req) as resp, open(dest_path, 'wb') as out_f:
            out_f.write(resp.read())
        size = os.path.getsize(dest_path)
        if size > 5000: # Valid audio size
            return True
        else:
            print(f"    Warning: Downloaded file size small ({size} bytes)")
            return True
    except Exception as e:
        print(f"    Download error for {file_id}: {e}")
        return False

def parse_all_dasakams():
    if not os.path.exists(excel_path):
        print(f"Error: {excel_path} not found")
        sys.exit(1)

    # 1. Read Shared Strings & Sheets
    with zipfile.ZipFile(excel_path, 'r') as z:
        shared_strings = []
        if 'xl/sharedStrings.xml' in z.namelist():
            tree = ET.parse(z.open('xl/sharedStrings.xml'))
            root = tree.getroot()
            ns = {'main': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
            for si in root.findall('.//main:si', ns):
                t_elems = si.findall('.//main:t', ns)
                text = "".join([t.text if t.text else "" for t in t_elems])
                shared_strings.append(text)

        wb_tree = ET.parse(z.open('xl/workbook.xml'))
        wb_root = wb_tree.getroot()
        ns = {
            'main': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main',
            'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
        }
        
        sheets = []
        for sheet in wb_root.findall('.//main:sheet', ns):
            sheets.append((sheet.attrib['name'], sheet.attrib.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')))

        rels_tree = ET.parse(z.open('xl/_rels/workbook.xml.rels'))
        rels_root = rels_tree.getroot()
        rel_ns = {'r': 'http://schemas.openxmlformats.org/package/2006/relationships'}
        rel_map = {}
        for rel in rels_root.findall('.//r:Relationship', rel_ns):
            rel_map[rel.attrib['Id']] = rel.attrib['Target']

        # Map dasakam_number -> list of slokas
        dasakam_slokas_map = {}

        for sheet_name, rId in sheets:
            target = rel_map.get(rId)
            if not target:
                continue
            sheet_path = 'xl/' + target if not target.startswith('xl/') else target
            sheet_tree = ET.parse(z.open(sheet_path))
            sheet_root = sheet_tree.getroot()
            
            rows = sheet_root.findall('.//main:row', ns)
            if not rows:
                continue
                
            for r in rows[1:]:
                cells = {}
                for c in r.findall('./main:c', ns):
                    ref = c.attrib.get('r')
                    col = "".join([ch for ch in ref if ch.isalpha()])
                    t_attr = c.attrib.get('t')
                    val_elem = c.find('main:v', ns)
                    val = val_elem.text if val_elem is not None else ""
                    
                    if t_attr == 's' and val.isdigit():
                        idx = int(val)
                        if idx < len(shared_strings):
                            val = shared_strings[idx]
                    elif t_attr == 'inlineStr':
                        t_elem = c.find('.//main:t', ns)
                        val = t_elem.text if t_elem is not None else ""
                    
                    cells[col] = val
                
                # A: Dasakam No, B: Sloka No, C: Text, D: Audio Link
                sloka_text = cells.get('C', '').strip()
                if not sloka_text:
                    continue

                d_str = cells.get('A', '0').strip()
                try:
                    d_no = int(float(d_str))
                except ValueError:
                    # Fallback to sheet name if row A cell empty
                    num_match = "".join([ch for ch in sheet_name if ch.isdigit()])
                    d_no = int(num_match) if num_match else 0

                if d_no == 0:
                    continue

                s_str = cells.get('B', '0').strip()
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

    print(f"Parsed {len(dasakam_slokas_map)} Dasakams from Excel file.")

    # Load existing JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    # Process each Dasakam (1 to 20)
    final_dasakams_list = []
    
    for d_no in sorted(dasakam_slokas_map.keys()):
        slokas_in = dasakam_slokas_map[d_no]
        meta = DASAKAM_METADATA.get(d_no, {
            "title": f"Dasakam {d_no}",
            "titleTelugu": f"దశకం {d_no}",
            "summary": f"Srimad Narayaneeyam Dasakam {d_no} slokas."
        })

        audio_dir = os.path.join("public", "audio", f"dasakam{d_no}")
        os.makedirs(audio_dir, exist_ok=True)

        processed_slokas = []
        print(f"\nProcessing Dasakam {d_no} ({len(slokas_in)} slokas)...")

        for s in slokas_in:
            s_no = s["slokaNo"]
            drive_url = s.get("driveUrl", "")
            mp3_filename = f"sloka_{s_no}.mp3"
            mp3_path = os.path.join(audio_dir, mp3_filename)
            rel_audio_url = f"/audio/dasakam{d_no}/{mp3_filename}"

            # Check if file already downloaded
            if not os.path.exists(mp3_path) or os.path.getsize(mp3_path) < 1000:
                file_id = extract_file_id(drive_url)
                if file_id:
                    print(f"  Downloading Dasakam {d_no} Sloka {s_no}...")
                    download_audio_file(file_id, mp3_path)
                    time.sleep(0.2) # Polite delay
                else:
                    print(f"  No valid drive ID for Dasakam {d_no} Sloka {s_no}")

            processed_slokas.append({
                "slokaNo": s_no,
                "text": s["text"],
                "audioUrl": rel_audio_url if os.path.exists(mp3_path) else drive_url,
                "driveUrl": drive_url
            })

        final_dasakams_list.append({
            "id": d_no,
            "number": d_no,
            "title": meta["title"],
            "titleTelugu": meta["titleTelugu"],
            "summary": meta["summary"],
            "slokaCount": len(processed_slokas),
            "slokas": processed_slokas
        })

    json_data["dasakams"] = final_dasakams_list
    json_data["totalDasakams"] = len(final_dasakams_list)

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)

    print(f"\nSuccessfully imported Dasakams 1 to {len(final_dasakams_list)} into {json_path}!")

if __name__ == "__main__":
    parse_all_dasakams()
