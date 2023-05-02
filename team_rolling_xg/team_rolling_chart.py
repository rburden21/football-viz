import team_roll_func as trf

url1 = 'https://fbref.com/en/squads/361ca564/2020-2021/matchlogs/c9/schedule/Tottenham-Hotspur-Scores-and-Fixtures-Premier-League'
url2 = 'https://fbref.com/en/squads/361ca564/2021-2022/matchlogs/c9/schedule/Tottenham-Hotspur-Scores-and-Fixtures-Premier-League'
url3 = 'https://fbref.com/en/squads/361ca564/2022-2023/matchlogs/c9/schedule/Tottenham-Hotspur-Scores-and-Fixtures-Premier-League'

team_name = trf.get_team_name(url1)
league_name = trf.get_league_name(url1)

tables = trf.extract_tables_from_url(url1)
tables2 = trf.extract_tables_from_url(url2)
tables3 = trf.extract_tables_from_url(url3)

df = trf.lists_to_dfs([tables, tables2, tables3])
df = trf.prepare_df(df)

trf.mpl_style(dark=True)

fig = trf.plt.figure(figsize=(10, 5), dpi = 300)
ax = trf.plt.subplot(111)

line_1 = ax.plot(df.index, df['xga_roll'], label = "xG conceded")
line_2 = ax.plot(df.index, df['xg_roll'], label = "xG created")
ax.set_ylim(0)

# Fill between
ax.fill_between(df.index, df['xg_roll'], df['xga_roll'], where = df['xg_roll'] < df['xga_roll'], interpolate = True, alpha = 0.5, zorder = 3)
ax.fill_between(df.index, df['xg_roll'], df['xga_roll'], where = df['xg_roll'] >= df['xga_roll'], interpolate = True, alpha = 0.5, zorder = 3)

# Add a line to mark the division between seasons
min_val_seasons = ax.get_ylim()[0]
max_val_seasons = ax.get_ylim()[1]
ax.plot([38,38],[min_val_seasons, max_val_seasons],ls = ":", lw = 1.5, color = "white", zorder = 2)
ax.plot([72,72],[min_val_seasons, max_val_seasons],ls = ":", lw = 1.5, color = "white", zorder = 2)

# Title and subtitle for the legend
trf.fig_text(x = 0.12, y = 0.98, s = team_name, 
            color = "white", weight = "bold", size = 10, annotationbbox_kw={"xycoords": "figure fraction"})
trf.fig_text(x = 0.12, y = 0.94, s = "Expected goals <created> and <conceded> | 10-match rolling average",
            highlight_textprops = [{"color": line_2[0].get_color(), "weight": "bold"},{"color": line_1[0].get_color(), "weight": "bold"}],
            color = "white", size = 6, annotationbbox_kw={"xycoords": "figure fraction"})
trf.fig_text(x = 0.12, y = 0.92, s = f"{league_name} seasons 20/21, 21/22 and 22/23", 
            color = "white", size = 6, annotationbbox_kw={"xycoords": "figure fraction"})

ax.legend()

trf.plt.show()