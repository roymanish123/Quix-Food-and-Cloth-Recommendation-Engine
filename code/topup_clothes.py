# =============================================================================
# topup_clothes.py — Targeted Top-Up for Under-filled Clothes Folders
# Reads actual current image count, downloads ONLY what is missing to reach 15
# Uses broader queries than originals since narrow queries already failed
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
MAX_NUM       = 40

# Images saved into the SAME existing folder — no new folders created
# This resolves to: C:\Users\MANISH\Downloads\Quix_Recommendation_engine\code\dataset\clothes\images\
BASE_PATH  = "dataset/clothes/images"
TEMP_BASE  = "dataset/_temp_topup"

HASH_REGISTRY = set()
HASH_LOCK     = Lock()

# =============================================================================
# ALL 64 FOLDERS FROM YOUR DOCUMENT
# (location, gender, month_folder, season, time_of_day, current_count)
# =============================================================================
TOPUP_FOLDERS = [
    # 0 images
    ("dubai",    "female",  "08_august",    "hot",    "night",     0),
    ("dubai",    "male",    "08_august",    "hot",    "evening",   0),
    ("miami",    "male",    "08_august",    "summer", "night",     0),
    ("miami",    "male",    "10_october",   "autumn", "afternoon", 0),
    ("miami",    "male",    "11_november",  "autumn", "evening",   0),
    ("miami",    "male",    "11_november",  "autumn", "night",     0),
    ("paris",    "male",    "03_march",     "spring", "night",     0),
    ("paris",    "male",    "04_april",     "spring", "night",     0),
    ("paris",    "male",    "12_december",  "winter", "night",     0),
    # 1 image
    ("dubai",    "female",  "08_august",    "hot",    "morning",   1),
    ("dubai",    "male",    "01_january",   "mild",   "night",     1),
    ("dubai",    "unisex",  "10_october",   "warm",   "evening",   1),
    ("miami",    "male",    "05_may",       "summer", "night",     1),
    ("miami",    "male",    "07_july",      "summer", "evening",   1),
    ("miami",    "male",    "08_august",    "summer", "morning",   1),
    ("miami",    "male",    "11_november",  "autumn", "afternoon", 1),
    ("paris",    "female",  "08_august",    "summer", "night",     1),
    ("paris",    "female",  "11_november",  "autumn", "evening",   1),
    ("paris",    "unisex",  "05_may",       "spring", "night",     1),
    # 2 images
    ("dubai",    "female",  "07_july",      "hot",    "evening",   2),
    ("dubai",    "female",  "08_august",    "hot",    "evening",   2),
    ("dubai",    "female",  "09_september", "hot",    "night",     2),
    ("dubai",    "male",    "09_september", "hot",    "afternoon", 2),
    ("dubai",    "male",    "12_december",  "mild",   "night",     2),
    ("dubai",    "unisex",  "09_september", "hot",    "night",     2),
    ("dubai",    "unisex",  "12_december",  "mild",   "evening",   2),
    ("jungfrau", "female",  "08_august",    "summer", "night",     2),
    ("jungfrau", "unisex",  "03_march",     "winter", "evening",   2),
    ("miami",    "female",  "12_december",  "winter", "morning",   2),
    ("miami",    "male",    "06_june",      "summer", "evening",   2),
    ("miami",    "male",    "11_november",  "autumn", "morning",   2),
    ("miami",    "male",    "12_december",  "winter", "evening",   2),
    ("paris",    "male",    "01_january",   "winter", "afternoon", 2),
    ("paris",    "male",    "08_august",    "summer", "afternoon", 2),
    ("paris",    "unisex",  "08_august",    "summer", "night",     2),
    ("paris",    "unisex",  "12_december",  "winter", "night",     2),
    # 3 images
    ("dubai",    "female",  "08_august",    "hot",    "afternoon", 3),
    ("dubai",    "female",  "09_september", "hot",    "evening",   3),
    ("dubai",    "female",  "09_september", "hot",    "afternoon", 3),
    ("dubai",    "male",    "08_august",    "hot",    "afternoon", 3),
    ("dubai",    "male",    "09_september", "hot",    "evening",   3),
    ("jungfrau", "female",  "11_november",  "winter", "morning",   3),
    ("jungfrau", "male",    "08_august",    "summer", "afternoon", 3),
    ("jungfrau", "male",    "10_october",   "autumn", "night",     3),
    ("miami",    "female",  "07_july",      "summer", "afternoon", 3),
    ("miami",    "male",    "03_march",     "spring", "night",     3),
    ("miami",    "male",    "10_october",   "autumn", "evening",   3),
    ("paris",    "male",    "05_may",       "spring", "night",     3),
    ("paris",    "male",    "11_november",  "autumn", "night",     3),
    ("paris",    "unisex",  "11_november",  "autumn", "evening",   3),
    # 4 images
    ("dubai",    "female",  "10_october",   "warm",   "morning",   4),
    ("dubai",    "female",  "12_december",  "mild",   "morning",   4),
    ("dubai",    "male",    "09_september", "hot",    "morning",   4),
    ("dubai",    "unisex",  "09_september", "hot",    "evening",   4),
    ("jungfrau", "female",  "08_august",    "summer", "afternoon", 4),
    ("miami",    "male",    "03_march",     "spring", "evening",   4),
    ("miami",    "male",    "12_december",  "winter", "afternoon", 4),
    ("miami",    "male",    "12_december",  "winter", "morning",   4),
    ("miami",    "unisex",  "06_june",      "summer", "night",     4),
    ("miami",    "unisex",  "08_august",    "summer", "afternoon", 4),
    ("miami",    "unisex",  "08_august",    "summer", "night",     4),
    ("paris",    "female",  "08_august",    "summer", "evening",   4),
    ("paris",    "male",    "12_december",  "winter", "afternoon", 4),
    ("paris",    "unisex",  "07_july",      "summer", "night",     4),
]

