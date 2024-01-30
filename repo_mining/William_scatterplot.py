import json
import requests
import csv

import matplotlib.pyplot as plt
from datetime import date
import seaborn as sns

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
        return date(int(date_vals[0]), int(date_vals[1]), int(date_vals[2]))
    except:
        print("Invalid date string.")

# @dictFiles, empty dictionary of files
# @lstTokens, GitHub authentication tokens
# @repo, GitHub repo
def getcommits(commitlist, lsttokens, repo):
    ipage = 1  # url page counter
    ct = 0  # token counter
    
    repoUrl = 'https://api.github.com/repos/' + repo
    repoDetails, ct = github_auth(repoUrl, lsttokens, ct)
    createDate = get_date(repoDetails['created_at'])
    print('Repository Created: %s\n' % (createDate))

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
                        print('File: %s\n  Modified: %s\n  Author: %s' % (filename, modifyDate, author))
                        commitlist.append({
                            'filename': filename,
                            'author': author,
                            'date': modifyDate
                        })
            ipage += 1

        return createDate
    except:
        print("Error receiving data")
        exit(0)

plt.xlabel('file')
plt.ylabel('weeks')

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

commits = list()
authors = dict()
files   = dict()

originDate = getcommits(commits, lstTokens, repo)

for commit in commits:
    if not authors.get(commit['author']):
        authors[commit['author']] = len(authors)
    if not files.get(commit['filename']):
        files[commit['filename']] = len(files)

num_authors = len(authors)
num_files = len(files)

# Custom color mapping with 'num_authors' distinct colors
colors_dict = {
    value: sns.color_palette("hsv", n_colors=num_authors)[i] for i, value in enumerate(authors.keys())
}

plt.locator_params(axis='x', nbins=num_files)
plt.locator_params(axis='y', nbins=10)

for commit in commits:
    days = abs(commit['date'] - originDate).days
    weeks = (days + 6) // 7
    plt.scatter(files[commit['filename']], weeks, c=[[colors_dict[commit['author']]]], s=40)

plt.show()
