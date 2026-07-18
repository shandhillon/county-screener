import os
from dotenv import load_dotenv
load_dotenv()
import csv
import requests
import time

zip_code = "95148"
response = requests.get(f"https://api.zippopotam.us/us/{zip_code}")
data = response.json()

state = data["places"][0]["state"]
longitude = data["places"][0]["longitude"]
latitude = data["places"][0]["latitude"]
city = data["places"][0]["place name"]

print(f"State: {state}")
print(f"Longitude: {longitude}")
print(f"latitude: {latitude}")
print(f"City: {city}")
try:
    api_key = os.getenv("CENSUS_API_KEY")

    response2 = requests.get(
        f"https://api.census.gov/data/2022/acs/acs5?get=NAME,B01003_001E,B25077_001E,B19013_001E,B01002_001E&for=county:*&in=state:06&key={api_key}")
    data2 = response2.json()


    countyname = data2[1][0]
    print(f"County name: {countyname}")
    population = data2[1][1]
    print(f"Population: {population}")

    with open("counties.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "population", "median_home_value", "median_household_income", "median_age"])
        for county in data2[1:]:
            if "-666666666" in [county[1], county[2], county[3], county[4]]:
                print(f"Skipping {county[0]} -- missing data")
                continue
            writer.writerow([county[0], county[1], county[2], county[3], county[4]])
except: print("something went wrong, skipping")

counties_list = data2[1:]
sorted_counties = sorted(counties_list, key=lambda x: int(x[2]), reverse=True)

print("\nTop 5 Counties by Median Home Value:")
for county in sorted_counties[:5]:
    print(f"{county[0]}: ${county[2]}")





