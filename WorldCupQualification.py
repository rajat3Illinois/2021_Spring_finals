"""

This code is developed by Rajat Kumar (rajat3@illinois.edu)
The detailed description is present in the readme file. The project belongs to the category of Type 3 analysis.
Change the simulations in the main part of python. Currently, it is set as 50.
Make sure all the data sets file are in the same directory as this python file


"""

import pandas as pd
import random


def remove_regex_from_total_value(team_merged_frame: pd.DataFrame) -> pd.DataFrame:
    """
    It converts the total value depicting the dollars amount from str to float, by removing the characters
    $, m, bn and Th.
    :param team_merged_frame:
    :return:
    """
    team_merged_frame['Total Value'] = team_merged_frame['Total Value'].replace({'\$': ''}, regex=True)
    team_merged_frame['Total Value'] = team_merged_frame['Total Value'].replace({'m': ''}, regex=True)
    team_merged_frame['Total Value'] = team_merged_frame['Total Value'].replace({'bn': ''}, regex=True)
    team_merged_frame['Total Value'] = team_merged_frame['Total Value'].replace({'Th': ''}, regex=True)
    team_merged_frame['Total Value'] = team_merged_frame['Total Value'].astype(float)
    return team_merged_frame


def host_nation_df(host: str) -> pd.DataFrame:
    """
    This provides the details of the host nation that is Qatar right now.
    :param host:
    :return:
    """
    overall_rankings = pd.read_csv("Latest_Rankings.csv")
    grouped_players_df = players_df.groupby('nationality')['overall'].agg(['median', 'count'])
    host_nation = overall_rankings[overall_rankings['Nation'] == host]
    host_team_details = pd.merge(host_nation, grouped_players_df, left_on='Nation', right_index=True,
                                 how='left').fillna(0)
    host_team_details['Normalize_Rank'] = 0
    host_team_details['Above_Median_Count'] = 0
    return host_team_details


def world_cup_qualified_teams(player_team_merged_frame: pd.DataFrame, confideration_type: str) -> pd.DataFrame:
    """
    It returns the teams that are likely to qualify for the Fifa World Cup.
    :param player_team_merged_frame:
    :param confideration_type: (Type of confideration like AFC, Asia, North America)
    :return:
    """

    max_rank = player_team_merged_frame.max()['Rank']
    min_rank = player_team_merged_frame.min()['Rank']
    player_team_merged_frame['Normalize_Rank'] = (max_rank - player_team_merged_frame['Rank']) / \
                                                 (max_rank - min_rank)
    player_team_merged_frame['Above_Median_Count'] = player_team_merged_frame['count'] / 2
    player_team_merged_frame['Above_Median_Count'] = player_team_merged_frame['Above_Median_Count'].astype("int32")

    if confideration_type in ["CONCACAF", "OFC"]:
        teams_qualified = player_team_merged_frame.loc[(player_team_merged_frame['Normalize_Rank'].gt(0.3)) &
                                                       ((player_team_merged_frame['Squad_Size'] * 0.5) <
                                                        player_team_merged_frame['Above_Median_Count'])]
        remove_regex_from_total_value(player_team_merged_frame)
        different_teams_qualified = player_team_merged_frame.loc[(player_team_merged_frame['Normalize_Rank'].
                                                                  gt(0.3)) &
                                                                 (player_team_merged_frame['Total Value'].gt(100))]

    elif confideration_type == "UEFA":
        remove_regex_from_total_value(player_team_merged_frame)
        higher_team_correct = player_team_merged_frame[player_team_merged_frame['Pots'].isin([1])
                                                       & player_team_merged_frame['Normalize_Rank'].gt(0.4) &
                                                       ((player_team_merged_frame['Squad_Size'] * 1.5) <
                                                        player_team_merged_frame['Above_Median_Count']) &
                                                       (player_team_merged_frame['Total Value'].gt(150))]

        higher_team_missing = player_team_merged_frame[player_team_merged_frame['Pots'].isin([1])
                                                       & player_team_merged_frame['Normalize_Rank'].gt(0.4) &
                                                       ((player_team_merged_frame['Squad_Size'] * 1.5) <
                                                        player_team_merged_frame['Above_Median_Count']) &
                                                       (player_team_merged_frame['Total Value'].lt(1.5))]
        higher_frames = [higher_team_correct, higher_team_missing]
        teams_qualified = pd.concat(higher_frames)

        different_teams_qualified = player_team_merged_frame[player_team_merged_frame['Pots'].isin([2])
                                                             & player_team_merged_frame['Normalize_Rank'].gt(0.4) &
                                                             ((player_team_merged_frame['Squad_Size'] * 1.5) <
                                                              player_team_merged_frame['Above_Median_Count']) &
                                                             (player_team_merged_frame['Total Value'].gt(150))]

    else:
        teams_qualified = player_team_merged_frame.loc[(player_team_merged_frame['Normalize_Rank'].gt(0.4)) &
                                                       ((player_team_merged_frame['Squad_Size'] * 1.5) <
                                                        player_team_merged_frame['Above_Median_Count'])]
        remove_regex_from_total_value(player_team_merged_frame)

        if confideration_type == 'CAF':
            different_teams_qualified = player_team_merged_frame.loc[(player_team_merged_frame['Normalize_Rank'].
                                                                      gt(0.4)) &
                                                                     (player_team_merged_frame['Total Value'].gt(35))]
        else:
            different_teams_qualified = player_team_merged_frame.loc[(player_team_merged_frame['Normalize_Rank'].
                                                                      gt(0.4)) &
                                                                     (player_team_merged_frame['Total Value'].
                                                                      gt(150))]

    different_values = different_teams_qualified[~different_teams_qualified.isin(teams_qualified)].dropna()
    frames = [teams_qualified, different_values]
    final_result = pd.concat(frames)
    pick_random_teams = final_result.sample(n=confideration[confideration_type]).reset_index()
    return pick_random_teams


