# County Screener

A Python script that pulls US Census data for any state based on a zip code and ranks counties by median home value.

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

## How it works
- Enter any US zip code
- Looks up the city, state, and coordinates using Zippopotam.us
- Converts the state to a FIPS code and pulls county data from the US Census API
- Saves results to counties.csv and counties.db
- Prints the top 5 counties by median home value

## Output columns
- name: County name
- population: Total population (Census ACS 2022)
- median_home_value: Median home value in dollars
- median_household_income: Median household income in dollars
- median_age: Median age of residents
