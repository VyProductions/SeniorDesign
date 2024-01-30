import requests
import json
import csv
import os

repo = 'scottyab/rootbeer'
# repo = 'Skyscanner/backpack' # This repo is commit heavy. It takes long to finish executing
# repo = 'k9mail/k-9' # This repo is commit heavy. It takes long to finish executing
# repo = 'mendhak/gpslogger'

def github_auth(url, lstTokens, ct):
    jsonData = None
    try:
        ct = ct % len(lstTokens) # To alternate tokens from lstTokens array
        headers = {'Authorization': 'Bearer {}'.format(lstTokens[ct])}
        # This Does the API Call
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        ct += 1
    except Exception as e:
        print(e)
    return jsonData, ct

def get_source_files(repo, lstTokens):
    files = set()
    ct = 0
    page = 1
    while True:
        commitsUrl = f'https://api.github.com/repos/{repo}/commits?page={page}&per_page=100'
        jsonData, ct = github_auth(commitsUrl, lstTokens, ct)

        # Break the loop if there is no more data
        if not jsonData:
            break

        # Process each commit
        for commit in jsonData:
            sha = commit['sha']
            commitUrl = f'https://api.github.com/repos/{repo}/commits/{sha}'
            commitData, ct = github_auth(commitUrl, lstTokens, ct)

            # Check if 'files' key is in the commit data
            if 'files' in commitData:
                # Process each file in each commit
                for file in commitData['files']:
                    filename = file['filename']
                    # Check if the file matches the desired types
                    if filename.endswith(('.py', '.js', '.java', '.cpp', '.c', '.kt', '.ts', '.css', '.scss')):
                        files.add(filename)

        # Increment the page number to get the next page of commits
        page += 1

    return list(files)

# getting commit history for each file
def get_commit_history(file, repo, lstTokens):
    commit_history = []
    ct = 0
    url = f'https://api.github.com/repos/{repo}/commits?path={file}'
    jsonData, ct = github_auth(url, lstTokens, ct)
    
    # Checks if not empty
    if jsonData:
        for commit in jsonData:
            # gets author and date
            author = commit['commit']['author']['name']
            date = commit['commit']['author']['date']
            commit_history.append((author, date))
    return commit_history

if __name__ == "__main__":
    ## IMPORTANT: Do not include actual tokens when pushing to your Repository.
    lstTokens = [""]
    fileOutput = 'data/file_' + repo.split('/')[1] + '.csv'

    if not os.path.exists('data'):
        os.makedirs('data')

    source_files = get_source_files(repo, lstTokens)

    print(f'The unique source files count: {len(source_files)}')
    for f in source_files:
        print(f)

    with open(fileOutput, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['File Name', 'Author', 'Date'])

        for file in source_files:
            commit_history = get_commit_history(file, repo, lstTokens)
            # for each file we get each author with the Date. 
            # for each author per file we write file. 
            for author, date in commit_history:
                writer.writerow([file, author, date])
