import json
import requests
import csv
import os
from datetime import datetime, timedelta

if not os.path.exists("data"):
    os.makedirs("data")

# GitHub Authentication function
def github_auth(url, lsttoken, ct):
    jsonData = None
    try:
        ct = ct % len(lstTokens)
        headers = {'Authorization': 'Bearer {}'.format(lsttoken[ct])}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        ct += 1
    except Exception as e:
        pass
        print(e)
    return jsonData, ct

# Function to get authors and dates for each file
def get_authors_for_files(lstTokens, csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        
        # List to store all authors, dates, and filenames
        all_authors_dates = []

        for row in reader:
            filename = row['Filename']
            touches = int(row['Touches'])

            print(f"Collecting authors and dates for {filename}...")

            # GitHub repo
            repo = 'scottyab/rootbeer'  # Replace with your repository

            # loop through all the commit pages for the file
            for page in range(1, (touches // 100) + 2):
                commits_url = f'https://api.github.com/repos/{repo}/commits?path={filename}&page={page}&per_page=100'
                json_commits, _ = github_auth(commits_url, lstTokens, 0)

                # break out of the loop if there are no more commits
                if not json_commits:
                    break

                # iterate through the list of commits
                for commit_object in json_commits:
                    author_name = commit_object['commit']['author']['name']
                    commit_date_str = commit_object['commit']['author']['date']
                    commit_date = datetime.strptime(commit_date_str, '%Y-%m-%dT%H:%M:%SZ')

                    all_authors_dates.append({'filename': filename, 'author': author_name, 'date': commit_date})

        # Sort the collected authors and dates by date in ascending order
        all_authors_dates.sort(key=lambda x: x['date'])

        # Save the sorted authors and dates into a CSV file
        csv_output_file = 'data/file_authors_dates_sorted.csv'
        rows = ["Filename", "Author", "Date"]
        with open(csv_output_file, 'w') as fileCSV:
            writer = csv.writer(fileCSV)
            writer.writerow(rows)

            for entry in all_authors_dates:
                rows = [entry['filename'], entry['author'], entry['date'].strftime('%Y-%m-%d')]
                writer.writerow(rows)

        print(f"The sorted author and date information has been saved to {csv_output_file}")

# put your tokens here
# Remember to empty the list when going to commit to GitHub.
# Otherwise, they will all be reverted, and you will have to re-create them
# I would advise creating more than one token for repos with heavy commits
lstTokens = [""]

# we are gonna use the file created by CollectFiles.py
csv_file = 'data/file_src_rootbeer.csv' 

# Execute the function to get authors, dates, and save the sorted information into a CSV file
get_authors_for_files(lstTokens, csv_file)

