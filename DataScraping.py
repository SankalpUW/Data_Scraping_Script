from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
import os

all_teams = []  # list to store all teams

html = requests.get('https://fbref.com/en/comps/9/Premier-League-Stats').text  # getting the html from the website
soup = BeautifulSoup(html, 'lxml')
table = soup.find_all('table', class_='stats_table')[0]  # only want the first table, therefore the first index

links = table.find_all('a')  # finding all links in the table
links = [l.get("href") for l in links]  # parsing through links
links = [l for l in links if '/squads/' in l]  # filtering through links to only get squads

team_urls = [f"https://fbref.com{l}" for l in links]  # formatting back to links

for team_url in team_urls:
    team_name = team_url.split("/")[-1].replace("-Stats", "")  # isolating the names of the teams
    data = requests.get(team_url).text
    soup = BeautifulSoup(data, 'lxml')
    stats = soup.find_all('table', class_="stats_table")[0]  # again, only want the first table

    # Convert it into a DataFrame
    team_data = pd.read_html(str(stats))[0]
    team_data["Team"] = team_name
    all_teams.append(team_data)  # appending the data
    time.sleep(5)  # making sure we don't get blocked from scraping by delaying each loop by 5 seconds

stat_df = pd.concat(all_teams)  # concatenating all of the stats
print("Current working directory:", os.getcwd())
csv_file = "stats.csv"
stat_df.to_csv(csv_file, index=False)  # importing to csv

# # Automatically open the CSV file after saving
# if os.name == 'nt':  # For Windows
#     os.startfile(csv_file)
# elif os.name == 'posix':  # For macOS or Linux
#     os.system(f"open {csv_file}" if os.uname().sysname == 'Darwin' else f"xdg-open {csv_file}")