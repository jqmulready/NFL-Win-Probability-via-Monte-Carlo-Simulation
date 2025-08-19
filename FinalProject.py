"""NFL Win Probability Analysis"""

import os
import random
import time
import pandas as pd
import requests
import numpy as np
import matplotlib.pyplot as plt

def scrape_nfl_data(file_path):
    '''Function to scrape NFL data and save it to a CSV file'''
    if not os.path.isfile(file_path):
        seasons = [str(season) for season in range(2010, 2024)]
        team_abbrs = [
            'crd', 'atl', 'rav', 'buf', 'car', 'chi', 'cin', 'cle', 'dal', 'den',
            'det', 'gnb', 'htx', 'clt', 'jax', 'kan', 'sdg', 'ram', 'mia', 'min',
            'nwe', 'nor', 'nyg', 'nyj', 'rai', 'phi', 'pit', 'sfo', 'sea', 'tam', 'oti',
            'was'
        ]
        
        nfl_df = pd.DataFrame()
        
        for season in seasons:
            for team in team_abbrs:
                url = 'https://www.pro-football-reference.com/teams/' + team + '/' + season + '/gamelog/'
                off_df = pd.read_html(url, header=1, attrs={'id': 'gamelog' + season})[0]
                def_df = pd.read_html(url, header=1, attrs={'id': 'gamelog_opp' + season})[0]
                team_df = pd.concat([off_df, def_df], axis=1)
                team_df.insert(loc=0, column='Season', value=season)
                team_df.insert(loc=2, column='Team', value=team.upper())
                nfl_df = pd.concat([nfl_df, team_df], ignore_index=True)
                time.sleep(random.randint(4, 5))
                
        nfl_df = nfl_df.rename(columns={'Unnamed: 4': 'Outcome'})
        nfl_df = nfl_df.rename(columns={'Unnamed: 6': 'Home/Away'})
        nfl_df.to_csv(file_path, index=False)
    else:
        print("File already exists. Skipping data scraping.")

def clean_up_data(nfl_df):
    '''Function to clean up NFL data'''
    nfl_df['Outcome'] = nfl_df['Outcome'].map({'W': 1, 'L': 0})
    nfl_df['ToP'] = nfl_df['ToP'].str.split(':').apply(lambda x: int(x[0]) * 60 + int(x[1]) if isinstance(x, list) and len(x) == 2 else 0)
    
    return nfl_df

def get_categories(nfl_df):
    '''Function to get unique categories for 'Day' and 'Home/Away' columns'''
    day_categories = nfl_df['Day'].astype('category').cat.categories
    homeaway_categories = nfl_df['Home/Away'].astype('category').cat.categories
    
    print('Day codes and their categories:')
    for code, category in enumerate(day_categories):
        print(f'Code {code}: {category}')
    
    print('Home/Away codes and their categories:')
    for code, category in enumerate(homeaway_categories):
        print(f'Code {code}: {category}')

def calculate_correlation(nfl_df):
    '''Function to calculate correlation of numerical variables with 'Outcome''''
    nfl_data_numeric = nfl_df.select_dtypes(include=[np.number])
    nfl_data_corr = nfl_data_numeric.corr()['Outcome'].sort_values(ascending=False)
    
    return nfl_data_corr

def plot_distribution(team_data, variable, team_name, year):
    '''Function to plot the distribution of a variable for a team in a specific year'''
    plt.figure(figsize=(10, 6))
    plt.hist(team_data[variable], bins=20, density=True, alpha=0.6, color='g')
    plt.title(f'Probability Distribution of {variable} by {team_name} in {year}')
    plt.xlabel(f'{variable}')
    plt.ylabel('Probability')
    plt.show()

def monte_carlo_simulation(team1_data, team2_data, variable, num_simulations):
    '''Function to perform Monte Carlo simulation for a given variable and teams'''
    simulation_results = []
    for _ in range(num_simulations):
        simulated_team1 = [np.random.choice(team1_data[variable])]
        simulated_team2 = [np.random.choice(team2_data[variable])]
        outcome = 1 if simulated_team1[0] > simulated_team2[0] else 0
        simulation_results.append(outcome)

    return simulation_results

def display_simulation_results(win_probability, team_name, variable):
    '''Function to display Monte Carlo simulation results'''
    print(f"Monte Carlo Simulation Results:")
    print(f"Win Probability for {team_name} based on {variable}: {win_probability * 100:.2f}%")
    print(f"Win Probability for the Opponent based on {variable}: {(1 - win_probability) * 100:.2f}%")

def main():
    '''Main function'''
    file_path = 'C:\\Users\\John Mulready\\Downloads\\nfl_stats.csv'
    TEAM1 = 'KAN'
    TEAM2 = 'NWE'
    YEAR_P = (2021,2022,2023)
    
    scrape_nfl_data(file_path)
    
    nfl_df = pd.read_csv(file_path)
    nfl_df = clean_up_data(nfl_df)
    
    get_categories(nfl_df)
    
    nfl_data_corr = calculate_correlation(nfl_df)
    
    top_variable = (nfl_data_corr.index[1], nfl_data_corr.index[2], nfl_data_corr.index[3])
    
    team1_data = nfl_df[(nfl_df['Team'] == TEAM1) & (nfl_df['Season'].isin(YEAR_P))]
    team2_data = nfl_df[(nfl_df['Team'] == TEAM2) & (nfl_df['Season'].isin(YEAR_P))]
    
    
    for variable in top_variable:
        plot_distribution(team1_data, variable, TEAM1, YEAR_P)
    
    num_simulations = 10000
    overall_results = []
    
    for variable in top_variable:
        simulation_results = monte_carlo_simulation(team1_data, team2_data, variable, num_simulations)
        win_probability = np.mean(simulation_results)
        display_simulation_results(win_probability, TEAM1, variable)
        overall_results.append(win_probability)
    
    team1_prob = np.mean(overall_results) * 100
    team2_prob = (1 - np.mean(overall_results)) * 100
    team1_odds = (team1_prob/(1-(team1_prob/100)))*-1 if team1_prob > 50 else (100/(team1_prob/100)-100)
    team2_odds = (team2_prob/(1-(team2_prob/100)))*-1 if team2_prob > 50 else (100/(team2_prob/100)-100)


    print(f"Project Results:")
    print(f"Win Probability for {TEAM1}: {team1_prob}%. Therefore the betting odds are {team1_odds}")
    print(f"Win Probability for {TEAM2}: {team2_prob}%. Therefore the betting odds are {team2_odds}")


main()
