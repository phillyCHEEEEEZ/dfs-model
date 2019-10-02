from bs4 import BeautifulSoup
import pandas as pd
import requests


skater_url = requests.get(
    'https://www.numberfire.com/nhl/daily-fantasy/daily-hockey-projections/skaters').text

skater_names = []
skater_positions = []
skater_teams = []
skater_opponents = []
skater_projections = []
skater_salaries = []
skater_values = []
skater_shots = []
skater_goals = []
skater_assists = []
skater_points = []
skater_ppg = []
skater_ppa = []
skater_plusminus = []
skater_blocks = []
skater_mins = []
skater_pim = []

skater_soup = BeautifulSoup(skater_url, 'html.parser')

skater_table = skater_soup.find(
    'table', class_='stat-table fixed-head')

skater_html_dict = {
    'skater_names': [
        {'tag': 'a'},
        {'class': 'full'},
    ],
    'skater_positions': [
        {'tag': 'span'},
        {'class': 'player-info--position'},
    ],
    'skater_teams': [
        {'tag': 'span'},
        {'class': 'team-player__team active'},
    ],
    'skater_opponents': [
        {'tag': 'span'},
        {'class': 'team-player__team'},
    ],
    'skater_projections': [
        {'tag': 'td'},
        {'class': 'fp active'},
    ],
    'skater_salaries': [
        {'tag': 'td'},
        {'class': 'cost'},
    ],
    'skater_values': [
        {'tag': 'td'},
        {'class': 'value'},
    ],
    'skater_shots': [
        {'tag': 'td'},
        {'class': 's'},
    ],
    'skater_goals': [
        {'tag': 'td'},
        {'class': 'g'},
    ],
    'skater_assists': [
        {'tag': 'td'},
        {'class': 'ast'},
    ],
    'skater_points': [
        {'tag': 'td'},
        {'class': 'points'},
    ],
    'skater_ppg': [
        {'tag': 'td'},
        {'class': 'ppg'},
    ],
    'skater_ppa': [
        {'tag': 'td'},
        {'class': 'ppa'},
    ],
    'skater_plusminus': [
        {'tag': 'td'},
        {'class': 'plus_minus'},
    ],
    'skater_blocks': [
        {'tag': 'td'},
        {'class': 'blk'},
    ],
    'skater_mins': [
        {'tag': 'td'},
        {'class': 'min'},
    ],
    'skater_pim': [
        {'tag': 'td'},
        {'class': 'pim'},
    ],
}


def scrapeData(dictionary, soup, index):
    return soup.find_all(
        dictionary[list(dictionary.keys())[index]][0][list(
            list(dictionary[list(dictionary.keys())[index]])[0])[0]], class_=dictionary[list(dictionary.keys())[index]][1][list(
                list(dictionary[list(dictionary.keys())[index]])[1])[0]])


for i in range(0, len(skater_html_dict)):
    if i == 0:
        skater_names = scrapeData(skater_html_dict, skater_table, i)
    if i == 1:
        skater_positions = scrapeData(skater_html_dict, skater_table, i)
    if i == 2:
        skater_teams = scrapeData(skater_html_dict, skater_table, i)
    if i == 3:
        skater_opponents = scrapeData(skater_html_dict, skater_table, i)
    if i == 4:
        skater_projections = scrapeData(skater_html_dict, skater_table, i)
    if i == 5:
        skater_salaries = scrapeData(skater_html_dict, skater_table, i)
    if i == 6:
        skater_values = scrapeData(skater_html_dict, skater_table, i)
    if i == 7:
        skater_shots = scrapeData(skater_html_dict, skater_table, i)
    if i == 8:
        skater_goals = scrapeData(skater_html_dict, skater_table, i)
    if i == 9:
        skater_assists = scrapeData(skater_html_dict, skater_table, i)
    if i == 10:
        skater_points = scrapeData(skater_html_dict, skater_table, i)
    if i == 11:
        skater_ppg = scrapeData(skater_html_dict, skater_table, i)
    if i == 12:
        skater_ppa = scrapeData(skater_html_dict, skater_table, i)
    if i == 13:
        skater_plusminus = scrapeData(skater_html_dict, skater_table, i)
    if i == 14:
        skater_blocks = scrapeData(skater_html_dict, skater_table, i)
    if i == 15:
        skater_mins = scrapeData(skater_html_dict, skater_table, i)
    if i == 16:
        skater_pim = scrapeData(skater_html_dict, skater_table, i)

skater_names_final = []
skater_positions_final = []
skater_teams_final = []
skater_opponents_final = []
skater_projections_final = []
skater_salaries_final = []
skater_values_final = []
skater_shots_final = []
skater_goals_final = []
skater_assists_final = []
skater_points_final = []
skater_ppg_final = []
skater_ppa_final = []
skater_plusminus_final = []
skater_blocks_final = []
skater_mins_final = []
skater_pim_final = []

