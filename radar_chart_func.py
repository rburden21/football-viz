#packages
import requests
from bs4 import BeautifulSoup
import pandas as pd
from math import pi
import matplotlib.pyplot as plt
import numpy as np

# Set option to show all rows and columns
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

#functions
def get_player_name(url):
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
    name = title.split('Scouting Report')[0].strip()
    return name

def extract_tables_from_url(url):
    tables = pd.read_html(url, skiprows=1, header=0)
    return tables

def df_to_list(data):
    # convert dataframe to flattened list
    #flat_list = [item for sublist in data.values.tolist() for item in sublist]
    flat_list = data.values.tolist()
    flat_list_int = [int(x) for x in flat_list]
    return flat_list_int

def create_dataframe(df, metrics):
    #create dataframe from fbref data
    data_main = df[df['Statistic'].isin(metrics)].drop_duplicates()
    data_main = data_main.sort_values(by=['Statistic'], key=lambda x: x.map(dict(zip(metrics, range(len(metrics)))))).reset_index(drop=True)

    # duplicate the second row
    row_to_duplicate = data_main.iloc[0]
    first_row_df = pd.DataFrame(row_to_duplicate).transpose()
    data_main = pd.concat([data_main, first_row_df], ignore_index=True)

    data = data_main['Percentile']
    return data

def player_radar_chart(player1, data1, player2, data2, attributes):
    """
    Plot a radar chart showing the performance of two players across a set of attributes.

    Parameters:
    player1 (str): Name of the first player.
    data1 (list): List of values for the first player's performance across each attribute.
    player2 (str): Name of the second player.
    data2 (list): List of values for the second player's performance across each attribute.
    attributes (list): List of attribute names to plot.

    Returns:
    None: Displays the plot.

    Example:
    >>> player1_data = [85, 87, 93, 84, 79, 86, 75, 84]
    >>> player2_data = [89, 84, 92, 86, 78, 87, 77, 86]
    >>> attributes = ['overall', 'potential', 'pace', 'shooting', 'passing', 'dribbling', 'defending', 'physical']
    >>> player_radar_chart('Player 1', player1_data, 'Player 2', player2_data, attributes)
    """

    #These two lines of code compute a list of angles for the radar chart based on the number of attributes passed in.
    angles1 = [n / len(attributes) * 2 * pi for n in range(len(attributes))]
    angles1 += angles1[:1]

    #plt.figure(dpi=125)
    plt.figure(figsize=(8, 4), dpi=150, facecolor='black', edgecolor='red', frameon=True)

    #setting the subplot (ax)
    ax = plt.subplot(111, polar=True, facecolor='lightgray')
    # Center the plot by adjusting the subplot position - [left, bottom, width, height]
    ax.set_position([0.02, 0.1, 0.8, 0.8])
    # set the color of the grid lines
    ax.grid(color='dimgray', alpha=0.5)

    plt.xticks(angles1[:-1], attributes, fontsize=8, color='red', ha='center')
    ax.tick_params(axis='x', pad=15) 
    
    ax.plot(angles1, data1, color='green',linestyle='dashed')
    ax.fill(angles1, data1, 'green', alpha=0.1)

    angles2 = angles1.copy()
    ax.plot(angles2, data2, color='blue',linestyle='dashed')
    ax.fill(angles2, data2, 'blue', alpha=0.1)

    plt.figtext(0.1, 0.98, player1, color='green')
    plt.figtext(0.1, 0.94, player2, color='blue')

    plt.show()

def player_radar_chart_test(player1, data1, player2, data2, attributes):
    """
    Plot a radar chart showing the performance of two players across a set of attributes.

    Parameters:
    player1 (str): Name of the first player.
    data1 (list): List of values for the first player's performance across each attribute.
    player2 (str): Name of the second player.
    data2 (list): List of values for the second player's performance across each attribute.
    attributes (list): List of attribute names to plot.

    Returns:
    None: Displays the plot.

    Example:
    >>> player1_data = [85, 87, 93, 84, 79, 86, 75, 84]
    >>> player2_data = [89, 84, 92, 86, 78, 87, 77, 86]
    >>> attributes = ['overall', 'potential', 'pace', 'shooting', 'passing', 'dribbling', 'defending', 'physical']
    >>> player_radar_chart('Player 1', player1_data, 'Player 2', player2_data, attributes)
    """

    angles1 = [n / float(len(attributes)) * 2 * pi for n in range(len(attributes))]
    angles1 += angles1[:1]

    plt.figure(figsize=(8, 4), dpi=150, facecolor='black', edgecolor='red', frameon=True)

    ax = plt.subplot(111, polar=True, facecolor='lightgray')
    ax.set_position([0.02, 0.1, 0.8, 0.8])
    ax.grid(color='dimgray', alpha=0.5)

    plt.xticks(angles1[:-1], attributes, fontsize=8, color='red', ha='center')
    ax.tick_params(axis='x', pad=15) 
    
    ax.plot(angles1, data1, color='green', linestyle='dashed')
    ax.fill(angles1, data1, 'green', alpha=0.1)

    angles2 = angles1.copy()
    ax.plot(angles2, data2, color='blue', linestyle='dashed')
    ax.fill(angles2, data2, 'blue', alpha=0.1)

    plt.figtext(0.1, 0.98, player1, color='green')
    plt.figtext(0.1, 0.94, player2, color='blue')

    plt.show()
