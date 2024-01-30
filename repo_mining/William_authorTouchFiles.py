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
        ct = ct % len(lstTokens)
        headers = {'Authorization': 'Bearer {}'.format(lsttoken[ct])}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        ct += 1
    except Exception as e:
        pass
        print(e)
    return jsonData, ct

# extract date from string
def get_date(datestring):
    try:
        date_vals = datestring.split('T')[0].split('-')
        return {
            'year': int(date_vals[0]),
            'month': int(date_vals[1]),
            'day': int(date_vals[2])
        }
    except:
        print("Invalid date string.")

# @dictFiles, empty dictionary of files
# @lstTokens, GitHub authentication tokens
# @repo, GitHub repo
def countfiles(dictfiles, lsttokens, repo):
    ipage = 1  # url page counter
    ct = 0  # token counter

    try:
        # loop though all the commit pages until the last returned empty page
        while True:
            spage = str(ipage)
            commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?page=' + spage + '&per_page=100'
            jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)

            # break out of the while loop if there are no more commits in the pages
            if len(jsonCommits) == 0:
                break
            # iterate through the list of commits in  spage
            for shaObject in jsonCommits:
                sha = shaObject['sha']
                # For each commit, use the GitHub commit API to extract the files touched by the commit
                shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)
                
                modifyDate = get_date(shaDetails['commit']['author']['date'])
                author = shaDetails['commit']['author']['name']
                
                filesjson = shaDetails['files']
                for filenameObj in filesjson:
                    filename = filenameObj['filename']
                    extension = filename.split('.')[-1]
                    if extension == 'java':
                        print('File: %s\n  Modified: %s\n  Author: %s' % (filename, str(modifyDate['year']) + '/' + str(modifyDate['month']) + '/' + str(modifyDate['day']), author))
                        if dictfiles.get(filename):
                            dictfiles[filename]['authors'].append(author)
                            dictfiles[filename]['dates'].append(str(modifyDate['year']) + '/' + str(modifyDate['month']) + '/' + str(modifyDate['day']))
                        else:
                            dictfiles[filename] = {
                                'authors': [author],
                                'dates': [str(modifyDate['year']) + '/' + str(modifyDate['month']) + '/' + str(modifyDate['day'])]
                            }
            ipage += 1
    except:
        print("Error receiving data")
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
lstTokens = ["12345"]

dictfiles = dict()
countfiles(dictfiles, lstTokens, repo)

file = repo.split('/')[1]

# change this to the path of your file
fileOutput = 'data/file_' + file + '_commits.csv'
rows = ["Filename", "Author", "Date"]
fileCSV = open(fileOutput, 'w')
writer = csv.writer(fileCSV)
writer.writerow(rows)

for filename, info in dictfiles.items():
    for i in range(len(info['authors'])):
        rows = [filename, info['authors'][i], info['dates'][i]]
        writer.writerow(rows)

fileCSV.close()
