"""Manually add labels to various classification objects"""
import datetime

import re
import pandas as pd


def update_classification(raw_data_path,
                          output_file_path):
    # Read raw data file
    df_raw = pd.read_csv(raw_data_path)
    df = df_raw.copy()
    df['labels'] = None

    # Handle duplicate results for clothes
    condition = (df['item'].str.contains("clothes", flags=re.IGNORECASE)
                 & (df['item'] != "Plastic clothes hanger"))
    df = df[-condition]
    clothes_df = pd.DataFrame({
        "is_recyclable": [True],
        "item": ["Old items which are in good condition (e.g. clothes, shoes, bag, soft toy, umbrella, spectacle etc)"],
        "remarks": ["Donate to charity or give it away if possible. Bag before depositing into the recycling bin."],
        "labels": [""],
        "group": ["Others"]})
    df = df.append(clothes_df).reset_index(drop=True)

    # Add labels to 'clothes', but not `plastic clothes hanger`
    condition = (df['item'].str.contains("clothes", flags=re.IGNORECASE)
                 & (df['item'] != "Plastic clothes hanger"))
    condition_index = df.index[condition]

    for i in condition_index:
        df.at[i, 'labels'] = ["jersey", "shirt", "T-shirt", "tee shirt",
                              "sweatshirt", "pajama", "pyjama", "pj's",
                              "jammies gown robe"]

    # Add milk carton
    condition = df['item'].str.contains("milk carton", flags=re.IGNORECASE)
    condition_index = df.index[condition]

    for i in condition_index:
        df.at[i, 'labels'] = ["eggnog"]

    # Add mobile phones
    condition = df['item'].str.contains("mobile phone", flags=re.IGNORECASE)
    condition_index = df.index[condition]

    for i in condition_index:
        df.at[i, 'labels'] = ["cellular telephone"]

    # Add light bulbs
    condition = df['item'].str.contains("light bulb", flags=re.IGNORECASE)
    condition_index = df.index[condition]

    for i in condition_index:
        df.at[i, 'labels'] = ["spotlight"]

    # Add tea pot
    condition = df['item'].str.contains("tea pot", flags=re.IGNORECASE)
    condition_index = df.index[condition]

    for i in condition_index:
        df.at[i, 'labels'] = ["teapot"]

    # Add stationery
    condition = df['item'].str.contains("stationery", flags=re.IGNORECASE)
    condition_index = df.index[condition]

    for i in condition_index:
        df.at[i, 'labels'] = ["rubber eraser", "ballpoint", "pencil sharpener",
                              "pencil box", "quill", "fountain pen"]

    # Add bags
    condition = df['item'].str.contains("bag", flags=re.IGNORECASE)
    condition_index = df.index[condition]

    for i in condition_index:
        df.at[i, 'labels'] = ["mailbag"]

    # Add furniture
    condition = df['item'].str.contains("furniture", flags=re.IGNORECASE)
    condition_index = df.index[condition]

    for i in condition_index:
        df.at[i, 'labels'] = ["studio couch", "electric fan"]

    # Add eye glasses
    condition = df['item'].str.contains("spectacles", flags=re.IGNORECASE)
    condition_index = df.index[condition]

    for i in condition_index:
        df.at[i, 'labels'] = ["loupe", "sunglasses"]

    # Add beer bottle
    condition = df['item'].str.contains("beer", flags=re.IGNORECASE)
    condition_index = df.index[condition]

    for i in condition_index:
        df.at[i, 'labels'] = ["beer bottle"]

    # Save updated data
    df = (df.sort_values(["group", "is_recyclable"])
            .reset_index(drop=True))
    df.to_csv(output_file_path, index=False)


data_file_name = "classify_trash/output/recyclables_data.csv"
updated_file_name = ("classify_trash/output/recyclables_data_"
                     + datetime.datetime.strftime(datetime.datetime.now(),
                                                  '%Y%m%d%H%M') + ".csv")

update_classification(raw_data_path=data_file_name,
                      output_file_path=updated_file_name)
