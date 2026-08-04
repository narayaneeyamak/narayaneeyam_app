import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
json_path = os.path.join("src", "data", "narayaneeyam_data.json")

def audit_and_clean_slokas():
    if not os.path.exists(json_path):
        print("JSON file not found!")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    total_dasakams = len(data.get("dasakams", []))
    total_slokas = 0
    cleaned_slokas = 0
    issues_found = []

    for dasakam in data.get("dasakams", []):
        d_no = dasakam.get("number")
        for sloka in dasakam.get("slokas", []):
            s_no = sloka.get("slokaNo")
            text = sloka.get("text", "")
            total_slokas += 1
            
            original_text = text
            
            # 1. Fix mid-word spaces before matras/virama (e.g. "భూ తై" -> "భూతై", "దృ ష్ట" -> "దృష్ట", "నిష్క ళ" -> "నిష్కళ")
            text = re.sub(r'([\u0C05-\u0C39])\s+([\u0C3E-\u0C4D\u0C55\u0C56])', r'\1\2', text)
            
            # 2. Fix spaces between consonant and hyphen/virama
            text = re.sub(r'(\w)\s+-\s*(\w)', r'\1-\2', text)

            # 3. Clean up lines & spacing
            lines = text.split('\n')
            cleaned_lines = []
            for line in lines:
                line_rstripped = line.rstrip()
                # Collapse multiple spaces into 1 space
                line_cleaned = re.sub(r'[ \t]{2,}', ' ', line_rstripped)
                # Fix space before single/double virama (e.g., " ॥" -> " ॥")
                line_cleaned = re.sub(r'\s+([।॥])', r' \1', line_cleaned)
                cleaned_lines.append(line_cleaned)

            text = "\n".join(cleaned_lines)

            if text != original_text:
                cleaned_slokas += 1
                issues_found.append((d_no, s_no, original_text, text))
                sloka["text"] = text

    print(f"Audited {total_dasakams} Dasakams and {total_slokas} Slokas.")
    print(f"Fixed formatting & typos in {cleaned_slokas} slokas!")

    if issues_found:
        print("\nSample fixed slokas:")
        for d_no, s_no, orig, cleaned in issues_found[:5]:
            print(f"\n--- Dasakam {d_no} Sloka {s_no} ---")
            print("Before:\n", orig)
            print("After:\n", cleaned)

    # Save cleaned JSON back
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\nSuccessfully updated {json_path} with cleaned sloka text!")

if __name__ == "__main__":
    audit_and_clean_slokas()
