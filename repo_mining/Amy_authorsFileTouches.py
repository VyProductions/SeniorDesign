import json
import requests
import csv

import os

if not os.path.exists("data"):
    os.makedirs("data")

# GitHub Authentication function
def github_auth(url, lsttoken, ct):
    jsonData = None
    try:
        ct = ct % len(lsttoken)
        headers = {'Authorization': 'Bearer {}'.format(lsttoken[ct])}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        ct += 1
    except Exception as e:
        print(e)
    return jsonData, ct

# # @dictFiles, empty dictionary of files
# @lstTokens, GitHub authentication tokens
# @repo, GitHub repoollects authors and dates for each file touched by commits
def collect_file_touches(dictfiles, lsttokens, repo):
    ipage = 1  # url page counter
    ct = 0  # token counter

    try:
        # loop though all the commit pages until the last returned empty page
        while True:
            spage = str(ipage)
            commitsUrl = f'https://api.github.com/repos/{repo}/commits?page={spage}&per_page=100'
            jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)

            # break out of the while loop if there are no more commits in the pages
            if len(jsonCommits) == 0:
                break
            
            # iterate through the list of commits in the page
            for shaObject in jsonCommits:
                sha = shaObject['sha']
                # For each commit, use the GitHub commit API to extract the files touched by the commit
                shaUrl = f'https://api.github.com/repos/{repo}/commits/{sha}'
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)
                
                commit_author = shaDetails['commit']['author']['name']
                commit_date = shaDetails['commit']['author']['date']
                filesjson = shaDetails['files']
                
                for filenameObj in filesjson:
                    filename = filenameObj['filename']
                    if filename not in dictfiles:
                        dictfiles[filename] = []
                    dictfiles[filename].append((commit_author, commit_date))
                    print(filename, commit_author, commit_date)
            
            ipage += 1
    except Exception as e:
        print("Error receiving data:", e)
        exit(0)

# GitHub repo
repo = 'scottyab/rootbeer'
# repo = 'Skyscanner/backpack' # This repo is commit heavy. It takes long to finish executing
# repo = 'k9mail/k-9' # This repo is commit heavy. It takes long to finish executing
# repo = 'mendhak/gpslogger'

# put your tokens here
# Remember to empty the list when going to commit to GitHub.
# Otherwise they will all be reverted and you will have to re-create them
# I would advise to create more than one token for repos with heavy commits
lstTokens = ["lol_shjCPSicu3TEjgbCXTiqdRmIpEQAEnaw7yP6"]

dictfiles = dict()
collect_file_touches(dictfiles, lstTokens, repo)
print('Total number of files:', len(dictfiles))

file = repo.split('/')[1]
# change this to the path of your file
fileOutput = f'data/file_{file}_touches.csv'
rows = ["Filename", "Author", "Date"]
fileCSV = open(fileOutput, 'w', newline='')
writer = csv.writer(fileCSV)
writer.writerow(rows)

for filename, touches in dictfiles.items():
    for author, date in touches:
        rows = [filename, author, date]
        writer.writerow(rows)

fileCSV.close()
print(f'File touches data written to {fileOutput}')
