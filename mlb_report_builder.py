import pandas as pd
import requests
from pandas import DataFrame
import numpy as np


class MlbReport:
    def __init__(self, team):
        """ Used just to find game with team playing. """
        self.home = team
        self.away = team

    def get_game_id(self):
        """ Returns game_id (gamePK) given team name. """
        team_name = self.home
        mlb_report = MlbReport(team_name)
        endpoint = "http://statsapi.mlb.com/api/v1/schedule/games/?sportId=1"
        response = mlb_report.get_data(endpoint)
        response = response['dates']
        response = response[0]['games']
        for i in range(0, len(response)):
            away_name = response[i]['teams']['away']['team']['name']
            home_name = response[i]['teams']['home']['team']['name']
            if((team_name == away_name) | (team_name == home_name)):
                self.home = home_name
                self.away = away_name
                return response[i]['gamePk']
                break

    def get_game_score_response(self, gameID):
        """ Returns game's score for given game_id. """
        mlb_report = MlbReport('')
        endpoint = f"http://statsapi.mlb.com//api/v1/game/{gameID}/linescore"
        response = mlb_report.get_data(endpoint)
        return response

    def parse_dataframe(self, dataframe):
        """ """
        dataframe['Home'] = self.home
        dataframe['Away'] = self.away
        try:
            home_score = dataframe['teams'][0]['home']['runs']
        except:
            print('Team is not currently playing.')
            exit()
        try:
            away_score = dataframe['teams'][0]['away']['runs']
        except:
            print('Team is not currently playing.')
            exit()
        dataframe['RunsH'] = home_score
        dataframe['RunsA'] = away_score
        dataframe_parsed = dataframe[['Home', 'RunsH', 'Away', 'RunsA', 'currentInning', 'strikes', 'balls']].rename(
                columns={'RunsH': '', 'RunsA': '', 'currentInning': 'Inning', 'strikes':'strikes', 'balls':'Balls'})
        return dataframe_parsed

    @staticmethod
    def get_data(endpoint):
        """ Performs get request for parametrized endpoint. """
        response = requests.get(endpoint).json()
        return response

    def create_report(self):
        mlb_report = MlbReport(self.home)
        game_id = mlb_report.get_game_id()
        response = mlb_report.get_game_score_response(game_id)
        dataframe = DataFrame([response])
        formatted_dataframe = mlb_report.parse_dataframe(dataframe)
        return formatted_dataframe

if __name__ == '__main__':
    # input team names in 'teams' i.e. "New York Yankees"
    teams = ["New York Yankees"]
    box_scores = []
    for i in range(0, len(teams)):
        mlb_report = MlbReport(teams[i])
        box_scores.append(mlb_report.create_report())

    dataframe = pd.concat(box_scores, ignore_index=True)

    # doubles spaces report
    df = dataframe
    blank = np.where(np.empty_like(df.values), '', '')
    data = np.hstack([df.values, blank]).reshape(-1, df.shape[1])
    df_with_spaces = pd.DataFrame(data, columns=df.columns)
    df_double_spaced = df_with_spaces[::-1]

    df_double_spaced.to_excel('mlbreport.xlsx', index=False, freeze_panes=(1, 0))
