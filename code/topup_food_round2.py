# =============================================================================
# topup_food_round2.py — Round 2 Top-Up for Remaining Under-filled Food Folders
# These are folders that still had < 15 images after the first topup_food.py run.
# Uses even broader, more reliable food queries to guarantee Bing results.
# Run from: C:\Users\MANISH\Downloads\Quix_Recommendation_engine\code\
# =============================================================================

import os
import json
import hashlib
import shutil
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from icrawler.builtin import BingImageCrawler

logging.getLogger("icrawler").setLevel(logging.CRITICAL)
logging.getLogger("urllib3").setLevel(logging.CRITICAL)
logging.getLogger("requests").setLevel(logging.CRITICAL)

TARGET        = 15
TOPUP_WORKERS = 3
MAX_NUM       = 50        # higher than round 1 — stubborn folders need more attempts
TEMP_BASE     = "dataset/_temp_food_topup_r2"
BASE_PATH     = "dataset/food/images"

HASH_REGISTRY = set()
HASH_LOCK     = Lock()

# =============================================================================
# ALL 162 FOLDERS — parsed exactly from your 4 location files
# (location, meal_pref, month_folder, season, time_of_day, current_count)
# NOTE: jungfrau/non_veg/11_november/winter/breakfast was listed under "0 images"
#       but the file annotation says "- 4", so we treat it as 4 images.
# =============================================================================
TOPUP_FOLDERS = [

    # ================================================================
    # DUBAI — only vegan folders remain unfilled
    # ================================================================
    # 0 images
    ("dubai", "vegan", "02_february", "mild", "lunch",      0),
    ("dubai", "vegan", "02_february", "mild", "snack",      0),
    ("dubai", "vegan", "04_april",    "warm", "dinner",     0),
    ("dubai", "vegan", "04_april",    "warm", "snack",      0),
    ("dubai", "vegan", "05_may",      "hot",  "snack",      0),
    ("dubai", "vegan", "06_june",     "hot",  "breakfast",  0),
    ("dubai", "vegan", "06_june",     "hot",  "lunch",      0),
    ("dubai", "vegan", "06_june",     "hot",  "snack",      0),
    ("dubai", "vegan", "07_july",     "hot",  "lunch",      0),
    ("dubai", "vegan", "08_august",   "hot",  "breakfast",  0),
    ("dubai", "vegan", "08_august",   "hot",  "dinner",     0),
    ("dubai", "vegan", "08_august",   "hot",  "lunch",      0),
    ("dubai", "vegan", "08_august",   "hot",  "snack",      0),
    ("dubai", "vegan", "09_september","hot",  "breakfast",  0),
    ("dubai", "vegan", "09_september","hot",  "dinner",     0),
    ("dubai", "vegan", "09_september","hot",  "lunch",      0),
    ("dubai", "vegan", "09_september","hot",  "snack",      0),
    ("dubai", "vegan", "10_october",  "warm", "dinner",     0),
    ("dubai", "vegan", "11_november", "mild", "dinner",     0),
    ("dubai", "vegan", "11_november", "mild", "lunch",      0),
    ("dubai", "vegan", "11_november", "mild", "snack",      0),
    ("dubai", "vegan", "12_december", "mild", "breakfast",  0),
    ("dubai", "vegan", "12_december", "mild", "lunch",      0),
    ("dubai", "vegan", "12_december", "mild", "dinner",     0),
    # 1 image
    ("dubai", "vegan", "03_march",    "warm", "lunch",      1),
    ("dubai", "vegan", "04_april",    "warm", "lunch",      1),
    ("dubai", "vegan", "05_may",      "hot",  "lunch",      1),
    ("dubai", "vegan", "06_june",     "hot",  "dinner",     1),
    ("dubai", "vegan", "07_july",     "hot",  "breakfast",  1),
    ("dubai", "vegan", "07_july",     "hot",  "dinner",     1),
    ("dubai", "vegan", "10_october",  "warm", "lunch",      1),
    ("dubai", "vegan", "10_october",  "warm", "snack",      1),
    ("dubai", "vegan", "11_november", "mild", "breakfast",  1),
    # 2 images
    ("dubai", "vegan", "07_july",     "hot",  "snack",      2),
    # 3 images
    ("dubai", "vegan", "05_may",      "hot",  "dinner",     3),
    # 4 images
    ("dubai", "vegan", "02_february", "mild", "dinner",     4),
    # 5 images
    ("dubai", "veg",   "11_november", "mild", "lunch",      5),
    ("dubai", "veg",   "12_december", "mild", "breakfast",  5),
    ("dubai", "vegan", "02_february", "mild", "breakfast",  5),
    ("dubai", "vegan", "03_march",    "warm", "dinner",     5),

    # ================================================================
    # MIAMI
    # ================================================================
    # 0 images
    ("miami", "egg",     "06_june",     "summer", "lunch",     0),
    ("miami", "egg",     "08_august",   "summer", "dinner",    0),
    ("miami", "egg",     "08_august",   "summer", "lunch",     0),
    ("miami", "egg",     "10_october",  "autumn", "breakfast", 0),
    ("miami", "egg",     "10_october",  "autumn", "dinner",    0),
    ("miami", "egg",     "10_october",  "autumn", "lunch",     0),
    ("miami", "egg",     "11_november", "autumn", "breakfast", 0),
    ("miami", "egg",     "11_november", "autumn", "lunch",     0),
    ("miami", "egg",     "12_december", "winter", "snack",     0),
    ("miami", "non_veg", "04_april",    "spring", "breakfast", 0),
    ("miami", "non_veg", "04_april",    "spring", "dinner",    0),
    ("miami", "non_veg", "07_july",     "summer", "breakfast", 0),
    ("miami", "non_veg", "07_july",     "summer", "lunch",     0),
    ("miami", "non_veg", "08_august",   "summer", "breakfast", 0),
    ("miami", "non_veg", "08_august",   "summer", "lunch",     0),
    ("miami", "non_veg", "08_august",   "summer", "snack",     0),
    ("miami", "non_veg", "09_september","autumn", "lunch",     0),
    ("miami", "non_veg", "10_october",  "autumn", "dinner",    0),
    ("miami", "non_veg", "10_october",  "autumn", "lunch",     0),
    ("miami", "non_veg", "11_november", "autumn", "breakfast", 0),
    ("miami", "non_veg", "11_november", "autumn", "dinner",    0),
    ("miami", "non_veg", "11_november", "autumn", "lunch",     0),
    ("miami", "non_veg", "11_november", "autumn", "snack",     0),
    ("miami", "non_veg", "12_december", "winter", "snack",     0),
    ("miami", "vegan",   "08_august",   "summer", "lunch",     0),
    ("miami", "vegan",   "09_september","autumn", "dinner",    0),
    ("miami", "vegan",   "10_october",  "autumn", "dinner",    0),
    ("miami", "vegan",   "10_october",  "autumn", "lunch",     0),
    ("miami", "vegan",   "11_november", "autumn", "breakfast", 0),
    ("miami", "vegan",   "11_november", "autumn", "dinner",    0),
    ("miami", "vegan",   "11_november", "autumn", "lunch",     0),
    ("miami", "vegan",   "11_november", "autumn", "snack",     0),
    ("miami", "vegan",   "12_december", "winter", "snack",     0),
    # 1 image
    ("miami", "egg",     "11_november", "autumn", "dinner",    1),
    ("miami", "egg",     "12_december", "winter", "dinner",    1),
    ("miami", "non_veg", "07_july",     "summer", "snack",     1),
    ("miami", "veg",     "08_august",   "summer", "lunch",     1),
    ("miami", "vegan",   "02_february", "winter", "snack",     1),
    ("miami", "vegan",   "04_april",    "spring", "snack",     1),
    ("miami", "vegan",   "05_may",      "summer", "dinner",    1),
    ("miami", "vegan",   "06_june",     "summer", "lunch",     1),
    ("miami", "vegan",   "07_july",     "summer", "snack",     1),
    ("miami", "vegan",   "07_july",     "summer", "lunch",     1),
    ("miami", "vegan",   "09_september","autumn", "snack",     1),
    # 2 images
    ("miami", "egg",     "04_april",    "spring", "breakfast", 2),
    ("miami", "egg",     "04_april",    "spring", "dinner",    2),
    ("miami", "egg",     "04_april",    "spring", "lunch",     2),
    ("miami", "egg",     "07_july",     "summer", "snack",     2),
    ("miami", "egg",     "08_august",   "summer", "snack",     2),
    ("miami", "egg",     "12_december", "winter", "lunch",     2),
    ("miami", "veg",     "09_september","autumn", "dinner",    2),
    ("miami", "vegan",   "09_september","autumn", "breakfast", 2),
    ("miami", "vegan",   "09_september","autumn", "lunch",     2),
    ("miami", "vegan",   "10_october",  "autumn", "breakfast", 2),
    # 3 images
    ("miami", "egg",     "02_february", "winter", "lunch",     3),
    ("miami", "egg",     "04_april",    "spring", "snack",     3),
    ("miami", "egg",     "06_june",     "summer", "dinner",    3),
    ("miami", "egg",     "07_july",     "summer", "lunch",     3),
    ("miami", "egg",     "09_september","autumn", "dinner",    3),
    ("miami", "egg",     "09_september","autumn", "lunch",     3),
    ("miami", "egg",     "11_november", "autumn", "snack",     3),
    ("miami", "vegan",   "02_february", "winter", "dinner",    3),
    ("miami", "vegan",   "04_april",    "spring", "lunch",     3),
    ("miami", "vegan",   "06_june",     "summer", "dinner",    3),
    ("miami", "vegan",   "06_june",     "summer", "snack",     3),
    ("miami", "vegan",   "07_july",     "summer", "dinner",    3),
    ("miami", "vegan",   "12_december", "winter", "dinner",    3),
    ("miami", "vegan",   "12_december", "winter", "lunch",     3),
    # 4 images
    ("miami", "egg",     "02_february", "winter", "dinner",    4),
    ("miami", "egg",     "06_june",     "summer", "breakfast", 4),
    ("miami", "egg",     "07_july",     "summer", "breakfast", 4),
    ("miami", "egg",     "12_december", "winter", "breakfast", 4),
    ("miami", "vegan",   "03_march",    "spring", "breakfast", 4),
    ("miami", "vegan",   "03_march",    "spring", "snack",     4),
    # 5 images
    ("miami", "egg",     "03_march",    "spring", "lunch",     5),
    ("miami", "egg",     "05_may",      "summer", "snack",     5),
    ("miami", "veg",     "07_july",     "summer", "dinner",    5),

    # ================================================================
    # PARIS
    # ================================================================
    # 0 images — all veg folders
    ("paris", "veg",   "08_august",   "summer", "dinner",    0),
    ("paris", "veg",   "09_september","autumn", "breakfast", 0),
    ("paris", "veg",   "09_september","autumn", "dinner",    0),
    ("paris", "veg",   "09_september","autumn", "lunch",     0),
    ("paris", "veg",   "10_october",  "autumn", "lunch",     0),
    ("paris", "veg",   "11_november", "autumn", "lunch",     0),
    ("paris", "veg",   "11_november", "autumn", "snack",     0),
    ("paris", "veg",   "12_december", "winter", "breakfast", 0),
    ("paris", "veg",   "12_december", "winter", "dinner",    0),
    ("paris", "veg",   "12_december", "winter", "lunch",     0),
    # 1 image
    ("paris", "vegan", "07_july",     "summer", "snack",     1),
    ("paris", "vegan", "12_december", "winter", "lunch",     1),
    ("paris", "veg",   "06_june",     "summer", "lunch",     1),
    ("paris", "veg",   "07_july",     "summer", "dinner",    1),
    ("paris", "veg",   "09_september","autumn", "snack",     1),
    ("paris", "veg",   "10_october",  "autumn", "snack",     1),
    ("paris", "veg",   "11_november", "autumn", "dinner",    1),
    # 2 images
    ("paris", "vegan", "04_april",    "spring", "dinner",    2),
    ("paris", "vegan", "05_may",      "spring", "breakfast", 2),
    ("paris", "vegan", "05_may",      "spring", "snack",     2),
    ("paris", "vegan", "06_june",     "summer", "snack",     2),
    ("paris", "veg",   "08_august",   "summer", "lunch",     2),
    ("paris", "veg",   "10_october",  "autumn", "breakfast", 2),
    ("paris", "veg",   "10_october",  "autumn", "dinner",    2),
    # 3 images
    ("paris", "veg",   "07_july",     "summer", "lunch",     3),
    ("paris", "veg",   "08_august",   "summer", "snack",     3),
    ("paris", "veg",   "11_november", "autumn", "breakfast", 3),
    ("paris", "veg",   "12_december", "winter", "snack",     3),
    # 4 images
    ("paris", "vegan", "07_july",     "summer", "lunch",     4),
    ("paris", "vegan", "09_september","autumn", "dinner",    4),
    ("paris", "veg",   "07_july",     "summer", "snack",     4),
    # 5 images
    ("paris", "vegan", "05_may",      "spring", "dinner",    5),
    ("paris", "vegan", "06_june",     "summer", "lunch",     5),
    ("paris", "vegan", "07_july",     "summer", "breakfast", 5),
    ("paris", "non_veg","09_september","autumn", "lunch",    5),

    # ================================================================
    # JUNGFRAU
    # ================================================================
    # 1 image
    ("jungfrau", "non_veg", "03_march",    "winter", "breakfast", 1),
    ("jungfrau", "non_veg", "09_september","autumn", "breakfast", 1),
    ("jungfrau", "non_veg", "10_october",  "autumn", "breakfast", 1),
    # 3 images
    ("jungfrau", "non_veg", "02_february", "winter", "breakfast", 3),
    ("jungfrau", "non_veg", "08_august",   "summer", "breakfast", 3),
    ("jungfrau", "non_veg", "10_october",  "autumn", "lunch",     3),
    # 4 images
    ("jungfrau", "non_veg", "05_may",      "spring", "lunch",     4),
    ("jungfrau", "non_veg", "10_october",  "autumn", "dinner",    4),
    ("jungfrau", "non_veg", "11_november", "winter", "breakfast", 4),
    ("jungfrau", "veg",     "08_august",   "summer", "snack",     4),
]

