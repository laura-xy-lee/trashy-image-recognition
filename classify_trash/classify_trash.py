import os
from itertools import compress
from typing import Text
import ast

import re
import pandas as pd
import numpy as np

# Get latest list of recyclables
dir_name = "classify_trash/output"
file_names = os.listdir(dir_name)
prefix = "recyclables_data"
starts_with_prefix = [f.startswith(prefix) for f in file_names]
data_files = list(compress(file_names, starts_with_prefix))
latest_data_file = sorted(data_files)[-1]
recyclables_df = pd.read_csv(os.path.join(dir_name, latest_data_file))


def classify(trash: Text,
             classification: pd.DataFrame = recyclables_df):
    def literal_return(val):
        try:
            return ast.literal_eval(val)
        except (ValueError, SyntaxError) as e:
            return val

    if trash == "nipple":
        return {'identified_item': "inappropriate image",
                'material': "None",
                'item_classification_name': "None",
                'is_recyclable': False,
                'remarks': "None"}

    c_df = classification.copy()
    c_df["labels"] = c_df["labels"].replace(np.nan, '')
    c_df['remarks'] = c_df['remarks'].replace(np.nan, '')
    c_df['labels'] = c_df['labels'].apply(literal_return)

    # Search for trash in "labels" first
    df = c_df[c_df["labels"].apply(lambda x: True if trash in x else False)]

    # If not in "labels", search in "item" name
    if not df.empty:
        return_label = df.iloc[0]["item"]
    else:
        df = c_df[c_df['item'].str.contains(trash, flags=re.IGNORECASE)]
        return_label = trash

    if not df.empty:
        df_first = df.iloc[0]
        result = {'identified_item': return_label,
                  'material': df_first['group'],
                  'item_classification_name': df_first['item'],
                  'is_recyclable': df_first['is_recyclable'],
                  'remarks': df_first['remarks']}

    else:
        result = {'identified_item': trash,
                  'material': "None",
                  'item_classification_name': "None",
                  'is_recyclable': False,
                  'remarks': "This item is not yet in our database."}

    return result
