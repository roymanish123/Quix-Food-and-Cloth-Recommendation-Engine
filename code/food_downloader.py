# =============================================================================
# food_downloader.py — Parallel Food Downloader with Skip Completed
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
    SEASON_MAP, MONTH_FOLDERS, AVG_TEMP,
    FOOD_QUERIES, IMAGES_PER_FOLDER, MAX_WORKERS, MAX_NUM_PER_QUERY,
    COMPLETED_LOCATIONS
)

logging.getLogger("icrawler").setLevel(logging.CRITICAL)
logging.getLogger("urllib3").setLevel(logging.CRITICAL)

FOOD_HASH_REGISTRY = set()
FOOD_HASH_LOCK = Lock()

MEAL_PREFERENCES = ["veg", "vegan", "egg", "non_veg"]
FOOD_TIMES = ["breakfast", "lunch", "dinner", "snack"]

FOOD_FALLBACK_QUERIES = {
    "dubai":    ["dubai restaurant food dish arabic", "middle east food cuisine plate", "dubai meal food"],
    "paris":    ["paris french restaurant food", "french cuisine bistro dish", "paris cafe food"],
    "jungfrau": ["swiss food dish restaurant alpine", "switzerland cuisine food plate", "alpine restaurant meal"],
    "miami":    ["miami restaurant food dish", "miami beach food cuisine", "florida restaurant food plate"],
}


def get_file_hash(filepath):
    try:
        with open(filepath, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()
    except Exception:
        return None


def generate_food_metadata_json(folder_path, image_files, location, meal_pref,
                                 month_num, month_folder, season, time_of_day, queries_data):
    month_display = month_folder.replace("_", " ").title()
    avg_temp = AVG_TEMP[location][month_num]

    items = []
    for i, filename in enumerate(image_files):
        q_idx = i % len(queries_data) if queries_data else 0
        if queries_data:
            _, dish_name, food_category = queries_data[q_idx]
        else:
            dish_name = f"{location.title()} {meal_pref.title()} {time_of_day.title()} Dish"
            food_category = "placeholder"

        items.append({
            "filename": filename,
            "dish_name": dish_name,
            "food_category": food_category,
            "meal_preference": meal_pref,
            "time_of_day": time_of_day,
            "description": f"{dish_name} — {location.title()} {season} {time_of_day}",
            "restaurant_name": "placeholder - needs manual review",
            "price_range": "placeholder - needs manual review",
            "dietary_note": f"Suitable for {meal_pref} preference"
        })

    metadata = {
        "folder_context": {
            "location": location.title(),
            "meal_preference": meal_pref,
            "month": month_display,
            "month_number": month_num,
            "season": season.title(),
            "time_of_day": time_of_day.title(),
            "avg_temperature_celsius": avg_temp
        },
        "items": items
    }

    with open(os.path.join(folder_path, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)


def run_query(query, temp_dir, max_num):
    try:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir, exist_ok=True)
        crawler = BingImageCrawler(storage={"root_dir": temp_dir}, log_level=logging.CRITICAL)
        crawler.crawl(keyword=query, max_num=max_num)
        return [os.path.join(temp_dir, f) for f in os.listdir(temp_dir) if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))]
    except Exception:
        return []


