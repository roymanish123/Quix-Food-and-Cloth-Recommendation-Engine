# =============================================================================
# downloader.py — Parallel Downloader with Smart Fallbacks + Skip Completed
# =============================================================================

import os
import json
import hashlib
import shutil
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from icrawler.builtin import BingImageCrawler
from config import (
    SEASON_MAP, MONTH_FOLDERS, AVG_TEMP, WEATHER_NOTES,
    TIMES_OF_DAY, GENDERS, CLOTHES_QUERIES, UNISEX_QUERIES,
    IMAGES_PER_FOLDER, MAX_WORKERS, MAX_NUM_PER_QUERY,
    COMPLETED_LOCATIONS
)

logging.getLogger("icrawler").setLevel(logging.CRITICAL)
logging.getLogger("urllib3").setLevel(logging.CRITICAL)
logging.getLogger("requests").setLevel(logging.CRITICAL)

GLOBAL_HASH_REGISTRY = set()
HASH_LOCK = Lock()

FALLBACK_QUERIES = {
    "dubai":    ["dubai fashion outfit street style", "dubai clothing casual outfit", "dubai traditional fashion"],
    "paris":    ["paris fashion street style outfit", "parisian clothing style fashion", "paris casual fashion"],
    "jungfrau": ["alpine mountain outfit winter clothing", "ski resort fashion clothing", "mountain hiking clothing"],
    "miami":    ["miami beach fashion outfit", "miami casual street style", "beach summer clothing outfit"],
}


def get_file_hash(filepath):
    try:
        with open(filepath, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()
    except Exception:
        return None


def generate_metadata_json(folder_path, image_files, location, gender,
                            month_num, month_name, season, time_of_day, queries_data):
    month_display = month_name.replace("_", " ").title()
    avg_temp = AVG_TEMP[location][month_num]
    weather_note = WEATHER_NOTES[location][season]

    items = []
    for i, filename in enumerate(image_files):
        q_idx = i % len(queries_data) if queries_data else 0
        if queries_data:
            _, item_name, category, occasion = queries_data[q_idx]
        else:
            item_name = f"{location.title()} {gender.title()} {season.title()} {time_of_day.title()} Outfit"
            category = "placeholder"
            occasion = "placeholder"

        items.append({
            "filename": filename,
            "item_name": item_name,
            "category": category,
            "color": "placeholder - needs manual review",
            "occasion": occasion,
            "description": f"Outfit for {location.title()} in {month_display} ({season}) during {time_of_day}",
            "price_range": "placeholder - needs manual review",
            "cultural_note": f"Appropriate for {location.title()}"
        })

    metadata = {
        "folder_context": {
            "location": location.title(),
            "gender": gender.title(),
            "month": month_display,
            "month_number": month_num,
            "season": season.title(),
            "time_of_day": time_of_day.title(),
            "avg_temperature_celsius": avg_temp,
            "weather_note": weather_note
        },
        "items": items
    }

    with open(os.path.join(folder_path, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)


def run_single_query(query, temp_dir, max_num):
    try:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir, exist_ok=True)
        crawler = BingImageCrawler(storage={"root_dir": temp_dir}, log_level=logging.CRITICAL)
        crawler.crawl(keyword=query, max_num=max_num)
        return [
            os.path.join(temp_dir, f)
            for f in os.listdir(temp_dir)
            if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
        ]
    except Exception:
        return []


def download_one_folder(task):
    final_folder = task["final_folder"]
    queries_list = task["queries_list"]
    target_count = task["target_count"]
    location     = task["location"]
    gender       = task["gender"]
    month_num    = task["month_num"]
    month_folder = task["month_folder"]
    season       = task["season"]
    time_of_day  = task["time_of_day"]
    temp_base    = task["temp_base"]

    os.makedirs(final_folder, exist_ok=True)

    existing = [f for f in os.listdir(final_folder) if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))]
    if len(existing) >= target_count:
        generate_metadata_json(final_folder, sorted(existing), location, gender,
                               month_num, month_folder, season, time_of_day, queries_list)
        return f"⏭️  SKIP {gender}/{month_folder}/{season}/{time_of_day} — {len(existing)} imgs already"

    collected = list(existing)
    all_queries = [q[0] for q in queries_list]
    fallbacks = FALLBACK_QUERIES.get(location, [])

    safe_name = f"{location}_{gender}_{month_folder}_{season}_{time_of_day}".replace("/", "_")
    temp_dir = os.path.join(temp_base, safe_name)

    for query in all_queries + fallbacks:
        if len(collected) >= target_count:
            break
        needed = target_count - len(collected)
        file_paths = run_single_query(query, temp_dir, max(MAX_NUM_PER_QUERY, needed * 2))
        if not file_paths:
            continue
        for fpath in file_paths:
            if len(collected) >= target_count:
                break
            file_hash = get_file_hash(fpath)
            if file_hash is None:
                continue
            with HASH_LOCK:
                if file_hash in GLOBAL_HASH_REGISTRY:
                    continue
                GLOBAL_HASH_REGISTRY.add(file_hash)
            img_index = len(collected) + 1
            final_filename = f"img_{img_index:03d}.jpg"
            shutil.copy2(fpath, os.path.join(final_folder, final_filename))
            collected.append(final_filename)

    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir, ignore_errors=True)

    final_images = sorted([f for f in os.listdir(final_folder) if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))])
    generate_metadata_json(final_folder, final_images, location, gender,
                           month_num, month_folder, season, time_of_day, queries_list)

    status = "✅" if len(final_images) >= target_count else "⚠️ "
    return f"{status} {gender}/{month_folder}/{season}/{time_of_day} → {len(final_images)}/{target_count}"