skater_contents_dict = {
    'skater_names': [
        {'soup': skater_names},
        {'final': skater_names_final},
    ],
    'skater_positions': [
        {'soup': skater_positions},
        {'final': skater_positions_final},
    ],
    'skater_teams': [
        {'soup': skater_teams},
        {'final': skater_teams_final},
    ],
    'skater_opponents': [
        {'soup': skater_opponents},
        {'final': skater_opponents_final},
    ],
    'skater_projections': [
        {'soup': skater_projections},
        {'final': skater_projections_final},
    ],
    'skater_salaries': [
        {'soup': skater_salaries},
        {'final': skater_salaries_final},
    ],
    'skater_values': [
        {'soup': skater_values},
        {'final': skater_values_final},
    ],
    'skater_shots': [
        {'soup': skater_shots},
        {'final': skater_shots_final},
    ],
    'skater_goals': [
        {'soup': skater_goals},
        {'final': skater_goals_final},
    ],
    'skater_assists': [
        {'soup': skater_assists},
        {'final': skater_assists_final},
    ],
    'skater_points': [
        {'soup': skater_points},
        {'final': skater_points_final},
    ],
    'skater_ppg': [
        {'soup': skater_ppg},
        {'final': skater_ppg_final},
    ],
    'skater_ppa': [
        {'soup': skater_ppa},
        {'final': skater_ppa_final},
    ],
    'skater_plusminus': [
        {'soup': skater_plusminus},
        {'final': skater_plusminus_final},
    ],
    'skater_blocks': [
        {'soup': skater_blocks},
        {'final': skater_blocks_final},
    ],
    'skater_mins': [
        {'soup': skater_mins},
        {'final': skater_mins_final},
    ],
    'skater_pim': [
        {'soup': skater_pim},
        {'final': skater_pim_final},
    ],
}


def getContents(dictionary, index):
    soup = dictionary[list(dictionary.keys())[index]][0][list(
        list(dictionary[list(dictionary.keys())[index]])[0])[0]]
    final = dictionary[list(dictionary.keys())[index]][1][list(
        list(dictionary[list(dictionary.keys())[index]])[1])[0]]
    for x in soup:
        final.append(x.contents)
    return final


for i in range(0, len(skater_contents_dict)):
    if i == 0:
        skater_names_final = getContents(skater_contents_dict, i)
    if i == 1:
        skater_positions_final = getContents(skater_contents_dict, i)
    if i == 2:
        skater_teams_final = getContents(skater_contents_dict, i)
    if i == 3:
        skater_opponents_final = getContents(skater_contents_dict, i)
    if i == 4:
        skater_projections_final = getContents(skater_contents_dict, i)
    if i == 5:
        skater_salaries_final = getContents(skater_contents_dict, i)
    if i == 6:
        skater_values_final = getContents(skater_contents_dict, i)
    if i == 7:
        skater_shots_final = getContents(skater_contents_dict, i)
    if i == 8:
        skater_goals_final = getContents(skater_contents_dict, i)
    if i == 9:
        skater_assists_final = getContents(skater_contents_dict, i)
    if i == 10:
        skater_points_final = getContents(skater_contents_dict, i)
    if i == 11:
        skater_ppg_final = getContents(skater_contents_dict, i)
    if i == 12:
        skater_ppa_final = getContents(skater_contents_dict, i)
    if i == 13:
        skater_plusminus_final = getContents(skater_contents_dict, i)
    if i == 14:
        skater_blocks_final = getContents(skater_contents_dict, i)
    if i == 15:
        skater_mins_final = getContents(skater_contents_dict, i)
    if i == 16:
        skater_pim_final = getContents(skater_contents_dict, i)


def populateColumn(columnName, data):
    temp_df = pd.DataFrame()
    temp_df[columnName] = data
    temp_df[columnName] = temp_df[columnName].astype(str)
    temp_df[columnName] = temp_df[columnName].apply(lambda x: x.replace('\\t', '').replace(
        '\\n', '').replace('\'', '').replace('[', '').replace(']', '').strip())
    return temp_df[columnName]


skater_df = pd.DataFrame()

skater_df['Name'] = populateColumn('Name', skater_names_final)
skater_df['Position'] = populateColumn('Position', skater_positions_final)
skater_df['Team'] = populateColumn('Team', skater_teams_final)
skater_df['Opponent'] = populateColumn('Opponent', skater_opponents_final)
skater_df['Projection'] = populateColumn(
    'Projection', skater_projections_final)
skater_df['Salary'] = populateColumn('Salary', skater_salaries_final)
skater_df['Value'] = populateColumn('Value', skater_values_final)
skater_df['Shots'] = populateColumn('Shots', skater_shots_final)
skater_df['Goals'] = populateColumn('Goals', skater_goals_final)
skater_df['Assists'] = populateColumn('Assists', skater_assists_final)
skater_df['Points'] = populateColumn('Points', skater_points_final)
skater_df['PPG'] = populateColumn('PPG', skater_ppg_final)
skater_df['PPA'] = populateColumn('PPA', skater_ppa_final)
skater_df['+/-'] = populateColumn('+/-', skater_plusminus_final)
skater_df['Blocks'] = populateColumn('Blocks', skater_blocks_final)
skater_df['Minutes'] = populateColumn('Minutes', skater_mins_final)
skater_df['PIM'] = populateColumn('PIM', skater_pim_final)

skater_df.to_csv(
    'c:\dev\Python\Repos\dfs-model\\numberfire_fanduel_skaters.csv')
