import sys
import os
import json
import zipfile
import xml.etree.ElementTree as ET

def parse_excel_file(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)

    shared_strings = []
    with zipfile.ZipFile(file_path, 'r') as z:
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

        all_slokas = []
        dasakam_num = 1

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
            
            # Skip header row (row 1)
            for r in rows[1:]:
                cells = {}
                for c in r.findall('./main:c', ns):
                    ref = c.attrib.get('r')
                    col_letter = "".join([char for char in ref if char.isalpha()])
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
                    
                    cells[col_letter] = val
                
                # A: Dasakam No, B: Sloka No, C: Text, D: Audio Link
                sloka_text = cells.get('C', '').strip()
                if not sloka_text:
                    continue
                
                try:
                    dasakam_num = int(float(cells.get('A', '1')))
                except ValueError:
                    dasakam_num = 1
                    
                try:
                    sloka_no = int(float(cells.get('B', len(all_slokas) + 1)))
                except ValueError:
                    sloka_no = len(all_slokas) + 1
                    
                audio_link = cells.get('D', '').strip()
                
                all_slokas.append({
                    "slokaNo": sloka_no,
                    "text": sloka_text,
                    "audioUrl": audio_link
                })
                
        return dasakam_num, all_slokas

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/import_excel.py <path_to_excel_file>")
        sys.exit(1)
        
    excel_path = sys.argv[1]
    dasakam_num, slokas = parse_excel_file(excel_path)
    
    data_json_path = os.path.join(os.path.dirname(__file__), "..", "src", "data", "narayaneeyam_data.json")
    with open(data_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    # Check if dasakam exists
    existing = False
    for d in data.get("dasakams", []):
        if d.get("number") == dasakam_num:
            d["slokas"] = slokas
            d["slokaCount"] = len(slokas)
            existing = True
            break
            
    if not existing:
        data["dasakams"].append({
            "id": dasakam_num,
            "number": dasakam_num,
            "title": f"Dasakam {dasakam_num}",
            "titleTelugu": f"దశకం {dasakam_num}",
            "summary": f"Dasakam {dasakam_num} slokas and audio",
            "slokaCount": len(slokas),
            "slokas": slokas
        })
        # Sort dasakams by number
        data["dasakams"].sort(key=lambda x: x["number"])
        
    with open(data_json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print(f"Successfully imported Dasakam {dasakam_num} ({len(slokas)} slokas) into narayaneeyam_data.json!")
