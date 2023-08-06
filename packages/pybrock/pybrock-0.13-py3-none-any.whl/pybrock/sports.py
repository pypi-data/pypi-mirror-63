import pandas as pd
import json
import requests

def nhl_games(season=201920):
  # build the url for Nice time on Ice API
  URL = 'http://www.nicetimeonice.com/api/seasons/{}/games'
  url = URL.format(season)
  # get the games
  games = requests.get(url).json()
  # put into a dataframe
  df = pd.DataFrame(games)
  df.columns = df.columns.str.lower()
  # return
  return(df)

def nhl_parse_pbp(gid='2019020010'):
  # parse a json file from the NHL stats pbp files
  URL = 'http://statsapi.web.nhl.com/api/v1/game/{}/feed/live'
  url = URL.format(gid)
  # get the data
  pbp = requests.get(url).json()
  # filter out some data
  plays = pbp['liveData']['plays']['allPlays']
  # the container
  df = pd.DataFrame()
  # iterate over each entry
  for i, play in enumerate(plays):
    # setup the dataframe row for the event
    pbp = pd.DataFrame({'gid':[gid]})
    
    # ------- result 
    test = 'result'
    if test in play.keys():
      tmp = play[test]
      r = pd.DataFrame([tmp])
      r.columns = test + "_" + r.columns
      r.columns = r.columns.str.lower()
      pbp = pd.concat([pbp, r], axis=1)
      del r
    
    #  ------- coordinates
    test = 'coordinates'
    if test in play.keys():
      tmp = play[test]
      # ensure that there are data
      if len(tmp) > 0:
        c = pd.DataFrame([tmp])
        c.columns = "coords_" + c.columns
        c.columns = c.columns.str.lower()
        pbp = pd.concat([pbp, c], axis=1)
        del c
    
    #  ------- team
    test = 'team'
    if test in play.keys():
      tmp = play[test]
      t = pd.DataFrame([tmp])
      t.columns = test + "_" + t.columns
      t.columns = t.columns.str.lower()
      pbp = pd.concat([pbp, t], axis=1)
      del t
    
    #  ------- players
    test = 'players'
    if test in play.keys():
      tmp = play[test]
      players_df = pd.DataFrame()
      for i, p in enumerate(tmp):
        tmp_p = p['player']
        tmp_pdf = pd.DataFrame([tmp_p])
        tmp_pdf.columns = "player{}_".format(i+1) + tmp_pdf.columns
        tmp_pdf.columns = tmp_pdf.columns.str.lower()
        players_df = pd.concat([players_df, tmp_pdf], axis=1)
      # append the data
      pbp = pd.concat([pbp, players_df], axis=1)
    
    #  ------- about
    test = 'about'
    if test in play.keys():
      tmp = play[test]
      # extract the goals - we want 1 row worth
      goals = pd.DataFrame.from_dict([tmp['goals']])
      goals.columns = "goals_" + goals.columns
      del tmp['goals']
      # the about data
      a = pd.DataFrame([tmp])
      a.columns = test + "_" + a.columns
      a.columns = a.columns.str.lower()
      # combine
      a = pd.concat([a, goals], axis=1)
      pbp = pd.concat([pbp, a], axis=1)
      # remove
      del a
      del goals
    
    # bind to the pbp
    df = df.append(pbp, ignore_index=True)
    
  # return the data
  return(df)



      