# =============================================================================
# QUERY BUILDER
# Round 2 uses broader, higher-yield queries than round 1.
# Key insight: drop season/month from query — food images don't change by month.
# Focus on: location food style + meal type + meal time = reliable Bing results.
# =============================================================================

# Base food styles per location and meal preference
FOOD_STYLES = {
    "dubai": {
        "veg":     ["arabic vegetarian food", "middle east veg food dish", "vegetarian food dubai"],
        "vegan":   ["vegan arabic food", "middle east vegan dish", "vegan food dubai plate"],
        "egg":     ["egg dish breakfast arabic", "arabic egg food", "egg food middle east"],
        "non_veg": ["arabic meat grilled food", "shawarma kebab arabic", "middle east meat dish"],
    },
    "miami": {
        "veg":     ["miami vegetarian food", "american vegetarian dish", "florida veg food plate"],
        "vegan":   ["miami vegan food", "american vegan dish", "florida vegan plate restaurant"],
        "egg":     ["american egg breakfast dish", "egg food miami", "egg plate american restaurant"],
        "non_veg": ["miami seafood meat dish", "american bbq burger food", "florida grilled meat food"],
    },
    "paris": {
        "veg":     ["french vegetarian food", "paris veg dish restaurant", "vegetarian french cuisine"],
        "vegan":   ["french vegan food", "paris vegan dish", "vegan french cuisine plate"],
        "egg":     ["french omelette egg dish", "paris egg food", "french egg cuisine"],
        "non_veg": ["french meat steak bistro", "paris non veg food", "french beef duck dish"],
    },
    "jungfrau": {
        "veg":     ["swiss vegetarian food", "alpine veg dish restaurant", "switzerland vegetarian cuisine"],
        "vegan":   ["swiss vegan food", "alpine vegan dish", "switzerland vegan plate"],
        "egg":     ["swiss egg breakfast dish", "alpine egg food", "swiss egg cuisine"],
        "non_veg": ["swiss meat fondue raclette", "alpine meat dish restaurant", "switzerland meat cuisine"],
    },
}

