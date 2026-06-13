"""
clothes_recommendation.py
==========================
Clothes Recommendation Engine for Quix Recommendation Engine project.

Two modes:
  Mode 1 — Quick: location + month → 10 random images from ALL genders combined
  Mode 2 — Full:  location + month + gender + time of day → full folder + metadata

Run from:
    C:\\Users\\MANISH\\Downloads\\Quix_Recommendation_engine\\code\\
Command:
    python clothes_recommendation.py
"""

import os
import json
import random
import sys

# ── CONFIG ────────────────────────────────────────────────────────────────────
BASE_DIR = r"dataset\clothes\images"

# Season map per location per month (1=Jan ... 12=Dec)
SEASON_MAP = {
    "dubai": {
        1: "mild",  2: "mild",  3: "warm",  4: "warm",
        5: "hot",   6: "hot",   7: "hot",   8: "hot",
        9: "hot",  10: "warm", 11: "mild", 12: "mild"
    },
    "paris": {
        1: "winter",  2: "winter",  3: "spring",  4: "spring",
        5: "spring",  6: "summer",  7: "summer",  8: "summer",
        9: "autumn", 10: "autumn", 11: "autumn", 12: "winter"
    },
    "jungfrau": {
        1: "winter",  2: "winter",  3: "winter",  4: "spring",
        5: "spring",  6: "summer",  7: "summer",  8: "summer",
        9: "autumn", 10: "autumn", 11: "winter", 12: "winter"
    },
    "miami": {
        1: "winter",  2: "winter",  3: "spring",  4: "spring",
        5: "summer",  6: "summer",  7: "summer",  8: "summer",
        9: "autumn", 10: "autumn", 11: "autumn", 12: "winter"
    }
}

MONTH_NAME_MAP = {
    "january": 1,  "february": 2,  "march": 3,     "april": 4,
    "may": 5,      "june": 6,      "july": 7,       "august": 8,
    "september": 9,"october": 10,  "november": 11,  "december": 12
}

MONTH_FOLDER_MAP = {
    1:  "01_january",   2:  "02_february",  3:  "03_march",
    4:  "04_april",     5:  "05_may",       6:  "06_june",
    7:  "07_july",      8:  "08_august",    9:  "09_september",
    10: "10_october",  11: "11_november",  12: "12_december"
}

VALID_LOCATIONS    = ["dubai", "paris", "jungfrau", "miami"]
VALID_GENDERS      = ["male", "female", "unisex"]
VALID_TIMES        = ["morning", "afternoon", "evening", "night"]
IMAGE_EXTS         = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
MODE_1_IMAGE_COUNT = 10
# ─────────────────────────────────────────────────────────────────────────────


def divider(char="=", width=65):
    print(char * width)


def parse_month(raw):
    """Accept '1'–'12' or month name. Returns int 1–12 or None."""
    raw = raw.strip().lower()
    if raw.isdigit():
        val = int(raw)
        if 1 <= val <= 12:
            return val
    elif raw in MONTH_NAME_MAP:
        return MONTH_NAME_MAP[raw]
    return None


def get_input(prompt, valid_options, parser=None):
    """Prompt until valid input. Returns validated value."""
    while True:
        raw = input(prompt).strip().lower()
        if raw == "exit":
            print("\n  👋 Goodbye!\n")
            sys.exit()
        if parser:
            result = parser(raw)
            if result is not None:
                return result
            print(f"  ❌ Invalid input. Valid options: {', '.join(str(o) for o in valid_options)}\n")
        else:
            if raw in valid_options:
                return raw
            print(f"  ❌ Invalid input. Valid options: {', '.join(valid_options)}\n")


def get_image_files(folder_path):
    """Return sorted list of image filenames in a folder."""
    if not os.path.exists(folder_path):
        return []
    return sorted([
        f for f in os.listdir(folder_path)
        if os.path.splitext(f)[1].lower() in IMAGE_EXTS
    ])


def open_images(image_paths):
    """Open all images using Windows default photo viewer."""
    for path in image_paths:
        try:
            os.startfile(path)
        except Exception as e:
            print(f"  ⚠️  Could not open {os.path.basename(path)}: {e}")


