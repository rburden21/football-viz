import radar_chart_func as rcf


#need to improve visualisation
#need to work out how to change colour of 20/40/60/80/100

#variables
url = 'https://fbref.com/en/players/1f44ac21/scout/11566/Erling-Haaland-Scouting-Report'
url2 = 'https://fbref.com/en/players/21a66f6a/scout/11566/Harry-Kane-Scouting-Report'

#attributes = ['Goals','xG', 'Assists','xAG', 'Shots Total','Shots on target %','Average Shot Distance','Progressive Passes Rec']
attributes = ['Non-Penalty Goals','Non-Penalty xG','Shots Total','Assists','xAG','npxG + xAG',
                'Shot-Creating Actions','Progressive Passes']

#outputs for player 1
player1 = rcf.get_player_name(url)
tables = rcf.extract_tables_from_url(url)
df = rcf.create_dataframe(tables[2], attributes)
data1 = rcf.df_to_list(df)

#outputs for player 2
player2 = rcf.get_player_name(url2)
tables2 = rcf.extract_tables_from_url(url2)
df2 = rcf.create_dataframe(tables2[2], attributes)
data2 = rcf.df_to_list(df2)

rcf.player_radar_chart(player1,data1,player2,data2,attributes)