MEAL_TIMES = {
    "breakfast": "breakfast morning",
    "lunch":     "lunch midday",
    "dinner":    "dinner evening",
    "snack":     "snack bite",
}

def get_queries(location, meal_pref, season, time_of_day):
    styles   = FOOD_STYLES.get(location, {}).get(meal_pref, [f"{location} food"])
    mtime    = MEAL_TIMES.get(time_of_day, time_of_day)
    queries  = []

    # Specific: style + mealtime
    for style in styles:
        queries.append(f"{style} {time_of_day}")

    # Broader: location + meal_pref + time
    queries.append(f"{location} {meal_pref} food {time_of_day} plate")
    queries.append(f"{location} food restaurant {mtime}")

    # Ultimate fallback: just the food style without time
    for style in styles:
        queries.append(style)

    # Absolute last resort: location + food
    queries.append(f"{location} food restaurant dish")
    queries.append(f"{meal_pref} food dish plate")

    return queries


# =============================================================================
# UTILITIES
# =============================================================================
def get_hash(filepath):
    try:
        with open(filepath, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()
    except Exception:
        return None


def load_existing_hashes(folder):
    for f in os.listdir(folder):
        if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
            h = get_hash(os.path.join(folder, f))
            if h:
                with HASH_LOCK:
                    HASH_REGISTRY.add(h)


def run_query(query, temp_dir, max_num):
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


def update_metadata_json(folder_path, location, meal_pref, month_folder, season, time_of_day):
    images    = sorted([f for f in os.listdir(folder_path) if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))])
    meta_path = os.path.join(folder_path, "metadata.json")
    existing_ctx = {}
    if os.path.exists(meta_path):
        try:
            existing_ctx = json.load(open(meta_path)).get("folder_context", {})
        except Exception:
            pass
    if not existing_ctx:
        existing_ctx = {
            "location":        location.title(),
            "meal_preference": meal_pref,
            "month":           month_folder.replace("_", " ").title(),
            "season":          season.title(),
            "time_of_day":     time_of_day.title(),
        }
    items = [{
        "filename":        f,
        "dish_name":       f"{location.title()} {meal_pref} {time_of_day} dish",
        "food_category":   meal_pref,
        "meal_preference": meal_pref,
        "time_of_day":     time_of_day,
        "description":     f"Round-2 top-up food image for {location}/{meal_pref}/{season}/{time_of_day}",
        "restaurant_name": "placeholder - needs manual review",
        "price_range":     "placeholder - needs manual review",
        "dietary_note":    f"Suitable for {meal_pref} preference"
    } for f in images]
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump({"folder_context": existing_ctx, "items": items}, f, indent=2, ensure_ascii=False)


