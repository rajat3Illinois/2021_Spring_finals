"""

This code is developed by Rajat Kumar (rajat3@illinois.edu)


"""

import numpy as np
import pandas as pd


class Team:

    def __init__(self, last_winner):
        self.name = self.name
        self.rank = self.rank
        self.squad_size = self.squad_size
        self.avg_age = self.avg_age
        self.confideration = self.confideration
        self.points = self.points
        self.mean_player_rating = self.mean_player_rating
        self.player_count = self.player_count
        self.lastWinner = last_winner
        self.is_qualified = False

    @property
    def is_qualified(self):
        return self.is_qualified()

    @is_qualified.setter
    def is_qualified(self, value):
        if value in [True, False]:
            self.is_qualified = value

    @staticmethod
    def fetch_team_details(team: pd.DataFrame) -> pd.DataFrame:
        """

        :param team:
        :return:
        """
        team_details = pd.merge(team, team_rankings, left_on='Nation', right_index=True, how='left')
        return Players.team_player_details(team_details)

    @staticmethod
    def qualified_teams(player_team_merged_frame: pd.DataFrame, confideration_count: int):
        """

        :param player_team_merged_frame:
        :param confideration_count:
        :return:
        """

        max_rank = player_team_merged_frame.max()['Rank']
        min_rank = player_team_merged_frame.min()['Rank']
        player_team_merged_frame['Normalize_Rank'] = (max_rank - player_team_merged_frame['Rank']) / \
                                                     (max_rank - min_rank)
        player_team_merged_frame['Above_Median_Count'] = player_team_merged_frame['count'] / 2
        player_team_merged_frame['Above_Median_Count'] = player_team_merged_frame['Above_Median_Count'].astype("int32")
        teams_qualified = player_team_merged_frame.loc[(player_team_merged_frame['Normalize_Rank'].gt(0.4)) &
                                                  ((player_team_merged_frame['Squad_Size'] * 1.5) < player_team_merged_frame[
                                                      'Above_Median_Count'])]
        player_team_merged_frame['Total Value'] = player_team_merged_frame['Total Value'].replace({'\$': ''}, regex=True)
        player_team_merged_frame['Total Value'] = player_team_merged_frame['Total Value'].replace({'m': ''}, regex=True)

        player_team_merged_frame['Total Value'] = player_team_merged_frame['Total Value'].astype(float)
        different_teams_qualified = player_team_merged_frame.loc[(player_team_merged_frame['Normalize_Rank'].gt(0.4)) &
                                                                 (player_team_merged_frame['Total Value'].gt(150))]
        different_values = different_teams_qualified[~different_teams_qualified.isin(teams_qualified)].dropna()
        frames = [teams_qualified, different_values]
        final_result = pd.concat(frames)
        pick_random_teams = final_result.sample(n=confideration_count).reset_index()
        qualified_teams.append(pick_random_teams['Nation'].tolist())


class Players:

    @staticmethod
    def team_player_details(details: pd.DataFrame) -> pd.DataFrame:
        """
        It details the team and its player.

        :param details:
        :return:
        """
        grouped_players_df = players_df.groupby('nationality')['overall'].agg(['mean', 'count'])
        team_player_details = pd.merge(details, grouped_players_df, left_on='Nation', right_index=True, how='left').fillna(0)
        return team_player_details


class MatchResult:

    def __init__(self, winning_chance):
        self.chance = winning_chance


if __name__ == '__main__':

    qualified_teams = []
    confideration = {'CAF': 5, 'AFC': 5, 'UEFA': 13, 'CONMEBOL': 5, 'CONCACAF': 4, 'OFC': 1}
    team_rankings = pd.read_csv("Latest_Rankings.csv", index_col='Nation')
    africa_teams = pd.read_csv("AFC.csv")
    players_df = pd.read_csv("players_20.csv", index_col="sofifa_id")
    Team.qualified_teams(Team.fetch_team_details(africa_teams), confideration['CAF'])
    print(qualified_teams)

    asia_teams = pd.read_csv("Asia.csv")
    Team.qualified_teams(Team.fetch_team_details(asia_teams), confideration['AFC'])
    print(qualified_teams)
    North_America_teams = pd.read_csv("North_America.csv")
    Team.qualified_teams(Team.fetch_team_details(North_America_teams), confideration['CONCACAF'])
    print(qualified_teams)
    South_America_teams = pd.read_csv("South_America.csv")
    Oceania_Teams = pd.read_csv("Oceania.csv")
    UEFA_Teams = pd.read_csv("UEFA.csv")
    Past_World_Cup_Winning_Teams = pd.read_csv("Winner.csv", index_col="Year")
    Already_Eliminated_Teams = pd.read_csv("Eliminated_Teams.csv")
