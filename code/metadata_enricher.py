def enrich_metadata(row):

    if "kandura" in row["image_filename"].lower():

        row["gender"] = "male"
        row["subcategory"] = "kandura"
        row["cultural_tag"] = "emirati"

    elif "abaya" in row["image_filename"].lower():

        row["gender"] = "female"
        row["subcategory"] = "abaya"
        row["cultural_tag"] = "emirati"

    return row