def fetch_team_details(team: pd.DataFrame) -> pd.DataFrame:
    """
    It merges the particular confideration (like AFC, Asia) team dataframe with the Latest Rankings dataframe.
    :param team:
    :return:
    """
    team_details = pd.merge(team, team_rankings, left_on='Nation', right_index=True, how='left')
    return team_player_details(team_details)


def team_player_details(details: pd.DataFrame) -> pd.DataFrame:
    """
    It provides the player statistics belonging to the qualifying team as per the players_20 data file.

    :param details:
    :return:
    """
    grouped_players_df = players_df.groupby('nationality')['overall'].agg(['mean', 'count'])
    team_player_details = pd.merge(details, grouped_players_df, left_on='Nation',
                                   right_index=True, how='left').fillna(0)
    return team_player_details


def qualifying_team_attack_def_stats(officially_qualified_teams: pd.DataFrame, players_details_df: pd.DataFrame) -> pd.DataFrame:
    """
    It computes the qualifying team attack stats based on the LW,RW,ST,CAM players in the players_20.csv file.
    It also computes the qualifying team defence stats based on CDM, CB
    :param officially_qualified_teams:
    :param players_details_df:
    :return:
    """
    final_grouped_players_df = players_details_df.loc[players_details_df.team_position == 'RW'].groupby('nationality')['overall'].agg(['mean'])
    final_grouped_players_df['LW'] = players_details_df.loc[players_details_df.team_position == 'LW'].groupby('nationality')['overall'].agg(['mean'])
    final_grouped_players_df['LW'] = final_grouped_players_df['LW'].fillna(0)
    final_grouped_players_df['ST'] = players_details_df.loc[players_details_df.team_position == 'ST'].groupby('nationality')['overall'].agg(['mean'])
    final_grouped_players_df['ST'] = final_grouped_players_df['ST'].fillna(0)
    final_grouped_players_df['CAM'] = players_details_df.loc[players_details_df.team_position == 'CAM'].groupby('nationality')['overall'].agg(['mean'])
    final_grouped_players_df['CAM'] = final_grouped_players_df['CAM'].fillna(0)
    final_grouped_players_df['CDM'] = players_details_df.loc[players_details_df.team_position == 'CDM'].groupby('nationality')['overall'].agg(['mean'])
    final_grouped_players_df['CDM'] = final_grouped_players_df['CDM'].fillna(0)
    final_grouped_players_df['CB'] = players_details_df.loc[players_details_df.team_position == 'CB'].groupby('nationality')['overall'].agg(['mean'])
    final_grouped_players_df['CB'] = final_grouped_players_df['CB'].fillna(0)
    final_grouped_players_df['GK'] = players_df.loc[players_df.team_position == 'GK'].groupby('nationality')['overall'].agg(['mean'])
    final_grouped_players_df['GK'] = final_grouped_players_df['GK'].fillna(0)
    final_grouped_players_df['Attacking_Prowess'] = (final_grouped_players_df['mean'] + final_grouped_players_df['LW'] +
                                                     final_grouped_players_df['ST'] + final_grouped_players_df[
                                                         'CAM']) / 4
    final_grouped_players_df['Defensive_Prowess'] = (final_grouped_players_df['CDM'] + final_grouped_players_df[
        'CB']) / 2

    officially_qualified_teams = pd.merge(officially_qualified_teams, final_grouped_players_df, left_on='Nation',
                                          right_index=True, how='left').fillna(0)
    return officially_qualified_teams


