import requests
import csv
import sys
import pandas as pd
import numpy as np

# get me all active players

url_allPlayers = ("http://stats.nba.com/stats/commonallplayers?IsOnlyCurrentSeason=0&LeagueID=00&Season=2017-18")
seasons = ['2000-01','2001-02','2002-03','2003-04','2004-05','2005-06','2006-07','2007-08','2008-09','2009-10','2010-11','2011-12','2012-13','2013-14','2014-15','2015-16','2016-17','2017-18']
league_ids = ['00','20']
for league_id in league_ids:
	for season in seasons:
		players_stats_url = f'https://stats.nba.com/stats/leaguedashplayerstats/?measureType=Base&perMode=PerGame&plusMinus=N&paceAdjust=N&rank=N&leagueId={league_id}&season={season}&seasonType=Regular+Season&poRound=0&outcome=&location=&month=0&seasonSegment=&dateFrom=&dateTo=&opponentTeamId=0&vsConference=&vsDivision=&conference=&division=&gameSegment=&period=0&shotClockRange=&lastNGames=0&gameScope=Last+10&playerExperience=&playerPosition=&starterBench=&draftYear=&draftPick=&college=&country=&height=&weight='
		response = requests.get(players_stats_url, headers={
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'})
		response.raise_for_status()

		z = pd.DataFrame(np.asarray(response.json()['resultSets'][0]['rowSet']))
		if len(z)>0:
			z.columns = response.json()['resultSets'][0]['headers']
			z.to_csv(f'players_{season}_{league_id}_per36.csv')
#request url and parse the JSON


players = response.json()['resultSets'][0]['rowSet']

# use roster status flag to check if player is still actively playing
active_players = [players[i] for i in range(0,len(players)) if players[i][3]==1 ]
ids_names = {}
for i in range(0,len(active_players)):
	ids_names[active_players[i][0]] = active_players[i][2]

print("Number of Active Players: " + str(len(ids_names)))

name_height_pos = []
players_df = pd.DataFrame()
for i in ids_names.keys():
	print(i)
	url_onePlayer = ("https://stats.nba.com/stats/leaguedashplayerstats/?measureType=Base&perMode=PerGame&plusMinus=N&paceAdjust=N&rank=N&leagueId=00&season=2017-18&seasonType=Regular+Season&poRound=0&outcome=&location=&month=0&seasonSegment=&dateFrom=&dateTo=&opponentTeamId=0&vsConference=&vsDivision=&conference=&division=&gameSegment=&period=0&shotClockRange=&lastNGames=0&gameScope=Last+10&playerExperience=&playerPosition=&starterBench=&draftYear=&draftPick=&college=&country=&height=&weight=")
	# url_onePlayer=("http://stats.nba.com/stats/playerprofilev2/?leagueId=20&playerId=" + str(i) + "&perMode=PerGame")
	#request url and parse the JSON
	response = requests.get(url_onePlayer, headers= {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"})
	response.raise_for_status()
	if len(response.json()['resultSets'][0]['rowSet'])>0:
		stats = response.json()['resultSets'][0]['rowSet'][-1]
		stats = np.append(stats,ids_names[i])
		stats = np.asarray(stats)
		players_df = players_df.append(pd.DataFrame(stats.reshape(1, stats.shape[0])),ignore_index=True)
	#
	# one_player = response.json()['resultSets'][0]['rowSet']
	# stats_player = response.json()['resultSets'][1]['rowSet']
    #
	# try:
	# 	points = stats_player[0][3]
	# 	assists = stats_player[0][4]
	# 	rebounds = stats_player[0][5]
	# 	PIE = stats_player[0][6]
	# # handle the case, where player is active, but didn't play
	# # in any game so far in this season (-1 just a place holder value)
	# except IndexError:
	# 	points = -1
	# 	assists = -1
	# 	rebounds = -1
	# 	PIE = -1
    #
	# name_height_pos.append([one_player[0][1] + " " + one_player[0][2],
	# 	one_player[0][10],
	# 	one_player[0][14],
	# 	one_player[0][18],
	# 	"http://i.cdn.turner.com/nba/nba/.element/img/2.0/sect/statscube/players/large/"+one_player[0][1].lower()+"_"+ one_player[0][2].lower() +".png",
	# 	points,
	# 	assists,
	# 	rebounds,
	# 	PIE])

#convert from inches to cm
df_headers = response.json()['resultSets'][0]['headers']
df_headers.append('NAME')
players_df.columns = df_headers
players_df = players_df.set_index(players_df['PLAYER_ID'])
players_df = players_df.drop('PLAYER_ID',axis=1)
for i in range(0,len(name_height_pos)):
	feet = name_height_pos[i][1][0]
	inches = name_height_pos[i][1][2:]

	result = (float(feet) * 12 + float(inches)) * 2.54;
	name_height_pos[i][1] = result



answer = input("Save as player.csv -- y/n\t")
if answer[0] == "n":
	sys.exit()
elif answer[0] != "y":
	sys.exit()
else:

	with open("player.csv", "w") as csvfile:
		writer = csv.writer(csvfile, delimiter=",", lineterminator="\n")
		writer.writerow(["Name","Height","Pos","Team","img_Link","PTS","AST","REB","PIE"])
		for row in name_height_pos:
			writer.writerow(row)
		print("Saved as \'player.csv\'")