# =============================================================================
# CORE: Top-up one folder
# =============================================================================
def topup_folder(task):
    location     = task["location"]
    meal_pref    = task["meal_pref"]
    month_folder = task["month_folder"]
    season       = task["season"]
    time_of_day  = task["time_of_day"]
    orig_count   = task["orig_count"]

    folder_path = os.path.join(BASE_PATH, location, meal_pref, month_folder, season, time_of_day)
    os.makedirs(folder_path, exist_ok=True)

    # Read live count — may have improved since document was made
    current_images = sorted([f for f in os.listdir(folder_path) if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))])
    current_count  = len(current_images)

    if current_count >= TARGET:
        return f"⏭️  SKIP {location}/{meal_pref}/{month_folder}/{season}/{time_of_day} — already {current_count}"

    load_existing_hashes(folder_path)

    queries   = get_queries(location, meal_pref, season, time_of_day)
    safe      = f"{location}_{meal_pref}_{month_folder}_{season}_{time_of_day}"
    temp_dir  = os.path.join(TEMP_BASE, safe)
    collected = list(current_images)

    for query in queries:
        if len(collected) >= TARGET:
            break
        file_paths = run_query(query, temp_dir, MAX_NUM)
        for fpath in file_paths:
            if len(collected) >= TARGET:
                break
            h = get_hash(fpath)
            if h is None:
                continue
            with HASH_LOCK:
                if h in HASH_REGISTRY:
                    continue
                HASH_REGISTRY.add(h)
            idx  = len(collected) + 1
            dest = os.path.join(folder_path, f"img_{idx:03d}.jpg")
            shutil.copy2(fpath, dest)
            collected.append(f"img_{idx:03d}.jpg")

    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir, ignore_errors=True)

    final_count = len([f for f in os.listdir(folder_path) if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))])
    update_metadata_json(folder_path, location, meal_pref, month_folder, season, time_of_day)

    added  = final_count - current_count
    status = "✅" if final_count >= TARGET else "⚠️ "
    return f"{status} {location}/{meal_pref}/{month_folder}/{season}/{time_of_day}: {orig_count}→{final_count}/15 (+{added})"