class WorldCupTeam:

    world_cup_team_stats_list = []

    def __init__(self, team_details_df, team_count):
        self.count = 0
        self.Name = team_details_df['Nation']
        self.Rank = team_details_df['Rank']
        self.Attacking_Strength = team_details_df['Attacking_Prowess']
        self.Defensive_Strength = team_details_df['Defensive_Prowess']
        self.Goalkeeper_Strength = team_details_df['GK']
        if self.Name == 'France':
            self.last_winner = True
        else:
            self.last_winner = False

        if team_count <= 7:
            self.pot = 1
        elif 7 < team_count <= 15:
            self.pot = 2
        elif 15 < team_count <= 23:
            self.pot = 3
        else:
            self.pot = 4

        if self.Name == 'Qatar':
            self.pot = 1
            self.Attacking_Strength = random.randint(60, 65)
            self.Defensive_Strength = random.randint(62, 67)

        WorldCupTeam.world_cup_team_stats_list.append(self)

    @staticmethod
    def create_team_instances(team_details_df):
        """
        It creates the team object instances for all the qualifying teams.
        :param team_details_df:
        :return:
        """

        if len(WorldCupTeam.world_cup_team_stats_list) > 0:
            WorldCupTeam.world_cup_team_stats_list.clear()

        sorted_team_details_df = team_details_df.sort_values(by=['Rank'])
        # sorted_team_details_df = sorted_team_details_df.set_index('Nation')
        team_count = 1
        for index, row in sorted_team_details_df.iterrows():
            WorldCupTeam(row, team_count)
            team_count += 1


# Below code is yet to be implemented.
class MatchResult:

    def __init__(self, winning_chance):
        self.chance = winning_chance