def build_clothes_tasks(location):
    tasks = []
    temp_base = os.path.join("dataset", "_temp", "clothes")

    for gender in GENDERS:
        query_source = UNISEX_QUERIES.get(location, {}) if gender == "unisex" else CLOTHES_QUERIES.get(location, {}).get(gender, {})

        for month_num in range(1, 13):
            month_folder = MONTH_FOLDERS[month_num]
            season = SEASON_MAP[location][month_num]
            season_queries = query_source.get(season, {})

            for time_of_day in TIMES_OF_DAY:
                tod_queries = season_queries.get(time_of_day, [])
                final_folder = os.path.join("dataset", "clothes", "images", location, gender, month_folder, season, time_of_day)

                if not tod_queries:
                    os.makedirs(final_folder, exist_ok=True)
                    generate_metadata_json(final_folder, [], location, gender, month_num, month_folder, season, time_of_day, [])
                    continue

                tasks.append({
                    "final_folder": final_folder,
                    "queries_list": tod_queries,
                    "target_count": IMAGES_PER_FOLDER,
                    "location": location,
                    "gender": gender,
                    "month_num": month_num,
                    "month_folder": month_folder,
                    "season": season,
                    "time_of_day": time_of_day,
                    "temp_base": temp_base,
                })
    return tasks


def download_clothes_location(location):
    if location in COMPLETED_LOCATIONS:
        print(f"\n⏭️  SKIPPING {location.upper()} — already in COMPLETED_LOCATIONS")
        return

    print(f"\n{'='*60}")
    print(f"📍 CLOTHES — {location.upper()} | {MAX_WORKERS} parallel threads")
    print(f"{'='*60}")

    tasks = build_clothes_tasks(location)
    total = len(tasks)
    done = 0
    print(f"   📋 Folders to download: {total}")

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(download_one_folder, t): t for t in tasks}
        for future in as_completed(futures):
            result = future.result()
            done += 1
            print(f"   [{done:>3}/{total}] {result}")

    shutil.rmtree(os.path.join("dataset", "_temp", "clothes"), ignore_errors=True)
    print(f"\n✅ CLOTHES {location.upper()} complete")