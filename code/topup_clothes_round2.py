# =============================================================================
# topup_clothes_round2.py — Round 2 Top-Up for Remaining Under-filled Folders
# These are folders that still had < 15 images after the first topup run.
# Uses even broader queries to guarantee results from Bing.
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
MAX_NUM       = 50        # higher than round 1 — these folders are stubborn
TEMP_BASE     = "dataset/_temp_topup_r2"
BASE_PATH     = "dataset/clothes/images"

HASH_REGISTRY = set()
HASH_LOCK     = Lock()

# =============================================================================
# 49 FOLDERS — exactly as reported in your document
# (location, gender, month_folder, season, time_of_day, current_count)
# =============================================================================
TOPUP_FOLDERS = [
    # 0 images
    ("miami",    "male",   "05_may",      "summer", "night",     0),
    ("miami",    "male",   "08_august",   "summer", "night",     0),
    ("miami",    "male",   "10_october",  "autumn", "afternoon", 0),
    ("paris",    "male",   "03_march",    "spring", "night",     0),
    ("paris",    "male",   "04_april",    "spring", "night",     0),
    ("paris",    "male",   "12_december", "winter", "night",     0),
    # 1 image
    ("dubai",    "male",   "01_january",  "mild",   "night",     1),
    ("miami",    "male",   "07_july",     "summer", "evening",   1),
    ("miami",    "male",   "08_august",   "summer", "morning",   1),
    ("miami",    "male",   "11_november", "autumn", "afternoon", 1),
    # 2 images
    ("dubai",    "male",   "09_september","hot",    "afternoon", 2),
    ("jungfrau", "female", "08_august",   "summer", "night",     2),
    ("jungfrau", "unisex", "03_march",    "winter", "evening",   2),
    ("miami",    "male",   "06_june",     "summer", "evening",   2),
    ("paris",    "male",   "01_january",  "winter", "afternoon", 2),
    ("paris",    "male",   "08_august",   "summer", "afternoon", 2),
    # 3 images
    ("dubai",    "male",   "08_august",   "hot",    "afternoon", 3),
    ("dubai",    "male",   "09_september","hot",    "evening",   3),
    ("jungfrau", "female", "11_november", "winter", "morning",   3),
    ("jungfrau", "male",   "08_august",   "summer", "afternoon", 3),
    ("jungfrau", "male",   "10_october",  "autumn", "night",     3),
    ("miami",    "male",   "03_march",    "spring", "night",     3),
    ("miami",    "male",   "10_october",  "autumn", "evening",   3),
    ("miami",    "male",   "10_october",  "autumn", "night",     3),
    ("paris",    "male",   "05_may",      "spring", "night",     3),
    ("paris",    "male",   "11_november", "autumn", "night",     3),
    # 4 images
    ("jungfrau", "female", "08_august",   "summer", "afternoon", 4),
    ("miami",    "male",   "03_march",    "spring", "evening",   4),
    ("paris",    "male",   "12_december", "winter", "afternoon", 4),
    # 5 images
    ("dubai",    "female", "09_september","hot",    "morning",   5),
    ("dubai",    "male",   "02_february", "mild",   "night",     5),
    ("dubai",    "male",   "08_august",   "hot",    "morning",   5),
    ("dubai",    "male",   "10_october",  "warm",   "evening",   5),
    ("dubai",    "unisex", "08_august",   "hot",    "night",     5),
    ("jungfrau", "female", "03_march",    "winter", "afternoon", 5),
    ("jungfrau", "female", "07_july",     "summer", "evening",   5),
    ("jungfrau", "female", "08_august",   "summer", "morning",   5),
    ("miami",    "male",   "08_august",   "summer", "afternoon", 5),
    ("miami",    "male",   "08_august",   "summer", "evening",   5),
    ("miami",    "male",   "06_june",     "summer", "night",     5),
    ("miami",    "male",   "07_july",     "summer", "night",     5),
    ("miami",    "male",   "09_september","autumn", "evening",   5),
    ("miami",    "male",   "10_october",  "autumn", "morning",   5),
    ("paris",    "male",   "08_august",   "summer", "evening",   5),
    ("paris",    "male",   "10_october",  "autumn", "evening",   5),
    ("paris",    "male",   "10_october",  "autumn", "night",     5),
    ("paris",    "male",   "11_november", "autumn", "afternoon", 5),
    ("paris",    "unisex", "05_may",      "spring", "afternoon", 5),
    ("paris",    "unisex", "08_august",   "summer", "evening",   5),
]

