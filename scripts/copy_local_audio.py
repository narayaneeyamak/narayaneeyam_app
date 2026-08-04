import os
import sys
import json
import shutil
import re

base_dir = r"C:\Users\Lenovo\Downloads\Narayaneeyam D51 to D100 split audios-20260804T065954Z-1-001\Narayaneeyam D51 to D100 split audios"
json_path = os.path.join("src", "data", "narayaneeyam_data.json")

def process_local_audio():
    if not os.path.exists(base_dir):
        print(f"Error: {base_dir} not found")
        sys.exit(1)

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    mapped_count = 0
    missing_count = 0

    for dasakam in data.get("dasakams", []):
        d_no = dasakam.get("number")
        if d_no < 51:
            continue

        # Look for folder named "Dasaka 51" or "Dasaka51" or "Dasakam 51"
        folder_candidates = [
            f"Dasaka {d_no}",
            f"Dasaka{d_no}",
            f"Dasakam {d_no}",
            f"Dasakam{d_no}",
            f"dasaka {d_no}",
            f"dasaka{d_no}"
        ]

        target_folder = None
        for candidate in folder_candidates:
            possible_path = os.path.join(base_dir, candidate)
            if os.path.exists(possible_path):
                target_folder = possible_path
                break

        if not target_folder:
            print(f"Warning: Folder for Dasakam {d_no} not found in {base_dir}")
            continue

        # Target directory in public/audio/dasakamX/
        public_dest_dir = os.path.join("public", "audio", f"dasakam{d_no}")
        os.makedirs(public_dest_dir, exist_ok=True)

        # List all audio files in the folder
        audio_files = [f for f in os.listdir(target_folder) if f.lower().endswith(('.m4a', '.mp3', '.wav', '.aac'))]

        # Build map from sloka_no -> filename
        # Pattern: D51 (1).m4a or D51(1).m4a or 1.m4a
        file_map = {}
        for fname in audio_files:
            match = re.search(r'\((\d+)\)', fname)
            if match:
                s_no = int(match.group(1))
                file_map[s_no] = fname
            else:
                num_match = re.search(r'\d+', fname)
                if num_match:
                    s_no = int(num_match.group(0))
                    file_map[s_no] = fname

        for sloka in dasakam.get("slokas", []):
            s_no = sloka.get("slokaNo")
            matched_fname = file_map.get(s_no)

            if matched_fname:
                src_file_path = os.path.join(target_folder, matched_fname)
                ext = os.path.splitext(matched_fname)[1].lower()
                dest_filename = f"sloka_{s_no}{ext}"
                dest_file_path = os.path.join(public_dest_dir, dest_filename)

                # Copy file
                shutil.copy2(src_file_path, dest_file_path)

                # Update audioUrl in JSON
                sloka["audioUrl"] = f"/audio/dasakam{d_no}/{dest_filename}"
                mapped_count += 1
            else:
                print(f"  Missing local audio for Dasakam {d_no} Sloka {s_no}")
                missing_count += 1

    # Save updated JSON
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n=======================================================")
    print(f"SUCCESS! Mapped and copied {mapped_count} audio files into public/audio/")
    if missing_count > 0:
        print(f"Warning: {missing_count} slokas were missing audio files.")
    print(f"Updated {json_path}!")
    print(f"=======================================================")

if __name__ == "__main__":
    process_local_audio()