# =============================================================================
# BROADER TOP-UP QUERIES
# Wider than original — original narrow queries already failed on Bing
# 3 queries per slot gives the crawler 3 chances before falling back
# =============================================================================
TOPUP_QUERIES = {
    "dubai": {
        "female": {
            "hot": {
                "morning":   ["abaya modest fashion morning", "hijab outfit summer morning", "modest women fashion morning hot"],
                "afternoon": ["abaya modest fashion afternoon summer", "arabic women fashion hot day", "modest women afternoon outfit hot"],
                "evening":   ["abaya fashion evening arabic women", "modest evening outfit women", "hijab evening fashion outfit"],
                "night":     ["abaya fashion night arabic women", "modest night outfit fashion women", "hijab night fashion outfit"],
            },
            "warm": {
                "morning":   ["abaya modest fashion morning warm", "modest women spring morning fashion", "arabic women outfit warm morning"],
                "evening":   ["abaya evening fashion warm", "modest women evening outfit warm season"],
            },
            "mild": {
                "morning":   ["abaya modest fashion morning mild winter", "modest women winter morning fashion", "hijab outfit mild morning"],
                "evening":   ["abaya evening fashion mild winter", "modest evening outfit winter women"],
            },
            "summer": {
                "night":     ["women summer night fashion outfit", "summer night dress fashion street style", "casual summer night women fashion"],
                "evening":   ["women summer evening fashion", "summer evening dress fashion", "casual evening dress summer women"],
            },
            "winter": {
                "morning":   ["modest women winter morning fashion", "hijab outfit winter morning", "women winter morning casual outfit"],
                "evening":   ["modest women winter evening fashion", "women winter evening casual outfit"],
            },
            "autumn": {
                "evening":   ["women autumn evening fashion outfit", "casual autumn evening outfit women"],
            },
            "spring": {
                "night":     ["women spring night fashion outfit", "casual spring night outfit women"],
            },
        },
        "male": {
            "hot": {
                "morning":   ["kandura fashion morning", "emirati man summer morning outfit", "arabic men morning summer fashion"],
                "afternoon": ["kandura fashion afternoon summer", "emirati men afternoon summer outfit", "arabic man hot afternoon fashion"],
                "evening":   ["kandura fashion evening summer", "emirati man evening summer outfit", "arabic men evening summer fashion"],
                "night":     ["kandura fashion night summer", "emirati man night outfit summer", "arabic men night summer fashion"],
            },
            "mild": {
                "night":     ["men casual night outfit winter", "smart casual man night mild winter", "men night fashion mild"],
            },
            "warm": {
                "evening":   ["men casual evening outfit warm", "smart casual man evening warm season", "men evening fashion warm"],
            },
            "winter": {
                "afternoon": ["men smart casual winter afternoon", "men winter afternoon outfit fashion"],
                "night":     ["men smart casual winter night", "men night outfit winter fashion"],
            },
            "spring": {
                "night":     ["men casual spring night fashion", "men spring night outfit street style"],
            },
            "summer": {
                "afternoon": ["men casual summer afternoon fashion", "men summer afternoon outfit street style"],
                "evening":   ["men casual summer evening fashion", "men summer evening outfit street style"],
                "night":     ["men casual summer night fashion", "men summer night outfit street style"],
            },
            "autumn": {
                "morning":   ["men casual autumn morning fashion", "men autumn morning outfit street style"],
                "afternoon": ["men casual autumn afternoon fashion", "men autumn afternoon outfit street style"],
                "evening":   ["men casual autumn evening fashion", "men autumn evening outfit street style"],
                "night":     ["men casual autumn night fashion", "men autumn night outfit street style"],
            },
        },
        "unisex": {
            "hot": {
                "evening":   ["unisex summer evening fashion", "gender neutral summer evening outfit", "unisex outfit summer evening"],
                "night":     ["unisex summer night fashion", "gender neutral night outfit summer", "unisex night outfit hot weather"],
            },
            "warm": {
                "evening":   ["unisex warm evening fashion", "gender neutral evening outfit warm", "unisex outfit evening warm season"],
            },
            "mild": {
                "evening":   ["unisex mild weather evening fashion", "gender neutral evening outfit mild", "unisex light jacket evening outfit"],
            },
        },
    },
    "jungfrau": {
        "female": {
            "summer": {
                "morning":   ["women alpine summer morning hiking outfit", "female mountain summer morning fashion"],
                "afternoon": ["women alpine summer afternoon hiking", "female mountain summer afternoon fashion"],
                "evening":   ["women alpine lodge summer evening outfit", "female mountain resort summer evening"],
                "night":     ["women alpine lodge summer night outfit", "female mountain resort summer night fashion"],
            },
            "winter": {
                "morning":   ["women ski jacket winter morning alps", "female ski resort morning winter fashion"],
                "evening":   ["women ski lodge winter evening outfit", "female alpine winter evening fashion"],
            },
            "autumn": {
                "evening":   ["women alpine autumn evening outfit", "female mountain autumn evening fashion"],
                "night":     ["women alpine autumn night outfit", "female mountain autumn night fashion"],
            },
            "spring": {
                "morning":   ["women hiking spring morning alps", "female alpine spring morning outfit"],
            },
        },
        "male": {
            "summer": {
                "afternoon": ["men alpine summer afternoon hiking outfit", "male mountain summer afternoon fashion"],
                "evening":   ["men alpine lodge summer evening outfit", "male mountain resort summer evening"],
                "night":     ["men alpine lodge summer night outfit", "male mountain summer night fashion"],
            },
            "winter": {
                "evening":   ["men ski lodge winter evening outfit", "male alpine winter evening fashion"],
                "night":     ["men ski lodge winter night outfit", "male alpine winter night fashion"],
            },
            "autumn": {
                "night":     ["men alpine lodge autumn night outfit", "male mountain autumn night fashion"],
                "evening":   ["men alpine autumn evening outfit", "male mountain autumn evening fashion"],
            },
            "spring": {
                "night":     ["men alpine spring night outfit", "male mountain spring night fashion"],
            },
        },
        "unisex": {
            "winter": {
                "evening":   ["unisex ski lodge evening outfit", "gender neutral alpine winter evening fashion", "unisex winter evening ski resort"],
                "night":     ["unisex alpine winter night outfit", "gender neutral winter night lodge fashion"],
            },
            "summer": {
                "night":     ["unisex alpine summer night outfit", "gender neutral mountain summer night"],
                "afternoon": ["unisex alpine summer afternoon outfit", "gender neutral hiking summer afternoon"],
            },
            "autumn": {
                "evening":   ["unisex alpine autumn evening outfit", "gender neutral mountain autumn evening"],
            },
            "spring": {
                "morning":   ["unisex alpine spring morning outfit", "gender neutral hiking spring morning"],
                "night":     ["unisex alpine spring night outfit", "gender neutral mountain spring night"],
            },
        },
    },
    "miami": {
        "female": {
            "summer": {
                "afternoon": ["women miami beach summer afternoon outfit", "female miami summer afternoon fashion"],
                "evening":   ["women miami summer evening dress fashion", "female miami summer evening outfit"],
                "night":     ["women miami summer night fashion outfit", "female miami summer night dress"],
            },
            "winter": {
                "morning":   ["women miami winter morning casual outfit", "female miami winter morning fashion"],
                "evening":   ["women miami winter evening fashion", "female winter evening outfit miami"],
            },
            "autumn": {
                "evening":   ["women miami autumn evening fashion", "female autumn evening outfit miami beach"],
                "night":     ["women miami autumn night fashion", "female autumn night outfit miami"],
            },
            "spring": {
                "night":     ["women miami spring night fashion", "female miami spring night outfit"],
                "afternoon": ["women miami spring afternoon beach outfit", "female miami spring afternoon fashion"],
            },
        },
        "male": {
            "summer": {
                "morning":   ["men miami beach summer morning outfit", "male beach summer morning casual fashion"],
                "afternoon": ["men miami beach summer afternoon outfit", "male beach summer afternoon casual"],
                "evening":   ["men miami summer evening casual outfit", "male miami summer evening fashion"],
                "night":     ["men miami summer night casual outfit", "male miami summer night fashion"],
            },
            "spring": {
                "evening":   ["men miami spring evening casual outfit", "male miami spring evening fashion"],
                "night":     ["men miami spring night casual", "male miami spring night fashion"],
            },
            "autumn": {
                "morning":   ["men miami autumn morning casual outfit", "male miami autumn morning fashion"],
                "afternoon": ["men miami autumn afternoon casual", "male miami autumn afternoon fashion"],
                "evening":   ["men miami autumn evening casual outfit", "male miami autumn evening fashion"],
                "night":     ["men miami autumn night casual outfit", "male miami autumn night fashion"],
            },
            "winter": {
                "morning":   ["men miami winter morning casual outfit", "male miami winter morning fashion"],
                "afternoon": ["men miami winter afternoon casual outfit", "male miami winter afternoon fashion"],
                "evening":   ["men miami winter evening casual outfit", "male miami winter evening fashion"],
                "night":     ["men miami winter night casual outfit", "male miami winter night fashion"],
            },
        },
        "unisex": {
            "summer": {
                "afternoon": ["unisex beach summer afternoon outfit miami", "gender neutral beach summer afternoon"],
                "evening":   ["unisex beach summer evening outfit", "gender neutral beach summer evening"],
                "night":     ["unisex beach summer night outfit", "gender neutral beach summer night fashion"],
            },
            "winter": {
                "morning":   ["unisex miami winter morning outfit", "gender neutral miami winter morning"],
                "night":     ["unisex miami winter night outfit", "gender neutral winter night miami"],
            },
            "autumn": {
                "night":     ["unisex miami autumn night outfit", "gender neutral autumn night miami"],
                "afternoon": ["unisex miami autumn afternoon outfit", "gender neutral autumn afternoon miami"],
            },
        },
    },
    "paris": {
        "female": {
            "summer": {
                "evening":   ["parisian women summer evening chic fashion", "french women summer evening dress"],
                "night":     ["parisian women summer night fashion", "french women summer night outfit chic"],
            },
            "autumn": {
                "evening":   ["parisian women autumn evening chic fashion", "french women autumn evening outfit"],
                "night":     ["parisian women autumn night fashion", "french women autumn night outfit"],
            },
            "winter": {
                "morning":   ["parisian women winter morning chic fashion", "french women winter morning outfit"],
                "evening":   ["parisian women winter evening chic fashion", "french women winter evening outfit"],
            },
            "spring": {
                "night":     ["parisian women spring night fashion", "french women spring night outfit"],
                "afternoon": ["parisian women spring afternoon chic", "french women spring afternoon fashion"],
            },
        },
        "male": {
            "winter": {
                "afternoon": ["parisian men winter afternoon fashion", "french men winter afternoon outfit"],
                "night":     ["parisian men winter night fashion", "french men winter night outfit"],
            },
            "summer": {
                "afternoon": ["parisian men summer afternoon fashion", "french men summer afternoon outfit"],
                "evening":   ["parisian men summer evening fashion", "french men summer evening outfit"],
                "night":     ["parisian men summer night fashion", "french men summer night outfit"],
            },
            "spring": {
                "night":     ["parisian men spring night fashion", "french men spring night outfit"],
            },
            "autumn": {
                "afternoon": ["parisian men autumn afternoon fashion", "french men autumn afternoon outfit"],
                "evening":   ["parisian men autumn evening fashion", "french men autumn evening outfit"],
                "night":     ["parisian men autumn night fashion", "french men autumn night outfit"],
            },
        },
        "unisex": {
            "spring": {
                "afternoon": ["unisex spring fashion paris", "gender neutral spring paris outfit"],
                "night":     ["unisex spring night fashion", "gender neutral spring night outfit paris"],
            },
            "summer": {
                "evening":   ["unisex summer evening fashion paris", "gender neutral summer evening paris"],
                "night":     ["unisex summer night fashion paris", "gender neutral summer night outfit paris"],
            },
            "autumn": {
                "evening":   ["unisex autumn evening fashion", "gender neutral autumn evening outfit paris"],
                "night":     ["unisex autumn night fashion", "gender neutral autumn night outfit"],
            },
            "winter": {
                "night":     ["unisex winter night fashion", "gender neutral winter night outfit paris"],
                "afternoon": ["unisex winter afternoon fashion paris", "gender neutral winter afternoon outfit"],
            },
        },
    },
}


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


