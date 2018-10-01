import requests
import csv
import sys
import pandas as pd
import numpy as np

# get me all active players
all_teams = [
  {
    "teamId": 1610612737,
    "abbreviation": "ATL",
    "teamName": "Atlanta Hawks",
    "simpleName": "Hawks",
    "location": "Atlanta"
  },
  {
    "teamId": 1610612738,
    "abbreviation": "BOS",
    "teamName": "Boston Celtics",
    "simpleName": "Celtics",
    "location": "Boston"
  },
  {
    "teamId": 1610612751,
    "abbreviation": "BKN",
    "teamName": "Brooklyn Nets",
    "simpleName": "Nets",
    "location": "Brooklyn"
  },
  {
    "teamId": 1610612766,
    "abbreviation": "CHA",
    "teamName": "Charlotte Hornets",
    "simpleName": "Hornets",
    "location": "Charlotte"
  },
  {
    "teamId": 1610612741,
    "abbreviation": "CHI",
    "teamName": "Chicago Bulls",
    "simpleName": "Bulls",
    "location": "Chicago"
  },
  {
    "teamId": 1610612739,
    "abbreviation": "CLE",
    "teamName": "Cleveland Cavaliers",
    "simpleName": "Cavaliers",
    "location": "Cleveland"
  },
  {
    "teamId": 1610612742,
    "abbreviation": "DAL",
    "teamName": "Dallas Mavericks",
    "simpleName": "Mavericks",
    "location": "Dallas"
  },
  {
    "teamId": 1610612743,
    "abbreviation": "DEN",
    "teamName": "Denver Nuggets",
    "simpleName": "Nuggets",
    "location": "Denver"
  },
  {
    "teamId": 1610612765,
    "abbreviation": "DET",
    "teamName": "Detroit Pistons",
    "simpleName": "Pistons",
    "location": "Detroit"
  },
  {
    "teamId": 1610612744,
    "abbreviation": "GSW",
    "teamName": "Golden State Warriors",
    "simpleName": "Warriors",
    "location": "Golden State"
  },
  {
    "teamId": 1610612745,
    "abbreviation": "HOU",
    "teamName": "Houston Rockets",
    "simpleName": "Rockets",
    "location": "Houston"
  },
  {
    "teamId": 1610612754,
    "abbreviation": "IND",
    "teamName": "Indiana Pacers",
    "simpleName": "Pacers",
    "location": "Indiana"
  },
  {
    "teamId": 1610612746,
    "abbreviation": "LAC",
    "teamName": "Los Angeles Clippers",
    "simpleName": "Clippers",
    "location": "Los Angeles"
  },
  {
    "teamId": 1610612747,
    "abbreviation": "LAL",
    "teamName": "Los Angeles Lakers",
    "simpleName": "Lakers",
    "location": "Los Angeles"
  },
  {
    "teamId": 1610612763,
    "abbreviation": "MEM",
    "teamName": "Memphis Grizzlies",
    "simpleName": "Grizzlies",
    "location": "Memphis"
  },
  {
    "teamId": 1610612748,
    "abbreviation": "MIA",
    "teamName": "Miami Heat",
    "simpleName": "Heat",
    "location": "Miami"
  },
  {
    "teamId": 1610612749,
    "abbreviation": "MIL",
    "teamName": "Milwaukee Bucks",
    "simpleName": "Bucks",
    "location": "Milwaukee"
  },
  {
    "teamId": 1610612750,
    "abbreviation": "MIN",
    "teamName": "Minnesota Timberwolves",
    "simpleName": "Timberwolves",
    "location": "Minnesota"
  },
  {
    "teamId": 1610612740,
    "abbreviation": "NOP",
    "teamName": "New Orleans Pelicans",
    "simpleName": "Pelicans",
    "location": "New Orleans"
  },
  {
    "teamId": 1610612752,
    "abbreviation": "NYK",
    "teamName": "New York Knicks",
    "simpleName": "Knicks",
    "location": "New York"
  },
  {
    "teamId": 1610612760,
    "abbreviation": "OKC",
    "teamName": "Oklahoma City Thunder",
    "simpleName": "Thunder",
    "location": "Oklahoma City"
  },
  {
    "teamId": 1610612753,
    "abbreviation": "ORL",
    "teamName": "Orlando Magic",
    "simpleName": "Magic",
    "location": "Orlando"
  },
  {
    "teamId": 1610612755,
    "abbreviation": "PHI",
    "teamName": "Philadelphia 76ers",
    "simpleName": "76ers",
    "location": "Philadelphia"
  },
  {
    "teamId": 1610612756,
    "abbreviation": "PHX",
    "teamName": "Phoenix Suns",
    "simpleName": "Suns",
    "location": "Phoenix"
  },
  {
    "teamId": 1610612757,
    "abbreviation": "POR",
    "teamName": "Portland Trail Blazers",
    "simpleName": "Trail Blazers",
    "location": "Portland"
  },
  {
    "teamId": 1610612758,
    "abbreviation": "SAC",
    "teamName": "Sacramento Kings",
    "simpleName": "Kings",
    "location": "Sacramento"
  },
  {
    "teamId": 1610612759,
    "abbreviation": "SAS",
    "teamName": "San Antonio Spurs",
    "simpleName": "Spurs",
    "location": "San Antonio"
  },
  {
    "teamId": 1610612761,
    "abbreviation": "TOR",
    "teamName": "Toronto Raptors",
    "simpleName": "Raptors",
    "location": "Toronto"
  },
  {
    "teamId": 1610612762,
    "abbreviation": "UTA",
    "teamName": "Utah Jazz",
    "simpleName": "Jazz",
    "location": "Utah"
  },
  {
    "teamId": 1610612764,
    "abbreviation": "WAS",
    "teamName": "Washington Wizards",
    "simpleName": "Wizards",
    "location": "Washington"
  }
]

