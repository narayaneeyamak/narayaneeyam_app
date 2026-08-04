import zipfile
import xml.etree.ElementTree as ET
import sys
import os
import json
import urllib.request
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

file_1_50 = r"C:\Users\Lenovo\Downloads\Narayaneeyam 1-50.xlsx"
file_51_100 = r"C:\Users\Lenovo\Downloads\Narayaneeyam 51-100.xlsx"
json_path = os.path.join("src", "data", "narayaneeyam_data.json")

def extract_file_id(drive_url):
    if not drive_url: return None
    if "/d/" in drive_url:
        return drive_url.split("/d/")[1].split("/")[0].split("?")[0]
    if "id=" in drive_url:
        return drive_url.split("id=")[1].split("&")[0]
    return None

def download_audio_task(item):
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
        return dest_path, False

def parse_excel_file(file_path):
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found")
        return {}

    with zipfile.ZipFile(file_path, 'r') as z:
        shared_strings = []
        if 'xl/sharedStrings.xml' in z.namelist():
            tree = ET.parse(z.open('xl/sharedStrings.xml'))
            ns = {'main': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
            for si in tree.getroot().findall('.//main:si', ns):
                t_elems = si.findall('.//main:t', ns)
                text = ''.join([t.text if t.text else '' for t in t_elems])
                shared_strings.append(text)

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

                # C: Slokam Text (preserve exact newlines & spacing)
                sloka_text = cells.get('C', '')
                if not sloka_text or not sloka_text.strip():
                    continue

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
                    "text": sloka_text, # Exact string with spacing & indentation
                    "driveUrl": audio_link
                })

    return dasakam_slokas_map

def run_import_all_100():
    print("Parsing Dasakams 1 to 50 from 'Narayaneeyam 1-50.xlsx'...")
    map_1_50 = parse_excel_file(file_1_50)

    print("Parsing Dasakams 51 to 100 from 'Narayaneeyam 51-100.xlsx'...")
    map_51_100 = parse_excel_file(file_51_100)

    # Merge all 100 maps
    combined_map = {}
    combined_map.update(map_1_50)
    combined_map.update(map_51_100)

    print(f"\nSuccessfully parsed total {len(combined_map)} Dasakams!")

    # Build download queue for missing audio files
    download_queue = []
    for d_no, slokas in combined_map.items():
        audio_dir = os.path.join("public", "audio", f"dasakam{d_no}")
        os.makedirs(audio_dir, exist_ok=True)
        for s in slokas:
            mp3_path = os.path.join(audio_dir, f"sloka_{s['slokaNo']}.mp3")
            if not os.path.exists(mp3_path) or os.path.getsize(mp3_path) < 1000:
                file_id = extract_file_id(s.get("driveUrl", ""))
                if file_id:
                    download_queue.append((file_id, mp3_path))

    if download_queue:
        print(f"\nDownloading {len(download_queue)} new/missing audio MP3 files using 16 workers...")
        done_count = 0
        with ThreadPoolExecutor(max_workers=16) as executor:
            futures = [executor.submit(download_audio_task, item) for item in download_queue]
            for f in as_completed(futures):
                dest, success = f.result()
                done_count += 1
                if done_count % 50 == 0 or done_count == len(download_queue):
                    print(f"  Progress: {done_count}/{len(download_queue)} audio files downloaded...")
    else:
        print("\nAll audio files are already downloaded locally!")

    # Read existing JSON structure
    with open(json_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    # Build final list for all 100 Dasakams
    final_dasakams = []
    total_slokas_count = 0

    for d_no in range(1, 101):
        slokas_in = combined_map.get(d_no, [])
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

        total_slokas_count += len(processed_slokas)

        title = f"Dasakam {d_no}"
        title_telugu = f"దశకం {d_no}"
        summary = f"Srimad Narayaneeyam Dasakam {d_no} slokas."

        final_dasakams.append({
            "id": d_no,
            "number": d_no,
            "title": title,
            "titleTelugu": title_telugu,
            "summary": summary,
            "slokaCount": len(processed_slokas),
            "slokas": processed_slokas
        })

    json_data["dasakams"] = final_dasakams
    json_data["totalDasakams"] = len(final_dasakams)

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)

    print(f"\n=======================================================")
    print(f"SUCCESS! All {len(final_dasakams)} Dasakams ({total_slokas_count} slokas) imported into {json_path}!")
    print(f"=======================================================")

if __name__ == "__main__":
    run_import_all_100()
