# 🌍 Quix Recommendation Engine

A context-aware recommendation engine that suggests **what to wear** and **what to eat** based on where you are, what time of year it is, and your personal preferences.

Built around a curated image dataset organized by location, season, gender, meal type, and time of day — with rich metadata attached to every folder.

---

## What does it actually do?

You tell Quix: *"I'm in Paris, it's November, I'm vegetarian, and I want dinner ideas"* — and it pulls relevant food images straight from a locally organized dataset, along with context like average temperature, season notes, dish descriptions, and price ranges.

Same idea for clothes: *"I'm heading to Dubai in August, I'm female, going out in the evening"* — it finds appropriate outfits for that exact context.

There are two modes for both food and clothes:

- **Quick mode** — just give it a location and month, get 10 random images from across all categories
- **Full mode** — give it everything (location + month + gender/meal preference + time of day), and it shows you the complete folder with full metadata

---

## Locations covered

| Location | Climate style |
|---|---|
| 🇦🇪 Dubai | mild / warm / hot |
| 🇫🇷 Paris | winter / spring / summer / autumn |
| 🇨🇭 Jungfrau | alpine winter / spring / summer / autumn |
| 🇺🇸 Miami | winter / spring / summer / autumn |

---

## Project structure

```
Quix_Recommendation_engine/
│
├── code/
│   │
│   │   ── CORE PIPELINE ──
│   ├── main.py                    # Entry point — orchestrates the full download pipeline for clothes and food across all locations
│   ├── config.py                  # Master config — holds season maps, avg temperatures, weather notes, and all image search queries
│   │
│   │   ── DOWNLOADERS ──
│   ├── downloader.py              # Downloads clothes images from Bing in parallel, deduplicates by MD5 hash, and writes metadata.json
│   ├── food_downloader.py         # Same as downloader.py but for food — organized by meal preference instead of gender
│   │
│   │   ── TOP-UP SCRIPTS ──
│   ├── topup_clothes.py           # Scans clothes folders that fell short of the target count and downloads only the missing images
│   ├── topup_clothes_round2.py    # Second top-up pass for clothes using even broader search queries when round 1 still wasn't enough
│   ├── topup_food.py              # Same targeted top-up logic, applied to food folders
│   ├── topup_food_round2.py       # Second top-up pass for food with broader fallback queries
│   │
│   │   ── CLEANUP ──
│   ├── cleanup_and_sync_cloth.py  # Removes metadata.json entries for deleted images and renames remaining files to serial order (img_001, img_002 ...)
│   ├── duplicate_remover.py       # Walks the dataset and removes exact duplicate images using MD5 hash comparison
│   ├── metadata_enricher.py       # Detects cultural clothing items by filename (e.g. kandura, abaya) and updates gender and tags in metadata
│   │
│   │   ── RECOMMENDATION ENGINE ──
│   ├── clothes_recommendation.py  # Interactive CLI that takes location, month, gender, and time of day, then displays matching outfit images with metadata
│   └── food_recommendation.py     # Interactive CLI that takes location, month, meal preference, and time of day, then displays matching food images with metadata
│
├── to_keep.txt                    # List of 402 manually approved image paths from the Dubai curation pass — serves as the sample dataset reference
├── to_delete.txt                  # List of image paths flagged for removal during manual review
│
└── dataset/
    ├── clothes/
    │   └── images/
    │       └── {location}/{gender}/{month}/{season}/{time_of_day}/
    │           ├── img_001.jpg
    │           ├── img_002.jpg
    │           └── metadata.json      # Folder context + per-image details (item name, category, occasion, price range)
    └── food/
        └── images/
            └── {location}/{meal_preference}/{month}/{season}/{time_of_day}/
                ├── img_001.jpg
                └── metadata.json      # Folder context + per-image details (dish name, dietary info, price range)
```

---

## Dataset

The full dataset is not included in this repository — it's too large to push to GitHub, and the images are downloaded from the web anyway so it makes more sense to generate it yourself.

That said, **`to_keep.txt` acts as a sample dataset reference**. It contains the list of 402 image paths (255 clothes + 147 food) across 31 folders that were manually reviewed and approved for the Dubai location. These are the exact files from the curated dataset before the images themselves were removed for the repo push.

It shows you the full folder structure the pipeline produces, which combinations are populated, and gives you a concrete sense of what a complete location looks like — without needing to download anything first.

