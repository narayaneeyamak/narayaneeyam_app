import json
import os
import sys
import urllib.request
import re

def download_drive_audio():
    json_path = os.path.join("src", "data", "narayaneeyam_data.json")
    if not os.path.exists(json_path):
        print("Data json not found")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    os.makedirs(os.path.join("public", "audio", "dasakam1"), exist_ok=True)
    
    dasakam1 = data["dasakams"][0]
    for s in dasakam1["slokas"]:
        url = s.get("audioUrl", "")
        if not url or "/d/" not in url:
            continue
        
        file_id = url.split("/d/")[1].split("/")[0]
        sloka_no = s["slokaNo"]
        dl_url = f"https://drive.usercontent.google.com/download?id={file_id}&export=download"
        dest_path = os.path.join("public", "audio", "dasakam1", f"sloka_{sloka_no}.mp3")
        
        print(f"Downloading Sloka {sloka_no} (File ID: {file_id})...")
        try:
            req = urllib.request.Request(
                dl_url,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            )
            with urllib.request.urlopen(req) as resp, open(dest_path, 'wb') as out_f:
                out_f.write(resp.read())
            
            size = os.path.getsize(dest_path)
            print(f"  -> Success: {dest_path} ({size} bytes)")
        except Exception as e:
            print(f"  -> Download failed: {e}")

if __name__ == "__main__":
    download_drive_audio()
