# # =============================================================================
# # main.py — Orchestrator for Quix Dataset Pipeline
# # =============================================================================

# import os
# import json
# import time
# from config import PILOT_MODE, PILOT_LOCATION, SEASON_MAP, MONTH_FOLDERS
# from downloader import download_clothes_location, GLOBAL_HASH_REGISTRY
# from food_downloader import download_food_location

# # All 4 locations — order matters for pilot
# ALL_LOCATIONS = ["dubai", "paris", "jungfrau", "miami"]

# def count_dataset_stats(base_path):
#     """Count images and folders in dataset"""
#     total_images = 0
#     total_folders = 0
#     stats = {}

#     if not os.path.exists(base_path):
#         return stats, 0, 0

#     for root, dirs, files in os.walk(base_path):
#         images = [f for f in files if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))]
#         if images:
#             total_folders += 1
#             total_images += len(images)
#             # Get relative path for display
#             rel = os.path.relpath(root, base_path)
#             stats[rel] = len(images)

#     return stats, total_images, total_folders


# def print_summary():
#     """Print final dataset summary"""
#     print("\n" + "="*60)
#     print("📊 DATASET SUMMARY")
#     print("="*60)

#     for dataset_type in ["clothes", "food"]:
#         base = os.path.join("dataset", dataset_type, "images")
#         _, total_images, total_folders = count_dataset_stats(base)
#         print(f"\n{dataset_type.upper()}")
#         print(f"  Total images  : {total_images}")
#         print(f"  Total folders : {total_folders}")

#         if os.path.exists(base):
#             for location in os.listdir(base):
#                 loc_path = os.path.join(base, location)
#                 _, loc_images, loc_folders = count_dataset_stats(loc_path)
#                 print(f"  📍 {location:<12}: {loc_images:>5} images in {loc_folders} folders")


# def run_pilot():
#     """Run Dubai pilot only"""
#     print("\n" + "="*60)
#     print(f"🚀 PILOT MODE — Running {PILOT_LOCATION.upper()} only")
#     print("="*60)
#     print("✅ After pilot completes, verify structure then set")
#     print("   PILOT_MODE = False in config.py to run all locations")
#     print("="*60)

#     start = time.time()

#     # Phase 1: Clothes
#     print("\n\n📦 PHASE 1: CLOTHES DATASET")
#     download_clothes_location(PILOT_LOCATION)

#     # Phase 2: Food
#     print("\n\n🍽️  PHASE 2: FOOD DATASET")
#     download_food_location(PILOT_LOCATION)

#     elapsed = time.time() - start
#     print(f"\n⏱️  Pilot completed in {elapsed/60:.1f} minutes")
#     print_summary()

#     print("\n" + "="*60)
#     print("✅ PILOT COMPLETE — Please verify:")
#     print(f"   dataset/clothes/images/{PILOT_LOCATION}/")
#     print(f"   dataset/food/images/{PILOT_LOCATION}/")
#     print("\nIf structure looks correct:")
#     print("   → Set PILOT_MODE = False in config.py")
#     print("   → Run python main.py again for all 4 locations")
#     print("="*60)


# def run_full():
#     """Run all 4 locations"""
#     print("\n" + "="*60)
#     print("🚀 FULL MODE — Running all 4 locations")
#     print("="*60)

#     start = time.time()

#     print("\n\n📦 PHASE 1: CLOTHES DATASET — ALL LOCATIONS")
#     for location in ALL_LOCATIONS:
#         download_clothes_location(location)

#     print("\n\n🍽️  PHASE 2: FOOD DATASET — ALL LOCATIONS")
#     for location in ALL_LOCATIONS:
#         download_food_location(location)

#     elapsed = time.time() - start
#     print(f"\n⏱️  Full pipeline completed in {elapsed/60:.1f} minutes")
#     print_summary()
#     print("\n🎉 DATASET COMPLETE — Ready for recommendation engine!")


# if __name__ == "__main__":
#     print("\n" + "="*60)
#     print("  QUIX RECOMMENDATION ENGINE — DATASET PIPELINE")
#     print("="*60)

#     if PILOT_MODE:
#         run_pilot()
#     else:
#         run_full()


# =============================================================================
# main.py — Orchestrator | Skips completed locations automatically
# =============================================================================

import os
import time
import shutil
from config import PILOT_MODE, PILOT_LOCATION, COMPLETED_LOCATIONS, MAX_WORKERS
from downloader import download_clothes_location
from food_downloader import download_food_location

ALL_LOCATIONS = ["dubai", "paris", "jungfrau", "miami"]


def count_stats(base_path):
    total_images, total_folders = 0, 0
    if not os.path.exists(base_path):
        return 0, 0
    for root, dirs, files in os.walk(base_path):
        imgs = [f for f in files if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))]
        if imgs:
            total_folders += 1
            total_images += len(imgs)
    return total_images, total_folders


def print_summary():
    print("\n" + "="*60)
    print("📊 FINAL DATASET SUMMARY")
    print("="*60)
    for dtype in ["clothes", "food"]:
        base = os.path.join("dataset", dtype, "images")
        total_imgs, total_flds = count_stats(base)
        print(f"\n{dtype.upper()}: {total_imgs} images | {total_flds} folders")
        if os.path.exists(base):
            for loc in sorted(os.listdir(base)):
                loc_path = os.path.join(base, loc)
                imgs, flds = count_stats(loc_path)
                tag = "✅" if loc in COMPLETED_LOCATIONS else "🔄"
                print(f"  {tag} {loc:<12}: {imgs:>5} images | {flds} folders")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("  QUIX RECOMMENDATION ENGINE — DATASET PIPELINE")
    print(f"  Parallel threads : {MAX_WORKERS}")
    print(f"  Skipping         : {COMPLETED_LOCATIONS}")
    print(f"  Remaining        : {[l for l in ALL_LOCATIONS if l not in COMPLETED_LOCATIONS]}")
    print("="*60)

    start = time.time()

    locations_to_run = [l for l in ALL_LOCATIONS if l not in COMPLETED_LOCATIONS]

    if not locations_to_run:
        print("\n🎉 All locations already completed! Nothing to download.")
        print_summary()
    else:
        print(f"\n🚀 Will process: {locations_to_run}")

        print("\n\n📦 PHASE 1: CLOTHES")
        for loc in ALL_LOCATIONS:
            download_clothes_location(loc)

        print("\n\n🍽️  PHASE 2: FOOD")
        for loc in ALL_LOCATIONS:
            download_food_location(loc)

        elapsed = time.time() - start
        hrs = int(elapsed // 3600)
        mins = int((elapsed % 3600) // 60)
        print(f"\n⏱️  Total time: {hrs}h {mins}m")

        print_summary()
        print("\n🎉 Pipeline complete!")
        print("\nNext step: Set PILOT_MODE = False already done.")
        print("After verifying all 4 locations:")
        print("  COMPLETED_LOCATIONS = ['dubai', 'paris', 'jungfrau', 'miami']")