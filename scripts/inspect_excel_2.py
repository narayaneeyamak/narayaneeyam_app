import zipfile
import xml.etree.ElementTree as ET
import sys
import os

file_path = r"C:\Users\Lenovo\Downloads\Narayaneeyam (1).xlsx"

if not os.path.exists(file_path):
    print(f"File not found at {file_path}")
    sys.exit(1)

with zipfile.ZipFile(file_path, 'r') as z:
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

    print(f"Found {len(sheets)} sheet(s): {[s[0] for s in sheets]}")

    rels_tree = ET.parse(z.open('xl/_rels/workbook.xml.rels'))
    rels_root = rels_tree.getroot()
    rel_ns = {'r': 'http://schemas.openxmlformats.org/package/2006/relationships'}
    rel_map = {}
    for rel in rels_root.findall('.//r:Relationship', rel_ns):
        rel_map[rel.attrib['Id']] = rel.attrib['Target']

    dasakam_counts = {}

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
            
        for r in rows[1:]: # Skip header
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
            
            d_no_str = cells.get('A', '')
            sloka_text = cells.get('C', '').strip()
            if sloka_text:
                try:
                    d_no = int(float(d_no_str))
                    dasakam_counts[d_no] = dasakam_counts.get(d_no, 0) + 1
                except ValueError:
                    pass

    print("Dasakam breakdown in Excel file:")
    for d in sorted(dasakam_counts.keys()):
        print(f"  Dasakam {d}: {dasakam_counts[d]} slokas")
