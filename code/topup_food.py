# =============================================================================
# topup_food.py — Targeted Top-Up for Under-filled Food Folders
# Reads actual current image count, downloads ONLY what is missing to reach 15
# Uses broader food-specific queries designed to return results reliably
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
MAX_NUM       = 40
TEMP_BASE     = "dataset/_temp_food_topup"
BASE_PATH     = "dataset/food/images"

HASH_REGISTRY = set()
HASH_LOCK     = Lock()

# =============================================================================
# ALL UNDER-FILLED FOOD FOLDERS — parsed from your 4 location files
# Format: (location, meal_pref, month_folder, season, time_of_day, current_count)
# Special note: "vegan/09_september/hot" in Dubai = ALL 4 meal times are 0
#               "paris/veg" = ALL folders are 0
#               "miami/vegan/11_november/autumn" = ALL 4 meal times are 0
# =============================================================================
TOPUP_FOLDERS = [

    # ================================================================
    # DUBAI
    # ================================================================

    # egg — 0 images
    ("dubai", "egg", "06_june",     "hot",  "lunch",     0),
    ("dubai", "egg", "07_july",     "hot",  "breakfast", 0),
    ("dubai", "egg", "07_july",     "hot",  "lunch",     0),
    ("dubai", "egg", "07_july",     "hot",  "snack",     0),
    ("dubai", "egg", "08_august",   "hot",  "breakfast", 0),
    ("dubai", "egg", "08_august",   "hot",  "snack",     0),
    ("dubai", "egg", "09_september","hot",  "breakfast", 0),
    ("dubai", "egg", "09_september","hot",  "dinner",    0),
    ("dubai", "egg", "09_september","hot",  "lunch",     0),
    ("dubai", "egg", "09_september","hot",  "snack",     0),
    # egg — 1 image
    ("dubai", "egg", "07_july",     "hot",  "dinner",    1),
    ("dubai", "egg", "08_august",   "hot",  "lunch",     1),
    ("dubai", "egg", "10_october",  "warm", "lunch",     1),
    ("dubai", "egg", "12_december", "mild", "snack",     1),
    # egg — 2 images
    ("dubai", "egg", "10_october",  "warm", "lunch",     2),
    # egg — 3 images
    ("dubai", "egg", "06_june",     "hot",  "dinner",    3),
    ("dubai", "egg", "12_december", "mild", "dinner",    3),
    ("dubai", "egg", "12_december", "mild", "lunch",     3),
    # egg — 4 images
    ("dubai", "egg", "10_october",  "warm", "breakfast", 4),
    # egg — 5 images (none for dubai egg)

    # non_veg — 0 images
    ("dubai", "non_veg", "07_july",     "hot",  "breakfast", 0),
    ("dubai", "non_veg", "08_august",   "hot",  "breakfast", 0),
    ("dubai", "non_veg", "08_august",   "hot",  "lunch",     0),
    ("dubai", "non_veg", "08_august",   "hot",  "snack",     0),
    ("dubai", "non_veg", "09_september","hot",  "breakfast", 0),
    ("dubai", "non_veg", "12_december", "mild", "breakfast", 0),
    ("dubai", "non_veg", "12_december", "mild", "lunch",     0),
    # non_veg — 1 image
    ("dubai", "non_veg", "04_april",    "warm", "breakfast", 1),
    ("dubai", "non_veg", "09_september","hot",  "dinner",    1),
    ("dubai", "non_veg", "10_october",  "warm", "breakfast", 1),
    ("dubai", "non_veg", "10_october",  "warm", "dinner",    1),
    ("dubai", "non_veg", "10_october",  "warm", "lunch",     1),
    ("dubai", "non_veg", "11_november", "mild", "lunch",     1),
    # non_veg — 2 images
    ("dubai", "non_veg", "06_june",     "hot",  "snack",     2),
    ("dubai", "non_veg", "09_september","hot",  "snack",     2),
    # non_veg — 3 images
    ("dubai", "non_veg", "05_may",      "hot",  "breakfast", 3),
    ("dubai", "non_veg", "06_june",     "hot",  "breakfast", 3),
    ("dubai", "non_veg", "07_july",     "hot",  "lunch",     3),
    ("dubai", "non_veg", "12_december", "mild", "snack",     3),
    # non_veg — 4 images
    ("dubai", "non_veg", "07_july",     "hot",  "dinner",    4),
    ("dubai", "non_veg", "07_july",     "hot",  "snack",     4),
    ("dubai", "non_veg", "08_august",   "hot",  "dinner",    4),
    # non_veg — 5 images
    ("dubai", "non_veg", "09_september","hot",  "lunch",     5),
    ("dubai", "non_veg", "10_october",  "warm", "lunch",     5),

    # veg — 0 images
    ("dubai", "veg", "04_april",    "warm", "dinner",    0),
    ("dubai", "veg", "07_july",     "hot",  "dinner",    0),
    ("dubai", "veg", "08_august",   "hot",  "breakfast", 0),
    ("dubai", "veg", "08_august",   "hot",  "dinner",    0),
    ("dubai", "veg", "08_august",   "hot",  "snack",     0),
    ("dubai", "veg", "09_september","hot",  "breakfast", 0),
    ("dubai", "veg", "09_september","hot",  "dinner",    0),
    ("dubai", "veg", "09_september","hot",  "lunch",     0),
    ("dubai", "veg", "10_october",  "warm", "breakfast", 0),
    ("dubai", "veg", "10_october",  "warm", "dinner",    0),
    ("dubai", "veg", "12_december", "mild", "lunch",     0),
    # veg — 1 image
    ("dubai", "veg", "06_june",     "hot",  "dinner",    1),
    ("dubai", "veg", "07_july",     "hot",  "breakfast", 1),
    ("dubai", "veg", "10_october",  "warm", "snack",     1),
    ("dubai", "veg", "12_december", "mild", "dinner",    1),
    # veg — 2 images
    ("dubai", "veg", "11_november", "mild", "dinner",    2),
    # veg — 3 images
    ("dubai", "veg", "04_april",    "warm", "snack",     3),
    ("dubai", "veg", "06_june",     "hot",  "snack",     3),
    # veg — 4 images
    ("dubai", "veg", "04_april",    "warm", "snack",     4),
    ("dubai", "veg", "07_july",     "hot",  "snack",     4),
    # veg — 5 images
    ("dubai", "veg", "08_august",   "hot",  "lunch",     5),
    ("dubai", "veg", "11_november", "mild", "lunch",     5),
    ("dubai", "veg", "12_december", "mild", "breakfast", 5),

    # vegan — 0 images
    ("dubai", "vegan", "02_february", "mild", "lunch",     0),
    ("dubai", "vegan", "02_february", "mild", "snack",     0),
    ("dubai", "vegan", "04_april",    "warm", "dinner",    0),
    ("dubai", "vegan", "04_april",    "warm", "snack",     0),
    ("dubai", "vegan", "05_may",      "hot",  "snack",     0),
    ("dubai", "vegan", "06_june",     "hot",  "breakfast", 0),
    ("dubai", "vegan", "06_june",     "hot",  "lunch",     0),
    ("dubai", "vegan", "06_june",     "hot",  "snack",     0),
    ("dubai", "vegan", "07_july",     "hot",  "lunch",     0),
    ("dubai", "vegan", "08_august",   "hot",  "breakfast", 0),
    ("dubai", "vegan", "08_august",   "hot",  "dinner",    0),
    ("dubai", "vegan", "08_august",   "hot",  "lunch",     0),
    ("dubai", "vegan", "08_august",   "hot",  "snack",     0),
    ("dubai", "vegan", "09_september","hot",  "breakfast", 0),
    ("dubai", "vegan", "09_september","hot",  "dinner",    0),
    ("dubai", "vegan", "09_september","hot",  "lunch",     0),
    ("dubai", "vegan", "09_september","hot",  "snack",     0),
    ("dubai", "vegan", "10_october",  "warm", "dinner",    0),
    ("dubai", "vegan", "11_november", "mild", "dinner",    0),
    ("dubai", "vegan", "11_november", "mild", "lunch",     0),
    ("dubai", "vegan", "11_november", "mild", "snack",     0),
    ("dubai", "vegan", "12_december", "mild", "breakfast", 0),
    ("dubai", "vegan", "12_december", "mild", "lunch",     0),
    ("dubai", "vegan", "12_december", "mild", "dinner",    0),
    # vegan — 1 image
    ("dubai", "vegan", "03_march",    "warm", "lunch",     1),
    ("dubai", "vegan", "04_april",    "warm", "lunch",     1),
    ("dubai", "vegan", "05_may",      "hot",  "lunch",     1),
    ("dubai", "vegan", "06_june",     "hot",  "dinner",    1),
    ("dubai", "vegan", "07_july",     "hot",  "breakfast", 1),
    ("dubai", "vegan", "07_july",     "hot",  "dinner",    1),
    ("dubai", "vegan", "10_october",  "warm", "lunch",     1),
    ("dubai", "vegan", "10_october",  "warm", "snack",     1),
    ("dubai", "vegan", "11_november", "mild", "breakfast", 1),
    # vegan — 2 images
    ("dubai", "vegan", "07_july",     "hot",  "snack",     2),
    # vegan — 3 images
    ("dubai", "vegan", "05_may",      "hot",  "dinner",    3),
    # vegan — 4 images
    ("dubai", "vegan", "02_february", "mild", "dinner",    4),
    # vegan — 5 images
    ("dubai", "vegan", "02_february", "mild", "breakfast", 5),
    ("dubai", "vegan", "03_march",    "warm", "dinner",    5),

    # ================================================================
    # MIAMI
    # ================================================================

    # egg — 0 images
    ("miami", "egg", "08_august",   "summer", "dinner",    0),
    ("miami", "egg", "08_august",   "summer", "lunch",     0),
    ("miami", "egg", "10_october",  "autumn", "breakfast", 0),
    ("miami", "egg", "10_october",  "autumn", "dinner",    0),
    ("miami", "egg", "10_october",  "autumn", "lunch",     0),
    ("miami", "egg", "11_november", "autumn", "breakfast", 0),
    ("miami", "egg", "11_november", "autumn", "lunch",     0),
    ("miami", "egg", "12_december", "winter", "snack",     0),
    # egg — 1 image
    ("miami", "egg", "06_june",     "summer", "lunch",     1),
    ("miami", "egg", "11_november", "autumn", "dinner",    1),
    ("miami", "egg", "12_december", "winter", "dinner",    1),
    # egg — 2 images
    ("miami", "egg", "04_april",    "spring", "breakfast", 2),
    ("miami", "egg", "04_april",    "spring", "dinner",    2),
    ("miami", "egg", "04_april",    "spring", "lunch",     2),
    ("miami", "egg", "07_july",     "summer", "snack",     2),
    ("miami", "egg", "08_august",   "summer", "snack",     2),
    ("miami", "egg", "12_december", "winter", "lunch",     2),
    # egg — 3 images
    ("miami", "egg", "02_february", "winter", "lunch",     3),
    ("miami", "egg", "04_april",    "spring", "snack",     3),
    ("miami", "egg", "06_june",     "summer", "dinner",    3),
    ("miami", "egg", "07_july",     "summer", "lunch",     3),
    ("miami", "egg", "09_september","autumn", "dinner",    3),
    ("miami", "egg", "09_september","autumn", "lunch",     3),
    ("miami", "egg", "11_november", "autumn", "snack",     3),
    # egg — 4 images
    ("miami", "egg", "02_february", "winter", "dinner",    4),
    ("miami", "egg", "06_june",     "summer", "breakfast", 4),
    ("miami", "egg", "07_july",     "summer", "breakfast", 4),
    ("miami", "egg", "12_december", "winter", "breakfast", 4),
    # egg — 5 images
    ("miami", "egg", "03_march",    "spring", "lunch",     5),
    ("miami", "egg", "05_may",      "summer", "snack",     5),

    # non_veg — 0 images
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
    # non_veg — 1 image
    ("miami", "non_veg", "03_march",    "spring", "dinner",    1),
    ("miami", "non_veg", "06_june",     "summer", "breakfast", 1),
    ("miami", "non_veg", "07_july",     "summer", "snack",     1),
    ("miami", "non_veg", "09_september","autumn", "breakfast", 1),
    ("miami", "non_veg", "09_september","autumn", "dinner",    1),
    ("miami", "non_veg", "12_december", "winter", "lunch",     1),
    # non_veg — 2 images
    ("miami", "non_veg", "05_may",      "summer", "breakfast", 2),
    ("miami", "non_veg", "06_june",     "summer", "breakfast", 2),
    ("miami", "non_veg", "08_august",   "summer", "dinner",    2),
    ("miami", "non_veg", "10_october",  "autumn", "snack",     2),
    ("miami", "non_veg", "12_december", "winter", "dinner",    2),
    # non_veg — 3 images
    ("miami", "non_veg", "04_april",    "spring", "snack",     3),
    # non_veg — 4 images
    ("miami", "non_veg", "03_march",    "spring", "breakfast", 4),

    # veg — 0 images
    ("miami", "veg", "06_june",     "summer", "dinner",    0),
    ("miami", "veg", "08_august",   "summer", "dinner",    0),
    ("miami", "veg", "09_september","autumn", "breakfast", 0),
    ("miami", "veg", "10_october",  "autumn", "dinner",    0),
    ("miami", "veg", "11_november", "autumn", "breakfast", 0),
    ("miami", "veg", "11_november", "autumn", "dinner",    0),
    ("miami", "veg", "11_november", "autumn", "lunch",     0),
    ("miami", "veg", "11_november", "autumn", "snack",     0),
    ("miami", "veg", "12_december", "winter", "breakfast", 0),
    ("miami", "veg", "12_december", "winter", "dinner",    0),
    ("miami", "veg", "12_december", "winter", "lunch",     0),
    # veg — 1 image
    ("miami", "veg", "08_august",   "summer", "lunch",     1),
    ("miami", "veg", "08_august",   "summer", "snack",     1),
    ("miami", "veg", "09_september","autumn", "dinner",    1),
    # veg — 2 images
    ("miami", "veg", "07_july",     "summer", "breakfast", 2),
    # veg — 3 images
    ("miami", "veg", "10_october",  "autumn", "breakfast", 3),
    # veg — 4 images
    ("miami", "veg", "09_september","autumn", "snack",     4),
    # veg — 5 images
    ("miami", "veg", "06_june",     "summer", "lunch",     5),
    ("miami", "veg", "07_july",     "summer", "dinner",    5),

    # vegan — 0 images
    ("miami", "vegan", "03_march",    "spring", "dinner",    0),
    ("miami", "vegan", "04_april",    "spring", "breakfast", 0),
    ("miami", "vegan", "04_april",    "spring", "dinner",    0),
    ("miami", "vegan", "04_april",    "spring", "lunch",     0),
    ("miami", "vegan", "07_july",     "summer", "lunch",     0),
    ("miami", "vegan", "08_august",   "summer", "breakfast", 0),
    ("miami", "vegan", "08_august",   "summer", "dinner",    0),
    ("miami", "vegan", "08_august",   "summer", "lunch",     0),
    ("miami", "vegan", "08_august",   "summer", "snack",     0),
    ("miami", "vegan", "09_september","autumn", "dinner",    0),
    ("miami", "vegan", "09_september","autumn", "lunch",     0),
    ("miami", "vegan", "10_october",  "autumn", "dinner",    0),
    ("miami", "vegan", "10_october",  "autumn", "lunch",     0),
    ("miami", "vegan", "10_october",  "autumn", "snack",     0),
    ("miami", "vegan", "11_november", "autumn", "breakfast", 0),
    ("miami", "vegan", "11_november", "autumn", "dinner",    0),
    ("miami", "vegan", "11_november", "autumn", "lunch",     0),
    ("miami", "vegan", "11_november", "autumn", "snack",     0),
    ("miami", "vegan", "12_december", "winter", "snack",     0),
    # vegan — 1 image
    ("miami", "vegan", "02_february", "winter", "snack",     1),
    ("miami", "vegan", "04_april",    "spring", "snack",     1),
    ("miami", "vegan", "05_may",      "summer", "dinner",    1),
    ("miami", "vegan", "06_june",     "summer", "lunch",     1),
    ("miami", "vegan", "07_july",     "summer", "snack",     1),
    ("miami", "vegan", "09_september","autumn", "snack",     1),
    ("miami", "vegan", "10_october",  "autumn", "breakfast", 1),
    # vegan — 2 images
    ("miami", "vegan", "06_june",     "summer", "dinner",    2),
    ("miami", "vegan", "07_july",     "summer", "dinner",    2),
    ("miami", "vegan", "09_september","autumn", "breakfast", 2),
    # vegan — 3 images
    ("miami", "vegan", "02_february", "winter", "dinner",    3),
    ("miami", "vegan", "06_june",     "summer", "snack",     3),
    ("miami", "vegan", "12_december", "winter", "dinner",    3),
    ("miami", "vegan", "12_december", "winter", "lunch",     3),
    # vegan — 4 images
    ("miami", "vegan", "03_march",    "spring", "breakfast", 4),
    ("miami", "vegan", "03_march",    "spring", "snack",     4),
    ("miami", "vegan", "05_may",      "summer", "lunch",     4),
    ("miami", "vegan", "05_may",      "summer", "snack",     4),

    # ================================================================
    # PARIS
    # ================================================================

    # egg — 0 images
    ("paris", "egg", "04_april",    "spring", "snack",     0),
    ("paris", "egg", "05_may",      "spring", "dinner",    0),
    ("paris", "egg", "05_may",      "spring", "lunch",     0),
    ("paris", "egg", "07_july",     "summer", "dinner",    0),
    ("paris", "egg", "08_august",   "summer", "breakfast", 0),
    ("paris", "egg", "08_august",   "summer", "dinner",    0),
    ("paris", "egg", "10_october",  "autumn", "snack",     0),
    ("paris", "egg", "11_november", "autumn", "snack",     0),
    # egg — 1 image
    ("paris", "egg", "07_july",     "summer", "lunch",     1),
    ("paris", "egg", "08_august",   "summer", "snack",     1),
    ("paris", "egg", "11_november", "autumn", "dinner",    1),
    ("paris", "egg", "12_december", "winter", "dinner",    1),
    # egg — 2 images
    ("paris", "egg", "04_april",    "spring", "dinner",    2),
    ("paris", "egg", "07_july",     "summer", "breakfast", 2),
    ("paris", "egg", "07_july",     "summer", "snack",     2),
    ("paris", "egg", "08_august",   "summer", "lunch",     2),
    ("paris", "egg", "11_november", "autumn", "breakfast", 2),
    # egg — 3 images
    ("paris", "egg", "04_april",    "spring", "lunch",     3),
    ("paris", "egg", "10_october",  "autumn", "lunch",     3),
    ("paris", "egg", "12_december", "winter", "lunch",     3),
    # egg — 4 images
    ("paris", "egg", "10_october",  "autumn", "breakfast", 4),
    ("paris", "egg", "10_october",  "autumn", "dinner",    4),
    ("paris", "egg", "11_november", "autumn", "lunch",     4),
    ("paris", "egg", "12_december", "winter", "snack",     4),
    # egg — 5 images
    ("paris", "egg", "09_september","autumn", "snack",     5),

    # non_veg — 0 images
    ("paris", "non_veg", "05_may",      "spring", "breakfast", 0),
    ("paris", "non_veg", "05_may",      "spring", "dinner",    0),
    ("paris", "non_veg", "05_may",      "spring", "snack",     0),
    ("paris", "non_veg", "08_august",   "summer", "breakfast", 0),
    ("paris", "non_veg", "08_august",   "summer", "lunch",     0),
    ("paris", "non_veg", "08_august",   "summer", "snack",     0),
    ("paris", "non_veg", "10_october",  "autumn", "dinner",    0),
    ("paris", "non_veg", "11_november", "autumn", "dinner",    0),
    ("paris", "non_veg", "12_december", "winter", "snack",     0),
    # non_veg — 1 image
    ("paris", "non_veg", "11_november", "autumn", "breakfast", 1),
    ("paris", "non_veg", "11_november", "autumn", "lunch",     1),
    # non_veg — 2 images
    ("paris", "non_veg", "04_april",    "spring", "dinner",    2),
    ("paris", "non_veg", "05_may",      "spring", "lunch",     2),
    ("paris", "non_veg", "07_july",     "summer", "breakfast", 2),
    ("paris", "non_veg", "07_july",     "summer", "snack",     2),
    ("paris", "non_veg", "10_october",  "autumn", "breakfast", 2),
    # non_veg — 3 images
    ("paris", "non_veg", "04_april",    "spring", "snack",     3),
    ("paris", "non_veg", "10_october",  "autumn", "snack",     3),
    # non_veg — 4 images
    ("paris", "non_veg", "04_april",    "spring", "breakfast", 4),
    ("paris", "non_veg", "10_october",  "autumn", "lunch",     4),
    # non_veg — 5 images
    ("paris", "non_veg", "07_july",     "summer", "lunch",     5),
    ("paris", "non_veg", "09_september","autumn", "lunch",     5),

    # veg — ALL folders 0 images (entire paris/veg is empty)
    ("paris", "veg", "01_january",  "winter", "breakfast", 0),
    ("paris", "veg", "01_january",  "winter", "lunch",     0),
    ("paris", "veg", "01_january",  "winter", "dinner",    0),
    ("paris", "veg", "01_january",  "winter", "snack",     0),
    ("paris", "veg", "02_february", "winter", "breakfast", 0),
    ("paris", "veg", "02_february", "winter", "lunch",     0),
    ("paris", "veg", "02_february", "winter", "dinner",    0),
    ("paris", "veg", "02_february", "winter", "snack",     0),
    ("paris", "veg", "03_march",    "spring", "breakfast", 0),
    ("paris", "veg", "03_march",    "spring", "lunch",     0),
    ("paris", "veg", "03_march",    "spring", "dinner",    0),
    ("paris", "veg", "03_march",    "spring", "snack",     0),
    ("paris", "veg", "04_april",    "spring", "breakfast", 0),
    ("paris", "veg", "04_april",    "spring", "lunch",     0),
    ("paris", "veg", "04_april",    "spring", "dinner",    0),
    ("paris", "veg", "04_april",    "spring", "snack",     0),
    ("paris", "veg", "05_may",      "spring", "breakfast", 0),
    ("paris", "veg", "05_may",      "spring", "lunch",     0),
    ("paris", "veg", "05_may",      "spring", "dinner",    0),
    ("paris", "veg", "05_may",      "spring", "snack",     0),
    ("paris", "veg", "06_june",     "summer", "breakfast", 0),
    ("paris", "veg", "06_june",     "summer", "lunch",     0),
    ("paris", "veg", "06_june",     "summer", "dinner",    0),
    ("paris", "veg", "06_june",     "summer", "snack",     0),
    ("paris", "veg", "07_july",     "summer", "breakfast", 0),
    ("paris", "veg", "07_july",     "summer", "lunch",     0),
    ("paris", "veg", "07_july",     "summer", "dinner",    0),
    ("paris", "veg", "07_july",     "summer", "snack",     0),
    ("paris", "veg", "08_august",   "summer", "breakfast", 0),
    ("paris", "veg", "08_august",   "summer", "lunch",     0),
    ("paris", "veg", "08_august",   "summer", "dinner",    0),
    ("paris", "veg", "08_august",   "summer", "snack",     0),
    ("paris", "veg", "09_september","autumn", "breakfast", 0),
    ("paris", "veg", "09_september","autumn", "lunch",     0),
    ("paris", "veg", "09_september","autumn", "dinner",    0),
    ("paris", "veg", "09_september","autumn", "snack",     0),
    ("paris", "veg", "10_october",  "autumn", "breakfast", 0),
    ("paris", "veg", "10_october",  "autumn", "lunch",     0),
    ("paris", "veg", "10_october",  "autumn", "dinner",    0),
    ("paris", "veg", "10_october",  "autumn", "snack",     0),
    ("paris", "veg", "11_november", "autumn", "breakfast", 0),
    ("paris", "veg", "11_november", "autumn", "lunch",     0),
    ("paris", "veg", "11_november", "autumn", "dinner",    0),
    ("paris", "veg", "11_november", "autumn", "snack",     0),
    ("paris", "veg", "12_december", "winter", "breakfast", 0),
    ("paris", "veg", "12_december", "winter", "lunch",     0),
    ("paris", "veg", "12_december", "winter", "dinner",    0),
    ("paris", "veg", "12_december", "winter", "snack",     0),

    # vegan — 0 images
    ("paris", "vegan", "08_august",   "summer", "breakfast", 0),
    ("paris", "vegan", "08_august",   "summer", "lunch",     0),
    ("paris", "vegan", "08_august",   "summer", "dinner",    0),
    ("paris", "vegan", "09_september","autumn", "snack",     0),
    ("paris", "vegan", "10_october",  "autumn", "lunch",     0),
    ("paris", "vegan", "11_november", "autumn", "dinner",    0),
    ("paris", "vegan", "11_november", "autumn", "lunch",     0),
    ("paris", "vegan", "12_december", "winter", "dinner",    0),
    ("paris", "vegan", "12_december", "winter", "snack",     0),
    # vegan — 1 image
    ("paris", "vegan", "06_june",     "summer", "dinner",    1),
    ("paris", "vegan", "08_august",   "summer", "snack",     1),
    ("paris", "vegan", "09_september","autumn", "breakfast", 1),
    ("paris", "vegan", "09_september","autumn", "lunch",     1),
    ("paris", "vegan", "11_november", "autumn", "breakfast", 1),
    ("paris", "vegan", "11_november", "autumn", "snack",     1),
    ("paris", "vegan", "12_december", "winter", "breakfast", 1),
    # vegan — 2 images
    ("paris", "vegan", "04_april",    "spring", "dinner",    2),
    ("paris", "vegan", "05_may",      "spring", "breakfast", 2),
    ("paris", "vegan", "05_may",      "spring", "snack",     2),
    ("paris", "vegan", "06_june",     "summer", "snack",     2),
    ("paris", "vegan", "07_july",     "summer", "snack",     2),
    ("paris", "vegan", "10_october",  "autumn", "dinner",    2),
    # vegan — 3 images
    ("paris", "vegan", "05_may",      "spring", "dinner",    3),
    ("paris", "vegan", "09_september","autumn", "dinner",    3),
    ("paris", "vegan", "10_october",  "autumn", "breakfast", 3),
    # vegan — 4 images
    ("paris", "vegan", "06_june",     "summer", "lunch",     4),
    ("paris", "vegan", "07_july",     "summer", "lunch",     4),
    ("paris", "vegan", "10_october",  "autumn", "snack",     4),
    ("paris", "vegan", "12_december", "winter", "lunch",     4),
    # vegan — 5 images
    ("paris", "vegan", "06_june",     "summer", "breakfast", 5),
    ("paris", "vegan", "07_july",     "summer", "breakfast", 5),

    # ================================================================
    # JUNGFRAU
    # ================================================================

    # egg — 0 images
    ("jungfrau", "egg", "08_august",   "summer", "dinner",    0),
    ("jungfrau", "egg", "10_october",  "autumn", "dinner",    0),
    ("jungfrau", "egg", "12_december", "winter", "breakfast", 0),
    ("jungfrau", "egg", "12_december", "winter", "dinner",    0),
    ("jungfrau", "egg", "12_december", "winter", "lunch",     0),
    # egg — 1 image
    ("jungfrau", "egg", "03_march",    "winter", "snack",     1),
    ("jungfrau", "egg", "08_august",   "summer", "lunch",     1),
    ("jungfrau", "egg", "11_november", "winter", "breakfast", 1),
    ("jungfrau", "egg", "11_november", "winter", "dinner",    1),
    ("jungfrau", "egg", "11_november", "winter", "lunch",     1),
    # egg — 2 images
    ("jungfrau", "egg", "03_march",    "winter", "breakfast", 2),
    ("jungfrau", "egg", "07_july",     "summer", "dinner",    2),
    ("jungfrau", "egg", "08_august",   "summer", "breakfast", 2),
    ("jungfrau", "egg", "08_august",   "summer", "snack",     2),
    # egg — 3 images
    ("jungfrau", "egg", "07_july",     "summer", "breakfast", 3),
    ("jungfrau", "egg", "11_november", "winter", "snack",     3),
    ("jungfrau", "egg", "12_december", "winter", "snack",     3),
    # egg — 4 images
    ("jungfrau", "egg", "02_february", "winter", "snack",     4),
    ("jungfrau", "egg", "07_july",     "summer", "snack",     4),
    ("jungfrau", "egg", "10_october",  "autumn", "breakfast", 4),
    # egg — 5 images
    ("jungfrau", "egg", "06_june",     "summer", "snack",     5),
    ("jungfrau", "egg", "09_september","autumn", "breakfast", 5),

    # non_veg — 0 images
    ("jungfrau", "non_veg", "03_march",    "winter", "snack",     0),
    ("jungfrau", "non_veg", "06_june",     "summer", "breakfast", 0),
    ("jungfrau", "non_veg", "07_july",     "summer", "breakfast", 0),
    ("jungfrau", "non_veg", "08_august",   "summer", "dinner",    0),
    ("jungfrau", "non_veg", "11_november", "winter", "breakfast", 0),
    ("jungfrau", "non_veg", "11_november", "winter", "dinner",    0),
    ("jungfrau", "non_veg", "11_november", "winter", "lunch",     0),
    ("jungfrau", "non_veg", "11_november", "winter", "snack",     0),
    ("jungfrau", "non_veg", "12_december", "winter", "breakfast", 0),
    # non_veg — 1 image
    ("jungfrau", "non_veg", "03_march",    "winter", "breakfast", 1),
    ("jungfrau", "non_veg", "03_march",    "winter", "lunch",     1),
    ("jungfrau", "non_veg", "08_august",   "summer", "lunch",     1),
    ("jungfrau", "non_veg", "09_september","autumn", "breakfast", 1),
    ("jungfrau", "non_veg", "10_october",  "autumn", "breakfast", 1),
    ("jungfrau", "non_veg", "12_december", "winter", "snack",     1),
    # non_veg — 2 images
    ("jungfrau", "non_veg", "02_february", "winter", "snack",     2),
    ("jungfrau", "non_veg", "07_july",     "summer", "dinner",    2),
    # non_veg — 3 images
    ("jungfrau", "non_veg", "05_may",      "spring", "breakfast", 3),
    ("jungfrau", "non_veg", "05_may",      "spring", "snack",     3),
    ("jungfrau", "non_veg", "07_july",     "summer", "lunch",     3),
    ("jungfrau", "non_veg", "08_august",   "summer", "breakfast", 3),
    ("jungfrau", "non_veg", "08_august",   "summer", "snack",     3),
    ("jungfrau", "non_veg", "10_october",  "autumn", "lunch",     3),
    ("jungfrau", "non_veg", "12_december", "winter", "dinner",    3),
    # non_veg — 4 images
    ("jungfrau", "non_veg", "02_february", "winter", "breakfast", 4),
    ("jungfrau", "non_veg", "05_may",      "spring", "lunch",     4),
    # non_veg — 5 images
    ("jungfrau", "non_veg", "10_october",  "autumn", "dinner",    5),

    # veg — 0 images
    ("jungfrau", "veg", "12_december", "winter", "dinner",    0),
    ("jungfrau", "veg", "12_december", "winter", "lunch",     0),
    # veg — 1 image
    ("jungfrau", "veg", "11_november", "winter", "snack",     1),
    # veg — 2 images
    ("jungfrau", "veg", "10_october",  "autumn", "snack",     2),
    ("jungfrau", "veg", "11_november", "winter", "breakfast", 2),
    # veg — 3 images
    ("jungfrau", "veg", "12_december", "winter", "breakfast", 3),
    # veg — 4 images
    ("jungfrau", "veg", "08_august",   "summer", "snack",     4),
    # veg — 5 images
    ("jungfrau", "veg", "11_november", "winter", "dinner",    5),
    ("jungfrau", "veg", "12_december", "winter", "snack",     5),

    # vegan — 0 images
    ("jungfrau", "vegan", "10_october",  "autumn", "lunch",     0),
    ("jungfrau", "vegan", "11_november", "winter", "breakfast", 0),
    ("jungfrau", "vegan", "12_december", "winter", "snack",     0),
    # vegan — 1 image
    ("jungfrau", "vegan", "03_march",    "winter", "lunch",     1),
    ("jungfrau", "vegan", "12_december", "winter", "dinner",    1),
    ("jungfrau", "vegan", "12_december", "winter", "lunch",     1),
    # vegan — 2 images
    ("jungfrau", "vegan", "10_october",  "autumn", "snack",     2),
    ("jungfrau", "vegan", "11_november", "winter", "lunch",     2),
    ("jungfrau", "vegan", "11_november", "winter", "snack",     2),
    # vegan — 3 images
    ("jungfrau", "vegan", "12_december", "winter", "breakfast", 3),
    # vegan — 4 images
    ("jungfrau", "vegan", "03_march",    "winter", "breakfast", 4),
    ("jungfrau", "vegan", "03_march",    "winter", "snack",     4),
]