url_all_teams = ("http://stats.nba.com/stats/commonallplayers?IsOnlyCurrentSeason=0&LeagueID=00&Season=2017-18")
seasons = ['2017-18']
league_ids = ['00']
counter = 0
for league_id in league_ids:
	for season in seasons:
            for team in all_teams:
                team_url_stats = f'https://stats.nba.com/stats/leaguegamefinder/?playerOrTeam=T&leagueId={league_id}&season={season}&seasonType=Regular+Season&teamId={team["teamId"]}&vsTeamId=&playerId=&outcome=&location=&dateFrom=&dateTo=&vsConference=&vsDivision=&conference=&division=&seasonSegment=&poRound=0&starterBench=&gtPts=&gtReb=&gtAst=&gtStl=&gtBlk=&gtOReb=&gtDReb=&gtDD=&gtTD=&gtMinutes=&gtTov=&gtPF=&gtFGM=&gtFGA=&gtFG_Pct=&gtFTM=&gtFTA=&gtFT_Pct=&gtFG3M=&gtFG3A=&gtFG3_Pct=&ltPts=&ltReb=&ltAst=&ltStl=&ltBlk=&ltOReb=&ltDReb=&ltDD=&ltTD=&ltMinutes=&ltTov=&ltPF=&ltFGM=&ltFGA=&ltFG_Pct=&ltFTM=&ltFTA=&ltFT_Pct=&ltFG3M=&ltFG3A=&ltFG3_Pct=&eqPts=&eqReb=&eqAst=&eqStl=&eqBlk=&eqOReb=&eqDReb=&eqDD=&eqTD=&eqMinutes=&eqTov=&eqPF=&eqFGM=&eqFGA=&eqFG_Pct=&eqFTM=&eqFTA=&eqFT_Pct=&eqFG3M=&eqFG3A=&eqFG3_Pct='
                response = requests.get(team_url_stats, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'})
                response.raise_for_status()
                if counter ==0:

                    team_game_df = pd.DataFrame(np.asarray(response.json()['resultSets'][0]['rowSet']))
                    team_game_df.columns = np.asarray(response.json()['resultSets'][0]['headers'])
                    counter=1
                else:
                    z=pd.DataFrame(np.asarray(response.json()['resultSets'][0]['rowSet']))
                    z.columns = np.asarray(response.json()['resultSets'][0]['headers'])
                    team_game_df = team_game_df.append(z,ignore_index=True)

game_ids = team_game_df['GAME_ID']
counter = 0
for game_id in game_ids:
    game_box_score_url = f'https://stats.nba.com/stats/boxscoretraditionalv2/?gameId={game_id}&startPeriod=0&endPeriod=14&startRange=0&endRange=2147483647&rangeType=0'
    response = requests.get(game_box_score_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'})
    response.raise_for_status()
    if counter == 0:
        game_box_score_df = pd.DataFrame(np.asarray(response.json()['resultSets'][0]['rowSet']))
        game_box_score_df.columns = np.asarray(response.json()['resultSets'][0]['headers'])
        counter += 1
        print(counter)
    else:
        counter= counter+1
        z = pd.DataFrame(np.asarray(response.json()['resultSets'][0]['rowSet']))
        z.columns = np.asarray(response.json()['resultSets'][0]['headers'])
        game_box_score_df = game_box_score_df.append(z, ignore_index=True)

team_game_df.to_csv('team_stats.csv')

game_box_score_df.to_csv('box_score_stats.csv')