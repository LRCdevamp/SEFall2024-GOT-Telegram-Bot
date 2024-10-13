import pandas as pd
import os

# Get the directory of the current script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def get_csv_path(filename):
    return os.path.join(SCRIPT_DIR, filename)

def read_csv(filename):
    file_path = get_csv_path(filename)
    return pd.read_csv(file_path)

def search_csv(filename, column, value):
    df = read_csv(filename)
    return df[df[column].str.contains(value, case=False, na=False)]

def get_column_names(filename):
    df = read_csv(filename)
    return df.columns.tolist()

def get_column_value(file_path, column_name):
    df = pd.read_csv(file_path)
    return df[column_name].tolist()


def get_unique_values(filename, column):
    df = read_csv(filename)
    return df[column].unique().tolist()

def get_value_from_row_index(file_path, row_index=1, column_index=1):
    df = pd.read_csv(file_path)    

    if row_index >= len(df):
        raise ValueError(f"Row index {row_index} is out of bounds. The CSV file has {len(df)} rows.")
    
    if column_index >= len(df.columns):
        raise ValueError(f"Column index {column_index} is out of bounds. The CSV file has {len(df.columns)} columns.")
    
    return df.iloc[row_index, column_index]

def get_battles_names(filename):
    df = pd.read_csv(filename)
    battle_names = []
    for i in range(0,len(df)):
        battle_names.append(df.iloc[i,0])
    return battle_names


    