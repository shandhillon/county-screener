# Archer Oaks — County Screener

## Setup
1. Clone the repo
2. Install dependencies:
   pip install requests python-dotenv
3. Copy .env.example to .env:
   cp .env.example .env
4. Add your Census API key to .env:
   CENSUS_API_KEY=your_key_here
5. Run the script:
   python Week1.py

## What it does
Pulls public data for all California counties using the US Census API
and ranks them by median home value. Also looks up city/state info
for a zip code using Zippopotam.us.

## Output
Produces counties.csv with these columns:
- name: County name
- population: Total population (Census ACS 2022)
- median_home_value: Median home value in dollars
- median_household_income: Median household income in dollars
- median_age: Median age of residents

## Top 5 Counties by Median Home Value
1. San Mateo County — $1,441,300
2. San Francisco County — $1,348,700
3. Santa Clara County — $1,316,800
4. Marin County — $1,291,800
5. Alameda County — $999,200