def fetch_details_for_simulating_groups() -> pd.DataFrame:
    """
    It is main function that returns all the qualifying teams along with its statistics of attacking prowess,
    defensive prowess, rank and confideration.
    :return:
    """

    africa_teams = pd.read_csv("AFC.csv")
    afc_team_data = world_cup_qualified_teams(fetch_team_details(africa_teams), "AFC")

    asia_teams = pd.read_csv("Asia.csv")
    asia_team_data = world_cup_qualified_teams(fetch_team_details(asia_teams), "CAF")

    north_america_teams = pd.read_csv("North_America.csv")
    north_america_team_data = world_cup_qualified_teams(fetch_team_details(north_america_teams), "CONCACAF")

    south_america_teams = pd.read_csv("South_America.csv")
    south_america_team_data = world_cup_qualified_teams(fetch_team_details(south_america_teams), "CONMEBOL")

    oceania_teams = pd.read_csv("Oceania.csv")
    oceania_team_data = world_cup_qualified_teams(fetch_team_details(oceania_teams), "OFC")

    europe_teams = pd.read_csv("UEFA.csv")
    uefa_team_data = world_cup_qualified_teams(fetch_team_details(europe_teams), "UEFA")

    host_team_data = host_nation_df(host_nation_country)

    qualified_frames = [afc_team_data, asia_team_data, north_america_team_data,
                        south_america_team_data, oceania_team_data,
                        uefa_team_data, host_team_data]
    world_cup_team_data = pd.concat(qualified_frames)
    world_cup_team_stats = qualifying_team_attack_def_stats(world_cup_team_data, players_df)
    return world_cup_team_stats


def simulate_groups(simulations: int):
    """
    This is main simulation function that assigns the groups to its appropriate pots and then randomly
    assign each team to the group.
    :param simulations:
    :return:
    """
    winner_count = 0

    for i in range(simulations):
        pot1 = []
        pot2 = []
        pot3 = []
        pot4 = []

        groupA = []
        groupB = []
        groupC = []
        groupD = []
        groupE = []
        groupF = []
        groupG = []
        groupH = []
        Groups = [groupA, groupB, groupC, groupD, groupE, groupF, groupG, groupH]

        WorldCupTeam.create_team_instances(fetch_details_for_simulating_groups())
        teams_list = WorldCupTeam.world_cup_team_stats_list

        for each_team in teams_list:
            if each_team.pot == 1:
                # noinspection PyUnresolvedReferences
                pot1.append(each_team)
            elif each_team.pot == 2:
                # noinspection PyUnresolvedReferences
                pot2.append(each_team)
            elif each_team.pot == 3:
                # noinspection PyUnresolvedReferences
                pot3.append(each_team)
            else:
                # noinspection PyUnresolvedReferences
                pot4.append(each_team)

        random.shuffle(Groups)

        random.shuffle(pot1)
        for each_group in Groups:
            for each_team in pot1:
                each_group.append(each_team)
                if each_team.last_winner is True:
                    winner_count += 1
                pot1.remove(each_team)
                break

        random.shuffle(pot2)
        for each_group in Groups:
            for each_team in pot2:
                each_group.append(each_team)
                pot2.remove(each_team)
                break

        random.shuffle(pot3)
        for each_group in Groups:
            for each_team in pot3:
                each_group.append(each_team)
                pot3.remove(each_team)
                break

        random.shuffle(pot4)
        for each_group in Groups:
            for each_team in pot4:
                each_group.append(each_team)
                pot4.remove(each_team)
                break

        print("\n Group A")
        for each_team in groupA:
            print(each_team.Name)

        print("\n Group B")
        for each_team in groupB:
            print(each_team.Name)

        print("\n Group C")
        for each_team in groupC:
            print(each_team.Name)

        print("\n Group D")
        for each_team in groupD:
            print(each_team.Name)

        print("\n Group E")
        for each_team in groupE:
            print(each_team.Name)

        print("\n Group F")
        for each_team in groupF:
            print(each_team.Name)

        print("\n Group G")
        for each_team in groupG:
            print(each_team.Name)

        print("\n Group H")
        for each_team in groupH:
            print(each_team.Name)

    print("Success Ratio of Last Winner (that is France) is {}".format(winner_count/simulations * 100))


if __name__ == '__main__':

    qualified_teams = []
    host_nation_country = 'Qatar'
    confideration = {'CAF': 4, 'AFC': 4, 'UEFA': 13, 'CONMEBOL': 5, 'CONCACAF': 4, 'OFC': 1}
    players_df = pd.read_csv("players_20.csv", index_col="sofifa_id")
    team_rankings = pd.read_csv("Latest_Rankings.csv", index_col='Nation')

    simulate_groups(50)
