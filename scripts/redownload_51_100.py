import os
import json
import urllib.request
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

json_path = os.path.join("src", "data", "narayaneeyam_data.json")

def extract_file_id(drive_url):
    if not drive_url: return None
    if "/d/" in drive_url:
        return drive_url.split("/d/")[1].split("/")[0].split("?")[0]
    if "id=" in drive_url:
        return drive_url.split("id=")[1].split("&")[0]
    return None

def is_valid_mp3(file_path):
    if not os.path.exists(file_path):
        return False
    try:
        with open(file_path, 'rb') as f:
            header = f.read(200)
            if b'<!DOCTYPE html>' in header or b'<!doctype html>' in header or b'<html' in header:
                return False
            # Check for ID3 header or MP3 frame sync
            if header.startswith(b'ID3') or header.startswith(b'\xff\xfb') or header.startswith(b'\xff\xf3') or header.startswith(b'\xff\xf2'):
                return True
            # Also allow general binary audio if not HTML
            return True
    except Exception:
        return False

def download_audio_task(item):
    file_id, dest_path = item
    if is_valid_mp3(dest_path):
        return dest_path, True, "Already Valid"
        
    if not file_id:
        return dest_path, False, "No File ID"
        
    # Remove bad HTML file if present
    if os.path.exists(dest_path):
        try:
            os.remove(dest_path)
        except Exception:
            pass

    dl_url = f"https://drive.usercontent.google.com/download?id={file_id}&export=download"
    try:
        req = urllib.request.Request(
            dl_url,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req, timeout=15) as resp, open(dest_path, 'wb') as out_f:
            out_f.write(resp.read())
            
        if is_valid_mp3(dest_path):
            return dest_path, True, "Downloaded OK"
        else:
            return dest_path, False, "Still Google Login HTML"
    except Exception as e:
        return dest_path, False, str(e)

def redownload_invalid_audio():
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    download_queue = []
    
    for d in data.get("dasakams", []):
        d_no = d.get("number")
        for s in d.get("slokas", []):
            s_no = s.get("slokaNo")
            drive_url = s.get("driveUrl", "")
            mp3_path = os.path.join("public", "audio", f"dasakam{d_no}", f"sloka_{s_no}.mp3")
            
            if not is_valid_mp3(mp3_path):
                file_id = extract_file_id(drive_url)
                if file_id:
                    download_queue.append((file_id, mp3_path))

    print(f"Found {len(download_queue)} invalid / un-downloaded audio files.")
    if not download_queue:
        print("All audio files are valid real MP3s!")
        return

    print(f"Attempting to re-download {len(download_queue)} audio files using 16 parallel workers...")
    success_count = 0
    fail_count = 0

    with ThreadPoolExecutor(max_workers=16) as executor:
        futures = [executor.submit(download_audio_task, item) for item in download_queue]
        for f in as_completed(futures):
            dest, success, status = f.result()
            if success and status == "Downloaded OK":
                success_count += 1
            else:
                fail_count += 1

    print(f"\nResults: Successfully downloaded {success_count} real MP3 files. Failed/Login blocked: {fail_count}.")

if __name__ == "__main__":
    redownload_invalid_audio()