If you want to regenerate the actual images, just run the pipeline as described below and it'll rebuild everything from scratch.

---

## Getting started

### Prerequisites

```bash
pip install icrawler
```

### Step 1 — Download the dataset

Open `config.py` and check the settings at the top:

```python
PILOT_MODE = True          # Start with True to test Dubai only
PILOT_LOCATION = "dubai"
COMPLETED_LOCATIONS = []   # Add locations here once they're done
IMAGES_PER_FOLDER = 15     # Target images per leaf folder
MAX_WORKERS = 5            # Parallel download threads
```

Then run the pipeline:

```bash
cd code
python main.py
```

It'll download clothes first, then food, for whichever locations aren't already in `COMPLETED_LOCATIONS`. Once you're happy with a location, add it to that list so it gets skipped on re-runs.

### Step 2 — Clean up and sync metadata

After downloading, run the cleanup script to remove any ghost entries from `metadata.json` and rename images to a clean serial order:

```bash
python cleanup_and_sync_cloth.py
```

### Step 3 — Top up thin folders

Some folder combinations will end up with fewer images than the target (certain queries just don't return much). Run the top-up scripts to fill those gaps with broader queries:

```bash
python topup_clothes.py
python topup_food.py
```

If folders are still thin after that:

```bash
python topup_clothes_round2.py
python topup_food_round2.py
```

### Step 4 — Run the recommendation engine

For clothes:

```bash
python clothes_recommendation.py
```

For food:

```bash
python food_recommendation.py
```

Follow the prompts — type `exit` at any point to quit.

---

## How the dataset is organized

Each leaf folder contains images + a `metadata.json` that looks like this (for clothes):

```json
{
  "folder_context": {
    "location": "Paris",
    "gender": "Female",
    "month": "November",
    "season": "Autumn",
    "time_of_day": "Evening",
    "avg_temperature_celsius": 9,
    "weather_note": "Cool Paris autumn, layering recommended, frequent rain expected"
  },
  "items": [
    {
      "filename": "img_001.jpg",
      "item_name": "Trench Coat",
      "category": "Outerwear",
      "color": "placeholder - needs manual review",
      "occasion": "Casual",
      "description": "Outfit for Paris in November (autumn) during evening",
      "price_range": "placeholder - needs manual review",
      "cultural_note": "Appropriate for Paris"
    }
  ]
}
```

Food metadata follows the same structure with dish-specific fields like `dish_name`, `meal_preference`, `dietary_note`, and `price_range`.

---

## Clothes categories

- **Gender:** male, female, unisex
- **Time of day:** morning, afternoon, evening, night

## Food categories

- **Meal preference:** veg, vegan, egg, non_veg
- **Time of day:** breakfast, lunch, dinner, snack

---

## A few things to know

**Images are downloaded via Bing Image Crawler.** The queries in `config.py` are carefully written per location, season, gender, and time slot — but some combinations will still come up short. The top-up scripts handle this.

**Deduplication is MD5-based.** The downloader keeps a hash registry in memory during a session so the same image won't appear twice in the dataset, even across different folders.

**Metadata placeholders.** Fields like `color` and `price_range` are marked as `"placeholder - needs manual review"` — these require human curation to fill in accurately.

**`to_keep.txt` and `to_delete.txt`** — produced during manual dataset review. `to_keep.txt` doubles as a sample dataset reference (see the Dataset section above). `to_delete.txt` lists images that were flagged and removed during curation.

---

## Running order (full fresh start)

```
config.py        → set your preferences
main.py          → download everything
cleanup_and_sync_cloth.py → clean metadata
duplicate_remover.py      → remove dupes
topup_clothes.py / topup_food.py       → fill thin folders
topup_*_round2.py                      → second pass if needed
clothes_recommendation.py / food_recommendation.py → run it!
```

---

## Notes for contributors

- All season-to-month mappings live in `config.py` under `SEASON_MAP` — easy to extend with new locations
- Adding a new location means adding entries in `SEASON_MAP`, `AVG_TEMP`, `WEATHER_NOTES`, `CLOTHES_QUERIES`, `UNISEX_QUERIES`, and `FOOD_QUERIES`
- The recommendation scripts use `os.startfile()` to open images, which is Windows-only — you'd need to swap that out for `subprocess` on Mac/Linux