def update_metadata_json(folder_path, location, gender, month_folder, season, time_of_day):
    images = sorted([f for f in os.listdir(folder_path) if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))])
    meta_path = os.path.join(folder_path, "metadata.json")
    existing_ctx = {}
    if os.path.exists(meta_path):
        try:
            existing_ctx = json.load(open(meta_path)).get("folder_context", {})
        except Exception:
            pass
    if not existing_ctx:
        existing_ctx = {
            "location": location.title(), "gender": gender.title(),
            "month": month_folder.replace("_", " ").title(),
            "season": season.title(), "time_of_day": time_of_day.title(),
        }
    items = [{
        "filename": f,
        "item_name": f"{location.title()} {gender.title()} {season.title()} {time_of_day.title()} Outfit",
        "category": "placeholder - needs manual review",
        "color": "placeholder - needs manual review",
        "occasion": "placeholder - needs manual review",
        "description": f"Top-up image for {location}/{gender}/{season}/{time_of_day}",
        "price_range": "placeholder - needs manual review",
        "cultural_note": f"Appropriate for {location.title()}"
    } for f in images]
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump({"folder_context": existing_ctx, "items": items}, f, indent=2, ensure_ascii=False)


# =============================================================================
# CORE: Top-up one folder
# =============================================================================
def topup_folder(task):
    location     = task["location"]
    gender       = task["gender"]
    month_folder = task["month_folder"]
    season       = task["season"]
    time_of_day  = task["time_of_day"]
    orig_count   = task["orig_count"]

    folder_path = os.path.join(BASE_PATH, location, gender, month_folder, season, time_of_day)
    os.makedirs(folder_path, exist_ok=True)

    current_images = sorted([f for f in os.listdir(folder_path) if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))])
    current_count = len(current_images)

    if current_count >= TARGET:
        return f"⏭️  SKIP  {location}/{gender}/{month_folder}/{season}/{time_of_day} — already {current_count}"

    load_existing_hashes(folder_path)

    queries = TOPUP_QUERIES.get(location, {}).get(gender, {}).get(season, {}).get(time_of_day, [])

    if not queries:
        # Ultimate fallback — very broad
        queries = [
            f"{location} {gender} fashion {season} {time_of_day}",
            f"{location} {gender} clothing outfit {time_of_day}",
            f"{gender} fashion {season} outfit street style",
        ]

    safe = f"{location}_{gender}_{month_folder}_{season}_{time_of_day}"
    temp_dir = os.path.join(TEMP_BASE, safe)
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
            idx = len(collected) + 1
            dest = os.path.join(folder_path, f"img_{idx:03d}.jpg")
            shutil.copy2(fpath, dest)
            collected.append(f"img_{idx:03d}.jpg")

    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir, ignore_errors=True)

    final_count = len([f for f in os.listdir(folder_path) if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))])
    update_metadata_json(folder_path, location, gender, month_folder, season, time_of_day)

    added = final_count - current_count
    status = "✅" if final_count >= TARGET else "⚠️ "
    return f"{status} {location}/{gender}/{month_folder}/{season}/{time_of_day}: {orig_count}→{final_count}/15 (+{added})"


# =============================================================================
# MAIN
# =============================================================================
if __name__ == "__main__":
    import time

    print("=" * 65)
    print("  CLOTHES TOP-UP SCRIPT")
    print(f"  Target         : {TARGET} images per folder")
    print(f"  Folders        : {len(TOPUP_FOLDERS)}")
    print(f"  Workers        : {TOPUP_WORKERS}")
    print("=" * 65)

    os.makedirs(TEMP_BASE, exist_ok=True)

    tasks = [
        {"location": loc, "gender": g, "month_folder": m,
         "season": s, "time_of_day": t, "orig_count": c}
        for loc, g, m, s, t, c in TOPUP_FOLDERS
    ]

    start = time.time()
    done, total = 0, len(tasks)
    success, partial, skipped = 0, 0, 0

    with ThreadPoolExecutor(max_workers=TOPUP_WORKERS) as executor:
        futures = {executor.submit(topup_folder, task): task for task in tasks}
        for future in as_completed(futures):
            result = future.result()
            done += 1
            print(f"  [{done:>2}/{total}] {result}")
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
    print("     Bing rate-limits recover after a few minutes.")