# =============================================================================
# BROADER TOP-UP QUERIES PER LOCATION + MEAL_PREF + MEAL_TIME
# Designed to return reliable results on Bing even for niche combos
# Logic: location food + meal type + meal time → high-probability search terms
# =============================================================================
def get_queries(location, meal_pref, season, time_of_day):
    """
    Returns a list of search queries for this combination.
    Uses progressively broader fallbacks to guarantee results.
    """

    # Base food style per location
    location_food = {
        "dubai":    {"base": "arabic middle east food", "veg": "arabic vegetarian food", "vegan": "arabic vegan food",
                     "egg": "egg dish arabic breakfast", "non_veg": "arabic meat grilled shawarma"},
        "miami":    {"base": "miami american food", "veg": "miami vegetarian food",  "vegan": "miami vegan food",
                     "egg": "egg dish american breakfast", "non_veg": "miami seafood meat burger"},
        "paris":    {"base": "french paris food", "veg": "french vegetarian food", "vegan": "french vegan food",
                     "egg": "egg dish french omelette", "non_veg": "french meat steak bistro"},
        "jungfrau": {"base": "swiss alpine food", "veg": "swiss vegetarian food", "vegan": "swiss vegan food",
                     "egg": "egg dish swiss breakfast", "non_veg": "swiss meat fondue raclette"},
    }

    meal_time_terms = {
        "breakfast": "breakfast morning meal",
        "lunch":     "lunch midday meal plate",
        "dinner":    "dinner evening meal plate",
        "snack":     "snack food bite",
    }

    loc_food = location_food.get(location, {})
    base     = loc_food.get("base", f"{location} food")
    specific = loc_food.get(meal_pref, base)
    mtime    = meal_time_terms.get(time_of_day, time_of_day)

    return [
        f"{specific} {time_of_day}",
        f"{location} {meal_pref} food {time_of_day} restaurant",
        f"{specific} {mtime}",
        f"{location} food restaurant dish {time_of_day}",
        f"{base} {time_of_day} dish plate",
    ]


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
            "location": location.title(), "meal_preference": meal_pref,
            "month": month_folder.replace("_", " ").title(),
            "season": season.title(), "time_of_day": time_of_day.title(),
        }
    items = [{
        "filename": f,
        "dish_name": f"{location.title()} {meal_pref} {time_of_day} dish",
        "food_category": meal_pref,
        "meal_preference": meal_pref,
        "time_of_day": time_of_day,
        "description": f"Top-up food image for {location}/{meal_pref}/{season}/{time_of_day}",
        "restaurant_name": "placeholder - needs manual review",
        "price_range": "placeholder - needs manual review",
        "dietary_note": f"Suitable for {meal_pref} preference"
    } for f in images]
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump({"folder_context": existing_ctx, "items": items}, f, indent=2, ensure_ascii=False)


# =============================================================================
# CORE: Top-up one food folder
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

    current_images = sorted([f for f in os.listdir(folder_path) if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))])
    current_count  = len(current_images)

    if current_count >= TARGET:
        return f"⏭️  SKIP {location}/{meal_pref}/{month_folder}/{season}/{time_of_day} — {current_count} imgs"

    load_existing_hashes(folder_path)

    queries  = get_queries(location, meal_pref, season, time_of_day)
    safe     = f"{location}_{meal_pref}_{month_folder}_{season}_{time_of_day}"
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

    total = len(TOPUP_FOLDERS)
    by_loc = {}
    for t in TOPUP_FOLDERS:
        by_loc[t[0]] = by_loc.get(t[0], 0) + 1

    print("=" * 65)
    print("  FOOD TOP-UP SCRIPT")
    print(f"  Target         : {TARGET} images per folder")
    print(f"  Total folders  : {total}")
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
            print(f"  [{done:>3}/{total}] {result}")
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