def download_food_folder(task):
    final_folder = task["final_folder"]
    queries_list = task["queries_list"]
    target_count = task["target_count"]
    location     = task["location"]
    meal_pref    = task["meal_pref"]
    month_num    = task["month_num"]
    month_folder = task["month_folder"]
    season       = task["season"]
    time_of_day  = task["time_of_day"]
    temp_base    = task["temp_base"]

    os.makedirs(final_folder, exist_ok=True)

    existing = [f for f in os.listdir(final_folder) if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))]
    if len(existing) >= target_count:
        generate_food_metadata_json(final_folder, sorted(existing), location, meal_pref,
                                    month_num, month_folder, season, time_of_day, queries_list)
        return f"⏭️  SKIP {meal_pref}/{month_folder}/{season}/{time_of_day} — {len(existing)} imgs"

    collected = list(existing)
    all_queries = [q[0] for q in queries_list]
    fallbacks = FOOD_FALLBACK_QUERIES.get(location, [])

    safe_name = f"{location}_{meal_pref}_{month_folder}_{season}_{time_of_day}".replace("/", "_")
    temp_dir = os.path.join(temp_base, safe_name)

    for query in all_queries + fallbacks:
        if len(collected) >= target_count:
            break
        needed = target_count - len(collected)
        file_paths = run_query(query, temp_dir, max(MAX_NUM_PER_QUERY, needed * 2))
        if not file_paths:
            continue
        for fpath in file_paths:
            if len(collected) >= target_count:
                break
            file_hash = get_file_hash(fpath)
            if file_hash is None:
                continue
            with FOOD_HASH_LOCK:
                if file_hash in FOOD_HASH_REGISTRY:
                    continue
                FOOD_HASH_REGISTRY.add(file_hash)
            img_index = len(collected) + 1
            shutil.copy2(fpath, os.path.join(final_folder, f"img_{img_index:03d}.jpg"))
            collected.append(f"img_{img_index:03d}.jpg")

    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir, ignore_errors=True)

    final_images = sorted([f for f in os.listdir(final_folder) if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))])
    generate_food_metadata_json(final_folder, final_images, location, meal_pref,
                                month_num, month_folder, season, time_of_day, queries_list)

    status = "✅" if len(final_images) >= target_count else "⚠️ "
    return f"{status} {meal_pref}/{month_folder}/{season}/{time_of_day} → {len(final_images)}/{target_count}"


def build_food_tasks(location):
    tasks = []
    temp_base = os.path.join("dataset", "_temp", "food")
    location_food = FOOD_QUERIES.get(location, {})

    for meal_pref in MEAL_PREFERENCES:
        meal_data = location_food.get(meal_pref, {})
        for month_num in range(1, 13):
            month_folder = MONTH_FOLDERS[month_num]
            season = SEASON_MAP[location][month_num]
            season_data = meal_data.get(season, {})
            for time_of_day in FOOD_TIMES:
                queries_list = season_data.get(time_of_day, [])
                final_folder = os.path.join("dataset", "food", "images", location, meal_pref, month_folder, season, time_of_day)

                if not queries_list:
                    os.makedirs(final_folder, exist_ok=True)
                    generate_food_metadata_json(final_folder, [], location, meal_pref, month_num, month_folder, season, time_of_day, [])
                    continue

                tasks.append({
                    "final_folder": final_folder,
                    "queries_list": queries_list,
                    "target_count": IMAGES_PER_FOLDER,
                    "location": location,
                    "meal_pref": meal_pref,
                    "month_num": month_num,
                    "month_folder": month_folder,
                    "season": season,
                    "time_of_day": time_of_day,
                    "temp_base": temp_base,
                })
    return tasks


def download_food_location(location):
    if location in COMPLETED_LOCATIONS:
        print(f"\n⏭️  SKIPPING FOOD {location.upper()} — already in COMPLETED_LOCATIONS")
        return

    print(f"\n{'='*60}")
    print(f"🍽️  FOOD — {location.upper()} | {MAX_WORKERS} parallel threads")
    print(f"{'='*60}")

    tasks = build_food_tasks(location)
    total = len(tasks)
    done = 0
    print(f"   📋 Folders to download: {total}")

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(download_food_folder, t): t for t in tasks}
        for future in as_completed(futures):
            result = future.result()
            done += 1
            print(f"   [{done:>3}/{total}] {result}")

    shutil.rmtree(os.path.join("dataset", "_temp", "food"), ignore_errors=True)
    print(f"\n✅ FOOD {location.upper()} complete")