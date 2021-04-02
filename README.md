# 2021_Spring_finals

All final assignments (projects) for IS597PR in Spring 2021 are expected to be forks from here.

See the course Moodle for the detailed expectations and instructions.

USING MONTE CARLO SIMULATION TO CALCULATE MATCH IMPORTANCE: THE CASE OF ENGLISH PREMIER LEAGUE 
Rajat Kumar (rajat3illinois)
Introduction: - 
In typical premier league, various clubs compete to win the championship, get promoted to a higher league, qualify for other competitions, or to avoid relegation. Because the leagues usually use a round-robin tournament system (sometimes combined with play-offs), not all matches have the same impact to the outcome of the season – there are highly important last-round matches where a single result can decide which team becomes the new league champion, on the other hand, there are unimportant matches between clubs without a realistic chance of being either promoted or relegated.
In this project, for calculating the match importance using Monte Carlo simulation data for previous seasons of soccer matches (2000/01-2009/10) in the English Premier League will be used.
Firstly, probabilities of all individual match results until the end of season are estimated based on past performances of all teams. These match result probabilities are then used to simulate the rest of the season and estimate probabilities of various season outcomes (final team ranks).
Literature: -
There are two distinct components of match importance: first, how likely a team is to achieve a certain outcome, such as championship, promotion, or relegation (this is usually called seasonal uncertainty); second, how much a specific match can influence the probability of this outcome. 
Hypothesis: - 
The uncertainty of winning the championship works in this way: first, take the number of points that were eventually necessary to win the championship (of course, this ex-post information is not actually available before the end of the season, but it could be argued that it is possible to estimate it) – let’s say it is 65. If it is still theoretically possible for a team to reach 65 points, set match importance for this team to 1/(number of matches necessary to reach 65 points), otherwise set match importance to zero. At the beginning of the season, all teams are able to reach 65 points, but they would need at least 22 matches (assuming 3 points for a win), so match importance equals 1/22. As the season progresses, importance for a specific team either increases towards 1 or drops to zero (when it is no longer possible to win). The match in which the eventual winner reaches 65 points must have the importance equal to one (this can happen in the last round or sooner). 
Data: - 
In each season of Premier League, there are 20 teams playing two matches (one home and one away) against each other, so each team plays 38 matches per season. Winning a match is worth three points, drawing a match one point, and losing a match zero points. English Premier League does not use the head-on matches criterion to rank teams with the same number of points, so the final table ranking criteria are total points, total goal difference, and total goals scored (in this order). The first team wins a championship title and the last three teams are relegated to a lower competition – therefore, winning championship and not being relegated are two primary goals that enter into match importance calculations. Other possible goals could be qualifying for a European competition (usually first five teams) or just placing as well as possible. 
To verify predictions of individual match results, the latest available betting odds of a big British bookmaker William Hill are used – these odds have been obtained for all the matches played since December 26th, 2005.. The odds have been converted to implied probabilities of a home win, draw, and away win. 
The betting and actual result data can be extracted from below.
https://www.oddsportal.com/soccer/england/premier-league-2005-2006/results/
Method: -
As stated above, the importance of a specific match for a specific team can be decomposed into two components first, the probability that the team reaches a particular season outcome, such as championship or not being relegated; second, how this probability depends on the match result. More formally, it is necessary to calculate the probabilities of various outcomes conditional on the specific match result. The match importance can then be expressed as a measure of association between the match result and the outcome. 
Multiple relevant outcomes imply multiple types of match importance; a particular match can have a small influence on the probability that a team wins the competition, a large influence on the final rank, and a zero influence on the probability that the team is relegated. These various types of match importance are likely to be valued differently by potential match spectators. 
The proposed Monte Carlo method of consists of three steps leading to the desired result: first, calculate the result probabilities of all the remaining matches of the season; second, use these probabilities to estimate the probabilities of final team ranks; third, calculate the association between the match result and various season outcomes. 

The reference for this simulation is 
https://mpra.ub.uni-muenchen.de/40998/1/MPRA_paper_40998.pdf
This is just a thought process of this simulation and can change with the development process. I am thinking of implementing a prediction scenario for the next season as well, if there is time for further extrapolation.

