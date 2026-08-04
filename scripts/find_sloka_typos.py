import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
json_path = os.path.join("src", "data", "narayaneeyam_data.json")

# Dictionary of known OCR/Excel typos in Srimad Narayaneeyam Telugu text -> corrected text
TEXT_CORRECTIONS = {
    "మనీ షితం": "మనీషితం",
    "భూ మన్": "భూమన్",
    "దృ ష్ట": "దృష్ట",
    "భూ తై": "భూతై",
    "నిష్క ళ": "నిష్కళ",
    "త్వత్కలాస్వేవ భూ మన్": "త్వత్కలాస్వేవ భూమన్",
    "పద్మ పత్ర": "పద్మపత్ర",
    "సారార్-ద్రం": "సారార్ద్రం",
    "సార్-ద్రం": "సార్ద్రం",
    "అంతః-": "అంతః",
    "త్వత్-": "త్వత్",
    "యత్-": "యత్",
    "నిర్-": "నిర్",
    "తత్-": "తత్"
}

def clean_all_slokas():
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    fixed_count = 0

    for dasakam in data.get("dasakams", []):
        d_no = dasakam.get("number")
        for sloka in dasakam.get("slokas", []):
            s_no = sloka.get("slokaNo")
            text = sloka.get("text", "")
            orig = text

            # Apply specific corrections
            for err, corr in TEXT_CORRECTIONS.items():
                text = text.replace(err, corr)

            # Fix hyphenated Sanskrit prefixes like "త్వత్-పాద" -> "త్వత్పాద", "సత్త్వ-రూపం" -> "సత్త్వరూపం"
            text = re.sub(r'([\u0C00-\u0C7F]+)-\s*([\u0C00-\u0C7F]+)', r'\1\2', text)

            # Fix space before comma or punctuation
            text = re.sub(r'\s+,', ',', text)

            if text != orig:
                fixed_count += 1
                sloka["text"] = text

    print(f"Cleaned and polished {fixed_count} additional slokas!")

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Saved pristine text to {json_path}!")

if __name__ == "__main__":
    clean_all_slokas()
