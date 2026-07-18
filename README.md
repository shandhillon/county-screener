# Archer Oaks Week 1 — County Screener v0

## What it does
This script pulls public data about all California counties using the Zippopotam.us API
and the US Census API. It outputs a ranked list of counties by median home value and
writes the results to a CSV file.

## How to run it
1. Make sure Python 3 is installed
2. Install the requests library: pip install requests
3. Run the script: python screener.py

## Output
The script produces a file called counties.csv with the following columns:

- name: County name
- population: Total population (Census ACS 2022)
- median_home_value: Median home value in dollars (Census ACS 2022)
- median_household_income: Median household income in dollars (Census ACS 2022)
- median_age: Median age of residents (Census ACS 2022)

## Top 5 Counties by Median Home Value
1. San Mateo County — $1,441,300
2. San Francisco County — $1,348,700
3. Santa Clara County — $1,316,800
4. Marin County — $1,291,800
5. Alameda County — $999,200