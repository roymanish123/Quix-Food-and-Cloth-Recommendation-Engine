"""
cleanup_and_sync.py
====================
For every folder in the clothes dataset:
  1. Reads actual image files present on disk
  2. Removes entries from metadata.json that no longer exist on disk
  3. Renames remaining images to serial order: img_001.jpg, img_002.jpg ...
  4. Updates metadata.json filenames to match the new serial names
  5. Saves the cleaned metadata.json back

Run from:
  C:\\Users\\MANISH\\Downloads\\Quix_Recommendation_engine\\code\\
Command:
  python cleanup_and_sync.py
"""

import os
import json
import shutil

# ── CONFIG ────────────────────────────────────────────────────────────────────
BASE_DIR = r"dataset\clothes\images"   # relative to code\ folder
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
# ─────────────────────────────────────────────────────────────────────────────


def get_image_files(folder_path):
    """Return sorted list of image filenames in a folder (no metadata.json)."""
    files = []
    for f in os.listdir(folder_path):
        if os.path.splitext(f)[1].lower() in IMAGE_EXTS:
            files.append(f)
    files.sort()
    return files


def rename_images_serially(folder_path, image_files):
    """
    Rename images to img_001.jpg, img_002.jpg ...
    Returns a dict mapping old_name -> new_name.
    Uses a temp rename pass to avoid collision (e.g. img_002 -> img_001 clash).
    """
    rename_map = {}

    # Pass 1: rename all to temp names to avoid collisions
    for i, old_name in enumerate(image_files):
        ext = os.path.splitext(old_name)[1].lower()
        # Normalize to .jpg for consistency
        temp_name = f"__temp_{i:04d}{ext}"
        os.rename(
            os.path.join(folder_path, old_name),
            os.path.join(folder_path, temp_name)
        )
        rename_map[old_name] = temp_name

    # Pass 2: rename temp names to final serial names
    final_map = {}
    temp_files = sorted([v for v in rename_map.values()])
    for i, temp_name in enumerate(temp_files):
        ext = os.path.splitext(temp_name)[1].lower()
        final_name = f"img_{i+1:03d}{ext}"
        os.rename(
            os.path.join(folder_path, temp_name),
            os.path.join(folder_path, final_name)
        )
        # Map original name -> final serial name
        orig_name = [k for k, v in rename_map.items() if v == temp_name][0]
        final_map[orig_name] = final_name

    return final_map


def clean_metadata(folder_path, rename_map):
    """
    Update metadata.json:
      - Remove items whose original filename no longer exists
      - Update filenames in items to new serial names
    """
    meta_path = os.path.join(folder_path, "metadata.json")

    if not os.path.exists(meta_path):
        # No metadata.json — nothing to update
        return 0, 0

    with open(meta_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print(f"  ⚠️  Could not parse metadata.json in {folder_path} — skipping")
            return 0, 0

    original_count = len(data.get("items", []))
    kept_items = []

    for item in data.get("items", []):
        old_filename = item.get("filename", "")
        if old_filename in rename_map:
            # File still exists — update to new serial name
            item["filename"] = rename_map[old_filename]
            kept_items.append(item)
        # else: file was deleted — drop this item from metadata

    removed_count = original_count - len(kept_items)
    data["items"] = kept_items

    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return original_count, removed_count


def process_folder(folder_path):
    """Process a single time_of_day leaf folder."""
    image_files = get_image_files(folder_path)

    if not image_files:
        return  # Empty folder — nothing to do

    # Step 1: Rename images serially
    rename_map = rename_images_serially(folder_path, image_files)

    # Step 2: Update metadata.json
    original_count, removed_count = clean_metadata(folder_path, rename_map)

    kept = len(rename_map)
    rel_path = os.path.relpath(folder_path, BASE_DIR)

    if removed_count > 0:
        print(f"  ✅ {rel_path}")
        print(f"     Removed from metadata: {removed_count} | Kept: {kept} | Renamed: {kept}")
    # Uncomment below line to see ALL folders (not just changed ones):
    # else:
    #     print(f"  ✓  {rel_path} — {kept} images, no changes needed")


def is_leaf_folder(folder_path):
    """
    A leaf folder = time_of_day level = contains image files directly.
    Depth pattern: images/{location}/{gender}/{month}/{season}/{time_of_day}/
    """
    for f in os.listdir(folder_path):
        if os.path.splitext(f)[1].lower() in IMAGE_EXTS:
            return True
    return False


def walk_and_process(base_dir):
    """Walk the entire dataset tree and process every leaf folder."""
    total_folders = 0
    changed_folders = 0
    total_removed = 0

    for root, dirs, files in os.walk(base_dir):
        # Skip non-leaf folders
        has_images = any(
            os.path.splitext(f)[1].lower() in IMAGE_EXTS for f in files
        )
        if not has_images:
            continue

        # Count before
        image_files_before = get_image_files(root)
        count_before = len(image_files_before)

        if count_before == 0:
            continue

        total_folders += 1

        # Check if metadata.json has ghost entries
        meta_path = os.path.join(root, "metadata.json")
        ghost_count = 0
        if os.path.exists(meta_path):
            try:
                with open(meta_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                meta_filenames = {item.get("filename", "") for item in data.get("items", [])}
                actual_filenames = set(image_files_before)
                ghost_count = len(meta_filenames - actual_filenames)
            except Exception:
                pass

        process_folder(root)

        if ghost_count > 0:
            changed_folders += 1
            total_removed += ghost_count

    return total_folders, changed_folders, total_removed


def main():
    if not os.path.exists(BASE_DIR):
        print(f"❌ Dataset not found at: {os.path.abspath(BASE_DIR)}")
        print("   Make sure you're running this from:")
        print("   C:\\Users\\MANISH\\Downloads\\Quix_Recommendation_engine\\code\\")
        return

    print("=" * 65)
    print("  CLOTHES DATASET — CLEANUP & SYNC")
    print("  • Removes deleted image entries from metadata.json")
    print("  • Renames remaining images to serial order (img_001, ...)")
    print("=" * 65)
    print()

    total_folders, changed_folders, total_removed = walk_and_process(BASE_DIR)

    print()
    print("=" * 65)
    print("  SUMMARY")
    print(f"  Total leaf folders processed : {total_folders}")
    print(f"  Folders with changes         : {changed_folders}")
    print(f"  Total ghost entries removed  : {total_removed}")
    print("=" * 65)
    print()
    print("✅ Done! All metadata.json files are now in sync with disk.")
    print("   Images renamed to img_001, img_002 ... serial order.")


if __name__ == "__main__":
    main()