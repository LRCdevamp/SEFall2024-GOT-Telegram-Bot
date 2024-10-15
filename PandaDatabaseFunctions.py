import pandas as pd
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BattlesDatabase = 'battles.csv'
CharactersDeathesDatabase = 'character-deaths.csv'
CharactersPredictions = 'character-predictions.csv'

def get_csv_path(filename):
    return os.path.join(SCRIPT_DIR, filename)

def read_csv(filename):
    file_path = get_csv_path(filename)
    return pd.read_csv(file_path)

def get_battles_names():
    df = pd.read_csv(BattlesDatabase)
    battle_names = []
    for i in range(0,len(df)):
        battle_names.append(df.iloc[i,0])
    return battle_names

def get_entry(filename,index):
    df = pd.read_csv(filename)
    return df.iloc[index]
    
def get_splitted_characters_name(word):
    df = pd.read_csv(CharactersPredictions)
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

def get_characters_names_length(word):
    df = pd.read_csv(CharactersPredictions)
    names = []
    for i in range(0,len(df)):
        if df.iloc[i,5][0] == word:
            names.append(df.iloc[i,5])
    return len(names)
   
def get_characters_deaths_length(word):
    df = pd.read_csv(CharactersDeathesDatabase)
    names = []
    for i in range(0,len(df)):
        if df.iloc[i,0][0] == word:
            names.append(df.iloc[i,0])
    return len(names)

def get_names_from_characters():
    df = pd.read_csv(CharactersPredictions)
    names = []
    for i in range(0,len(df)):
        names.append(df.iloc[i,5])
    return names

def get_all_names_from_deaths():
    df = pd.read_csv(CharactersDeathesDatabase)
    names = []
    for i in range(0,len(df)):
        names.append(df.iloc[i,0])
    return names

def get_splitted_names_from_deaths(word):
    df = pd.read_csv(CharactersDeathesDatabase)
    names = []
    for i in range(0,len(df)):
        if df.iloc[i,0][0] == word:
            names.append(df.iloc[i,0])
    return split_list(names,20)