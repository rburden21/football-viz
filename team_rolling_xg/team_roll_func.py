import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from highlight_text import fig_text
from qbstyles import mpl_style
import requests
from bs4 import BeautifulSoup
import re

def extract_tables_from_url(url):
    tables = pd.read_html(url)
    return tables

def get_team_name(url):
    """
    Returns the name of a player based on their scouting report URL.

    Parameters:
    url (str): The URL of the player's scouting report.

    Returns:
    str: The player's name extracted from the scouting report title.

    Example:
    >>> url = "https://www.example.com/scouting-report/player-name"
    >>> get_player_name(url)
    'Player Name'
    """
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.find('title').get_text()
    if re.match('.*\d.*', title):
        name = title.split('Scores')[0].strip()
        name = name.split()[1:]
        name = ' '.join(name)
    else:
        name = title.split('Scores')[0].strip()
    return name

def get_league_name(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.find('title').get_text()
    name = title.split('|')[0].strip()
    name = name.split(',')[1].strip()
    return name

def lists_to_dfs(lists):
    dfs = []
    for lst in lists:
        # convert the list to a numpy array
        arr = np.array(lst)
        # reshape the numpy array into a two-dimensional array
        reshaped_arr = arr.reshape(-1, arr.shape[-1])
        cols = ['date','time','round','day','venue','result','gf','ga','opponent',
                    'xg','xga','possession','attendance','captain','formation','referee','match report','notes']
        # create a DataFrame from the reshaped data
        df = pd.DataFrame(reshaped_arr, columns=cols)
        dfs.append(df)
    # Concatenate all the dataframes
    combined_df = pd.concat(dfs, ignore_index=True)
    return combined_df

def prepare_df(df):
    df = df.drop(columns=['time','day','captain','formation','referee','match report', 'notes','attendance'])
    df = df.dropna()
    df['date'] = pd.to_datetime(df['date'])
    df['gf'] = df['gf'].astype(int)
    df['ga'] = df['ga'].astype(int)
    df['xg'] = df['xg'].astype(float)
    df['xga'] = df['xga'].astype(float)
    df['possession'] = df['possession'].astype(int)
    df['xg_roll'] = df['xg'].rolling(window = 10, min_periods = 10).mean()
    df['xga_roll'] = df['xga'].rolling(window = 10, min_periods = 10).mean()
    return df