# =============================================================================
# QUERIES — wider/stronger than round 1 since these folders already failed once
# Strategy: drop season/time specificity, keep location+gender+style reliable
# Each slot has 4 queries — first 2 specific, last 2 very broad fallbacks
# =============================================================================
QUERIES = {
    "dubai": {
        "female": {
            "hot": {
                "morning":   ["abaya morning fashion women", "modest fashion morning outfit women", "hijab fashion summer morning", "women fashion summer morning"],
                "afternoon": ["abaya afternoon fashion summer women", "modest fashion afternoon outfit", "arabic women summer fashion", "women summer afternoon outfit"],
                "evening":   ["abaya evening fashion women arabic", "modest fashion evening outfit", "hijab evening fashion", "women evening fashion outfit"],
                "night":     ["abaya night fashion arabic women", "modest night outfit women", "hijab night fashion", "women night fashion outfit"],
            },
            "warm": {
                "morning":   ["abaya spring fashion morning", "modest women spring morning", "arabic women spring outfit", "women spring morning fashion"],
            },
            "mild": {
                "night":     ["kandura men mild winter fashion", "men winter night casual outfit", "arabic men mild night", "men night fashion winter"],
            },
        },
        "male": {
            "hot": {
                "morning":   ["men summer morning casual beach", "men summer morning outfit street style", "men casual hot weather morning", "men fashion summer morning"],
                "afternoon": ["men summer afternoon casual outfit", "men hot weather afternoon fashion", "arabic men hot afternoon", "men summer afternoon fashion"],
                "evening":   ["men summer evening casual outfit", "men hot weather evening fashion", "arabic men summer evening", "men evening fashion hot"],
            },
            "mild": {
                "night":     ["men winter night casual outfit", "men mild night fashion outfit", "smart casual men winter night", "men night winter fashion"],
            },
            "warm": {
                "evening":   ["men warm evening casual outfit", "men spring evening fashion", "arabic men warm evening", "men evening fashion warm"],
            },
        },
        "unisex": {
            "hot": {
                "night":     ["unisex summer night outfit fashion", "gender neutral summer night fashion", "unisex hot weather night outfit", "neutral fashion summer night"],
            },
        },
    },
    "jungfrau": {
        "female": {
            "summer": {
                "morning":   ["women mountain summer morning hiking", "female alpine summer morning outfit", "women summer hiking morning alps", "women outdoor summer morning"],
                "afternoon": ["women mountain summer afternoon outfit", "female alpine summer afternoon", "women summer hiking afternoon", "women outdoor summer afternoon"],
                "evening":   ["women mountain summer evening outfit lodge", "female alpine summer evening", "women mountain resort evening", "women outdoor summer evening"],
                "night":     ["women mountain lodge night outfit summer", "female alpine resort summer night", "women ski lodge summer night", "women outdoor summer night"],
            },
            "winter": {
                "morning":   ["women ski jacket winter morning", "female alpine winter morning outfit", "women ski resort morning fashion", "women outdoor winter morning"],
                "afternoon": ["women ski jacket winter afternoon", "female alpine winter afternoon outfit", "women mountain winter afternoon", "women outdoor winter afternoon"],
                "evening":   ["women ski lodge evening winter", "female alpine winter evening outfit", "women mountain winter evening", "women outdoor winter evening"],
            },
            "autumn": {
                "evening":   ["women mountain autumn evening outfit", "female alpine autumn evening", "women hiking autumn evening", "women outdoor autumn evening"],
            },
        },
        "male": {
            "summer": {
                "afternoon": ["men mountain summer afternoon hiking", "male alpine summer afternoon outfit", "men hiking summer afternoon alps", "men outdoor summer afternoon"],
                "evening":   ["men mountain lodge summer evening", "male alpine summer evening", "men mountain resort summer evening", "men outdoor summer evening"],
            },
            "autumn": {
                "night":     ["men mountain autumn night outfit lodge", "male alpine autumn night fashion", "men mountain lodge autumn night", "men outdoor autumn night"],
                "evening":   ["men mountain autumn evening outfit", "male alpine autumn evening", "men mountain lodge autumn evening", "men outdoor autumn evening"],
            },
            "winter": {
                "evening":   ["men ski lodge winter evening outfit", "male alpine winter evening", "men mountain winter evening fashion", "men outdoor winter evening"],
                "night":     ["men ski lodge winter night outfit", "male alpine winter night", "men mountain winter night fashion", "men outdoor winter night"],
            },
        },
        "unisex": {
            "winter": {
                "evening":   ["unisex ski lodge winter evening", "gender neutral alpine winter evening", "unisex winter jacket evening mountain", "neutral winter fashion evening"],
                "morning":   ["unisex ski jacket winter morning", "gender neutral alpine winter morning", "unisex winter outfit morning mountain", "neutral winter fashion morning"],
            },
            "summer": {
                "afternoon": ["unisex alpine summer afternoon hiking", "gender neutral mountain summer afternoon", "unisex summer hiking outfit afternoon", "neutral summer hiking fashion"],
                "evening":   ["unisex alpine summer evening lodge", "gender neutral mountain summer evening", "unisex summer mountain evening", "neutral summer mountain fashion"],
            },
        },
    },
    "miami": {
        "male": {
            "summer": {
                "morning":   ["men miami beach summer morning casual", "male beach summer morning outfit", "men summer morning beach fashion", "men casual summer morning"],
                "afternoon": ["men miami beach summer afternoon casual", "male beach summer afternoon outfit", "men summer afternoon beach fashion", "men casual summer afternoon"],
                "evening":   ["men miami summer evening casual outfit", "male beach summer evening fashion", "men summer evening beach style", "men casual summer evening"],
                "night":     ["men miami summer night casual outfit", "male beach summer night fashion", "men summer night beach style", "men casual summer night"],
            },
            "spring": {
                "evening":   ["men miami spring evening casual outfit", "male spring evening fashion miami", "men spring evening beach style", "men casual spring evening"],
                "night":     ["men miami spring night casual outfit", "male spring night fashion miami", "men spring night style", "men casual spring night"],
            },
            "autumn": {
                "morning":   ["men miami autumn morning casual outfit", "male autumn morning fashion miami", "men autumn morning style", "men casual autumn morning"],
                "afternoon": ["men miami autumn afternoon casual outfit", "male autumn afternoon fashion miami", "men autumn afternoon street style", "men casual autumn afternoon"],
                "evening":   ["men miami autumn evening casual outfit", "male autumn evening fashion miami", "men autumn evening street style", "men casual autumn evening"],
                "night":     ["men miami autumn night casual outfit", "male autumn night fashion miami", "men autumn night street style", "men casual autumn night"],
            },
            "winter": {
                "afternoon": ["men miami winter afternoon casual outfit", "male winter afternoon fashion miami", "men winter afternoon street style", "men casual winter afternoon"],
                "evening":   ["men miami winter evening casual outfit", "male winter evening fashion miami", "men winter evening street style", "men casual winter evening"],
                "night":     ["men miami winter night casual outfit", "male winter night fashion miami", "men winter night street style", "men casual winter night"],
            },
        },
        "female": {
            "summer": {
                "morning":   ["women miami beach summer morning", "female summer morning beach outfit", "women summer morning beach fashion", "women casual summer morning"],
                "afternoon": ["women miami beach summer afternoon", "female summer afternoon beach outfit", "women summer afternoon beach fashion", "women casual summer afternoon"],
                "evening":   ["women miami summer evening outfit", "female summer evening beach fashion", "women summer evening beach style", "women casual summer evening"],
                "night":     ["women miami summer night outfit", "female summer night fashion miami", "women summer night beach style", "women casual summer night"],
            },
            "winter": {
                "morning":   ["women miami winter morning casual", "female winter morning fashion miami", "women winter morning style", "women casual winter morning"],
            },
        },
        "unisex": {
            "summer": {
                "afternoon": ["unisex beach summer afternoon outfit miami", "gender neutral summer afternoon beach", "unisex summer beach afternoon", "neutral beach summer outfit"],
                "evening":   ["unisex beach summer evening outfit", "gender neutral summer evening beach", "unisex summer beach evening", "neutral beach summer evening"],
                "night":     ["unisex beach summer night outfit", "gender neutral summer night beach", "unisex summer beach night", "neutral beach summer night"],
            },
            "autumn": {
                "evening":   ["unisex autumn evening fashion miami", "gender neutral autumn evening outfit", "unisex autumn evening style", "neutral autumn evening fashion"],
                "night":     ["unisex autumn night fashion", "gender neutral autumn night outfit", "unisex autumn night style", "neutral autumn night fashion"],
            },
        },
    },
    "paris": {
        "male": {
            "spring": {
                "afternoon": ["parisian men spring afternoon fashion", "french men spring afternoon outfit", "paris men spring afternoon style", "men spring afternoon chic"],
                "evening":   ["parisian men spring evening fashion", "french men spring evening outfit", "paris men spring evening style", "men spring evening chic"],
                "night":     ["parisian men spring night fashion", "french men spring night outfit", "paris men spring night style", "men spring night chic"],
            },
            "summer": {
                "afternoon": ["parisian men summer afternoon fashion", "french men summer afternoon outfit", "paris men summer afternoon style", "men summer afternoon chic"],
                "evening":   ["parisian men summer evening fashion", "french men summer evening outfit", "paris men summer evening style", "men summer evening chic"],
                "night":     ["parisian men summer night fashion", "french men summer night outfit", "paris men summer night style", "men summer night chic"],
            },
            "autumn": {
                "afternoon": ["parisian men autumn afternoon fashion", "french men autumn afternoon outfit", "paris men autumn afternoon style", "men autumn afternoon chic"],
                "evening":   ["parisian men autumn evening fashion", "french men autumn evening outfit", "paris men autumn evening style", "men autumn evening chic"],
                "night":     ["parisian men autumn night fashion", "french men autumn night outfit", "paris men autumn night style", "men autumn night chic"],
            },
            "winter": {
                "afternoon": ["parisian men winter afternoon fashion", "french men winter afternoon outfit", "paris men winter afternoon style", "men winter afternoon chic"],
                "evening":   ["parisian men winter evening fashion", "french men winter evening outfit", "paris men winter evening style", "men winter evening chic"],
                "night":     ["parisian men winter night fashion", "french men winter night outfit", "paris men winter night style", "men winter night chic"],
            },
        },
        "female": {
            "summer": {
                "morning":   ["parisian women summer morning fashion", "french women summer morning outfit", "paris women summer morning style", "women summer morning chic"],
                "afternoon": ["parisian women summer afternoon fashion", "french women summer afternoon outfit", "paris women summer afternoon", "women summer afternoon chic"],
                "evening":   ["parisian women summer evening fashion", "french women summer evening outfit", "paris women summer evening", "women summer evening chic"],
                "night":     ["parisian women summer night fashion", "french women summer night outfit", "paris women summer night style", "women summer night chic"],
            },
            "autumn": {
                "evening":   ["parisian women autumn evening fashion", "french women autumn evening outfit", "paris women autumn evening", "women autumn evening chic"],
            },
        },
        "unisex": {
            "spring": {
                "afternoon": ["unisex paris spring afternoon fashion", "gender neutral spring afternoon outfit paris", "unisex spring afternoon chic paris", "neutral spring fashion afternoon"],
                "evening":   ["unisex paris spring evening fashion", "gender neutral spring evening outfit paris", "unisex spring evening chic paris", "neutral spring fashion evening"],
                "night":     ["unisex paris spring night fashion", "gender neutral spring night outfit paris", "unisex spring night chic paris", "neutral spring fashion night"],
            },
            "summer": {
                "afternoon": ["unisex paris summer afternoon fashion", "gender neutral summer afternoon outfit paris", "unisex summer afternoon chic paris", "neutral summer fashion afternoon"],
                "evening":   ["unisex paris summer evening fashion", "gender neutral summer evening outfit paris", "unisex summer evening chic paris", "neutral summer fashion evening"],
                "night":     ["unisex paris summer night fashion", "gender neutral summer night outfit paris", "unisex summer night chic paris", "neutral summer fashion night"],
            },
            "autumn": {
                "afternoon": ["unisex paris autumn afternoon fashion", "gender neutral autumn afternoon outfit paris", "unisex autumn afternoon chic", "neutral autumn fashion afternoon"],
                "evening":   ["unisex paris autumn evening fashion", "gender neutral autumn evening outfit paris", "unisex autumn evening chic", "neutral autumn fashion evening"],
                "night":     ["unisex paris autumn night fashion", "gender neutral autumn night outfit paris", "unisex autumn night chic", "neutral autumn fashion night"],
            },
            "winter": {
                "afternoon": ["unisex paris winter afternoon fashion", "gender neutral winter afternoon outfit paris", "unisex winter afternoon chic", "neutral winter fashion afternoon"],
                "evening":   ["unisex paris winter evening fashion", "gender neutral winter evening outfit paris", "unisex winter evening chic", "neutral winter fashion evening"],
                "night":     ["unisex paris winter night fashion", "gender neutral winter night outfit paris", "unisex winter night chic", "neutral winter fashion night"],
            },
        },
    },
}

