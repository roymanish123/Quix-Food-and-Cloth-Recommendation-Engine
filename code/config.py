# =============================================================================
# config.py — Master Configuration for Quix Recommendation Engine Dataset
# =============================================================================

# ----------------------------------------------------------------------------
# SEASON MAP: Real climate-based seasons per location per month
# ----------------------------------------------------------------------------
SEASON_MAP = {
    "dubai": {
        1: "mild",   2: "mild",   3: "warm",  4: "warm",
        5: "hot",    6: "hot",    7: "hot",   8: "hot",
        9: "hot",   10: "warm",  11: "mild", 12: "mild"
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

# ----------------------------------------------------------------------------
# MONTH FOLDERS: Zero-padded month folder names
# ----------------------------------------------------------------------------
MONTH_FOLDERS = {
    1:  "01_january",   2:  "02_february",  3:  "03_march",
    4:  "04_april",     5:  "05_may",       6:  "06_june",
    7:  "07_july",      8:  "08_august",    9:  "09_september",
    10: "10_october",  11:  "11_november", 12:  "12_december"
}

# ----------------------------------------------------------------------------
# AVERAGE TEMPERATURES per location per month (Celsius)
# ----------------------------------------------------------------------------
AVG_TEMP = {
    "dubai":    {1:24, 2:25, 3:28, 4:33, 5:38, 6:41, 7:43, 8:43, 9:40, 10:35, 11:30, 12:26},
    "paris":    {1:5,  2:6,  3:10, 4:13, 5:17, 6:21, 7:24, 8:23, 9:19, 10:14, 11:9,  12:6},
    "jungfrau": {1:-8, 2:-8, 3:-6, 4:-2, 5:3,  6:8,  7:11, 8:10, 9:7,  10:2,  11:-4, 12:-7},
    "miami":    {1:20, 2:21, 3:23, 4:25, 5:27, 6:29, 7:30, 8:30, 9:29, 10:27, 11:24, 12:21}
}

# ----------------------------------------------------------------------------
# WEATHER NOTES per location per season
# ----------------------------------------------------------------------------
WEATHER_NOTES = {
    "dubai": {
        "mild":  "Pleasant Dubai weather, light layers comfortable, cooler in early morning and evening",
        "warm":  "Warm Dubai weather, light breathable clothing recommended, sun protection advised",
        "hot":   "Intense Dubai heat, loose lightweight fabrics essential, stay hydrated"
    },
    "paris": {
        "winter": "Cold Paris winter, heavy coat and layers required, possible rain or frost",
        "spring": "Mild Paris spring, light jacket recommended, occasional showers",
        "summer": "Warm Paris summer, light clothing suitable, evenings may be cool",
        "autumn": "Cool Paris autumn, layering recommended, frequent rain expected"
    },
    "jungfrau": {
        "winter": "Extreme Jungfrau cold, heavy ski/thermal wear mandatory, snowfall likely",
        "spring": "Cool alpine spring, warm base layers needed, changeable mountain weather",
        "summer": "Mild alpine summer, light jacket for altitude, UV protection important",
        "autumn": "Cold alpine autumn, warm waterproof layers needed, early snow possible"
    },
    "miami": {
        "winter": "Mild Miami winter, light clothing sufficient, comfortable evenings",
        "spring": "Warm Miami spring, breathable fabrics ideal, increasing humidity",
        "summer": "Hot humid Miami summer, very light clothing, beach-ready outfits",
        "autumn": "Warm Miami autumn, light layers for occasional cool spells"
    }
}

# ----------------------------------------------------------------------------
# TIME OF DAY FOLDERS
# ----------------------------------------------------------------------------
TIMES_OF_DAY = ["morning", "afternoon", "evening", "night"]

# ----------------------------------------------------------------------------
# GENDERS
# ----------------------------------------------------------------------------
GENDERS = ["male", "female", "unisex"]

# ----------------------------------------------------------------------------
# CLOTHES SEARCH QUERIES
# Organized by: location → gender → season → time_of_day
# Each entry: (search_query, item_name, category, occasion)
# ----------------------------------------------------------------------------
CLOTHES_QUERIES = {

    # ==========================================================================
    # DUBAI
    # ==========================================================================
    "dubai": {
        "male": {
            "mild": {
                "morning":   [
                    ("emirati man kandura morning dubai mild winter", "White Kandura", "Traditional Wear", "Cultural/Daily"),
                    ("dubai man light jacket morning casual mild", "Light Casual Jacket", "Outerwear", "Casual"),
                ],
                "afternoon": [
                    ("emirati kandura traditional dubai afternoon", "White Kandura", "Traditional Wear", "Cultural/Daily"),
                    ("dubai man casual shirt chinos afternoon mild", "Casual Shirt & Chinos", "Smart Casual", "Smart Casual"),
                ],
                "evening":   [
                    ("dubai man kandura evening traditional mild", "Kandura Evening", "Traditional Wear", "Formal/Cultural"),
                    ("dubai man smart casual evening mild weather", "Smart Casual Outfit", "Smart Casual", "Evening Wear"),
                ],
                "night":     [
                    ("dubai man smart outfit night mild weather", "Smart Night Outfit", "Formal", "Evening/Night"),
                    ("emirati man kandura night dubai traditional", "Night Kandura", "Traditional Wear", "Cultural/Formal"),
                ],
            },
            "warm": {
                "morning":   [
                    ("dubai man light cotton outfit morning warm spring", "Light Cotton Outfit", "Casual", "Casual"),
                    ("emirati man kandura morning warm dubai april", "Spring Kandura", "Traditional Wear", "Cultural"),
                ],
                "afternoon": [
                    ("dubai man breathable outfit afternoon warm sun", "Breathable Casual Outfit", "Casual", "Casual"),
                    ("dubai man linen shirt trousers warm afternoon", "Linen Shirt & Trousers", "Smart Casual", "Smart Casual"),
                ],
                "evening":   [
                    ("dubai man evening casual warm weather outfit", "Evening Casual", "Casual", "Evening Wear"),
                    ("emirati man kandura evening warm dubai", "Warm Evening Kandura", "Traditional Wear", "Cultural/Formal"),
                ],
                "night":     [
                    ("dubai man smart night outfit warm weather", "Smart Night Casual", "Smart Casual", "Night Out"),
                    ("dubai man traditional outfit night warm", "Traditional Night Wear", "Traditional Wear", "Cultural/Formal"),
                ],
            },
            "hot": {
                "morning":   [
                    ("dubai man loose white outfit morning extreme heat", "Loose White Morning Outfit", "Casual", "Casual"),
                    ("emirati kandura summer morning dubai hot", "Summer Morning Kandura", "Traditional Wear", "Cultural"),
                ],
                "afternoon": [
                    ("dubai man lightweight breathable shirt afternoon hot summer", "Lightweight Summer Shirt", "Casual", "Casual"),
                    ("emirati kandura afternoon dubai summer heat", "Summer Afternoon Kandura", "Traditional Wear", "Cultural"),
                ],
                "evening":   [
                    ("dubai man light casual evening summer hot", "Light Summer Evening Outfit", "Casual", "Evening Wear"),
                    ("emirati man kandura evening summer dubai", "Summer Evening Kandura", "Traditional Wear", "Cultural/Formal"),
                ],
                "night":     [
                    ("dubai man summer night casual outfit hot", "Summer Night Casual", "Casual", "Night Out"),
                    ("dubai man traditional outfit night summer", "Traditional Summer Night", "Traditional Wear", "Cultural/Formal"),
                ],
            },
        },
        "female": {
            "mild": {
                "morning":   [
                    ("emirati woman abaya morning mild dubai winter", "Morning Abaya", "Traditional Wear", "Cultural/Daily"),
                    ("dubai woman modest fashion morning mild", "Modest Morning Fashion", "Modest Wear", "Daily"),
                ],
                "afternoon": [
                    ("emirati abaya afternoon dubai mild", "Afternoon Abaya", "Traditional Wear", "Cultural/Daily"),
                    ("dubai woman modest outfit afternoon mild winter", "Modest Afternoon Outfit", "Modest Wear", "Smart Casual"),
                ],
                "evening":   [
                    ("emirati woman abaya evening dubai mild", "Evening Abaya", "Traditional Wear", "Cultural/Formal"),
                    ("dubai woman jalabiya fashion evening mild", "Evening Jalabiya", "Traditional Wear", "Cultural/Formal"),
                ],
                "night":     [
                    ("dubai woman modest evening gown night mild", "Modest Night Gown", "Formal", "Formal/Evening"),
                    ("emirati woman abaya night dubai traditional", "Night Abaya", "Traditional Wear", "Cultural/Formal"),
                ],
            },
            "warm": {
                "morning":   [
                    ("emirati woman abaya morning warm dubai spring", "Spring Morning Abaya", "Traditional Wear", "Cultural"),
                    ("dubai woman light modest outfit morning warm", "Light Modest Morning Wear", "Modest Wear", "Casual"),
                ],
                "afternoon": [
                    ("dubai woman light abaya afternoon warm", "Light Afternoon Abaya", "Traditional Wear", "Cultural"),
                    ("dubai woman modest summer dress afternoon warm", "Modest Summer Dress", "Modest Wear", "Casual"),
                ],
                "evening":   [
                    ("emirati woman jalabiya evening warm dubai", "Warm Evening Jalabiya", "Traditional Wear", "Cultural/Formal"),
                    ("dubai woman modest fashion evening warm spring", "Modest Evening Fashion", "Modest Wear", "Evening Wear"),
                ],
                "night":     [
                    ("dubai woman modest night outfit warm", "Modest Night Outfit", "Formal", "Evening/Night"),
                    ("emirati abaya night dubai warm traditional", "Traditional Night Abaya", "Traditional Wear", "Cultural/Formal"),
                ],
            },
            "hot": {
                "morning":   [
                    ("emirati woman light abaya morning hot summer dubai", "Light Summer Abaya", "Traditional Wear", "Cultural"),
                    ("dubai woman modest light outfit morning summer hot", "Light Summer Modest Wear", "Modest Wear", "Casual"),
                ],
                "afternoon": [
                    ("dubai woman breathable abaya afternoon hot summer", "Breathable Summer Abaya", "Traditional Wear", "Cultural"),
                    ("dubai woman light modest dress afternoon dubai heat", "Light Modest Dress", "Modest Wear", "Casual"),
                ],
                "evening":   [
                    ("emirati woman abaya evening summer dubai hot", "Summer Evening Abaya", "Traditional Wear", "Cultural/Formal"),
                    ("dubai woman modest fashion evening summer", "Summer Evening Fashion", "Modest Wear", "Evening Wear"),
                ],
                "night":     [
                    ("dubai woman modest night outfit summer hot", "Summer Night Modest Wear", "Casual", "Night Out"),
                    ("emirati woman abaya night summer dubai", "Summer Night Abaya", "Traditional Wear", "Cultural/Formal"),
                ],
            },
        },
    },

    # ==========================================================================
    # PARIS
    # ==========================================================================
    "paris": {
        "male": {
            "winter": {
                "morning":   [
                    ("paris man heavy coat scarf morning winter", "Heavy Winter Coat & Scarf", "Outerwear", "Casual"),
                    ("parisian man layered outfit cold morning", "Layered Winter Outfit", "Smart Casual", "Casual"),
                ],
                "afternoon": [
                    ("paris man trench coat winter afternoon eiffel", "Trench Coat", "Outerwear", "Smart Casual"),
                    ("parisian man smart winter outfit afternoon", "Smart Winter Outfit", "Smart Casual", "Smart Casual"),
                ],
                "evening":   [
                    ("paris man formal coat evening winter dinner", "Formal Winter Coat", "Formal Outerwear", "Formal"),
                    ("parisian man smart casual evening winter outfit", "Smart Evening Winter", "Smart Casual", "Evening Wear"),
                ],
                "night":     [
                    ("paris man formal night winter dinner outfit", "Formal Night Outfit", "Formal", "Formal/Night"),
                    ("parisian man warm night casual outfit winter", "Warm Night Casual", "Smart Casual", "Night Out"),
                ],
            },
            "spring": {
                "morning":   [
                    ("paris man light jacket spring morning casual", "Light Spring Jacket", "Outerwear", "Casual"),
                    ("parisian man spring casual outfit morning", "Spring Morning Casual", "Casual", "Casual"),
                ],
                "afternoon": [
                    ("paris man smart casual spring afternoon outfit", "Smart Spring Afternoon", "Smart Casual", "Smart Casual"),
                    ("parisian man chinos light jacket spring", "Chinos & Light Jacket", "Smart Casual", "Smart Casual"),
                ],
                "evening":   [
                    ("paris man spring evening smart outfit dinner", "Spring Evening Smart", "Smart Casual", "Evening Wear"),
                    ("parisian man casual spring evening light jacket", "Casual Spring Evening", "Casual", "Evening Wear"),
                ],
                "night":     [
                    ("paris man smart night spring outfit", "Smart Spring Night", "Smart Casual", "Night Out"),
                    ("parisian man casual night spring outfit", "Casual Spring Night", "Casual", "Night Out"),
                ],
            },
            "summer": {
                "morning":   [
                    ("paris man summer casual morning linen shirt", "Linen Summer Shirt", "Casual", "Casual"),
                    ("parisian man light outfit summer morning", "Light Summer Morning", "Casual", "Casual"),
                ],
                "afternoon": [
                    ("paris man summer afternoon casual t-shirt chinos", "Summer Casual Afternoon", "Casual", "Casual"),
                    ("parisian man light summer afternoon fashion", "Light Summer Fashion", "Casual", "Casual"),
                ],
                "evening":   [
                    ("paris man summer evening smart casual dinner", "Summer Evening Smart", "Smart Casual", "Evening Wear"),
                    ("parisian man summer evening light outfit", "Summer Evening Light", "Casual", "Evening Wear"),
                ],
                "night":     [
                    ("paris man summer night smart casual outfit", "Summer Smart Night", "Smart Casual", "Night Out"),
                    ("parisian man summer night casual fashion", "Casual Summer Night", "Casual", "Night Out"),
                ],
            },
            "autumn": {
                "morning":   [
                    ("paris man autumn jacket morning casual", "Autumn Morning Jacket", "Outerwear", "Casual"),
                    ("parisian man layered autumn outfit morning", "Layered Autumn Outfit", "Casual", "Casual"),
                ],
                "afternoon": [
                    ("paris man autumn smart casual afternoon outfit", "Smart Autumn Afternoon", "Smart Casual", "Smart Casual"),
                    ("parisian man trench coat autumn afternoon", "Autumn Trench Coat", "Outerwear", "Smart Casual"),
                ],
                "evening":   [
                    ("paris man autumn evening smart coat dinner", "Autumn Evening Coat", "Outerwear", "Evening Wear"),
                    ("parisian man autumn evening casual jacket", "Autumn Evening Jacket", "Outerwear", "Evening Wear"),
                ],
                "night":     [
                    ("paris man autumn night smart casual outfit", "Autumn Smart Night", "Smart Casual", "Night Out"),
                    ("parisian man autumn night warm outfit", "Warm Autumn Night", "Casual", "Night Out"),
                ],
            },
        },
        "female": {
            "winter": {
                "morning":   [
                    ("paris woman heavy winter coat morning scarf", "Heavy Winter Coat & Scarf", "Outerwear", "Casual"),
                    ("parisian woman winter layered outfit morning", "Layered Winter Outfit", "Smart Casual", "Casual"),
                ],
                "afternoon": [
                    ("paris woman chic winter coat afternoon eiffel", "Chic Winter Coat", "Outerwear", "Smart Casual"),
                    ("parisian woman winter fashion afternoon street style", "Parisian Winter Fashion", "Smart Casual", "Smart Casual"),
                ],
                "evening":   [
                    ("paris woman elegant winter evening coat dinner", "Elegant Winter Evening", "Formal Outerwear", "Formal"),
                    ("parisian woman chic winter evening outfit", "Chic Winter Evening", "Smart Casual", "Evening Wear"),
                ],
                "night":     [
                    ("paris woman formal night winter dinner elegant", "Formal Winter Night", "Formal", "Formal/Night"),
                    ("parisian woman warm chic night outfit winter", "Chic Winter Night", "Smart Casual", "Night Out"),
                ],
            },
            "spring": {
                "morning":   [
                    ("paris woman spring light jacket morning casual", "Spring Light Jacket", "Outerwear", "Casual"),
                    ("parisian woman spring dress morning casual", "Spring Morning Dress", "Dress", "Casual"),
                ],
                "afternoon": [
                    ("paris woman spring dress afternoon eiffel tower", "Spring Afternoon Dress", "Dress", "Casual"),
                    ("parisian woman chic spring outfit afternoon", "Chic Spring Afternoon", "Smart Casual", "Smart Casual"),
                ],
                "evening":   [
                    ("paris woman spring evening dress dinner", "Spring Evening Dress", "Dress", "Evening Wear"),
                    ("parisian woman chic spring evening outfit", "Chic Spring Evening", "Smart Casual", "Evening Wear"),
                ],
                "night":     [
                    ("paris woman spring night elegant outfit", "Elegant Spring Night", "Smart Casual", "Night Out"),
                    ("parisian woman casual spring night fashion", "Casual Spring Night", "Casual", "Night Out"),
                ],
            },
            "summer": {
                "morning":   [
                    ("paris woman summer dress morning light casual", "Summer Morning Dress", "Dress", "Casual"),
                    ("parisian woman summer morning light outfit", "Light Summer Morning", "Casual", "Casual"),
                ],
                "afternoon": [
                    ("paris woman summer dress afternoon casual", "Summer Afternoon Dress", "Dress", "Casual"),
                    ("parisian woman chic summer afternoon fashion", "Chic Summer Afternoon", "Smart Casual", "Casual"),
                ],
                "evening":   [
                    ("paris woman summer evening elegant dress dinner", "Elegant Summer Evening", "Dress", "Evening Wear"),
                    ("parisian woman summer evening chic outfit", "Chic Summer Evening", "Smart Casual", "Evening Wear"),
                ],
                "night":     [
                    ("paris woman summer night elegant dinner outfit", "Elegant Summer Night", "Formal", "Night Out"),
                    ("parisian woman summer night casual chic fashion", "Chic Summer Night", "Smart Casual", "Night Out"),
                ],
            },
            "autumn": {
                "morning":   [
                    ("paris woman autumn jacket morning casual scarf", "Autumn Jacket & Scarf", "Outerwear", "Casual"),
                    ("parisian woman autumn dress morning layered", "Layered Autumn Dress", "Dress", "Casual"),
                ],
                "afternoon": [
                    ("paris woman autumn coat afternoon eiffel street style", "Autumn Street Style Coat", "Outerwear", "Smart Casual"),
                    ("parisian woman chic autumn afternoon fashion", "Chic Autumn Afternoon", "Smart Casual", "Smart Casual"),
                ],
                "evening":   [
                    ("paris woman autumn evening coat dinner elegant", "Elegant Autumn Evening", "Formal Outerwear", "Evening Wear"),
                    ("parisian woman autumn evening chic fashion", "Chic Autumn Evening", "Smart Casual", "Evening Wear"),
                ],
                "night":     [
                    ("paris woman autumn night elegant outfit dinner", "Elegant Autumn Night", "Formal", "Night Out"),
                    ("parisian woman autumn night chic casual", "Chic Autumn Night", "Smart Casual", "Night Out"),
                ],
            },
        },
    },

    # ==========================================================================
    # JUNGFRAU
    # ==========================================================================
    "jungfrau": {
        "male": {
            "winter": {
                "morning":   [
                    ("man ski jacket snow jungfrau winter morning", "Ski Jacket", "Outerwear", "Snow/Ski"),
                    ("man heavy thermal outfit alps jungfrau morning cold", "Heavy Thermal Outfit", "Thermal Wear", "Snow/Ski"),
                ],
                "afternoon": [
                    ("man ski suit snow alps jungfrau afternoon", "Ski Suit", "Snow Wear", "Snow/Ski"),
                    ("man winter snow outfit jungfrau mountain afternoon", "Mountain Snow Outfit", "Snow Wear", "Outdoor"),
                ],
                "evening":   [
                    ("man alpine lodge evening outfit warm jungfrau winter", "Alpine Lodge Evening", "Smart Casual", "Evening Wear"),
                    ("man ski resort evening casual warm outfit", "Ski Resort Evening", "Casual", "Evening Wear"),
                ],
                "night":     [
                    ("man alpine resort night warm cozy outfit winter", "Alpine Resort Night", "Casual", "Night/Indoor"),
                    ("man jungfrau resort night smart casual warm", "Resort Smart Night", "Smart Casual", "Night/Indoor"),
                ],
            },
            "spring": {
                "morning":   [
                    ("man alpine spring jacket jungfrau morning cool", "Alpine Spring Jacket", "Outerwear", "Casual/Outdoor"),
                    ("man hiking outfit swiss alps spring morning", "Alpine Hiking Outfit", "Outdoor Wear", "Hiking"),
                ],
                "afternoon": [
                    ("man jungfrau spring hiking outfit afternoon", "Hiking Afternoon Outfit", "Outdoor Wear", "Hiking"),
                    ("man swiss alps spring casual afternoon cool", "Alpine Spring Casual", "Casual", "Outdoor"),
                ],
                "evening":   [
                    ("man swiss mountain spring evening casual warm", "Alpine Spring Evening", "Casual", "Evening Wear"),
                    ("man jungfrau spring lodge evening outfit", "Lodge Spring Evening", "Smart Casual", "Evening Wear"),
                ],
                "night":     [
                    ("man alpine lodge night spring casual warm outfit", "Alpine Night Casual", "Casual", "Night/Indoor"),
                    ("man jungfrau spring resort night smart", "Resort Spring Night", "Smart Casual", "Night/Indoor"),
                ],
            },
            "summer": {
                "morning":   [
                    ("man jungfrau summer hiking morning light jacket", "Summer Hiking Jacket", "Outerwear", "Hiking"),
                    ("man swiss alps summer morning casual light", "Summer Alpine Morning", "Casual", "Outdoor"),
                ],
                "afternoon": [
                    ("man swiss alps summer afternoon hiking casual", "Summer Alpine Afternoon", "Casual", "Hiking/Outdoor"),
                    ("man jungfrau summer casual afternoon mountain", "Mountain Summer Casual", "Casual", "Outdoor"),
                ],
                "evening":   [
                    ("man alpine summer evening casual mountain lodge", "Summer Alpine Evening", "Casual", "Evening Wear"),
                    ("man jungfrau summer lodge evening smart", "Summer Lodge Evening", "Smart Casual", "Evening Wear"),
                ],
                "night":     [
                    ("man alpine lodge summer night casual outfit", "Alpine Summer Night", "Casual", "Night/Indoor"),
                    ("man jungfrau summer resort night smart outfit", "Summer Resort Night", "Smart Casual", "Night/Indoor"),
                ],
            },
            "autumn": {
                "morning":   [
                    ("man jungfrau autumn jacket morning cool mountain", "Autumn Mountain Jacket", "Outerwear", "Outdoor"),
                    ("man swiss alps autumn hiking morning outfit", "Autumn Hiking Outfit", "Outdoor Wear", "Hiking"),
                ],
                "afternoon": [
                    ("man alps autumn afternoon hiking jacket waterproof", "Waterproof Autumn Jacket", "Outerwear", "Hiking"),
                    ("man jungfrau autumn casual afternoon mountain", "Autumn Mountain Casual", "Casual", "Outdoor"),
                ],
                "evening":   [
                    ("man alpine lodge autumn evening warm outfit", "Autumn Alpine Evening", "Casual", "Evening Wear"),
                    ("man swiss mountain autumn evening smart", "Autumn Mountain Evening", "Smart Casual", "Evening Wear"),
                ],
                "night":     [
                    ("man alpine lodge autumn night warm casual", "Autumn Lodge Night", "Casual", "Night/Indoor"),
                    ("man jungfrau autumn resort night smart", "Autumn Resort Night", "Smart Casual", "Night/Indoor"),
                ],
            },
        },
        "female": {
            "winter": {
                "morning":   [
                    ("woman ski jacket snow jungfrau winter morning", "Women Ski Jacket", "Outerwear", "Snow/Ski"),
                    ("woman heavy thermal outfit alps jungfrau morning", "Heavy Thermal Outfit", "Thermal Wear", "Snow/Ski"),
                ],
                "afternoon": [
                    ("woman ski suit snow alps jungfrau afternoon", "Women Ski Suit", "Snow Wear", "Snow/Ski"),
                    ("woman winter snow outfit mountain jungfrau afternoon", "Mountain Snow Outfit", "Snow Wear", "Outdoor"),
                ],
                "evening":   [
                    ("woman alpine lodge evening outfit warm jungfrau winter", "Alpine Lodge Evening", "Smart Casual", "Evening Wear"),
                    ("woman ski resort evening casual warm", "Ski Resort Evening", "Casual", "Evening Wear"),
                ],
                "night":     [
                    ("woman alpine resort night warm cozy outfit winter", "Alpine Resort Night", "Casual", "Night/Indoor"),
                    ("woman jungfrau resort night smart casual warm", "Resort Smart Night", "Smart Casual", "Night/Indoor"),
                ],
            },
            "spring": {
                "morning":   [
                    ("woman alpine spring jacket jungfrau morning cool", "Alpine Spring Jacket", "Outerwear", "Casual/Outdoor"),
                    ("woman hiking outfit swiss alps spring morning", "Alpine Hiking Outfit", "Outdoor Wear", "Hiking"),
                ],
                "afternoon": [
                    ("woman jungfrau spring hiking outfit afternoon", "Hiking Afternoon Outfit", "Outdoor Wear", "Hiking"),
                    ("woman swiss alps spring casual afternoon", "Alpine Spring Casual", "Casual", "Outdoor"),
                ],
                "evening":   [
                    ("woman swiss mountain spring evening casual warm", "Alpine Spring Evening", "Casual", "Evening Wear"),
                    ("woman jungfrau spring lodge evening outfit", "Lodge Spring Evening", "Smart Casual", "Evening Wear"),
                ],
                "night":     [
                    ("woman alpine lodge night spring casual warm", "Alpine Night Casual", "Casual", "Night/Indoor"),
                    ("woman jungfrau spring resort night smart", "Resort Spring Night", "Smart Casual", "Night/Indoor"),
                ],
            },
            "summer": {
                "morning":   [
                    ("woman jungfrau summer hiking morning jacket", "Summer Hiking Jacket", "Outerwear", "Hiking"),
                    ("woman swiss alps summer morning casual light", "Summer Alpine Morning", "Casual", "Outdoor"),
                ],
                "afternoon": [
                    ("woman swiss alps summer afternoon hiking casual", "Summer Alpine Afternoon", "Casual", "Hiking/Outdoor"),
                    ("woman jungfrau summer casual afternoon mountain", "Mountain Summer Casual", "Casual", "Outdoor"),
                ],
                "evening":   [
                    ("woman alpine summer evening casual mountain lodge", "Summer Alpine Evening", "Casual", "Evening Wear"),
                    ("woman jungfrau summer lodge evening smart", "Summer Lodge Evening", "Smart Casual", "Evening Wear"),
                ],
                "night":     [
                    ("woman alpine lodge summer night casual", "Alpine Summer Night", "Casual", "Night/Indoor"),
                    ("woman jungfrau summer resort night smart", "Summer Resort Night", "Smart Casual", "Night/Indoor"),
                ],
            },
            "autumn": {
                "morning":   [
                    ("woman jungfrau autumn jacket morning mountain", "Autumn Mountain Jacket", "Outerwear", "Outdoor"),
                    ("woman swiss alps autumn hiking morning outfit", "Autumn Hiking Outfit", "Outdoor Wear", "Hiking"),
                ],
                "afternoon": [
                    ("woman alps autumn afternoon hiking waterproof jacket", "Waterproof Autumn Jacket", "Outerwear", "Hiking"),
                    ("woman jungfrau autumn casual afternoon mountain", "Autumn Mountain Casual", "Casual", "Outdoor"),
                ],
                "evening":   [
                    ("woman alpine lodge autumn evening warm outfit", "Autumn Alpine Evening", "Casual", "Evening Wear"),
                    ("woman swiss mountain autumn evening smart casual", "Autumn Mountain Evening", "Smart Casual", "Evening Wear"),
                ],
                "night":     [
                    ("woman alpine lodge autumn night warm casual", "Autumn Lodge Night", "Casual", "Night/Indoor"),
                    ("woman jungfrau autumn resort night smart", "Autumn Resort Night", "Smart Casual", "Night/Indoor"),
                ],
            },
        },
    },

    # ==========================================================================
    # MIAMI
    # ==========================================================================
    "miami": {
        "male": {
            "winter": {
                "morning":   [
                    ("miami man winter morning casual light jacket", "Light Winter Jacket", "Outerwear", "Casual"),
                    ("miami beach man winter casual morning outfit", "Winter Morning Casual", "Casual", "Casual"),
                ],
                "afternoon": [
                    ("miami man casual afternoon winter light outfit", "Casual Winter Afternoon", "Casual", "Casual"),
                    ("miami beach man shorts casual afternoon winter", "Winter Beach Casual", "Casual", "Casual"),
                ],
                "evening":   [
                    ("miami man smart casual evening winter dinner", "Smart Winter Evening", "Smart Casual", "Evening Wear"),
                    ("miami beach man casual evening light jacket", "Casual Winter Evening", "Casual", "Evening Wear"),
                ],
                "night":     [
                    ("miami man night casual smart winter outfit", "Smart Winter Night", "Smart Casual", "Night Out"),
                    ("miami beach man casual night winter bar", "Casual Winter Night", "Casual", "Night Out"),
                ],
            },
            "spring": {
                "morning":   [
                    ("miami man spring morning casual light beach", "Spring Morning Casual", "Casual", "Casual"),
                    ("miami beach man shorts spring morning casual", "Spring Beach Morning", "Casual", "Casual/Beach"),
                ],
                "afternoon": [
                    ("miami man casual afternoon spring beach shorts", "Spring Beach Afternoon", "Casual", "Casual/Beach"),
                    ("miami beach man light outfit spring afternoon", "Light Spring Afternoon", "Casual", "Casual"),
                ],
                "evening":   [
                    ("miami man spring evening smart casual dinner", "Smart Spring Evening", "Smart Casual", "Evening Wear"),
                    ("miami beach man casual spring evening light", "Casual Spring Evening", "Casual", "Evening Wear"),
                ],
                "night":     [
                    ("miami man smart night spring outfit bar", "Smart Spring Night", "Smart Casual", "Night Out"),
                    ("miami beach man casual night spring", "Casual Spring Night", "Casual", "Night Out"),
                ],
            },
            "summer": {
                "morning":   [
                    ("miami man summer beach morning shorts casual", "Summer Beach Shorts", "Casual/Beach", "Casual"),
                    ("miami beach man summer morning swimwear casual", "Summer Morning Swimwear", "Swimwear", "Beach"),
                ],
                "afternoon": [
                    ("miami man summer afternoon beach shorts swimwear", "Beach Summer Afternoon", "Swimwear", "Beach"),
                    ("miami beach man summer casual afternoon light", "Light Summer Afternoon", "Casual", "Casual/Beach"),
                ],
                "evening":   [
                    ("miami man summer evening smart casual dinner", "Smart Summer Evening", "Smart Casual", "Evening Wear"),
                    ("miami beach man casual summer evening light", "Casual Summer Evening", "Casual", "Evening Wear"),
                ],
                "night":     [
                    ("miami man summer night smart casual bar", "Smart Summer Night", "Smart Casual", "Night Out"),
                    ("miami beach man casual summer night outfit", "Casual Summer Night", "Casual", "Night Out"),
                ],
            },
            "autumn": {
                "morning":   [
                    ("miami man autumn morning casual light jacket", "Autumn Morning Casual", "Casual", "Casual"),
                    ("miami beach man autumn morning casual outfit", "Autumn Beach Morning", "Casual", "Casual"),
                ],
                "afternoon": [
                    ("miami man casual afternoon autumn light outfit", "Casual Autumn Afternoon", "Casual", "Casual"),
                    ("miami beach man autumn afternoon casual", "Autumn Beach Afternoon", "Casual", "Casual"),
                ],
                "evening":   [
                    ("miami man autumn evening smart casual dinner", "Smart Autumn Evening", "Smart Casual", "Evening Wear"),
                    ("miami beach man autumn evening light jacket", "Casual Autumn Evening", "Casual", "Evening Wear"),
                ],
                "night":     [
                    ("miami man autumn night smart casual", "Smart Autumn Night", "Smart Casual", "Night Out"),
                    ("miami beach man casual autumn night bar", "Casual Autumn Night", "Casual", "Night Out"),
                ],
            },
        },
        "female": {
            "winter": {
                "morning":   [
                    ("miami woman winter morning casual light jacket", "Light Winter Jacket", "Outerwear", "Casual"),
                    ("miami beach woman winter casual morning dress", "Winter Morning Dress", "Dress", "Casual"),
                ],
                "afternoon": [
                    ("miami woman casual afternoon winter light dress", "Casual Winter Afternoon", "Dress", "Casual"),
                    ("miami beach woman winter afternoon casual fashion", "Winter Beach Fashion", "Casual", "Casual"),
                ],
                "evening":   [
                    ("miami woman smart casual evening winter dinner dress", "Smart Winter Evening Dress", "Dress", "Evening Wear"),
                    ("miami beach woman elegant evening winter", "Elegant Winter Evening", "Smart Casual", "Evening Wear"),
                ],
                "night":     [
                    ("miami woman night elegant winter dinner outfit", "Elegant Winter Night", "Formal", "Night Out"),
                    ("miami beach woman casual chic night winter", "Chic Winter Night", "Smart Casual", "Night Out"),
                ],
            },
            "spring": {
                "morning":   [
                    ("miami woman spring morning casual light dress beach", "Spring Morning Dress", "Dress", "Casual"),
                    ("miami beach woman spring morning casual outfit", "Spring Beach Morning", "Casual", "Casual/Beach"),
                ],
                "afternoon": [
                    ("miami woman spring afternoon beach dress casual", "Spring Beach Dress", "Dress", "Casual/Beach"),
                    ("miami beach woman light spring afternoon fashion", "Light Spring Afternoon", "Casual", "Casual"),
                ],
                "evening":   [
                    ("miami woman spring evening dress dinner", "Spring Evening Dress", "Dress", "Evening Wear"),
                    ("miami beach woman spring evening elegant outfit", "Elegant Spring Evening", "Smart Casual", "Evening Wear"),
                ],
                "night":     [
                    ("miami woman spring night elegant dress", "Elegant Spring Night", "Dress", "Night Out"),
                    ("miami beach woman chic spring night casual", "Chic Spring Night", "Smart Casual", "Night Out"),
                ],
            },
            "summer": {
                "morning":   [
                    ("miami woman summer beach morning swimwear casual", "Summer Beach Swimwear", "Swimwear", "Beach"),
                    ("miami beach woman summer morning sundress", "Summer Morning Sundress", "Dress", "Casual/Beach"),
                ],
                "afternoon": [
                    ("miami woman summer afternoon beach swimwear dress", "Summer Beach Afternoon", "Swimwear", "Beach"),
                    ("miami beach woman summer casual afternoon dress", "Casual Summer Afternoon", "Dress", "Casual"),
                ],
                "evening":   [
                    ("miami woman summer evening elegant dress dinner", "Elegant Summer Evening", "Dress", "Evening Wear"),
                    ("miami beach woman summer evening casual chic", "Chic Summer Evening", "Smart Casual", "Evening Wear"),
                ],
                "night":     [
                    ("miami woman summer night elegant dinner dress", "Elegant Summer Night", "Dress", "Night Out"),
                    ("miami beach woman casual chic summer night", "Chic Summer Night", "Smart Casual", "Night Out"),
                ],
            },
            "autumn": {
                "morning":   [
                    ("miami woman autumn morning casual light jacket", "Autumn Morning Jacket", "Outerwear", "Casual"),
                    ("miami beach woman autumn morning casual dress", "Autumn Beach Morning", "Dress", "Casual"),
                ],
                "afternoon": [
                    ("miami woman casual autumn afternoon light dress", "Casual Autumn Afternoon", "Dress", "Casual"),
                    ("miami beach woman autumn afternoon fashion", "Autumn Beach Fashion", "Casual", "Casual"),
                ],
                "evening":   [
                    ("miami woman autumn evening smart casual dinner", "Smart Autumn Evening", "Smart Casual", "Evening Wear"),
                    ("miami beach woman autumn evening elegant dress", "Elegant Autumn Evening", "Dress", "Evening Wear"),
                ],
                "night":     [
                    ("miami woman autumn night elegant dinner", "Elegant Autumn Night", "Formal", "Night Out"),
                    ("miami beach woman chic casual autumn night", "Chic Autumn Night", "Smart Casual", "Night Out"),
                ],
            },
        },
    },
}

# =============================================================================
# UNISEX QUERIES
# Organized by: location → season → time_of_day
# Search strategy: EXPLICIT "unisex" / "gender neutral" terms in every query
#
# Unisex scope per location:
#   Dubai    → unisex raincoats, windbreakers, gender neutral outerwear
#   Paris    → unisex scarves, gloves, raincoats, gender neutral winter accessories
#   Jungfrau → unisex ski jackets, snow gear, scarves, gloves, thermal accessories
#   Miami    → unisex beachwear, swimwear, gender neutral raincoats (hurricane season)
# =============================================================================
UNISEX_QUERIES = {

    # --------------------------------------------------------------------------
    # DUBAI — Unisex windbreakers, raincoats, gender neutral outerwear
    # --------------------------------------------------------------------------
    "dubai": {
        "mild": {
            "morning":   [
                ("unisex windbreaker jacket dubai mild morning gender neutral", "Unisex Windbreaker", "Outerwear", "Casual"),
                ("gender neutral raincoat dubai mild weather outerwear", "Gender Neutral Raincoat", "Outerwear", "Casual"),
                ("unisex light jacket outfit dubai morning mild season", "Unisex Light Jacket", "Outerwear", "Casual"),
            ],
            "afternoon": [
                ("unisex light outerwear dubai mild afternoon gender neutral", "Unisex Light Outerwear", "Outerwear", "Casual"),
                ("gender neutral windbreaker dubai mild afternoon fashion", "Gender Neutral Windbreaker", "Outerwear", "Casual"),
                ("unisex casual jacket dubai mild afternoon outfit", "Unisex Casual Jacket", "Outerwear", "Casual"),
            ],
            "evening":   [
                ("unisex evening jacket dubai mild gender neutral fashion", "Unisex Evening Jacket", "Outerwear", "Casual"),
                ("gender neutral outerwear dubai mild evening layer", "Gender Neutral Evening Layer", "Outerwear", "Casual"),
                ("unisex light wrap jacket dubai mild evening", "Unisex Evening Wrap", "Outerwear", "Casual"),
            ],
            "night":     [
                ("unisex night jacket dubai mild gender neutral", "Unisex Night Jacket", "Outerwear", "Casual"),
                ("gender neutral cool night layer dubai mild", "Gender Neutral Night Layer", "Outerwear", "Casual"),
                ("unisex windbreaker night outfit dubai mild", "Unisex Night Windbreaker", "Outerwear", "Casual"),
            ],
        },
        "warm": {
            "morning":   [
                ("unisex sun protection outfit dubai warm morning gender neutral", "Unisex Sun Protection Outfit", "Outerwear", "Casual"),
                ("gender neutral lightweight jacket dubai warm spring morning", "Gender Neutral Spring Jacket", "Outerwear", "Casual"),
                ("unisex outerwear dubai warm morning fashion", "Unisex Warm Morning Layer", "Outerwear", "Casual"),
            ],
            "afternoon": [
                ("unisex light jacket dubai warm afternoon gender neutral", "Unisex Afternoon Jacket", "Outerwear", "Casual"),
                ("gender neutral outerwear dubai warm afternoon", "Gender Neutral Warm Afternoon Layer", "Outerwear", "Casual"),
                ("unisex casual outfit dubai warm spring afternoon", "Unisex Warm Casual", "Outerwear", "Casual"),
            ],
            "evening":   [
                ("unisex evening jacket dubai warm gender neutral fashion", "Unisex Warm Evening Jacket", "Outerwear", "Casual"),
                ("gender neutral light layer dubai warm evening outfit", "Gender Neutral Warm Evening", "Outerwear", "Casual"),
                ("unisex outerwear dubai warm evening", "Unisex Warm Evening Layer", "Outerwear", "Casual"),
            ],
            "night":     [
                ("unisex night layer dubai warm gender neutral", "Unisex Warm Night Layer", "Outerwear", "Casual"),
                ("gender neutral night jacket dubai warm season", "Gender Neutral Warm Night Jacket", "Outerwear", "Casual"),
                ("unisex casual night outfit dubai warm", "Unisex Warm Night Outfit", "Outerwear", "Casual"),
            ],
        },
        "hot": {
            "morning":   [
                ("unisex sun hat cap dubai hot summer gender neutral", "Unisex Sun Hat", "Accessories", "Casual"),
                ("gender neutral sun scarf dubai hot morning", "Gender Neutral Sun Scarf", "Accessories", "Casual"),
                ("unisex summer accessories dubai hot morning outfit", "Unisex Summer Accessories", "Accessories", "Casual"),
            ],
            "afternoon": [
                ("unisex sun protection accessories dubai hot afternoon gender neutral", "Unisex Sun Protection", "Accessories", "Casual"),
                ("gender neutral summer hat sunglasses dubai hot", "Gender Neutral Summer Hat", "Accessories", "Casual"),
                ("unisex summer outfit dubai hot afternoon", "Unisex Hot Afternoon Outfit", "Accessories", "Casual"),
            ],
            "evening":   [
                ("unisex light scarf dubai summer hot evening gender neutral", "Unisex Summer Scarf", "Accessories", "Casual"),
                ("gender neutral accessories dubai hot summer evening", "Gender Neutral Summer Evening", "Accessories", "Casual"),
                ("unisex evening accessories dubai hot summer", "Unisex Hot Evening Accessories", "Accessories", "Casual"),
            ],
            "night":     [
                ("unisex light layer dubai hot summer night gender neutral", "Unisex Hot Night Layer", "Outerwear", "Casual"),
                ("gender neutral indoor jacket dubai summer night", "Gender Neutral Night Jacket", "Outerwear", "Casual"),
                ("unisex night outfit dubai hot summer", "Unisex Summer Night Outfit", "Outerwear", "Casual"),
            ],
        },
    },

    # --------------------------------------------------------------------------
    # PARIS — Unisex scarves, gloves, raincoats, gender neutral winter accessories
    # --------------------------------------------------------------------------
    "paris": {
        "winter": {
            "morning":   [
                ("unisex wool scarf gloves paris winter morning gender neutral", "Unisex Wool Scarf & Gloves", "Accessories", "Casual"),
                ("gender neutral raincoat waterproof paris winter morning", "Gender Neutral Winter Raincoat", "Outerwear", "Casual"),
                ("unisex winter jacket paris cold morning gender neutral fashion", "Unisex Winter Jacket", "Outerwear", "Casual"),
            ],
            "afternoon": [
                ("unisex scarf beret paris winter afternoon gender neutral", "Unisex Scarf & Beret", "Accessories", "Casual"),
                ("gender neutral raincoat paris winter afternoon", "Gender Neutral Afternoon Raincoat", "Outerwear", "Casual"),
                ("unisex winter accessories paris afternoon outfit", "Unisex Winter Accessories", "Accessories", "Casual"),
            ],
            "evening":   [
                ("unisex wool scarf gloves paris winter evening gender neutral", "Unisex Evening Scarf & Gloves", "Accessories", "Formal"),
                ("gender neutral raincoat paris winter evening outfit", "Gender Neutral Evening Raincoat", "Outerwear", "Formal"),
                ("unisex winter evening accessories paris fashion", "Unisex Winter Evening Accessories", "Accessories", "Formal"),
            ],
            "night":     [
                ("unisex winter night accessories paris scarf gloves gender neutral", "Unisex Night Winter Accessories", "Accessories", "Casual"),
                ("gender neutral waterproof jacket paris winter night", "Gender Neutral Night Jacket", "Outerwear", "Casual"),
                ("unisex winter night outfit paris gender neutral", "Unisex Paris Winter Night", "Outerwear", "Casual"),
            ],
        },
        "spring": {
            "morning":   [
                ("unisex rain jacket paris spring morning gender neutral", "Unisex Spring Rain Jacket", "Outerwear", "Casual"),
                ("gender neutral light scarf paris spring morning", "Gender Neutral Spring Scarf", "Accessories", "Casual"),
                ("unisex spring accessories paris morning outfit gender neutral", "Unisex Spring Accessories", "Accessories", "Casual"),
            ],
            "afternoon": [
                ("unisex raincoat paris spring afternoon gender neutral", "Unisex Spring Raincoat", "Outerwear", "Casual"),
                ("gender neutral spring accessories paris afternoon", "Gender Neutral Spring Accessories", "Accessories", "Casual"),
                ("unisex light jacket paris spring afternoon fashion", "Unisex Spring Light Jacket", "Outerwear", "Casual"),
            ],
            "evening":   [
                ("unisex light jacket scarf paris spring evening gender neutral", "Unisex Spring Evening Scarf", "Accessories", "Casual"),
                ("gender neutral spring rain jacket paris evening", "Gender Neutral Spring Evening Jacket", "Outerwear", "Casual"),
                ("unisex evening accessories paris spring fashion", "Unisex Spring Evening Accessories", "Accessories", "Casual"),
            ],
            "night":     [
                ("unisex spring night jacket paris gender neutral fashion", "Unisex Spring Night Jacket", "Outerwear", "Casual"),
                ("gender neutral night accessories paris spring", "Gender Neutral Spring Night Accessories", "Accessories", "Casual"),
                ("unisex paris spring night outfit gender neutral", "Unisex Spring Night Outfit", "Outerwear", "Casual"),
            ],
        },
        "summer": {
            "morning":   [
                ("unisex summer scarf accessories paris morning gender neutral", "Unisex Summer Scarf", "Accessories", "Casual"),
                ("gender neutral summer hat sunglasses paris morning", "Gender Neutral Summer Hat", "Accessories", "Casual"),
                ("unisex paris summer morning accessories fashion", "Unisex Paris Summer Accessories", "Accessories", "Casual"),
            ],
            "afternoon": [
                ("unisex summer accessories paris afternoon gender neutral", "Unisex Summer Afternoon Accessories", "Accessories", "Casual"),
                ("gender neutral light scarf paris summer afternoon", "Gender Neutral Summer Scarf", "Accessories", "Casual"),
                ("unisex sunglasses hat paris summer outfit", "Unisex Summer Hat & Sunglasses", "Accessories", "Casual"),
            ],
            "evening":   [
                ("unisex summer evening light layer paris gender neutral", "Unisex Summer Evening Layer", "Outerwear", "Casual"),
                ("gender neutral light jacket paris summer evening", "Gender Neutral Summer Evening Jacket", "Outerwear", "Casual"),
                ("unisex paris summer evening accessories scarf", "Unisex Summer Evening Scarf", "Accessories", "Casual"),
            ],
            "night":     [
                ("unisex summer night jacket layer paris gender neutral", "Unisex Summer Night Layer", "Outerwear", "Casual"),
                ("gender neutral paris summer night accessories", "Gender Neutral Summer Night Accessories", "Accessories", "Casual"),
                ("unisex paris summer night outfit fashion", "Unisex Paris Summer Night", "Outerwear", "Casual"),
            ],
        },
        "autumn": {
            "morning":   [
                ("unisex autumn scarf raincoat paris morning gender neutral", "Unisex Autumn Scarf & Raincoat", "Outerwear", "Casual"),
                ("gender neutral gloves scarf paris autumn morning", "Gender Neutral Autumn Gloves", "Accessories", "Casual"),
                ("unisex paris autumn morning accessories outfit", "Unisex Autumn Morning Accessories", "Accessories", "Casual"),
            ],
            "afternoon": [
                ("unisex autumn waterproof raincoat paris afternoon gender neutral", "Unisex Autumn Waterproof Coat", "Outerwear", "Casual"),
                ("gender neutral autumn scarf accessories paris afternoon", "Gender Neutral Autumn Scarf", "Accessories", "Casual"),
                ("unisex paris autumn afternoon jacket fashion", "Unisex Autumn Afternoon Jacket", "Outerwear", "Casual"),
            ],
            "evening":   [
                ("unisex autumn evening raincoat scarf paris gender neutral", "Unisex Autumn Evening Raincoat", "Outerwear", "Casual"),
                ("gender neutral paris autumn evening accessories gloves", "Gender Neutral Autumn Evening Accessories", "Accessories", "Formal"),
                ("unisex autumn evening jacket paris fashion", "Unisex Autumn Evening Jacket", "Outerwear", "Formal"),
            ],
            "night":     [
                ("unisex autumn night jacket scarf paris gender neutral", "Unisex Autumn Night Jacket", "Outerwear", "Casual"),
                ("gender neutral paris autumn night accessories gloves scarf", "Gender Neutral Autumn Night Accessories", "Accessories", "Casual"),
                ("unisex paris autumn night outfit fashion", "Unisex Autumn Night Outfit", "Outerwear", "Casual"),
            ],
        },
    },

    # --------------------------------------------------------------------------
    # JUNGFRAU — Unisex ski jackets, snow gear, gloves, scarves, thermal accessories
    # --------------------------------------------------------------------------
    "jungfrau": {
        "winter": {
            "morning":   [
                ("unisex ski jacket snow gear jungfrau winter morning gender neutral", "Unisex Ski Jacket", "Snow Wear", "Snow/Ski"),
                ("gender neutral thermal gloves ski goggles jungfrau winter alps", "Gender Neutral Ski Accessories", "Accessories", "Snow/Ski"),
                ("unisex snow outfit jungfrau winter morning alps gender neutral", "Unisex Snow Outfit", "Snow Wear", "Snow/Ski"),
            ],
            "afternoon": [
                ("unisex ski suit snow gear alps jungfrau afternoon gender neutral", "Unisex Ski Suit", "Snow Wear", "Snow/Ski"),
                ("gender neutral snow boots waterproof jungfrau winter afternoon", "Gender Neutral Snow Boots", "Footwear", "Snow/Ski"),
                ("unisex ski outfit jungfrau winter afternoon fashion", "Unisex Ski Outfit", "Snow Wear", "Snow/Ski"),
            ],
            "evening":   [
                ("unisex warm scarf gloves alpine evening jungfrau winter gender neutral", "Unisex Alpine Scarf & Gloves", "Accessories", "Casual"),
                ("gender neutral thermal jacket alpine lodge jungfrau evening", "Gender Neutral Thermal Jacket", "Outerwear", "Casual"),
                ("unisex alpine lodge evening outfit jungfrau winter", "Unisex Alpine Evening Outfit", "Outerwear", "Casual"),
            ],
            "night":     [
                ("unisex thermal accessories night alpine jungfrau winter gender neutral", "Unisex Thermal Night Accessories", "Accessories", "Casual"),
                ("gender neutral warm jacket alpine jungfrau night winter", "Gender Neutral Alpine Night Jacket", "Outerwear", "Casual"),
                ("unisex alpine indoor night outfit jungfrau winter", "Unisex Alpine Night Outfit", "Outerwear", "Casual"),
            ],
        },
        "spring": {
            "morning":   [
                ("unisex waterproof hiking jacket jungfrau spring morning gender neutral", "Unisex Waterproof Hiking Jacket", "Outerwear", "Hiking"),
                ("gender neutral hiking gloves jungfrau spring alps morning", "Gender Neutral Hiking Gloves", "Accessories", "Hiking"),
                ("unisex spring hiking outfit jungfrau gender neutral", "Unisex Spring Hiking Outfit", "Outerwear", "Hiking"),
            ],
            "afternoon": [
                ("unisex waterproof jacket alps jungfrau spring hiking afternoon gender neutral", "Unisex Spring Hiking Jacket", "Outerwear", "Hiking"),
                ("gender neutral hiking accessories jungfrau spring afternoon", "Gender Neutral Hiking Accessories", "Accessories", "Hiking"),
                ("unisex jungfrau spring afternoon outdoor outfit", "Unisex Spring Outdoor Outfit", "Outerwear", "Hiking"),
            ],
            "evening":   [
                ("unisex fleece jacket jungfrau spring evening alpine gender neutral", "Unisex Spring Fleece Jacket", "Outerwear", "Casual"),
                ("gender neutral alpine scarf jungfrau spring evening", "Gender Neutral Spring Alpine Scarf", "Accessories", "Casual"),
                ("unisex alpine spring evening outfit jungfrau", "Unisex Spring Alpine Evening", "Outerwear", "Casual"),
            ],
            "night":     [
                ("unisex warm layer jungfrau spring night alpine lodge gender neutral", "Unisex Spring Night Layer", "Outerwear", "Casual"),
                ("gender neutral alpine accessories jungfrau spring night", "Gender Neutral Spring Night Accessories", "Accessories", "Casual"),
                ("unisex jungfrau spring lodge night outfit", "Unisex Spring Lodge Night", "Outerwear", "Casual"),
            ],
        },
        "summer": {
            "morning":   [
                ("unisex light hiking jacket jungfrau summer morning alps gender neutral", "Unisex Summer Hiking Jacket", "Outerwear", "Hiking"),
                ("gender neutral sun hat sunglasses alpine jungfrau summer morning", "Gender Neutral Alpine Sun Hat", "Accessories", "Hiking"),
                ("unisex jungfrau summer morning hiking outfit gender neutral", "Unisex Summer Hiking Outfit", "Outerwear", "Hiking"),
            ],
            "afternoon": [
                ("unisex waterproof light jacket alps jungfrau summer afternoon gender neutral", "Unisex Light Waterproof Jacket", "Outerwear", "Hiking"),
                ("gender neutral hiking accessories sunglasses jungfrau summer", "Gender Neutral Summer Hiking Accessories", "Accessories", "Hiking"),
                ("unisex jungfrau summer afternoon outdoor outfit", "Unisex Summer Outdoor Outfit", "Outerwear", "Hiking"),
            ],
            "evening":   [
                ("unisex fleece jacket jungfrau summer evening alpine gender neutral", "Unisex Summer Fleece Jacket", "Outerwear", "Casual"),
                ("gender neutral alpine accessories jungfrau summer evening", "Gender Neutral Summer Alpine Accessories", "Accessories", "Casual"),
                ("unisex jungfrau summer alpine evening outfit", "Unisex Summer Alpine Evening", "Outerwear", "Casual"),
            ],
            "night":     [
                ("unisex warm jacket jungfrau summer night lodge gender neutral", "Unisex Summer Lodge Jacket", "Outerwear", "Casual"),
                ("gender neutral alpine jungfrau summer night accessories", "Gender Neutral Summer Night Accessories", "Accessories", "Casual"),
                ("unisex jungfrau summer lodge night outfit", "Unisex Summer Lodge Night", "Outerwear", "Casual"),
            ],
        },
        "autumn": {
            "morning":   [
                ("unisex waterproof jacket jungfrau autumn morning hiking gender neutral", "Unisex Autumn Waterproof Jacket", "Outerwear", "Hiking"),
                ("gender neutral gloves scarf alps jungfrau autumn morning", "Gender Neutral Autumn Gloves & Scarf", "Accessories", "Hiking"),
                ("unisex jungfrau autumn morning hiking outfit gender neutral", "Unisex Autumn Hiking Outfit", "Outerwear", "Hiking"),
            ],
            "afternoon": [
                ("unisex waterproof hiking jacket alps jungfrau autumn afternoon gender neutral", "Unisex Autumn Hiking Jacket", "Outerwear", "Hiking"),
                ("gender neutral hiking accessories jungfrau autumn afternoon", "Gender Neutral Autumn Hiking Accessories", "Accessories", "Hiking"),
                ("unisex jungfrau autumn afternoon outdoor fashion", "Unisex Autumn Outdoor Fashion", "Outerwear", "Hiking"),
            ],
            "evening":   [
                ("unisex warm fleece jacket jungfrau autumn evening gender neutral", "Unisex Autumn Fleece Jacket", "Outerwear", "Casual"),
                ("gender neutral scarf gloves alpine jungfrau autumn evening", "Gender Neutral Autumn Alpine Accessories", "Accessories", "Casual"),
                ("unisex jungfrau autumn alpine evening outfit", "Unisex Autumn Alpine Evening", "Outerwear", "Casual"),
            ],
            "night":     [
                ("unisex warm jacket alpine jungfrau autumn lodge night gender neutral", "Unisex Autumn Lodge Jacket", "Outerwear", "Casual"),
                ("gender neutral scarf gloves jungfrau autumn night alpine", "Gender Neutral Autumn Night Accessories", "Accessories", "Casual"),
                ("unisex jungfrau autumn night lodge outfit", "Unisex Autumn Night Lodge Outfit", "Outerwear", "Casual"),
            ],
        },
    },

    # --------------------------------------------------------------------------
    # MIAMI — Unisex beachwear, swimwear, gender neutral raincoats (hurricane season)
    # --------------------------------------------------------------------------
    "miami": {
        "winter": {
            "morning":   [
                ("unisex light raincoat miami winter morning gender neutral beach", "Unisex Light Raincoat", "Outerwear", "Casual"),
                ("gender neutral winter accessories miami morning light scarf", "Gender Neutral Winter Scarf", "Accessories", "Casual"),
                ("unisex miami winter morning outfit gender neutral fashion", "Unisex Miami Winter Morning", "Outerwear", "Casual"),
            ],
            "afternoon": [
                ("unisex light jacket miami beach winter afternoon gender neutral", "Unisex Beach Light Jacket", "Outerwear", "Casual"),
                ("gender neutral winter accessories miami afternoon sunglasses", "Gender Neutral Winter Sunglasses", "Accessories", "Casual"),
                ("unisex miami winter afternoon outfit gender neutral", "Unisex Miami Winter Afternoon", "Outerwear", "Casual"),
            ],
            "evening":   [
                ("unisex light jacket miami winter evening gender neutral beach", "Unisex Miami Winter Evening Jacket", "Outerwear", "Casual"),
                ("gender neutral evening accessories miami winter scarf", "Gender Neutral Miami Evening Scarf", "Accessories", "Casual"),
                ("unisex miami winter evening outfit gender neutral fashion", "Unisex Miami Winter Evening", "Outerwear", "Casual"),
            ],
            "night":     [
                ("unisex night layer miami winter gender neutral fashion", "Unisex Miami Night Layer", "Outerwear", "Casual"),
                ("gender neutral night accessories miami winter", "Gender Neutral Miami Night Accessories", "Accessories", "Casual"),
                ("unisex miami winter night outfit gender neutral", "Unisex Miami Winter Night", "Outerwear", "Casual"),
            ],
        },
        "spring": {
            "morning":   [
                ("unisex beach hat accessories miami spring morning gender neutral", "Unisex Beach Hat", "Accessories", "Beach"),
                ("gender neutral light raincoat miami spring morning", "Gender Neutral Spring Raincoat", "Outerwear", "Casual"),
                ("unisex miami spring morning beach outfit gender neutral", "Unisex Miami Spring Morning", "Accessories", "Beach"),
            ],
            "afternoon": [
                ("unisex beach accessories sunglasses hat miami spring afternoon gender neutral", "Unisex Beach Accessories", "Accessories", "Beach"),
                ("gender neutral beach towel cover up miami spring afternoon", "Gender Neutral Beach Accessories", "Accessories", "Beach"),
                ("unisex miami spring afternoon beach outfit gender neutral", "Unisex Spring Beach Afternoon", "Accessories", "Beach"),
            ],
            "evening":   [
                ("unisex light jacket evening miami spring gender neutral beach", "Unisex Spring Evening Jacket", "Outerwear", "Casual"),
                ("gender neutral spring evening accessories miami light", "Gender Neutral Spring Evening Accessories", "Accessories", "Casual"),
                ("unisex miami spring evening outfit gender neutral fashion", "Unisex Miami Spring Evening", "Outerwear", "Casual"),
            ],
            "night":     [
                ("unisex miami spring night outfit gender neutral light jacket", "Unisex Miami Spring Night", "Outerwear", "Casual"),
                ("gender neutral night accessories miami spring", "Gender Neutral Miami Spring Night", "Accessories", "Casual"),
                ("unisex spring night fashion miami gender neutral", "Unisex Spring Night Fashion", "Outerwear", "Casual"),
            ],
        },
        "summer": {
            "morning":   [
                ("unisex beach swimwear miami summer morning gender neutral", "Unisex Beach Swimwear", "Swimwear", "Beach"),
                ("gender neutral summer beach hat sunscreen miami morning", "Gender Neutral Beach Hat", "Accessories", "Beach"),
                ("unisex miami summer morning beach outfit gender neutral", "Unisex Miami Summer Morning", "Swimwear", "Beach"),
            ],
            "afternoon": [
                ("unisex beach swimwear accessories miami summer afternoon gender neutral", "Unisex Summer Swimwear", "Swimwear", "Beach"),
                ("gender neutral beach towel accessories miami summer afternoon", "Gender Neutral Beach Set", "Accessories", "Beach"),
                ("unisex miami summer beach afternoon outfit gender neutral", "Unisex Miami Summer Beach", "Swimwear", "Beach"),
            ],
            "evening":   [
                ("unisex beach cover up miami summer evening gender neutral", "Unisex Beach Cover-Up", "Swimwear", "Beach"),
                ("gender neutral summer evening accessories miami beach", "Gender Neutral Miami Summer Evening", "Accessories", "Casual"),
                ("unisex miami summer evening beach outfit gender neutral", "Unisex Miami Summer Evening", "Outerwear", "Casual"),
            ],
            "night":     [
                ("unisex summer night layer miami gender neutral beach", "Unisex Miami Summer Night Layer", "Outerwear", "Casual"),
                ("gender neutral miami summer night accessories beach", "Gender Neutral Miami Summer Night", "Accessories", "Casual"),
                ("unisex miami summer night outfit gender neutral fashion", "Unisex Miami Summer Night", "Outerwear", "Casual"),
            ],
        },
        "autumn": {
            "morning":   [
                ("unisex waterproof raincoat miami autumn morning gender neutral hurricane", "Unisex Waterproof Raincoat", "Outerwear", "Casual"),
                ("gender neutral light layer miami autumn morning beach", "Gender Neutral Autumn Light Layer", "Outerwear", "Casual"),
                ("unisex miami autumn morning outfit gender neutral fashion", "Unisex Miami Autumn Morning", "Outerwear", "Casual"),
            ],
            "afternoon": [
                ("unisex waterproof jacket miami autumn afternoon rain gender neutral", "Unisex Autumn Rain Jacket", "Outerwear", "Casual"),
                ("gender neutral autumn beach accessories miami afternoon", "Gender Neutral Autumn Beach Accessories", "Accessories", "Casual"),
                ("unisex miami autumn afternoon outfit gender neutral", "Unisex Miami Autumn Afternoon", "Outerwear", "Casual"),
            ],
            "evening":   [
                ("unisex autumn evening jacket miami rain gender neutral", "Unisex Autumn Evening Jacket", "Outerwear", "Casual"),
                ("gender neutral evening accessories miami autumn scarf", "Gender Neutral Autumn Evening Accessories", "Accessories", "Casual"),
                ("unisex miami autumn evening outfit gender neutral fashion", "Unisex Miami Autumn Evening", "Outerwear", "Casual"),
            ],
            "night":     [
                ("unisex autumn night jacket miami gender neutral layer", "Unisex Autumn Night Jacket", "Outerwear", "Casual"),
                ("gender neutral miami autumn night accessories scarf", "Gender Neutral Autumn Night Accessories", "Accessories", "Casual"),
                ("unisex miami autumn night outfit gender neutral", "Unisex Miami Autumn Night", "Outerwear", "Casual"),
            ],
        },
    },
}

# ----------------------------------------------------------------------------
# FOOD QUERIES
# Organized by: location → meal_preference → season → time_of_day
# Each entry: (search_query, dish_name, category)
# ----------------------------------------------------------------------------
FOOD_QUERIES = {
    "dubai": {
        "veg": {
            "mild":  {"breakfast": [("dubai vegetarian breakfast foul medames", "Foul Medames", "Breakfast")],
                      "lunch":     [("dubai vegetarian hummus falafel lunch", "Hummus & Falafel", "Main Course")],
                      "dinner":    [("dubai vegetarian mezze platter dinner", "Mezze Platter", "Main Course")],
                      "snack":     [("dubai vegetarian snack samosa", "Vegetarian Samosa", "Snack")]},
            "warm":  {"breakfast": [("dubai vegetarian breakfast warm spring", "Veg Breakfast Platter", "Breakfast")],
                      "lunch":     [("dubai vegetable biryani lunch warm", "Vegetable Biryani", "Main Course")],
                      "dinner":    [("dubai vegetarian dinner warm mezze", "Warm Mezze Dinner", "Main Course")],
                      "snack":     [("dubai veg snack warm season", "Veg Snack Platter", "Snack")]},
            "hot":   {"breakfast": [("dubai vegetarian light breakfast summer heat", "Light Veg Breakfast", "Breakfast")],
                      "lunch":     [("dubai vegetarian summer lunch light salad", "Summer Veg Salad", "Main Course")],
                      "dinner":    [("dubai vegetarian summer dinner cool dish", "Summer Veg Dinner", "Main Course")],
                      "snack":     [("dubai veg summer snack fruit", "Summer Fruit Snack", "Snack")]},
        },
        "vegan": {
            "mild":  {"breakfast": [("dubai vegan breakfast mild winter", "Vegan Breakfast Bowl", "Breakfast")],
                      "lunch":     [("dubai vegan lunch plant based mild", "Vegan Plant Bowl", "Main Course")],
                      "dinner":    [("dubai vegan dinner arabic mild", "Vegan Arabic Dinner", "Main Course")],
                      "snack":     [("dubai vegan snack mild", "Vegan Snack", "Snack")]},
            "warm":  {"breakfast": [("dubai vegan breakfast warm spring", "Vegan Spring Breakfast", "Breakfast")],
                      "lunch":     [("dubai vegan lunch warm plant based", "Warm Vegan Lunch", "Main Course")],
                      "dinner":    [("dubai vegan dinner warm", "Warm Vegan Dinner", "Main Course")],
                      "snack":     [("dubai vegan snack warm", "Vegan Warm Snack", "Snack")]},
            "hot":   {"breakfast": [("dubai vegan light breakfast summer", "Light Vegan Breakfast", "Breakfast")],
                      "lunch":     [("dubai vegan summer lunch cool", "Cool Vegan Summer Lunch", "Main Course")],
                      "dinner":    [("dubai vegan summer dinner", "Summer Vegan Dinner", "Main Course")],
                      "snack":     [("dubai vegan summer snack", "Summer Vegan Snack", "Snack")]},
        },
        "egg": {
            "mild":  {"breakfast": [("dubai egg breakfast shakshuka mild", "Shakshuka", "Breakfast")],
                      "lunch":     [("dubai egg lunch omelette mild", "Egg Omelette Lunch", "Main Course")],
                      "dinner":    [("dubai egg dinner mild", "Egg Dinner Dish", "Main Course")],
                      "snack":     [("dubai egg snack mild boiled", "Boiled Egg Snack", "Snack")]},
            "warm":  {"breakfast": [("dubai egg breakfast warm spring", "Spring Egg Breakfast", "Breakfast")],
                      "lunch":     [("dubai egg lunch warm", "Warm Egg Lunch", "Main Course")],
                      "dinner":    [("dubai egg dinner warm", "Warm Egg Dinner", "Main Course")],
                      "snack":     [("dubai egg snack warm", "Egg Warm Snack", "Snack")]},
            "hot":   {"breakfast": [("dubai egg light breakfast summer heat", "Light Summer Egg Breakfast", "Breakfast")],
                      "lunch":     [("dubai egg summer lunch", "Summer Egg Lunch", "Main Course")],
                      "dinner":    [("dubai egg summer dinner", "Summer Egg Dinner", "Main Course")],
                      "snack":     [("dubai egg summer snack", "Summer Egg Snack", "Snack")]},
        },
        "non_veg": {
            "mild":  {"breakfast": [("dubai non veg breakfast mild eggs meat", "Meat Breakfast Platter", "Breakfast")],
                      "lunch":     [("dubai shawarma chicken lunch mild", "Chicken Shawarma", "Main Course")],
                      "dinner":    [("dubai grilled lamb machboos dinner mild", "Machboos Lamb", "Main Course")],
                      "snack":     [("dubai meat snack mild kebab", "Mini Kebab Snack", "Snack")]},
            "warm":  {"breakfast": [("dubai non veg breakfast warm", "Warm Meat Breakfast", "Breakfast")],
                      "lunch":     [("dubai grilled chicken lunch warm spring", "Grilled Chicken Lunch", "Main Course")],
                      "dinner":    [("dubai non veg dinner warm seafood", "Warm Seafood Dinner", "Main Course")],
                      "snack":     [("dubai meat snack warm", "Warm Meat Snack", "Snack")]},
            "hot":   {"breakfast": [("dubai light non veg breakfast summer", "Light Summer Meat Breakfast", "Breakfast")],
                      "lunch":     [("dubai grilled fish lunch summer heat", "Grilled Fish Lunch", "Main Course")],
                      "dinner":    [("dubai seafood grilled dinner summer", "Summer Grilled Seafood", "Main Course")],
                      "snack":     [("dubai meat summer snack", "Summer Meat Snack", "Snack")]},
        },
    },
    # Paris, Jungfrau, Miami food queries follow same pattern
    # (abbreviated here for readability — full queries in food_config_extended.py)
    "paris": {
        "veg": {
            "winter":  {"breakfast": [("paris vegetarian breakfast croissant winter", "Vegetarian Croissant", "Breakfast")],
                        "lunch":     [("paris french onion soup vegetarian winter", "French Onion Soup", "Main Course")],
                        "dinner":    [("paris vegetarian ratatouille dinner winter", "Ratatouille", "Main Course")],
                        "snack":     [("paris vegetarian snack crepe winter", "Veggie Crepe", "Snack")]},
            "spring":  {"breakfast": [("paris vegetarian spring breakfast", "Spring Veg Breakfast", "Breakfast")],
                        "lunch":     [("paris vegetarian spring salad lunch", "Spring Salad", "Main Course")],
                        "dinner":    [("paris vegetarian spring dinner", "Spring Veg Dinner", "Main Course")],
                        "snack":     [("paris vegetarian spring snack", "Spring Veg Snack", "Snack")]},
            "summer":  {"breakfast": [("paris vegetarian summer breakfast light", "Light Summer Breakfast", "Breakfast")],
                        "lunch":     [("paris vegetarian summer salad lunch", "Summer Salad", "Main Course")],
                        "dinner":    [("paris vegetarian summer dinner", "Summer Veg Dinner", "Main Course")],
                        "snack":     [("paris vegetarian summer snack", "Summer Veg Snack", "Snack")]},
            "autumn":  {"breakfast": [("paris vegetarian autumn breakfast", "Autumn Veg Breakfast", "Breakfast")],
                        "lunch":     [("paris vegetarian autumn soup lunch", "Autumn Vegetable Soup", "Main Course")],
                        "dinner":    [("paris vegetarian autumn dinner", "Autumn Veg Dinner", "Main Course")],
                        "snack":     [("paris vegetarian autumn snack", "Autumn Veg Snack", "Snack")]},
        },
        "non_veg": {
            "winter":  {"breakfast": [("paris non veg breakfast winter eggs meat", "Meat & Eggs Breakfast", "Breakfast")],
                        "lunch":     [("paris croque monsieur lunch winter", "Croque Monsieur", "Main Course")],
                        "dinner":    [("paris duck confit dinner winter", "Duck Confit", "Main Course")],
                        "snack":     [("paris meat snack winter", "Winter Meat Snack", "Snack")]},
            "spring":  {"breakfast": [("paris non veg spring breakfast", "Spring Meat Breakfast", "Breakfast")],
                        "lunch":     [("paris steak frites spring lunch", "Steak Frites", "Main Course")],
                        "dinner":    [("paris non veg spring dinner", "Spring Meat Dinner", "Main Course")],
                        "snack":     [("paris meat spring snack", "Spring Meat Snack", "Snack")]},
            "summer":  {"breakfast": [("paris non veg summer breakfast", "Summer Meat Breakfast", "Breakfast")],
                        "lunch":     [("paris grilled chicken summer lunch", "Grilled Chicken Lunch", "Main Course")],
                        "dinner":    [("paris seafood summer dinner", "Summer Seafood Dinner", "Main Course")],
                        "snack":     [("paris meat summer snack", "Summer Meat Snack", "Snack")]},
            "autumn":  {"breakfast": [("paris non veg autumn breakfast", "Autumn Meat Breakfast", "Breakfast")],
                        "lunch":     [("paris non veg autumn lunch bistro", "Autumn Bistro Lunch", "Main Course")],
                        "dinner":    [("paris non veg autumn dinner", "Autumn Meat Dinner", "Main Course")],
                        "snack":     [("paris meat autumn snack", "Autumn Meat Snack", "Snack")]},
        },
        "veg":    {},  # defined above
        "vegan":  {
            "winter":  {"breakfast": [("paris vegan winter breakfast", "Vegan Winter Breakfast", "Breakfast")],
                        "lunch":     [("paris vegan winter lunch galette", "Vegan Galette", "Main Course")],
                        "dinner":    [("paris vegan winter dinner", "Vegan Winter Dinner", "Main Course")],
                        "snack":     [("paris vegan winter snack", "Vegan Winter Snack", "Snack")]},
            "spring":  {"breakfast": [("paris vegan spring breakfast", "Vegan Spring Breakfast", "Breakfast")],
                        "lunch":     [("paris vegan spring lunch", "Vegan Spring Lunch", "Main Course")],
                        "dinner":    [("paris vegan spring dinner", "Vegan Spring Dinner", "Main Course")],
                        "snack":     [("paris vegan spring snack", "Vegan Spring Snack", "Snack")]},
            "summer":  {"breakfast": [("paris vegan summer breakfast", "Vegan Summer Breakfast", "Breakfast")],
                        "lunch":     [("paris vegan summer lunch", "Vegan Summer Lunch", "Main Course")],
                        "dinner":    [("paris vegan summer dinner", "Vegan Summer Dinner", "Main Course")],
                        "snack":     [("paris vegan summer snack", "Vegan Summer Snack", "Snack")]},
            "autumn":  {"breakfast": [("paris vegan autumn breakfast", "Vegan Autumn Breakfast", "Breakfast")],
                        "lunch":     [("paris vegan autumn lunch", "Vegan Autumn Lunch", "Main Course")],
                        "dinner":    [("paris vegan autumn dinner", "Vegan Autumn Dinner", "Main Course")],
                        "snack":     [("paris vegan autumn snack", "Vegan Autumn Snack", "Snack")]},
        },
        "egg": {
            "winter":  {"breakfast": [("paris french omelette breakfast winter", "French Omelette", "Breakfast")],
                        "lunch":     [("paris egg lunch quiche winter", "Quiche Lorraine", "Main Course")],
                        "dinner":    [("paris egg dinner winter", "Egg Winter Dinner", "Main Course")],
                        "snack":     [("paris egg snack winter", "Egg Winter Snack", "Snack")]},
            "spring":  {"breakfast": [("paris egg spring breakfast", "Spring Egg Breakfast", "Breakfast")],
                        "lunch":     [("paris egg spring lunch", "Spring Egg Lunch", "Main Course")],
                        "dinner":    [("paris egg spring dinner", "Spring Egg Dinner", "Main Course")],
                        "snack":     [("paris egg spring snack", "Spring Egg Snack", "Snack")]},
            "summer":  {"breakfast": [("paris egg summer breakfast", "Summer Egg Breakfast", "Breakfast")],
                        "lunch":     [("paris egg summer lunch", "Summer Egg Lunch", "Main Course")],
                        "dinner":    [("paris egg summer dinner", "Summer Egg Dinner", "Main Course")],
                        "snack":     [("paris egg summer snack", "Summer Egg Snack", "Snack")]},
            "autumn":  {"breakfast": [("paris egg autumn breakfast", "Autumn Egg Breakfast", "Breakfast")],
                        "lunch":     [("paris egg autumn lunch", "Autumn Egg Lunch", "Main Course")],
                        "dinner":    [("paris egg autumn dinner", "Autumn Egg Dinner", "Main Course")],
                        "snack":     [("paris egg autumn snack", "Autumn Egg Snack", "Snack")]},
        },
    },
    "jungfrau": {
        "veg":     {"winter": {"breakfast": [("swiss vegetarian breakfast winter fondue", "Swiss Veg Breakfast", "Breakfast")],
                               "lunch":     [("swiss vegetarian rösti lunch winter", "Rösti", "Main Course")],
                               "dinner":    [("swiss cheese fondue vegetarian dinner", "Cheese Fondue", "Main Course")],
                               "snack":     [("swiss vegetarian snack winter", "Swiss Veg Snack", "Snack")]},
                    "spring": {"breakfast": [("swiss veg spring breakfast", "Swiss Spring Veg Breakfast", "Breakfast")],
                               "lunch":     [("swiss veg spring lunch", "Spring Veg Lunch", "Main Course")],
                               "dinner":    [("swiss veg spring dinner", "Spring Veg Dinner", "Main Course")],
                               "snack":     [("swiss veg spring snack", "Spring Veg Snack", "Snack")]},
                    "summer": {"breakfast": [("swiss veg summer breakfast", "Summer Veg Breakfast", "Breakfast")],
                               "lunch":     [("swiss veg summer lunch alpine", "Alpine Summer Lunch", "Main Course")],
                               "dinner":    [("swiss veg summer dinner", "Summer Veg Dinner", "Main Course")],
                               "snack":     [("swiss veg summer snack", "Summer Veg Snack", "Snack")]},
                    "autumn": {"breakfast": [("swiss veg autumn breakfast", "Autumn Veg Breakfast", "Breakfast")],
                               "lunch":     [("swiss veg autumn lunch", "Autumn Veg Lunch", "Main Course")],
                               "dinner":    [("swiss veg autumn dinner", "Autumn Veg Dinner", "Main Course")],
                               "snack":     [("swiss veg autumn snack", "Autumn Veg Snack", "Snack")]}},
        "non_veg": {"winter": {"breakfast": [("swiss meat breakfast winter", "Swiss Meat Breakfast", "Breakfast")],
                               "lunch":     [("switzerland dried meat cold cuts lunch winter", "Dried Meat Platter", "Main Course")],
                               "dinner":    [("switzerland raclette meat dinner winter", "Raclette", "Main Course")],
                               "snack":     [("swiss meat snack winter", "Swiss Meat Snack", "Snack")]},
                    "spring": {"breakfast": [("swiss non veg spring breakfast", "Spring Meat Breakfast", "Breakfast")],
                               "lunch":     [("swiss non veg spring lunch", "Spring Meat Lunch", "Main Course")],
                               "dinner":    [("swiss non veg spring dinner", "Spring Meat Dinner", "Main Course")],
                               "snack":     [("swiss non veg spring snack", "Spring Meat Snack", "Snack")]},
                    "summer": {"breakfast": [("swiss non veg summer breakfast", "Summer Meat Breakfast", "Breakfast")],
                               "lunch":     [("swiss grilled meat summer lunch alpine", "Alpine Grilled Lunch", "Main Course")],
                               "dinner":    [("swiss non veg summer dinner", "Summer Meat Dinner", "Main Course")],
                               "snack":     [("swiss non veg summer snack", "Summer Meat Snack", "Snack")]},
                    "autumn": {"breakfast": [("swiss non veg autumn breakfast", "Autumn Meat Breakfast", "Breakfast")],
                               "lunch":     [("swiss non veg autumn lunch", "Autumn Meat Lunch", "Main Course")],
                               "dinner":    [("swiss non veg autumn dinner", "Autumn Meat Dinner", "Main Course")],
                               "snack":     [("swiss non veg autumn snack", "Autumn Meat Snack", "Snack")]}},
        "vegan":   {"winter": {"breakfast": [("swiss vegan breakfast winter", "Swiss Vegan Breakfast", "Breakfast")],
                               "lunch":     [("swiss vegan lunch winter", "Vegan Winter Lunch", "Main Course")],
                               "dinner":    [("swiss vegan dinner winter", "Vegan Winter Dinner", "Main Course")],
                               "snack":     [("swiss vegan snack winter", "Vegan Winter Snack", "Snack")]},
                    "spring": {"breakfast": [("swiss vegan spring breakfast", "Vegan Spring Breakfast", "Breakfast")],
                               "lunch":     [("swiss vegan spring lunch", "Vegan Spring Lunch", "Main Course")],
                               "dinner":    [("swiss vegan spring dinner", "Vegan Spring Dinner", "Main Course")],
                               "snack":     [("swiss vegan spring snack", "Vegan Spring Snack", "Snack")]},
                    "summer": {"breakfast": [("swiss vegan summer breakfast", "Vegan Summer Breakfast", "Breakfast")],
                               "lunch":     [("swiss vegan summer lunch", "Vegan Summer Lunch", "Main Course")],
                               "dinner":    [("swiss vegan summer dinner", "Vegan Summer Dinner", "Main Course")],
                               "snack":     [("swiss vegan summer snack", "Vegan Summer Snack", "Snack")]},
                    "autumn": {"breakfast": [("swiss vegan autumn breakfast", "Vegan Autumn Breakfast", "Breakfast")],
                               "lunch":     [("swiss vegan autumn lunch", "Vegan Autumn Lunch", "Main Course")],
                               "dinner":    [("swiss vegan autumn dinner", "Vegan Autumn Dinner", "Main Course")],
                               "snack":     [("swiss vegan autumn snack", "Vegan Autumn Snack", "Snack")]}},
        "egg":     {"winter": {"breakfast": [("swiss egg breakfast winter rosti", "Egg Rösti Breakfast", "Breakfast")],
                               "lunch":     [("swiss egg lunch winter", "Swiss Egg Lunch", "Main Course")],
                               "dinner":    [("swiss egg dinner winter", "Swiss Egg Dinner", "Main Course")],
                               "snack":     [("swiss egg snack winter", "Swiss Egg Snack", "Snack")]},
                    "spring": {"breakfast": [("swiss egg spring breakfast", "Spring Egg Breakfast", "Breakfast")],
                               "lunch":     [("swiss egg spring lunch", "Spring Egg Lunch", "Main Course")],
                               "dinner":    [("swiss egg spring dinner", "Spring Egg Dinner", "Main Course")],
                               "snack":     [("swiss egg spring snack", "Spring Egg Snack", "Snack")]},
                    "summer": {"breakfast": [("swiss egg summer breakfast", "Summer Egg Breakfast", "Breakfast")],
                               "lunch":     [("swiss egg summer lunch", "Summer Egg Lunch", "Main Course")],
                               "dinner":    [("swiss egg summer dinner", "Summer Egg Dinner", "Main Course")],
                               "snack":     [("swiss egg summer snack", "Summer Egg Snack", "Snack")]},
                    "autumn": {"breakfast": [("swiss egg autumn breakfast", "Autumn Egg Breakfast", "Breakfast")],
                               "lunch":     [("swiss egg autumn lunch", "Autumn Egg Lunch", "Main Course")],
                               "dinner":    [("swiss egg autumn dinner", "Autumn Egg Dinner", "Main Course")],
                               "snack":     [("swiss egg autumn snack", "Autumn Egg Snack", "Snack")]}},
    },
    "miami": {
        "veg":     {"winter": {"breakfast": [("miami vegetarian breakfast winter", "Miami Veg Breakfast", "Breakfast")],
                               "lunch":     [("miami vegetarian lunch winter avocado", "Avocado Bowl", "Main Course")],
                               "dinner":    [("miami vegetarian dinner winter", "Miami Veg Dinner", "Main Course")],
                               "snack":     [("miami vegetarian snack winter", "Miami Veg Snack", "Snack")]},
                    "spring": {"breakfast": [("miami vegetarian spring breakfast", "Spring Veg Breakfast", "Breakfast")],
                               "lunch":     [("miami vegetarian spring lunch", "Spring Veg Lunch", "Main Course")],
                               "dinner":    [("miami vegetarian spring dinner", "Spring Veg Dinner", "Main Course")],
                               "snack":     [("miami vegetarian spring snack", "Spring Veg Snack", "Snack")]},
                    "summer": {"breakfast": [("miami vegetarian summer breakfast", "Summer Veg Breakfast", "Breakfast")],
                               "lunch":     [("miami vegetarian summer bowl lunch beach", "Summer Veg Bowl", "Main Course")],
                               "dinner":    [("miami vegetarian summer dinner", "Summer Veg Dinner", "Main Course")],
                               "snack":     [("miami vegetarian summer snack fruit", "Tropical Fruit Snack", "Snack")]},
                    "autumn": {"breakfast": [("miami vegetarian autumn breakfast", "Autumn Veg Breakfast", "Breakfast")],
                               "lunch":     [("miami vegetarian autumn lunch", "Autumn Veg Lunch", "Main Course")],
                               "dinner":    [("miami vegetarian autumn dinner", "Autumn Veg Dinner", "Main Course")],
                               "snack":     [("miami vegetarian autumn snack", "Autumn Veg Snack", "Snack")]}},
        "non_veg": {"winter": {"breakfast": [("miami non veg breakfast winter eggs", "Miami Meat Breakfast", "Breakfast")],
                               "lunch":     [("miami cuban sandwich lunch winter", "Cuban Sandwich", "Main Course")],
                               "dinner":    [("miami grilled fish dinner winter", "Grilled Fish Dinner", "Main Course")],
                               "snack":     [("miami non veg snack winter", "Miami Meat Snack", "Snack")]},
                    "spring": {"breakfast": [("miami non veg spring breakfast", "Spring Meat Breakfast", "Breakfast")],
                               "lunch":     [("miami non veg spring lunch seafood", "Spring Seafood Lunch", "Main Course")],
                               "dinner":    [("miami non veg spring dinner", "Spring Meat Dinner", "Main Course")],
                               "snack":     [("miami non veg spring snack", "Spring Meat Snack", "Snack")]},
                    "summer": {"breakfast": [("miami non veg summer breakfast", "Summer Meat Breakfast", "Breakfast")],
                               "lunch":     [("miami grilled seafood summer lunch beach", "Beach Seafood Lunch", "Main Course")],
                               "dinner":    [("miami bbq dinner summer", "BBQ Summer Dinner", "Main Course")],
                               "snack":     [("miami non veg summer snack", "Summer Meat Snack", "Snack")]},
                    "autumn": {"breakfast": [("miami non veg autumn breakfast", "Autumn Meat Breakfast", "Breakfast")],
                               "lunch":     [("miami non veg autumn lunch", "Autumn Meat Lunch", "Main Course")],
                               "dinner":    [("miami non veg autumn dinner", "Autumn Meat Dinner", "Main Course")],
                               "snack":     [("miami non veg autumn snack", "Autumn Meat Snack", "Snack")]}},
        "vegan":   {"winter": {"breakfast": [("miami vegan breakfast winter smoothie", "Vegan Smoothie Breakfast", "Breakfast")],
                               "lunch":     [("miami vegan lunch winter bowl", "Vegan Winter Bowl", "Main Course")],
                               "dinner":    [("miami vegan dinner winter", "Vegan Winter Dinner", "Main Course")],
                               "snack":     [("miami vegan snack winter", "Vegan Winter Snack", "Snack")]},
                    "spring": {"breakfast": [("miami vegan spring breakfast", "Vegan Spring Breakfast", "Breakfast")],
                               "lunch":     [("miami vegan spring lunch", "Vegan Spring Lunch", "Main Course")],
                               "dinner":    [("miami vegan spring dinner", "Vegan Spring Dinner", "Main Course")],
                               "snack":     [("miami vegan spring snack", "Vegan Spring Snack", "Snack")]},
                    "summer": {"breakfast": [("miami vegan summer breakfast smoothie bowl", "Vegan Smoothie Bowl", "Breakfast")],
                               "lunch":     [("miami vegan summer lunch beach", "Beach Vegan Bowl", "Main Course")],
                               "dinner":    [("miami vegan summer dinner", "Summer Vegan Dinner", "Main Course")],
                               "snack":     [("miami vegan summer snack tropical", "Tropical Vegan Snack", "Snack")]},
                    "autumn": {"breakfast": [("miami vegan autumn breakfast", "Autumn Vegan Breakfast", "Breakfast")],
                               "lunch":     [("miami vegan autumn lunch", "Autumn Vegan Lunch", "Main Course")],
                               "dinner":    [("miami vegan autumn dinner", "Autumn Vegan Dinner", "Main Course")],
                               "snack":     [("miami vegan autumn snack", "Autumn Vegan Snack", "Snack")]}},
        "egg":     {"winter": {"breakfast": [("miami egg breakfast winter brunch", "Miami Brunch Eggs", "Breakfast")],
                               "lunch":     [("miami egg lunch winter", "Miami Egg Lunch", "Main Course")],
                               "dinner":    [("miami egg dinner winter", "Miami Egg Dinner", "Main Course")],
                               "snack":     [("miami egg snack winter", "Miami Egg Snack", "Snack")]},
                    "spring": {"breakfast": [("miami egg spring breakfast", "Spring Egg Breakfast", "Breakfast")],
                               "lunch":     [("miami egg spring lunch", "Spring Egg Lunch", "Main Course")],
                               "dinner":    [("miami egg spring dinner", "Spring Egg Dinner", "Main Course")],
                               "snack":     [("miami egg spring snack", "Spring Egg Snack", "Snack")]},
                    "summer": {"breakfast": [("miami egg summer breakfast beach brunch", "Beach Brunch Eggs", "Breakfast")],
                               "lunch":     [("miami egg summer lunch", "Summer Egg Lunch", "Main Course")],
                               "dinner":    [("miami egg summer dinner", "Summer Egg Dinner", "Main Course")],
                               "snack":     [("miami egg summer snack", "Summer Egg Snack", "Snack")]},
                    "autumn": {"breakfast": [("miami egg autumn breakfast", "Autumn Egg Breakfast", "Breakfast")],
                               "lunch":     [("miami egg autumn lunch", "Autumn Egg Lunch", "Main Course")],
                               "dinner":    [("miami egg autumn dinner", "Autumn Egg Dinner", "Main Course")],
                               "snack":     [("miami egg autumn snack", "Autumn Egg Snack", "Snack")]}},
    },
}

# Pilot mode
PILOT_MODE = False
PILOT_LOCATION = "dubai"

# Locations already FULLY downloaded — skipped automatically
# Dubai pilot is done, so it is listed here
COMPLETED_LOCATIONS = ["dubai"]

# Images per time_of_day folder (target)
IMAGES_PER_FOLDER = 15

# Speed settings
MAX_WORKERS = 4        # parallel download threads (~4x faster)
MAX_NUM_PER_QUERY = 30 # max images requested per search query
CRAWLER_TIMEOUT = 30   # seconds timeout per query