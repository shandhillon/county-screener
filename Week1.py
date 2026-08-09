import os
from dotenv import load_dotenv
load_dotenv()
import csv
import requests

STATE_FIPS = {
    "AL": "01", "AK": "02", "AZ": "04", "AR": "05",
    "CA": "06", "CO": "08", "CT": "09", "DE": "10",
    "DC": "11", "FL": "12", "GA": "13", "HI": "15",
    "ID": "16", "IL": "17", "IN": "18", "IA": "19",
    "KS": "20", "KY": "21", "LA": "22", "ME": "23",
    "MD": "24", "MA": "25", "MI": "26", "MN": "27",
    "MS": "28", "MO": "29", "MT": "30", "NE": "31",
    "NV": "32", "NH": "33", "NJ": "34", "NM": "35",
    "NY": "36", "NC": "37", "ND": "38", "OH": "39",
    "OK": "40", "OR": "41", "PA": "42", "RI": "44",
    "SC": "45", "SD": "46", "TN": "47", "TX": "48",
    "UT": "49", "VT": "50", "VA": "51", "WA": "53",
    "WV": "54", "WI": "55", "WY": "56"
}

def get_location(zip_code):
    try:
        response = requests.get(f"https://api.zippopotam.us/us/{zip_code}")
        if response.status_code != 200:
            print(f"Zip code {zip_code} not found.")
            return None
        data = response.json()
        if not data.get("places"):
            print(f"No places found for zip code {zip_code}.")
            return None
        state = data["places"][0]["state"]
        state_abbr = data["places"][0]["state abbreviation"]
        longitude = data["places"][0]["longitude"]
        latitude = data["places"][0]["latitude"]
        city = data["places"][0]["place name"]
        return city, longitude, latitude, state, state_abbr
    except Exception as e:
        print(f"Error looking up zip code: {e}")
        return None

def is_valid_row(county):
    return "-666666666" not in [county[1], county[2], county[3], county[4]]

def get_county_data(api_key, state_fips):
    if not api_key:
        print("No API key found. Check your .env file.")
        return None
    try:
        census_response = requests.get(
            f"https://api.census.gov/data/2022/acs/acs5?get=NAME,B01003_001E,B25077_001E,B19013_001E,B01002_001E&for=county:*&in=state:{state_fips}&key={api_key}")
        census_data = census_response.json()
        return [census_data[0]] + [row for row in census_data[1:] if is_valid_row(row)]
    except Exception as e:
        print(f"something went wrong with Census API: {e}")
        return None

def write_csv(clean_data, filename="counties.csv"):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "population", "median_home_value", "median_household_income", "median_age"])
        for county in clean_data[1:]:
            writer.writerow([county[0], county[1], county[2], county[3], county[4]])

def save_to_db(clean_data):
    import sqlite3
    conn = sqlite3.connect("counties.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS counties (
            name TEXT,
            population INTEGER,
            median_home_value INTEGER,
            median_household_income INTEGER,
            median_age REAL,
            pulled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # one-time cleanup: rows inserted before this unique index existed may
    # already have duplicates by name; keep only the most recent per name
    cursor.execute("""
        DELETE FROM counties
        WHERE rowid NOT IN (SELECT MAX(rowid) FROM counties GROUP BY name)
    """)
    cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_counties_name ON counties(name)")
    for county in clean_data[1:]:
        cursor.execute("""
            INSERT INTO counties (name, population, median_home_value, median_household_income, median_age, pulled_at)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(name) DO UPDATE SET
                population = excluded.population,
                median_home_value = excluded.median_home_value,
                median_household_income = excluded.median_household_income,
                median_age = excluded.median_age,
                pulled_at = excluded.pulled_at
        """, (county[0], county[1], county[2], county[3], county[4]))
    conn.commit()
    conn.close()
    print("Saved to counties.db")

def main():
    zip_code = input("Enter a zip code: ")
    location = get_location(zip_code)
    if location is None:
        print("Could not look up zip code, stopping.")
        return
    city, longitude, latitude, state, state_abbr = location
    print(f"City: {city}")
    print(f"State: {state}")
    print(f"Longitude: {longitude}")
    print(f"Latitude: {latitude}")

    state_fips = STATE_FIPS.get(state_abbr)
    if state_fips is None:
        print(f"No FIPS code found for state: {state_abbr}")
        return

    api_key = os.getenv("CENSUS_API_KEY")
    clean_data = get_county_data(api_key, state_fips)

    if clean_data is None:
        print("No county data retrieved, stopping.")
        return

    write_csv(clean_data)
    save_to_db(clean_data)

    counties_list = clean_data[1:]
    sorted_counties = sorted(counties_list, key=lambda x: int(x[2]), reverse=True)
    print("\nTop 5 Counties by Median Home Value:")
    for county in sorted_counties[:5]:
        print(f"{county[0]}: ${county[2]}")

if __name__ == "__main__":
    main()