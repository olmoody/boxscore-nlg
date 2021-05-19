Data used in [Challenges in Data-to-Document Generation](https://arxiv.org/abs/1707.08052) (Wiseman, Shieber, Rush; EMNLP 2017).

# Getting Started
See rotowire/README.md for directions

# Data
This dataset consists of (human-written) NBA basketball game summaries aligned with their corresponding box- and line-scores. Summaries taken from rotowire.com are referred to as the "rotowire" data.

To extract the data, run `tar -jxvf rotowire.tar.bz2` to add data to rotowire/ directory


## Rotowire Data
The rotowire data can be found in rotowire/[train|valid|test].json. There are 4853 distinct rotowire summaries, covering NBA games played between 1/1/2014 and 3/29/2017; some games have multiple summaries. The summaries have been randomly split into training, validation, and test sets consisting of 3398, 727, and 728 summaries, respectively.


# Data Format
Each file is utf-8 encoded json, and contains a list of json objects corresponding to each aligned summary/data pair. These json objects have the following fields:

* home_name - Name of home team (unicode)
* home_city - City of home team (unicode)
* vis_name  - Name of visiting team (unicode)
* vis_city  - City of visiting team (unicode)
* day       - Date of game in %MM_%DD_%YY format (unicode)
* summary   - Tokenized summary of game
* home_line - Home team line-score object; see below
* vis_line  - Visiting team line-score object; see below
* box_score - Box-score object; see below

## Line-score Objects
Line-score objects have the following fields:

* TEAM-NAME     - Team name (unicode)
* TEAM-CITY     - Team city (unicode)
* TEAM-AST      - Number of team assists (integer as unicode)
* TEAM-FG3_PCT  - Percentage of 3 pointers made by team (integer as unicode)
* TEAM-FG_PCT   - Percentage of field goals made by team (integer as unicode)
* TEAM-FT_PCT   - Percentage of free throws made by team (integer as unicode)
* TEAM_LOSSES   - Team losses (integer as unicode)
* TEAM-PTS      - Total team points (integer as unicode)
* TEAM-PTS_QTR1 - Team points in first quarter (integer as unicode)
* TEAM-PTS_QTR2 - Team points in second quarter (integer as unicode)
* TEAM-PTS_QTR3 - Team points in third quarter (integer as unicode)
* TEAM-PTS_QTR4 - Team points in fourth quarter (integer as unicode)
* TEAM-REB      - Total team rebounds (integer as unicode)
* TEAM-TOV      - Total team turnovers (integer as unicode)
* TEAM-WINS     - Team wins (integer as unicode)

## Box-score Objects
Box-score objects contain (column) objects mapping row numbers to values. Rows are numbered from 0 to at most 25, and each row corresponds to a player in the game. In particular, a box-score object contains the following column objects:

* AST            - Player assists (row_number -> integer as unicode)
* BLK            - Player blocks (row_number -> integer as unicode)
* DREB           - Player defensive rebounds (row_number -> integer as unicode)
* FG3A           - Player 3-pointers attempted (row_number -> integer as unicode)
* FG3M           - Player 3-pointers made (row_number -> integer as unicode)
* FG3_PCT        - Player 3-pointer percentage (row_number -> integer as unicode)
* FGA            - Player field goals attempted (row_number -> integer as unicode)
* FGM            - Player field goals made (row_number -> integer as unicode)
* FG_PCT         - Player field goal percentage (row_number -> integer as unicode)
* FIRST_NAME     - Player first name (row_number ->  unicode)
* FTA            - Player free throws attempted (row_number -> integer as unicode)
* FTM            - Player free throws made (row_number -> integer as unicode)
* FT_PCT         - Player free throw percentage (row_number -> integer as unicode)
* MIN            - Player minutes played (row_number -> integer as unicode)
* OREB           - Player offensive rebounds (row_number -> integer as unicode)
* PF             - Player personal fouls (row_number -> integer as unicode)
* PLAYER_NAME    - Player full name (row_number -> integer as unicode)
* PTS            - Player points (row_number -> integer as unicode)
* REB            - Player total rebounds (row_number -> integer as unicode)
* SECOND_NAME    - Player second name (row_number -> integer as unicode)
* START_POSITION - Player position (row_number -> unicode)
* STL            - Player steals (row_number -> integer as unicode)
* TEAM_CITY      - Player team city (row_number -> unicode)
* TO             - Player turnovers (row_number -> integer as unicode)


# Preprocessing Details

## Box- and Line-scores
All number values in the box- and line-scores have been converted to integers by rounding if necessary. (So, percents are given as integers between 0 and 100).

## Summaries
Summaries are tokenized using nltk, and hyphenated phrases are separated.
