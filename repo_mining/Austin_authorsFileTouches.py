import json
import requests
import csv
import os
from datetime import datetime

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def github_auth(url, tokens, current_token_index):
    try:
        current_token_index %= len(tokens)
        headers = {'Authorization': 'Bearer {}'.format(tokens[current_token_index])}
        response = requests.get(url, headers=headers)
        json_data = json.loads(response.content)
        current_token_index += 1
        return json_data, current_token_index
    except Exception as e:
        print(e)
        return None, current_token_index

def collect_authors_and_dates(repo, filename, touches, tokens):
    all_authors_dates = []

    for page in range(1, (touches // 100) + 2):
        commits_url = f'https://api.github.com/repos/{repo}/commits?path={filename}&page={page}&per_page=100'
        json_commits, _ = github_auth(commits_url, tokens, 0)

        if not json_commits:
            break

        for commit_object in json_commits:
            author_name = commit_object['commit']['author']['name']
            commit_date_str = commit_object['commit']['author']['date']
            commit_date = datetime.strptime(commit_date_str, '%Y-%m-%dT%H:%M:%SZ')

            all_authors_dates.append({'filename': filename, 'author': author_name, 'date': commit_date})

    return all_authors_dates

def save_sorted_authors_and_dates(all_authors_dates, output_file):
    all_authors_dates.sort(key=lambda x: x['date'])

    rows = ["Filename", "Author", "Date"]
    with open(output_file, 'w', newline='') as file_csv:
        writer = csv.writer(file_csv)
        writer.writerow(rows)

        for entry in all_authors_dates:
            rows = [entry['filename'], entry['author'], entry['date'].strftime('%Y-%m-%d')]
            writer.writerow(rows)

    print(f"The sorted author and date information has been saved to {output_file}")

def main():
    create_directory("data")

    # GitHub repository and tokens
    repo = 'scottyab/rootbeer'  # Replace with your repository
    tokens = [""]  # Replace with your tokens

    # File created by CollectFiles.py
    csv_file = 'data/file_src_rootbeer.csv'

    # Execute the functions to get authors, dates, and save the sorted information into a CSV file
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        all_authors_dates = []

        for row in reader:
            filename = row['Filename']
            touches = int(row['Touches'])

            print(f"Collecting authors and dates for {filename}...")
            authors_dates = collect_authors_and_dates(repo, filename, touches, tokens)
            all_authors_dates.extend(authors_dates)

    output_file = 'data/file_authors_dates_sorted.csv'
    save_sorted_authors_and_dates(all_authors_dates, output_file)

if __name__ == "__main__":
    main()
