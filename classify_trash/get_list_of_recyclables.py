import os
from typing import Text, List
import re

import requests
import pandas as pd
import numpy as np


def html_to_df(source: Text,
               path: Text) -> List[pd.DataFrame]:
    """
    Convert html to list of pandas dataframes

    :param source: Source of html, either 'url' or 'file'
    :param path: If source is 'url', enter url. If source if 'file',
                 enter file path
    """
    if source == "url":
        r = requests.get(path)
        r_html = r.text
    elif source == "file":
        with open(path) as f:
            r_html = f.read()

    r_df_list = pd.read_html(r_html)

    return r_df_list


def get_mewr_recyclables(source: Text,
                         path: Text) -> pd.DataFrame:
    """
    Get recyclables from MEWR.

    :param source: Source of html, either 'url' or 'file'
    :param path: If source is 'url', enter url. If source if 'file',
                 enter file path
    """
    # Get mewr df
    mewr_df_list = html_to_df(source=source,
                              path=path)

    # Get item type
    mewr_df = pd.DataFrame()
    for i, df in enumerate(mewr_df_list):
        if i == 0:
            item_type = "Paper"
        elif i == 1:
            item_type = "Plastics"
        elif i == 2:
            item_type = "Glass"
        elif i == 3:
            item_type = "Metal"
        elif i == 4:
            item_type = "Others"

        df["group"] = item_type
        mewr_df = mewr_df.append(df)

    # Format df
    mewr_df = mewr_df.drop(columns="S/N")
    mewr_df = mewr_df.rename(columns={"Can recycle?": "is_recyclable",
                                      "Remarks": "remarks",
                                      "Item": "item"})

    mewr_df["is_recyclable"] = (mewr_df["is_recyclable"]
                                .apply(lambda x: False if x == "NO"
                                       else (True if x == "MAYBE" or x == "YES"
                                             else None)))
    mewr_df = mewr_df.reset_index(drop=True)

    return mewr_df


def get_zerowastesg_recyclables(source: Text,
                                path: Text) -> pd.DataFrame:
    """
    Get recyclables from zerowastesg.

    :param source: Source of html, either 'url' or 'file'
    :param path: If source is 'url', enter url. If source if 'file',
                 enter file path
    """
    # Get zerowaste df
    zws_df_list = html_to_df(source=source,
                             path=path)

    zws_df = pd.DataFrame()
    for df in zws_df_list:
        # Get item type
        item_type = df.columns[0]
        item_type = item_type.split()[0]

        # Split df for recyclables and non-recyclables
        df_recyclable = df.iloc[:, 0:2]
        df_recyclable.columns = ["item", "remarks"]
        df_recyclable['is_recyclable'] = True

        df_non_recyclable = df.iloc[:, 2:4]
        df_non_recyclable.columns = ["item", "remarks"]
        df_non_recyclable['is_recyclable'] = False

        # Format df
        df_group = df_recyclable.append(df_non_recyclable)
        df_group['group'] = item_type

        df_group['item'] = df_group['item'].replace("-", np.nan)
        df_group = df_group.dropna(subset=['item'])
        df_group['item'] = df_group['item'].apply(lambda x: ' '.join(x.split()[1:]))
        zws_df = zws_df.append(df_group)

    zws_df = zws_df.reset_index(drop=True)

    return zws_df


zerowastesg_output_file_name = "classify_trash/output/zws_data.csv"
mewr_output_file_name = "classify_trash/output/mewr_data.csv"
recyclables_output_file_name = "classify_trash/output/recyclables_data.csv"

# Get Zerowastesg recyclables data
if not os.path.isfile(zerowastesg_output_file_name):
    # # From url
    # zws_df = get_zerowastesg_recyclables(source="url",
    #                                      path="http://www.zerowastesg.com/recycle/")

    # From file
    zws_df = get_zerowastesg_recyclables(source="file",
                                         path="classify_trash/data/zerowastesg_recyclables.txt")

    zws_df.to_csv(zerowastesg_output_file_name, index=False)

# Get MEWR recyclables data
if not os.path.isfile(mewr_output_file_name):
    # # From url
    # mewr_df = get_mewr_recyclables(source="url",
    #                                path="https://raw.githubusercontent.com/isomerpages/isomerpages-mewr-zerowaste/staging/_recycle/03-what-to-recycle.md")

    # From file
    mewr_df = get_mewr_recyclables(source="file",
                                   path="classify_trash/data/mewr_recyclables.txt")

    mewr_df.to_csv(mewr_output_file_name, index=False)

# Get combined recyclables data
if not os.path.isfile(recyclables_output_file_name):
    mewr_df = pd.read_csv(mewr_output_file_name)
    zws_df = pd.read_csv(zerowastesg_output_file_name)

    recyclables_df = mewr_df.append(zws_df)

    # Remove duplicates
    recyclables_df['remarks'] = (recyclables_df['remarks']
                                 .replace({"-": "", np.nan: ""}))
    recyclables_df = recyclables_df.drop_duplicates()

    # Tidy text
    recyclables_df.at[recyclables_df['remarks'] == "Donate if it is in good conditionContact Town council to remove from your residential premises",
                      "remarks"] = "Donate if it is in good condition. Contact Town council to remove from your residential premises",

    # Remove light bulb duplicate
    recyclables_df = recyclables_df[recyclables_df['item'] != "Light bulbs"]

    # Update donation and ewaste points
    recyclables_df.at[recyclables_df['remarks'].str.contains("donate", flags=re.IGNORECASE), "group"] = "Donation"
    recyclables_df.at[recyclables_df['remarks'].str.contains("e-waste", flags=re.IGNORECASE), "group"] = "E-waste"
    recyclables_df.at[recyclables_df['remarks'].str.contains("specific collection points", flags=re.IGNORECASE), "group"] = "E-waste"

    recyclables_df = (recyclables_df
                      .sort_values(["group", "is_recyclable"])
                      .reset_index(drop=True))

    recyclables_df.to_csv(recyclables_output_file_name, index=False)
