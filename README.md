
# NFL Win Probability via Monte Carlo Simulation

This repository contains a Python-based analytical framework for estimating NFL team win probabilities using historical performance data and Monte Carlo simulation techniques. The project leverages game statistics from 2010 to 2023 to model and simulate matchups between teams, providing insights into expected outcomes and implied betting odds.

## Overview

The analysis is structured around the following core components:

- **Data Acquisition**: Scrapes team-level game logs from Pro Football Reference.
- **Data Cleaning**: Preprocesses raw data, including outcome encoding and time-of-possession conversion.
- **Feature Selection**: Identifies variables most correlated with game outcomes.
- **Simulation**: Performs Monte Carlo simulations to estimate win probabilities based on selected features.
- **Visualization**: Displays distributions of key performance metrics.
- **Betting Odds Calculation**: Converts win probabilities into implied betting odds.

## Repository Structure

```
NFL-Win-Probability-via-Monte-Carlo-Simulation/
│
├── main.py           # Main script containing all functions and execution logic
├── nfl_stats.csv     # Cached dataset (auto-generated if not present)
├── README.md         # Project documentation
```

## Requirements

- Python 3.8 or higher
- Required packages:

```bash
pip install pandas numpy matplotlib requests
```

## Usage

1. **Configure Parameters**: Update the following variables in the `main()` function:

```python
file_path = 'C:\Users\John Mulready\Downloads\nfl_stats.csv'
TEAM1 = 'KAN'
TEAM2 = 'NWE'
YEAR_P = (2021, 2022, 2023)
```

2. **Run the Script**:

```bash
python main.py
```

3. **Output**:
- Win probabilities for each team based on selected features
- Implied betting odds
- Distribution plots for key variables

## Methodology

- **Monte Carlo Simulation**: For each selected feature, the model randomly samples values from each team's historical distribution and compares them across 10,000 iterations.
- **Feature Selection**: Correlation analysis is used to identify the top three predictors of game outcomes.
- **Betting Odds**: Probabilities are converted using standard implied odds formulas.

## Example Output

```
Monte Carlo Simulation Results:
Win Probability for KAN based on Total Yards: 62.45%
Win Probability for the Opponent based on Total Yards: 37.55%

Project Results:
Win Probability for KAN: 64.12%. Therefore the betting odds are -178.6
Win Probability for NWE: 35.88%. Therefore the betting odds are +179.0
```

## Notes

- The script includes a delay between web requests to comply with data source usage policies.
- If the dataset already exists locally, scraping is skipped to improve efficiency.
