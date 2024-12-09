import os
import pandas as pd

def concat_files_with_reference(folder_path):
    """
    Concatenates files in a folder and adds a 'Reference' column based on the file name.

    Parameters:
    folder_path (str): Path to the folder containing input files.

    Returns:
    pd.DataFrame: Concatenated DataFrame with a 'Reference' column.
    """
    all_data = []
    encodings_to_try = ['utf-8', 'ISO-8859-1', 'cp1252']

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            try:
                if file_name.endswith('.csv'):
                    df = None
                    for encoding in encodings_to_try:
                        try:
                            df = pd.read_csv(file_path, encoding=encoding, low_memory=False)
                            break
                        except UnicodeDecodeError:
                            continue
                    if df is None:
                        raise UnicodeDecodeError(f"Could not decode {file_name} with any encoding.")

                elif file_name.endswith('.tsv'):
                    df = None
                    for encoding in encodings_to_try:
                        try:
                            df = pd.read_csv(file_path, sep='\t', encoding=encoding, low_memory=False)
                            break
                        except UnicodeDecodeError:
                            continue
                    if df is None:
                        raise UnicodeDecodeError(f"Could not decode {file_name} with any encoding.")

                elif file_name.endswith(('.xls', '.xlsx')):
                    df = pd.read_excel(file_path)

                else:
                    continue

                df['Reference'] = file_name
                all_data.append(df)
            except Exception as e:
                print(f"Error processing file {file_name}: {e}")

    if all_data:
        concatenated_df = pd.concat(all_data, ignore_index=True)
        return concatenated_df
    else:
        print("No valid files found in the folder.")
        return pd.DataFrame()
