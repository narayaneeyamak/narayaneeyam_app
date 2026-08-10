import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
json_path = os.path.join("src", "data", "narayaneeyam_data.json")

def fix_all_spacing():
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    total_slokas = 0
    modified_slokas = 0

    for dasakam in data.get("dasakams", []):
        d_no = dasakam.get("number")
        for sloka in dasakam.get("slokas", []):
            total_slokas += 1
            s_no = sloka.get("slokaNo")
            text = sloka.get("text", "")
            orig_text = text

            # 1. Fix space after commas if missing e.g. ",త్వమ్" -> ", త్వమ్"
            text = re.sub(r',([^\s\n])', r', \1', text)

            # 2. Fix space after exclamation marks if missing e.g. "!చక్ర" -> "! చక్ర"
            text = re.sub(r'!([^\s\n])', r'! \1', text)

            # 3. Fix space after single virama if missing e.g. "ధామ్నా।హే" -> "ధామ్నా। హే"
            text = re.sub(r'।([^\s\d॥\n])', r'। \1', text)

            # 4. Standardize double virama and sloka number e.g. "॥1॥" or "॥1 ॥" or "॥ 1॥" -> "॥ 1 ॥"
            text = re.sub(r'॥\s*(\d+)\s*॥', r'॥ \1 ॥', text)
            text = re.sub(r'॥\s*(\d+)\s*$', r'॥ \1 ॥', text, flags=re.MULTILINE)

            # 5. Fix hyphens embedded in words e.g. "సతేమనైర్-నిరగమదీశ" -> "సతేమనైర్ నిరగమదీశ" or "త్వత్-పాద" -> "త్వత్ పాద"
            text = re.sub(r'([\u0C00-\u0C7F]+)-\s*([\u0C00-\u0C7F]+)', r'\1 \2', text)

            # 6. Clean double spaces inside lines
            lines = text.split('\n')
            cleaned_lines = []
            for line in lines:
                l_clean = line.strip()
                l_clean = re.sub(r'[ \t]{2,}', ' ', l_clean)
                cleaned_lines.append(l_clean)

            text = "\n".join(cleaned_lines)

            if text != orig_text:
                modified_slokas += 1
                sloka["text"] = text

    print(f"Audited {total_slokas} slokas across all 100 Dasakams.")
    print(f"Fixed spacing & formatting in {modified_slokas} slokas!")

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Saved pristine spaced text to {json_path}!")

if __name__ == "__main__":
    fix_all_spacing()