def display_metadata(folder_path, image_files):
    """Read metadata.json and display folder context + per-image details."""
    meta_path = os.path.join(folder_path, "metadata.json")

    if not os.path.exists(meta_path):
        print("  ⚠️  metadata.json not found in this folder.")
        return

    with open(meta_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print("  ⚠️  Could not parse metadata.json.")
            return

    # ── Folder Context ────────────────────────────────────────────────────────
    ctx = data.get("folder_context", {})
    divider("-")
    print("  📍 FOLDER CONTEXT")
    divider("-")
    print(f"  Location       : {ctx.get('location', 'N/A')}")
    print(f"  Gender         : {ctx.get('gender', 'N/A')}")
    print(f"  Month          : {ctx.get('month', 'N/A')}")
    print(f"  Season         : {ctx.get('season', 'N/A')}")
    print(f"  Time of Day    : {ctx.get('time_of_day', 'N/A')}")
    print(f"  Avg Temp (°C)  : {ctx.get('avg_temperature_celsius', 'N/A')}")
    print(f"  Weather Note   : {ctx.get('weather_note', 'N/A')}")
    divider("-")

    # ── Per-image Details ─────────────────────────────────────────────────────
    items       = data.get("items", [])
    item_lookup = {item.get("filename", ""): item for item in items}

    print(f"\n  👗 CLOTHING ITEMS ({len(image_files)} images found)\n")

    for i, img_file in enumerate(sorted(image_files), 1):
        item = item_lookup.get(img_file, {})
        print(f"  [{i:02d}] {img_file}")
        print(f"       Item Name    : {item.get('item_name', 'N/A')}")
        print(f"       Category     : {item.get('category', 'N/A')}")
        print(f"       Color        : {item.get('color', 'N/A')}")
        print(f"       Occasion     : {item.get('occasion', 'N/A')}")
        print(f"       Description  : {item.get('description', 'N/A')}")
        print(f"       Price Range  : {item.get('price_range', 'N/A')}")
        print(f"       Cultural Note: {item.get('cultural_note', 'N/A')}")
        print()


# ══════════════════════════════════════════════════════════════════════════════
#  MODE 1 — Quick Recommendation (location + month → 10 random images)
# ══════════════════════════════════════════════════════════════════════════════

def mode_1():
    divider()
    print("  👗  MODE 1 — QUICK RECOMMENDATION")
    print("  Input: Location + Month")
    print("  Output: 10 random clothing images from ALL genders combined")
    divider()

    # Location
    print(f"\n  Locations: {', '.join(VALID_LOCATIONS)}")
    location = get_input("  Enter location: ", VALID_LOCATIONS)

    # Month
    print(f"\n  Month: number (1-12) or name (january ... december)")
    month_num    = get_input(
        "  Enter month: ",
        [str(i) for i in range(1, 13)] + list(MONTH_NAME_MAP.keys()),
        parser=parse_month
    )
    season       = SEASON_MAP[location][month_num]
    month_folder = MONTH_FOLDER_MAP[month_num]

    print(f"\n  ✅ Season auto-detected: {season.upper()}")
    print(f"\n  🔍 Scanning all genders for {location} / {month_folder} / {season}...")

    # Collect ALL images across all genders and all time slots for this month+season
    all_images = []

    for gender in VALID_GENDERS:
        for time_slot in VALID_TIMES:
            folder_path = os.path.join(
                BASE_DIR, location, gender, month_folder, season, time_slot
            )
            files = get_image_files(folder_path)
            for f in files:
                all_images.append({
                    "abs_path":  os.path.abspath(os.path.join(folder_path, f)),
                    "filename":  f,
                    "gender":    gender,
                    "time_slot": time_slot
                })

    if not all_images:
        print(f"\n  ℹ️  No images found for {location} in {month_folder} ({season}).")
        print("     This combination may be empty after dataset cleanup.\n")
        return

    # Pick 10 random (or all if less than 10)
    count  = min(MODE_1_IMAGE_COUNT, len(all_images))
    picked = random.sample(all_images, count)

    print()
    divider("-")
    print(f"  📦 Found {len(all_images)} total images. Showing {count} random picks.")
    divider("-")
    print(f"\n  {'#':<5} {'Filename':<15} {'Gender':<10} {'Time Slot'}")
    print(f"  {'-'*4:<5} {'-'*14:<15} {'-'*9:<10} {'-'*9}")
    for i, img in enumerate(picked, 1):
        print(f"  {i:<5} {img['filename']:<15} {img['gender']:<10} {img['time_slot']}")

    print()
    divider("-")
    print(f"  🖼️  Opening {count} random clothing images...")
    divider("-")

    open_images([img["abs_path"] for img in picked])
    print(f"\n  ✅ Done! {count} images opened.\n")


# ══════════════════════════════════════════════════════════════════════════════
#  MODE 2 — Full Recommendation (all inputs)
# ══════════════════════════════════════════════════════════════════════════════

def mode_2():
    divider()
    print("  👗  MODE 2 — FULL RECOMMENDATION")
    print("  Input: Location + Month + Gender + Time of Day")
    print("  Output: All images from exact folder + full metadata")
    divider()

    # Location
    print(f"\n  Locations: {', '.join(VALID_LOCATIONS)}")
    location = get_input("  Enter location: ", VALID_LOCATIONS)

    # Gender
    print(f"\n  Genders: {', '.join(VALID_GENDERS)}")
    gender = get_input("  Enter gender: ", VALID_GENDERS)

    # Month
    print(f"\n  Month: number (1-12) or name (january ... december)")
    month_num    = get_input(
        "  Enter month: ",
        [str(i) for i in range(1, 13)] + list(MONTH_NAME_MAP.keys()),
        parser=parse_month
    )
    season       = SEASON_MAP[location][month_num]
    month_folder = MONTH_FOLDER_MAP[month_num]
    print(f"\n  ✅ Season auto-detected: {season.upper()}")

    # Time of Day
    print(f"\n  Times: {', '.join(VALID_TIMES)}")
    time_of_day = get_input("  Enter time of day: ", VALID_TIMES)

    # Build path
    folder_path = os.path.join(
        BASE_DIR, location, gender, month_folder, season, time_of_day
    )

    print()
    divider()
    print(f"  📂 Path: {folder_path}")
    divider()

    # Check folder exists
    if not os.path.exists(folder_path):
        print(f"\n  ❌ Folder not found: {folder_path}")
        print("     This combination may not exist in the dataset.\n")
        return

    # Get images
    image_files = get_image_files(folder_path)

    if not image_files:
        print(f"\n  ℹ️  No images found in this folder.")
        print("     The folder exists but is empty after dataset cleanup.\n")
        return

    # Display metadata
    display_metadata(folder_path, image_files)

    # Open images
    divider("-")
    print(f"  🖼️  Opening {len(image_files)} images in Windows Photo Viewer...")
    divider("-")

    full_paths = [os.path.abspath(os.path.join(folder_path, f)) for f in image_files]
    open_images(full_paths)

    print(f"\n  ✅ Done! {len(image_files)} images opened.\n")


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN LOOP
# ══════════════════════════════════════════════════════════════════════════════

def run_engine():
    divider()
    print("       👗  QUIX CLOTHES RECOMMENDATION ENGINE")
    divider()
    print("  Type 'exit' at any prompt to quit.\n")

    while True:
        divider("-")
        print("  SELECT MODE:")
        print("  1 → Quick  (location + month → 10 random images)")
        print("  2 → Full   (location + month + gender + time of day)")
        divider("-")

        mode = get_input("  Enter mode (1 or 2): ", ["1", "2"])

        if mode == "1":
            mode_1()
        else:
            mode_2()

        divider()
        print("  Would you like another recommendation? (yes / no)")
        again = input("  → ").strip().lower()
        if again != "yes":
            print("\n  👋 Goodbye!\n")
            sys.exit()
        print()


if __name__ == "__main__":
    if not os.path.exists(BASE_DIR):
        print(f"\n❌ Dataset not found at: {os.path.abspath(BASE_DIR)}")
        print("   Make sure you run this from:")
        print("   C:\\Users\\MANISH\\Downloads\\Quix_Recommendation_engine\\code\\\n")
        sys.exit(1)

    run_engine()