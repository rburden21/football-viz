#packages
import requests
from bs4 import BeautifulSoup
import pandas as pd
from math import pi
import matplotlib.pyplot as plt
import numpy as np
import radar_chart_func as rcf
from qbstyles import mpl_style
from matplotlib.patches import Patch

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

def convert_to_float(value):
    if value.endswith('%'):
        return float(value[:-1])/100
    else:
        return float(value)

def df_to_list(data):
    # convert dataframe to flattened list
    flat_list = data.values.tolist()
    flat_list_int = [convert_to_float(x) for x in flat_list]
    return flat_list_int

def create_dataframe(df, metrics, col_name):
    #create dataframe from fbref data
    data_main = df.loc[df['Statistic'].isin(metrics)].drop_duplicates()
    data_main = data_main.loc[~(df.duplicated(['Statistic'], keep='first'))]
    data_main = data_main.sort_values(by=['Statistic'], key=lambda x: x.map(dict(zip(metrics, range(len(metrics)))))).reset_index(drop=True)

    # duplicate the second row
    row_to_duplicate = data_main.iloc[0]
    first_row_df = pd.DataFrame(row_to_duplicate).transpose()
    data_main = pd.concat([data_main, first_row_df], ignore_index=True)

    data = data_main[col_name]
    return data

def player_radar_chart(player1, data1, player2, data2, attributes,labels1,labels2,error_check=0):
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

    #Adding in custom chart style - https://github.com/quantumblacklabs/qbstyles
    mpl_style(dark=True)

    #These two lines of code compute a list of angles for the radar chart based on the number of attributes passed in.
    #Also need to append a 0 to create a joining angle to map to
    angles1 = [n / len(attributes) * 2 * pi for n in range(len(attributes))]
    angles1.append(0)

    if error_check == 1:
        print(f"length_{len(angles1)}_angles1: {angles1}")
        print(f"length_{len(data1)}_data1: {data1}")
        print(f"length_{len(attributes)}_attributes: {attributes}")

    # Setting the figure size and DPI
    fig, ax = plt.subplots(figsize=(10,8), dpi=300)

    # Setting the subplot to polar projection
    ax = plt.subplot(111, projection='polar')

    # Setting the position of the subplot in the figure - [left, bottom, width, height]
    ax.set_position([0.02, 0.1, 0.8, 0.8])

    # Setting the color and transparency of the grid lines
    ax.grid(color='white', alpha=0.2)

    if error_check == 1:
        print(f"checking xticks. angles1_length_{len(angles1)}; attributes_length_{len(attributes)}")
        print(f"checking plot 1. angles1_length_{len(angles1)}; data1_length_{len(data1)}")
        print(f"checking plot 2. angles2_length_{len(angles2)}; data2_length_{len(data2)}")

    # Setting the x-axis ticks and labels
    ax.set_xticks(angles1[:-1])
    ax.set_xticklabels(attributes, ha='center', rotation=45)
    ax.tick_params(axis='both', which='major', pad=20, labelsize=8)

    # Plotting the data
    ax.plot(angles1, data1, linestyle='dashed')
    ax.fill(angles1, data1, alpha=0.1)
    ax.plot(angles1, data2, linestyle='dashed')
    ax.fill(angles1, data2, alpha=0.1) 

    # Adding labels for data points
    for angle, data1, data2, labels1, labels2 in zip(angles1, data1, data2, labels1, labels2):
        ax.text(angle, data1, f"{labels1:.2f}", fontsize=8, ha='center', va='center', bbox=dict(facecolor='white', edgecolor='dimgray', alpha=0.2))
        ax.text(angle, data2, f"{labels2:.2f}", fontsize=8, ha='center', va='center', bbox=dict(facecolor='white', edgecolor='dimgray', alpha=0.2))

    # Create custom legend handles
    player1_legend = Patch(facecolor='C0', alpha=0.5, label=player1)
    player2_legend = Patch(facecolor='C1', alpha=0.5, label=player2)

    # Add a legend with custom position and handles
    ax.legend(handles=[player1_legend, player2_legend], bbox_to_anchor=(1.3, 0.05), fontsize=10, frameon=True)
    
    # Set the title and subtitles of the plot
    plt.figtext(0.00, 1.00, player1, fontsize='large', color='C0', ha ='left')
    plt.figtext(0.00, 0.98, ' vs ', fontsize='medium', color='w', ha ='left')
    plt.figtext(0.00, 0.96, player2, fontsize='large', color='C1', ha ='left')
    plt.figtext(0.00, 0.94, 'Attribute Comparison', fontsize='small', color='w', ha ='left')
    plt.figtext(0.45, 0.00, 'FBRef Data | Players compared over the last 365 days to similar strength competitions for their position', 
                    fontsize='xx-small', color='w', ha ='center')

    plt.show()