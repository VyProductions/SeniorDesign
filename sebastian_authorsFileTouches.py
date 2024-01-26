import requests
import json
import csv
import os

repo = 'scottyab/rootbeer'

def github_auth(url, lstTokens, ct):
    jsonData = None
    try:
        ct = ct % len(lstTokens)
        headers = {'Authorization': 'Bearer {}'.format(lstTokens[ct])}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        ct += 1
    except Exception as e:
        print(e)
    return jsonData, ct

def get_source_files(repo, lstTokens):
    files = []
    ct = 0
    url = f'https://api.github.com/repos/{repo}/git/trees/master?recursive=1'
    jsonData, ct = github_auth(url, lstTokens, ct)
    if jsonData:
        for file in jsonData['tree']:
            if file['type'] == 'blob' and file['path'].endswith(('.py', '.js', '.java', '.cpp', '.c', '.kt')):
                files.append(file['path'])
    return files

def get_commit_history(file, repo, lstTokens):
    commit_history = []
    ct = 0
    url = f'https://api.github.com/repos/{repo}/commits?path={file}'
    jsonData, ct = github_auth(url, lstTokens, ct)
    if jsonData:
        for commit in jsonData:
            author = commit['commit']['author']['name']
            date = commit['commit']['author']['date']
            commit_history.append((author, date))
    return commit_history

def main():
    lstTokens = [""]
    fileOutput = 'data/file_' + repo.split('/')[1] + '.csv'

    if not os.path.exists('data'):
        os.makedirs('data')

    source_files = get_source_files(repo, lstTokens)

    with open(fileOutput, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['File Name', 'Author', 'Date'])

        for file in source_files:
            commit_history = get_commit_history(file, repo, lstTokens)
            for author, date in commit_history:
                writer.writerow([file, author, date])

if __name__ == "__main__":
    main()
