import zipfile
import xml.etree.ElementTree as ET
import sys
import os
import json

sys.stdout.reconfigure(encoding='utf-8')

f1 = r"C:\Users\Lenovo\Downloads\Narayaneeyam 1-50 (1).xlsx"
f2 = r"C:\Users\Lenovo\Downloads\Narayaneeyam 51-100 (1).xlsx"
json_path = os.path.join("src", "data", "narayaneeyam_data.json")

def parse_excel_text_map(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File not found {file_path}")
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

        dasakam_map = {}

        for sheet_name, rId in sheets:
            # Skip non-dasaka sheets if any
            num_match = ''.join([ch for ch in sheet_name if ch.isdigit()])
            if not num_match:
                continue
            sheet_d_no = int(num_match)

            target = rel_map.get(rId)
            if not target: continue
            sheet_path = 'xl/' + target if not target.startswith('xl/') else target
            sheet_tree = ET.parse(z.open(sheet_path))
            rows = sheet_tree.getroot().findall('.//main:row', ns)
            if not rows: continue

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

                sloka_text = cells.get('C', '')
                if not sloka_text or not sloka_text.strip():
                    continue

                d_str = cells.get('A', '').strip()
                try:
                    d_no = int(float(d_str))
                except ValueError:
                    d_no = sheet_d_no

                s_str = cells.get('B', '').strip()
                try:
                    s_no = int(float(s_str))
                except ValueError:
                    s_no = len(dasakam_map.get(d_no, [])) + 1

                audio_link = cells.get('D', '').strip()

                if d_no not in dasakam_map:
                    dasakam_map[d_no] = []

                dasakam_map[d_no].append({
                    "slokaNo": s_no,
                    "text": sloka_text,
                    "driveUrl": audio_link
                })

    return dasakam_map

def update_dataset_with_final_excel():
    print("Parsing final text for Dasakams 1 to 50...")
    map_1_50 = parse_excel_text_map(f1)

    print("Parsing final text for Dasakams 51 to 100...")
    map_51_100 = parse_excel_text_map(f2)

    combined_map = {}
    combined_map.update(map_1_50)
    combined_map.update(map_51_100)

    print(f"\nParsed text for {len(combined_map)} Dasakams!")

    with open(json_path, 'r', encoding='utf-8') as f:
        existing_data = json.load(f)

    updated_count = 0
    total_slokas_parsed = 0

    for dasakam in existing_data.get("dasakams", []):
        d_no = dasakam.get("number")
        excel_slokas = combined_map.get(d_no, [])
        total_slokas_parsed += len(excel_slokas)

        # Update existing slokas array with pristine text from Excel
        excel_slokas_dict = {s["slokaNo"]: s for s in excel_slokas}

        new_slokas_list = []
        
        # If excel has slokas for this dasakam
        if excel_slokas:
            for s in excel_slokas:
                s_no = s["slokaNo"]
                text_from_excel = s["text"]

                # Find existing audio links
                existing_sloka = next((item for item in dasakam.get("slokas", []) if item["slokaNo"] == s_no), None)

                audio_url = existing_sloka.get("audioUrl") if existing_sloka else ""
                drive_url = s["driveUrl"] or (existing_sloka.get("driveUrl") if existing_sloka else "")

                # If no audioUrl yet, check if local audio file exists
                if not audio_url:
                    # check .m4a or .mp3
                    m4a_path = os.path.join("public", "audio", f"dasakam{d_no}", f"sloka_{s_no}.m4a")
                    mp3_path = os.path.join("public", "audio", f"dasakam{d_no}", f"sloka_{s_no}.mp3")
                    if os.path.exists(m4a_path):
                        audio_url = f"/audio/dasakam{d_no}/sloka_{s_no}.m4a"
                    elif os.path.exists(mp3_path):
                        audio_url = f"/audio/dasakam{d_no}/sloka_{s_no}.mp3"
                    else:
                        audio_url = drive_url

                new_slokas_list.append({
                    "slokaNo": s_no,
                    "text": text_from_excel,
                    "audioUrl": audio_url,
                    "driveUrl": drive_url
                })

            dasakam["slokas"] = new_slokas_list
            dasakam["slokaCount"] = len(new_slokas_list)
            updated_count += 1

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=2)

    print(f"\n=======================================================")
    print(f"SUCCESSFULLY updated {updated_count} Dasakams ({total_slokas_parsed} slokas) with final text!")
    print(f"=======================================================")

if __name__ == "__main__":
    update_dataset_with_final_excel()
