import pandas as pd
import numpy as np

# Load data (ensure CSV has 'team' column)
tables = pd.read_csv('pl-tables-1993-2024.csv')

# Get number of simulations from user
n_simulations = int(input("Enter number of simulations: "))

# Initialize results dictionary
results = {
    'Team': [],
    'Wins': [],
    'Relegations': [],
    'Total Points': [],
    'Appearances': []
}

# Run simulations
for _ in range(n_simulations):
    # Sample 20 distinct teams randomly
    season = tables.sample(n=20, replace=False)
    
    # Sort by points, GD, GF (Premier League tiebreakers)
    season = season.sort_values(
        by=['points', 'gd', 'gf'], 
        ascending=[False, False, False]
    )
    
    # Assign final positions
    season = season.assign(final_position=range(1, 21))
    
    # Update results for each team in this season
    for team in season['team'].unique():
        team_data = season[season['team'] == team].iloc[0]
        
        if team not in results['Team']:
            results['Team'].append(team)
            results['Wins'].append(0)
            results['Relegations'].append(0)
            results['Total Points'].append(0)
            results['Appearances'].append(0)
        
        idx = results['Team'].index(team)
        results['Appearances'][idx] += 1
        results['Total Points'][idx] += team_data['points']
        
        if team_data['final_position'] == 1:
            results['Wins'][idx] += 1
        elif team_data['final_position'] >= 18:
            results['Relegations'][idx] += 1

# Create results DataFrame
results_df = pd.DataFrame({
    'Team': results['Team'],
    'Wins': results['Wins'],
    'Relegations': results['Relegations'],
    'Avg Points': [
        tp / app 
        for tp, app in zip(results['Total Points'], results['Appearances'])
    ]
})

# Sort by wins then relegations (descending importance)
results_df = results_df.sort_values(
    by=['Wins', 'Relegations'], 
    ascending=[False, True]
)

# Display results
print(f"\nSimulation Results ({n_simulations} seasons):")
print(results_df.reset_index(drop=True))