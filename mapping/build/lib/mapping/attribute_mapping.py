import pandas as pd
import numpy as np
import os
from os.path import exists
import csv


def row_to_dict(rows):
    combined_dict = {}
    for col in rows.columns:
        values = rows[col].dropna().unique().tolist()
        values = [v for v in values if v not in ("", None, np.nan)]
        if values:
            combined_dict[col] = values
    return combined_dict


def process_attribute_mapping(input_skus, df1, df2, filtered_df, output_path):
    """
    Process attribute mappings and save results to a CSV file.

    Parameters:
    input_skus (list): List of SKUs to process.
    df1 (pd.DataFrame): DataFrame for source 1.
    df2 (pd.DataFrame): DataFrame for source 2.
    filtered_df (pd.DataFrame): Filtered DataFrame with attribute mappings.
    output_path (str): Path to save the output CSV file.
    """
    header = []
    for i in range(0, len(filtered_df)):
        row = filtered_df.loc[i]
        step = row['Source_1'] + '_Source_1'
        rms = row['Source_2'] + '_Source_2'
        is_present = 'is_present'
        is_multivalue = 'is_multivalue'
        header.extend([step, rms, is_present, is_multivalue])

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    if exists(output_path):
        os.remove(output_path)

    with open(output_path, 'a', encoding='utf-8', errors='ignore', newline='') as file:
        writer = csv.writer(file, delimiter='^')
        writer.writerow(header)

    for sku in input_skus:
        df1_rows = df1[df1['Item SKU Number'] == sku]
        df2_rows = df2[df2['ITEM'] == sku]

        df1_dict = row_to_dict(df1_rows) if not df1_rows.empty else {}
        df2_dict = row_to_dict(df2_rows) if not df2_rows.empty else {}

        out_row = []
        for i in range(len(filtered_df)):
            row = filtered_df.iloc[i]
            step = row['Source_1']
            rms = row['Source_2']

            val1 = ' ~ '.join(map(str, df1_dict.get(step, [None]))) if step in df1_dict else None
            val2 = ' ~ '.join(map(str, df2_dict.get(rms, [None]))) if rms in df2_dict else None

            is_present = bool(set(val1.split(' ~ ')) & set(val2.split(' ~ '))) if val1 and val2 else False
            is_multivalue = None
            if step in df1_dict and len(df1_dict[step]) > 1:
                is_multivalue = "Source_1"
            if rms in df2_dict and len(df2_dict[rms]) > 1:
                is_multivalue = "Source_2" if is_multivalue is None else "both"

            out_row.extend([val1, val2, is_present, is_multivalue])

        with open(output_path, 'a', encoding='utf-8', errors='ignore', newline='') as file:
            writer = csv.writer(file, delimiter='^')
            writer.writerow(out_row)