# =============================================================================
# MAIN
# =============================================================================
if __name__ == "__main__":
    import time

    by_loc = {}
    for t in TOPUP_FOLDERS:
        by_loc[t[0]] = by_loc.get(t[0], 0) + 1

    print("=" * 65)
    print("  FOOD TOP-UP — ROUND 2")
    print(f"  Target         : {TARGET} images per folder")
    print(f"  Total folders  : {len(TOPUP_FOLDERS)}")
    for loc, cnt in sorted(by_loc.items()):
        print(f"    {loc:<12}: {cnt} folders")
    print(f"  Workers        : {TOPUP_WORKERS}")
    print("=" * 65)

    os.makedirs(TEMP_BASE, exist_ok=True)

    tasks = [
        {"location": loc, "meal_pref": mp, "month_folder": mf,
         "season": s, "time_of_day": t, "orig_count": c}
        for loc, mp, mf, s, t, c in TOPUP_FOLDERS
    ]

    start = time.time()
    done, success, partial, skipped = 0, 0, 0, 0

    with ThreadPoolExecutor(max_workers=TOPUP_WORKERS) as executor:
        futures = {executor.submit(topup_folder, task): task for task in tasks}
        for future in as_completed(futures):
            result = future.result()
            done  += 1
            print(f"  [{done:>3}/{len(tasks)}] {result}")
            if "✅" in result:   success += 1
            elif "⏭️" in result: skipped += 1
            else:                partial += 1

    shutil.rmtree(TEMP_BASE, ignore_errors=True)

    elapsed = time.time() - start
    print(f"\n{'='*65}")
    print(f"  ✅ Reached 15  : {success}")
    print(f"  ⚠️  Still below : {partial}  ← run again to fill these")
    print(f"  ⏭️  Already done: {skipped}")
    print(f"  ⏱️  Time        : {elapsed/60:.1f} minutes")
    print(f"{'='*65}")
    print("\nTip: If ⚠️  folders remain, just run again.")
    print("     Bing rate-limits recover within minutes.")