# Ultimate fallback if no specific query found above
LOCATION_FALLBACKS = {
    "dubai":    ["dubai street fashion outfit", "dubai casual fashion men women", "middle east fashion modern"],
    "jungfrau": ["alpine mountain fashion outfit", "ski resort fashion clothing", "mountain lodge fashion"],
    "miami":    ["miami beach street fashion", "miami casual fashion outfit", "south beach fashion style"],
    "paris":    ["paris street fashion outfit", "parisian chic fashion", "french fashion style casual"],
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
            "location":    location.title(),
            "gender":      gender.title(),
            "month":       month_folder.replace("_", " ").title(),
            "season":      season.title(),
            "time_of_day": time_of_day.title(),
        }
    items = [{
        "filename":     f,
        "item_name":    f"{location.title()} {gender.title()} {season.title()} {time_of_day.title()} Outfit",
        "category":     "placeholder - needs manual review",
        "color":        "placeholder - needs manual review",
        "occasion":     "placeholder - needs manual review",
        "description":  f"Round-2 top-up image for {location}/{gender}/{season}/{time_of_day}",
        "price_range":  "placeholder - needs manual review",
        "cultural_note":f"Appropriate for {location.title()}"
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

    # Read live count — may have improved since document was made
    current_images = sorted([f for f in os.listdir(folder_path) if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))])
    current_count  = len(current_images)

    if current_count >= TARGET:
        return f"⏭️  SKIP {location}/{gender}/{month_folder}/{season}/{time_of_day} — already {current_count}"

    load_existing_hashes(folder_path)

    # Look up specific queries, fall back to broad location queries
    specific = QUERIES.get(location, {}).get(gender, {}).get(season, {}).get(time_of_day, [])
    fallbacks = LOCATION_FALLBACKS.get(location, [f"{location} fashion outfit"])
    all_queries = specific + fallbacks

    safe     = f"{location}_{gender}_{month_folder}_{season}_{time_of_day}"
    temp_dir = os.path.join(TEMP_BASE, safe)
    collected = list(current_images)

    for query in all_queries:
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
    update_metadata_json(folder_path, location, gender, month_folder, season, time_of_day)

    added  = final_count - current_count
    status = "✅" if final_count >= TARGET else "⚠️ "
    return f"{status} {location}/{gender}/{month_folder}/{season}/{time_of_day}: {orig_count}→{final_count}/15 (+{added})"


