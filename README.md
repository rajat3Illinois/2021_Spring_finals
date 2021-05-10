# 2021_Spring_finals

All final assignments (projects) for IS597PR in Spring 2021 are expected to be forks from here.

Soccer World Cup 2022 (Type III Analysis)

Rajat Kumar (rajat3illinois)

AIM: - 

The FIFA World Cup is the most widely viewed and followed sporting event in the world. Being a soccer player, and an ardent fan of soccer, I thank Professor John Weible in letting me choose a topic of the FIFA World Cup 2022. Since, this is a hugely popular topic, it was suggested by the professor, to categorize the analysis into Type 3 category (modifying an existing simulation).
As a result, I have simulated the FIFA World Cup 2022, by performing concrete modification to the previous simulation of FIFA 2018 World Cup. 

The link for the same is mentioned below.

Previous Project Link: - https://github.com/hiralrayani/World-Cup-Simulator.git

Do check the ppt on the repository for a better understanding.

INTRODUCTION: - 

There are in total 32 teams qualify for the tournament with the host nation given an automatic qualification. 
These 32 teams are decided based on confederations (continents) mentioned below: - 

CAF (Africa)
AFC (Asia)
CONENBOL (South America)
CONCACAF (North America)
Oceania
UEFA (Europe)

Only limited number of teams can qualify from a particular confederation. In other words, the number of teams from a particular confederation is pre-defined as follows: - 
{'CAF': 4, 'AFC': 4, 'UEFA': 13, 'CONMEBOL': 5, 'CONCACAF': 4, 'OFC': 1}

Although there is playoff among few teams of different confederation, but our analysis would be based, by keeping in mind this confederation wise number.

As per the rules the Tournament Format is as follow: - 
Group Stages (32 teams split into 8 groups)
Last -16 Stage (Top 2 teams from each group qualify)
Quarter-Final
Semi-Final
Final

APPROACH: - 

Since, we are in 2020, so we don't know have any teams that have qualified for the World Cup apart from the host nation (Qatar) who are given automatic qualification.
Below are the checkpoints of this whole implementation.

1) Compute the 31 teams that are likely to qualify for the World Cup, with Qatar given the automatic qualification.
2) Keeping in mind the number of teams likely to qualify from a particular confederation, we will predict the remaining 31 teams.
3) The team’s qualification will depend on its rank, avg attacking strength, avg defensive strength (includes goalkeeper strength), players median rating in the dataset player_20.csv, players total value (market rate value). 
4) After obtaining the entire 32 teams, we will split the teams into groups.
5) For making the group teams, pots seeding technique is used. The same is explained below: - 

POTS SEEDING UNDERSTANDING: - 

1) In order to compute the group of teams, there are 4 POTS identified (of 8 teams each), wherein all the qualified teams are put in as per their world ranking.
2) For example, if there is no 1 ranked team (i.e., Belgium right now) as one of the team that qualified to World Cup, then it is put in Pot 1.  Once, Pot 1 is filled, the filling of Pot 2 is undertaken. This process till all the 4 Pots are filled.

NOTE: - The host nation as per the rules are automatically assigned Pot1.

3) Once the pots are filled, the 8 groups are randomly constructed, with each group having a team from every Pot. No two teams from a single pot can belong to the same group.
For example, Belgium and Qatar can't be in the same group.
4) For better understanding, there is sample POTS and Groups created from these Pots mentioned below: - 

Pot 1: - Qatar, Belgium, Spain, Argentina, Portugal, England, France, Brazil
Pot 2: - Mexico, Italy, Croatia, Uruguay, Germany, Netherlands, Columbia, Chile
Pot 3: - Poland, Senegal, Sweden, United States, Japan, Iran, Serbia, Turkey
Pot 4: - Morocco, South Korea, Costa Rica, Ghana, Ivory Coast, Saudi Arabia, Canada, New Zealand

Based on the above Pots, below can be one of the possible groups for the World Cup.

Group A: - Brazil, Mexico, Serbia, Costa Rica
Group B: - France, Uruguay, Japan, Canada
Group C: - Spain, Germany, Turkey, New Zealand
Group D: - England, Italy, Sweden, South Korea
Group E: - Qatar, Croatia, Senegal, Morocco
Group F: - Belgium, Chile, United States, Ghana
Group G: - Argentina, Columbia, Poland, Saudi Arabia
Group H: - Portugal, Netherlands, Iran, Ivory Coast

