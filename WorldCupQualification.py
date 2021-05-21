"""

This code is developed taking into account the previous developed code of Spring 2018 batch Fifa World Cup
Simulation and the necessary source code provided in the readme file.

The code is referenced from the links provided in readme file.

The detailed description is present in the readme file. The project belongs to the category of Type 3 analysis.

Change the simulations in the main part of python. Currently, it is set as 100.
Make sure all the data sets file are in the same directory as this python file.
The comments for the better understanding are added in the code.
Go through the presentation as well for a better understanding of what this code is likely to do.


"""

import pandas as pd
import numpy as np
import random
import itertools


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


def host_nation_df(host: str, players_dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    This provides the details of the host nation that is Qatar right now.
    :param host:
    :param players_dataframe:
    :return:
    >>> players_df = pd.read_csv("players_20.csv", index_col="sofifa_id")
    >>> host_nation_country = 'Qatar'
    >>> host_nation_df(host_nation_country, players_df)
        Rank Nation  Squad_Size  ...  count Normalize_Rank Above_Median_Count
    57    58  Qatar          23  ...    0.0              0                  0
    <BLANKLINE>
    [1 rows x 11 columns]
    """
    overall_rankings = pd.read_csv("Latest_Rankings.csv")
    grouped_players_df = players_dataframe.groupby('nationality')['overall'].agg(['median', 'count'])
    host_nation = overall_rankings[overall_rankings['Nation'] == host]
    host_team_details = pd.merge(host_nation, grouped_players_df, left_on='Nation', right_index=True,
                                 how='left').fillna(0)
    host_team_details['Normalize_Rank'] = 0
    host_team_details['Above_Median_Count'] = 0
    return host_team_details


def world_cup_qualified_teams(player_team_merged_frame: pd.DataFrame, confideration_type: str) -> pd.DataFrame:
    """
    It returns the teams that are likely to qualify for the Fifa World Cup from each confideration.
    :param player_team_merged_frame:
    :param confideration_type: (Type of confideration like AFC, Asia, North America)
    :return:
    """

    max_rank = player_team_merged_frame['Rank'].max()
    min_rank = player_team_merged_frame['Rank'].min()
    # Rank is normalized as per the confideration.
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
    It merges the particular confideration (like AFC, Asia) team dataframe with the Latest Team Rankings dataframe.
    :param team:
    :return:
    >>> team_rankings = pd.read_csv("Latest_Rankings.csv", index_col='Nation')
    >>> africa_teams = pd.read_csv("AFC.csv")
    >>> team_details = pd.merge(africa_teams, team_rankings, left_on='Nation', right_index=True, how='left')
    """
    team_details = pd.merge(team, team_rankings, left_on='Nation', right_index=True, how='left')
    return team_player_details(team_details)


def team_player_details(details: pd.DataFrame) -> pd.DataFrame:
    """
    It provides the player statistics belonging to the qualifying team as per the players_20 data file i.e. players_df dataframe.

    :param details:
    :return
    >>> players_df = pd.read_csv("players_20.csv", index_col="sofifa_id")
    >>> grouped_players_df = players_df.groupby('nationality')['overall'].agg(['mean', 'count'])
    >>> team_rankings = pd.read_csv("Latest_Rankings.csv", index_col='Nation')
    >>> africa_teams = pd.read_csv("AFC.csv")
    >>> team_details = pd.merge(africa_teams, team_rankings, left_on='Nation', right_index=True, how='left')
    >>> team_player_details = pd.merge(team_details, grouped_players_df, left_on='Nation', right_index=True, how='left').fillna(0)
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
    players_details_df.loc[players_details_df['player_positions'].str.contains('ST', regex=False), 'player_positions'] = 'A'
    players_details_df.loc[players_details_df['player_positions'].str.contains('LW', regex=False), 'player_positions'] = 'A'
    players_details_df.loc[players_details_df['player_positions'].str.contains('RW', regex=False), 'player_positions'] = 'A'
    players_details_df.loc[players_details_df['player_positions'].str.contains('CAM', regex=False), 'player_positions'] = 'A'
    players_details_df.loc[players_details_df['player_positions'].str.contains('CM', regex=False), 'player_positions'] = 'A'
    players_details_df.loc[players_details_df['player_positions'].str.contains('RM', regex=False), 'player_positions'] = 'A'
    players_details_df.loc[players_details_df['player_positions'].str.contains('LM', regex=False), 'player_positions'] = 'A'
    players_details_df.loc[players_details_df['player_positions'].str.contains('CDM', regex=False), 'player_positions'] = 'D'
    players_details_df.loc[players_details_df['player_positions'].str.contains('CB', regex=False), 'player_positions'] = 'D'
    players_details_df.loc[players_details_df['player_positions'].str.contains('RB', regex=False), 'player_positions'] = 'D'
    players_details_df.loc[players_details_df['player_positions'].str.contains('LB', regex=False), 'player_positions'] = 'D'
    players_details_df.loc[players_details_df['player_positions'].str.contains('GK', regex=False), 'player_positions'] = 'D'
    players_details_df.fillna(0)

    final_grouped_players_df = players_details_df.loc[players_details_df['player_positions'] == 'A'].groupby('nationality')['overall'].agg(['median'])
    final_grouped_players_df['Defensive_Prowess'] = players_details_df.loc[players_details_df['player_positions'] == 'D'].groupby('nationality')['overall'].agg(['median'])

    officially_qualified_teams = pd.merge(officially_qualified_teams, final_grouped_players_df, left_on='Nation',
                                          right_index=True, how='left').fillna(0)
    return officially_qualified_teams


def fetch_details_for_simulating_groups() -> pd.DataFrame:
    """
    It is main function that returns all the qualifying teams along with its statistics of attacking prowess,
    defensive prowess, rank and confideration.
    :return:
    >>> africa_teams = pd.read_csv("AFC.csv")
    >>> africa_teams.head(5)
        Nation
    0  Senegal
    1  Tunisia
    2  Nigeria
    3  Algeria
    4  Morocco
    >>> players_df = pd.read_csv("players_20.csv", index_col="sofifa_id")
    >>> host_nation_country = 'Qatar'
    >>> host_team_data = host_nation_df(host_nation_country, players_df)
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

    host_team_data = host_nation_df(host_nation_country, players_df)

    qualified_frames = [afc_team_data, asia_team_data, north_america_team_data,
                        south_america_team_data, oceania_team_data,
                        uefa_team_data, host_team_data]
    world_cup_team_data = pd.concat(qualified_frames)
    world_cup_team_stats = qualifying_team_attack_def_stats(world_cup_team_data, players_df)
    return world_cup_team_stats


def qualification_count_for_host_and_defending_country(team_group: list) -> list:
    """
    This function sorts the team in a group based on their points, goal difference and goal scored in tournament.
    It calculates the count of whether the host nation and defending champion make it past through the group stages or not,
    This function after the match result of all the teams in a single group are calculated.

    :param team_group:
    :return:
    """
    defending_country_count = 0
    host_country_count = 0
    count_list = []

    arranged_team = sorted(team_group, key=lambda team: (team.points, team.goal_difference, team.goal_scored_in_tournament),
                           reverse=True)
    loop_count = 0
    for each_arranged_team in arranged_team:
        loop_count += 1
        if each_arranged_team.last_winner and loop_count < 3:
            defending_country_count += 1
            break

        elif each_arranged_team.Name == host_nation_country and loop_count <= 2:
            host_country_count += 1
            break

        elif loop_count > 2:
            break

    count_list.append(defending_country_count)
    count_list.append(host_country_count)
    return count_list


# The below class deals with the World Cup Team.
class WorldCupTeam:

    world_cup_team_stats_list = []

    def __init__(self, team_details_df, team_count):
        self.count = 0
        self.Name = team_details_df['Nation']
        self.Rank = team_details_df['Rank']
        self.Above_Median = team_details_df['Above_Median_Count']
        self.Rank_Points = team_details_df['Points']
        self.Attacking_Strength = team_details_df['median_y']
        self.Defensive_Strength = team_details_df['Defensive_Prowess']
        self.points = 0
        self.won = 0
        self.lost = 0
        self.drawn = 0
        self.goal_scored_in_match = 0
        self.goal_scored_in_tournament = 0
        self.goal_against_in_match = 0
        self.goal_against_in_tournament = 0
        self.goal_difference = 0

        if self.Name == defending_nation:
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

        if self.Attacking_Strength == 0.0:
            if 20 <= self.Rank <= 30:
                self.Attacking_Strength = random.randint(65, 67)
            elif 31 <= self.Rank <= 50:
                self.Attacking_Strength = random.randint(63, 65)
            elif 51 <= self.Rank <= 70:
                self.Attacking_Strength = random.randint(62, 64)
            else:
                self.Attacking_Strength = random.randint(60, 62)

        if self.Defensive_Strength == 0.0:
            if 20 <= self.Rank <= 30:
                self.Defensive_Strength = random.randint(65, 67)
            elif 31 <= self.Rank <= 50:
                self.Defensive_Strength = random.randint(63, 65)
            elif 51 <= self.Rank <= 70:
                self.Defensive_Strength = random.randint(62, 64)
            else:
                self.Defensive_Strength = random.randint(60, 62)

        if self.Name == 'Qatar':
            self.pot = 1
            self.Attacking_Strength = random.randint(63, 67)
            self.Defensive_Strength = random.randint(63, 67)

        WorldCupTeam.world_cup_team_stats_list.append(self)

    @staticmethod
    def create_team_instances(team_details_df):
        """
        It creates the team object instances for all the qualifying teams.
        :param team_details_df:
        :return:
        """
        # To clear the existing list of teams after every simulation.
        if len(WorldCupTeam.world_cup_team_stats_list) > 0:
            WorldCupTeam.world_cup_team_stats_list.clear()

        sorted_team_details_df = team_details_df.sort_values(by=['Rank'])
        # sorted_team_details_df = sorted_team_details_df.set_index('Nation')
        team_count = 1
        for index, row in sorted_team_details_df.iterrows():
            WorldCupTeam(row, team_count)
            team_count += 1


# Below class deals with the Match Result between any two teams.
class MatchResult:

    def __init__(self, team1, team2):
        self.team1 = team1
        self.team2 = team2
        self.host_factor = 0
        if team1.Name == host_nation_country or team2.Name == host_nation_country:
            self.host_factor = host_nation_factor
        self.get_match_result()

    def get_match_result(self):
        """
        This function estimates the result of the match between two teams based on the attacking strength and defensive strength.
        The team total rank points also plays an important role deciding the score.
        The host nation factor is also added whose value is defined in the main function.
        This factor also plays a major role is deciding the result of a match when a host nation is involved.

        :return:
        """
        try:
            if self.host_factor != 0:
                self.team1.scoring_power = (self.team1.Attacking_Strength / self.team2.Defensive_Strength) * (self.team1.Rank_Points / self.team2.Rank_Points)
                self.team2.scoring_power = (self.team2.Attacking_Strength / self.team1.Defensive_Strength) * (self.team2.Rank_Points / self.team1.Rank_Points)
            else:
                if self.team1.Name == host_nation_country:
                    self.team1.scoring_power = (self.team1.Attacking_Strength / self.team2.Defensive_Strength) * self.host_factor * (self.team1.Rank_Points / self.team2.Rank_Points)
                else:
                    self.team1.scoring_power = self.team1.Attacking_Strength / self.team2.Defensive_Strength * (self.team1.Rank_Points / self.team2.Rank_Points)

                if self.team2.Name != host_nation_country:
                    self.team2.scoring_power = self.team2.Attacking_Strength / self.team1.Defensive_Strength * (self.team2.Rank_Points / self.team1.Rank_Points)
                else:
                    self.team2.scoring_power = (self.team2.Attacking_Strength / self.team1.Defensive_Strength) * self.host_factor * (self.team2.Rank_Points / self.team1.Rank_Points)

            self.team1.goal_scored_in_match = np.random.poisson(self.team1.scoring_power)
            self.team2.goal_scored_in_match = np.random.poisson(self.team2.scoring_power)

            if self.team1.goal_scored_in_match > self.team2.goal_scored_in_match:
                self.team1.points += 3
                self.team1.won += 1
                self.team2.lost += 1
            elif self.team1.goal_scored_in_match < self.team2.goal_scored_in_match:
                self.team2.points += 3
                self.team2.won += 1
                self.team1.lost += 1
            else:
                self.team1.points += 1
                self.team2.points += 1
                self.team1.drawn += 1
                self.team2.drawn += 1

            self.team1.goal_scored_in_tournament += self.team1.goal_scored_in_match
            self.team2.goal_scored_in_tournament += self.team2.goal_scored_in_match
            self.team1.goal_against_in_tournament += self.team2.goal_scored_in_match
            self.team2.goal_against_in_tournament += self.team1.goal_scored_in_match
            self.team1.goal_difference = self.team1.goal_scored_in_tournament - self.team1.goal_against_in_tournament
            self.team2.goal_difference = self.team2.goal_scored_in_tournament - self.team2.goal_against_in_tournament

            print("The score between {} and {} is {} - {}".format(self.team1.Name, self.team2.Name,
                                                                  self.team1.goal_scored_in_match,
                                                                  self.team2.goal_scored_in_match))
        except(ArithmeticError):
            print("The teams {} or {} have zero defensive strength".format(self.team1.Name, self.team2.Name))

    @staticmethod
    def result_of_group_matches(all_group_teams_list):
        """
        It is a static method, which calls the Match Result class, to estimate the result of a soccer match between two teams.
        :param all_group_teams_list:
        :return:
        """

        for each_combination in all_group_teams_list:
            MatchResult(each_combination[0], each_combination[1])


# noinspection PyPep8Naming
def simulate_groups(simulations: int):
    """
    This is main simulation function that assigns the groups to its appropriate pots and then randomly
    assign each team to the group. It also estimates the match result and provides the result of whether to consider or
    disregard the hypothesis.
    :param simulations:
    :return:
    """
    winner_count = 0  # Used for Hypothesis 1
    host_nation_count = 0   # Used for Hypothesis 2
    defending_champion_count = 0   # Used for Hypothesis 3

    for i in range(simulations):
        # Declaring the 4 pots and 8 groups below
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

        # The below code determines the team that are likely to qualify for the World Cup.
        # Teams Object Oriented Design is used in here.
        # Team object has an attribute of Pot as well, assigned after sorting the qualified teams on the basis of rank.
        WorldCupTeam.create_team_instances(fetch_details_for_simulating_groups())
        teams_list = WorldCupTeam.world_cup_team_stats_list

        # Assigning the qualified teams into the pot list according to their rank. Host nation is given pot 1.
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

        # Below codes assigns the team into Groups from the Pots.
        # Since, France is likely to be in Pot 1 as it has  rank 3 currently, so Hypothesis one variable count increment in added in Pot 1 assignment
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

        # Print Group A teams
        print("\n Group A")
        for each_team in groupA:
            print(each_team.Name)

        # Below code is used to identify the winner of the matches among the teams of group A.
        possible_team_combinations_group_a = list(itertools.combinations(groupA, 2))
        MatchResult.result_of_group_matches(possible_team_combinations_group_a)

        # Below code is used for the analysis of Hypothesis 2 and 3.
        count_list = qualification_count_for_host_and_defending_country(groupA)
        defending_champion_count += count_list[0]
        host_nation_count += count_list[1]

        # Print Group B teams
        print("\n Group B")
        for each_team in groupB:
            print(each_team.Name)

        # Below code is used to identify the winner of the matches among the teams of group B.
        possible_team_combinations_group_b = list(itertools.combinations(groupB, 2))
        MatchResult.result_of_group_matches(possible_team_combinations_group_b)

        # Below code is used for the analysis of Hypothesis 2 and 3.
        count_list = qualification_count_for_host_and_defending_country(groupB)
        defending_champion_count += count_list[0]
        host_nation_count += count_list[1]

        # Print Group C teams
        print("\n Group C")
        for each_team in groupC:
            print(each_team.Name)

        # Below code is used to identify the winner of the matches among the teams of group C.
        possible_team_combinations_group_c = list(itertools.combinations(groupC, 2))
        MatchResult.result_of_group_matches(possible_team_combinations_group_c)

        # Below code is used for the analysis of Hypothesis 2 and 3.
        count_list = qualification_count_for_host_and_defending_country(groupC)
        defending_champion_count += count_list[0]
        host_nation_count += count_list[1]

        # Print Group D teams
        print("\n Group D")
        for each_team in groupD:
            print(each_team.Name)

        # Below code is used to identify the winner of the matches among the teams of group D.
        possible_team_combinations_group_d = list(itertools.combinations(groupD, 2))
        MatchResult.result_of_group_matches(possible_team_combinations_group_d)

        # Below code is used for the analysis of Hypothesis 2 and 3.
        count_list = qualification_count_for_host_and_defending_country(groupD)
        defending_champion_count += count_list[0]
        host_nation_count += count_list[1]

        # Print Group E teams
        print("\n Group E")
        for each_team in groupE:
            print(each_team.Name)

        # Below code is used to identify the winner of the matches among the teams of group E.
        possible_team_combinations_group_e = list(itertools.combinations(groupE, 2))
        MatchResult.result_of_group_matches(possible_team_combinations_group_e)

        # Below code is used for the analysis of Hypothesis 2 and 3.
        count_list = qualification_count_for_host_and_defending_country(groupE)
        defending_champion_count += count_list[0]
        host_nation_count += count_list[1]

        # Print Group F teams
        print("\n Group F")
        for each_team in groupF:
            print(each_team.Name)

        # Below code is used to identify the winner of the matches among the teams of group F.
        possible_team_combinations_group_f = list(itertools.combinations(groupF, 2))
        MatchResult.result_of_group_matches(possible_team_combinations_group_f)

        # Below code is used for the analysis of Hypothesis 2 and 3.
        count_list = qualification_count_for_host_and_defending_country(groupF)
        defending_champion_count += count_list[0]
        host_nation_count += count_list[1]

        # Print Group G teams
        print("\n Group G")
        for each_team in groupG:
            print(each_team.Name)

        # Below code is used to identify the winner of the matches among the teams of group G.
        possible_team_combinations_group_g = list(itertools.combinations(groupG, 2))
        MatchResult.result_of_group_matches(possible_team_combinations_group_g)

        # Below code is used for the analysis of Hypothesis 2 and 3.
        count_list = qualification_count_for_host_and_defending_country(groupG)
        defending_champion_count += count_list[0]
        host_nation_count += count_list[1]

        # Print Group H teams
        print("\n Group H")
        for each_team in groupH:
            print(each_team.Name)

        # Below code is used to identify the winner of the matches among the teams of group H.
        possible_team_combinations_group_h = list(itertools.combinations(groupH, 2))
        MatchResult.result_of_group_matches(possible_team_combinations_group_h)

        count_list = qualification_count_for_host_and_defending_country(groupH)
        defending_champion_count += count_list[0]
        host_nation_count += count_list[1]

    # Below are the final result percentage of all the three hypothesis.
    print("\nResults after {} simulations".format(simulations))

    print("\nThe chances of Defending champion (that is {}) qualifying for the world cup is {}".
          format(defending_nation, winner_count/simulations * 100))

    print("\nThe chances of Defending champion (that is {}) reaching the knockout stage of World Cup is {}".
          format(defending_nation, defending_champion_count / winner_count * 100))

    print("\nThe chances of Host Nation (that is {}) reaching the knockout stage of World Cup is {}".
          format(host_nation_country, host_nation_count / simulations * 100))


if __name__ == '__main__':

    qualified_teams = []
    host_nation_country = 'Qatar'
    defending_nation = 'France'
    # Host nation are likely to perform 25% better (assumption) as per their normal.
    host_nation_factor = 1.25
    # Confideration Qualifying Count Dictionary
    confideration = {'CAF': 4, 'AFC': 4, 'UEFA': 13, 'CONMEBOL': 5, 'CONCACAF': 4, 'OFC': 1}
    # Forming the players data frame and the team ranking data frame
    players_df = pd.read_csv("players_20.csv", index_col="sofifa_id")
    team_rankings = pd.read_csv("Latest_Rankings.csv", index_col='Nation')

    simulate_groups(100)  # One can change the simulation count from here.
