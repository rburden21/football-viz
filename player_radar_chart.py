import radar_chart_func as rcf

#variables
url = 'https://fbref.com/en/players/8c90fd7a/scout/365_m1/Victor-Osimhen-Scouting-Report'
url2 = 'https://fbref.com/en/players/21a66f6a/scout/365_m1/Harry-Kane-Scouting-Report'


gen_attributes = ['Non-Penalty Goals','Non-Penalty xG','Shots Total','Assists','xAG','npxG + xAG',
                    'Shot-Creating Actions','Progressive Passes']

def_attributes = ['Tackles Won', 'Dribblers Tackled','% of dribblers tackled', 'Blocks', 'Shots Blocked', 'Passes Blocked',
                    'Tkl+Int', 'Errors', 'Aerials won','% of Aerials Won' ]

pos_attributes = ['Touches', 'Carries', 'Progressive Carrying Distance', 'Progressive Carries', 'Miscontrols', 'Dispossessed', 
                    'Passes Received', 'Successful Take-Ons']

shoot_attributes = ['Goals', 'Shots Total', 'Shots on target %', 'xG', 'Non-Penalty xG', 'npxG/Sh']


pass_attributes = ['Passes Completed', 'Pass Completion %','Total Passing Distance', 'Pass Completion % (Short)','Pass Completion % (Medium)',
                    'Pass Completion % (Long)', 'Expected Assists', 'Key Passes', 'Passes into Final Third', 'Progressive Passes']

attributes = gen_attributes
col_name = 'Percentile'
val_col = 'Per 90'

#outputs for player 1
player1 = rcf.get_player_name(url)
tables = rcf.extract_tables_from_url(url)
df = rcf.create_dataframe(tables[2], attributes, col_name)
val1 = rcf.create_dataframe(tables[2], attributes, val_col)
data1 = rcf.df_to_list(df)
data_labels1 = rcf.df_to_list(val1)

#outputs for player 2
player2 = rcf.get_player_name(url2)
tables2 = rcf.extract_tables_from_url(url2)
df2 = rcf.create_dataframe(tables2[2], attributes, col_name)
val2 = rcf.create_dataframe(tables2[2], attributes, val_col)
data2 = rcf.df_to_list(df2)
data_labels2 = rcf.df_to_list(val2)

print("start radar chart: ")
rcf.player_radar_chart(player1,data1,player2,data2,attributes,data_labels1,data_labels2,0)

