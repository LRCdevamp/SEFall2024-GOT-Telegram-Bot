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

def get_battles_names(filename):
    df = pd.read_csv(filename)
    battle_names = []
    for i in range(0,len(df)):
        battle_names.append(df.iloc[i,0])
    return battle_names

def get_entry(filename,index):
    df = pd.read_csv(filename)
    return df.iloc[index]
    

def get_characters_name(filename,word):
    df = pd.read_csv(filename)
    names = []
    for i in range(0,len(df)):
        if df.iloc[i,5][0] == word:
            names.append(df.iloc[i,5])
    return split_list(names,20)


def split_list(input_list, max_length):
    if not input_list:
        return []
    
    result = []
    for i in range(0, len(input_list), max_length):
        if i + max_length < len(input_list):
            result.append(input_list[i:i + max_length])
        else:
            result.append(input_list[i:])
    return result

def get_characters_names_length(filename,word):
    df = pd.read_csv(filename)
    names = []
    for i in range(0,len(df)):
        if df.iloc[i,5][0] == word:
            names.append(df.iloc[i,5])
    return len(names)
   

def get_names(filename):
    df = pd.read_csv(filename)
    names = []
    for i in range(0,len(df)):
        names.append(df.iloc[i,5])
    return names