IMPORTANT ASSUMPTIONS/ MODIFICATIONS WHILE DESIGNING: -

1) Host nation is likely to perform 25% better as per their normal performance. Thus, a host nation factor is considered during the simulation.

2) Different confederation has different normalized threshold rank above which the team is likely to qualify for the World Cup.

3) There is at least 1 team from each confederation.

4) For UEFA confederation which has maximum teams, the higher ranked teams are more likely to qualify. 
The UEFA team have a grad from 1 to 6 as per their ranking. Thus, it is assumed that team are from grade 1 and then followed by grade 2 are more likely to qualify for the World Cup.

5) Squad size (Bench Strength) are crucial in determining the qualification of team.

6) The count of player above the median rating plays an important role in qualification.

7) The total market value combined of all the players of a team has an impact on team’s qualification.

8) For certain teams as well as host nation (Qatar), attacking prowess and defensive prowess are randomly added based on their ranking.

9) The Ranking points of the team along with the attacking and defensive prowess are important in deciding the match result between two teams.

10) Teams with the highest points from the group qualify for the knockout stage. If two teams end up with same points, then the goal difference (that is the difference between goal scored and goal conceded in the tournament) is considered. If that also becomes same for the two teams, then the team who have scored a greater number of goals in the tournament is likely to qualify.


HYPOTHESIS: - 

1) The defending champion (France) has a strong chance of making to the world cup. 

As per the results calculated below, we accept this hypothesis. 

2) The curse of defending champion (France) not reaching the knockout stages is highly unlikely.

As per the results calculated below, we accept this hypothesis. 

2) It is highly likely that the host nation (Qatar) would qualify for the knockout stages.

As per the results calculated below, we discard this hypothesis. 

RESULTS: - 

Below are the sample results of the simulation.

After 50 simulations: -

1) Defending champion (France) has 88% chance of qualifying for the World Cup.
2) Defending champion (France) has 75% chance of reaching the Knockouts.
3) Host nation (Qatar) has 34% chance of reaching the Knockouts.

After 100 simulations: -

1) Defending champion (France) has 80% chance of qualifying for the World Cup.
2) Defending champion (France) has 60% chance of reaching the Knockouts.
3) Host nation (Qatar) has 54% chance of reaching the Knockouts.

After 200 simulations: -

1) Defending champion (France) has 83% chance of qualifying for the World Cup.
2) Defending champion (France) has 74.1% chance of reaching the Knockouts.
3) Host nation (Qatar) has 46.5% chance of reaching the Knockouts.

After 500 simulations: -

1) Defending champion (France) has 78% chance of qualifying for the World Cup.
2) Defending champion (France) has 68.46% chance of reaching the Knockouts.
3) Host nation (Qatar) has 41.2% chance of reaching the Knockouts.

After 800 simulations: -

1) Defending champion (France) has 79.125% chance of qualifying for the World Cup.
2) Defending champion (France) has 63.19% chance of reaching the Knockouts.
3) Host nation (Qatar) has 39.875% chance of reaching the Knockouts.

After 1000 simulations: -

1) Defending champion (France) has 84.1% chance of qualifying for the World Cup.
2) Defending champion (France) has 67.18% chance of reaching the Knockouts.
3) Host nation (Qatar) has 43.4% chance of reaching the Knockouts.


DATA SOURCES: - 

FIFA 20 Players:  https://www.kaggle.com/stefanoleone992/fifa-20-complete-player-dataset

Latest FIFA Ranking: https://www.fifa.com/fifa-world-ranking/ranking-table/men/ 
                                    https://www.transfermarkt.us/statistik/weltrangliste

EXECUTION: - 

Execute the WorlCupQualification.py file for the results. 
The simulation count can be changed provided in the main clause of python file.
One can change the simulation count in the main call of the python file.
Make sure all the data files are in the same directory as the python file.
There is Jupyter notebook in the repository that is completely used for testing purpose. It doesn’t provide any analysis of this project.

REFERENCES: -

https://www.espn.com/soccer/fifa-world-cup/story/3860182/2022-world-cup-how-qualifying-works-around-the-world

https://towardsdatascience.com/simulating-the-fifa-world-cup-2022-d363fad7da22

https://core.ac.uk/download/pdf/216466812.pdf

https://en.wikipedia.org/wiki/2018_FIFA_World_Cup_seeding