# =============================================================================
# MAIN
# =============================================================================
if __name__ == "__main__":
    import time

    by_loc = {}
    for t in TOPUP_FOLDERS:
        by_loc[t[0]] = by_loc.get(t[0], 0) + 1

    print("=" * 65)
    print("  CLOTHES TOP-UP — ROUND 2")
    print(f"  Target         : {TARGET} images per folder")
    print(f"  Total folders  : {len(TOPUP_FOLDERS)}")
    for loc, cnt in sorted(by_loc.items()):
        print(f"    {loc:<12}: {cnt} folders")
    print(f"  Workers        : {TOPUP_WORKERS}")
    print("=" * 65)

    os.makedirs(TEMP_BASE, exist_ok=True)

    tasks = [
        {"location": loc, "gender": g, "month_folder": mf,
         "season": s, "time_of_day": t, "orig_count": c}
        for loc, g, mf, s, t, c in TOPUP_FOLDERS
    ]

    start = time.time()
    done, success, partial, skipped = 0, 0, 0, 0

    with ThreadPoolExecutor(max_workers=TOPUP_WORKERS) as executor:
        futures = {executor.submit(topup_folder, task): task for task in tasks}
        for future in as_completed(futures):
            result = future.result()
            done  += 1
            print(f"  [{done:>2}/{len(tasks)}] {result}")
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
    print("\nTip: If ⚠️  folders remain, run again.")
    print("     Bing recovers from rate-limits within minutes.")