import json
import requests
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from collections import defaultdict

import os

if not os.path.exists("data"):
 os.makedirs("data")

author_week_files = defaultdict(lambda: defaultdict(int))

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

# @dictFiles, empty dictionary of files
# @lstTokens, GitHub authentication tokens
# @repo, GitHub repo
def countfiles(dictfiles, lsttokens, repo):
    ipage = 1  # url page counter
    ct = 0  # token counter
    first_commit_date = None  # Initialize the date of the first commit

    # loop though all the commit pages until the last returned empty page
    while True:
        spage = str(ipage)
        commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?page=' + spage + '&per_page=100'
        jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)

        # break out of the while loop if there are no more commits in the pages
        if len(jsonCommits) == 0:
            break

        # Sort the commits by date
        sorted_commits = sorted(jsonCommits, key=lambda x: datetime.strptime(x['commit']['author']['date'], "%Y-%m-%dT%H:%M:%SZ"))

        # Update the date of the first commit
        for shaObject in sorted_commits:
            date = datetime.strptime(shaObject['commit']['author']['date'], "%Y-%m-%dT%H:%M:%SZ")
            if first_commit_date is None or date < first_commit_date:
                first_commit_date = date

        # iterate through the list of commits in  spage
        for shaObject in sorted_commits:
            sha = shaObject['sha']
            author = shaObject['commit']['author']['name']
            date = datetime.strptime(shaObject['commit']['author']['date'], "%Y-%m-%dT%H:%M:%SZ")

            # Calculate the number of weeks since the first commit
            weeks = (date - first_commit_date).days // 7
                
            # For each commit, use the GitHub commit API to extract the files touched by the commit
            shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha
            shaDetails, ct = github_auth(shaUrl, lsttokens, ct)
            filesjson = shaDetails['files']
            for filenameObj in filesjson:
                filename = filenameObj['filename']
                if filename.endswith('.java') or filename.endswith('.cpp') or filename.endswith('.xml'):
                    if filename not in dictfiles:
                        dictfiles[filename] = []
                    dictfiles[filename].append((author, weeks))

        ipage += 1  # increment the page counter to get the next page of commits

# GitHub repo
repo = 'scottyab/rootbeer'
# repo = 'Skyscanner/backpack' # This repo is commit heavy. It takes long to finish executing
# repo = 'k9mail/k-9' # This repo is commit heavy. It takes long to finish executing
# repo = 'mendhak/gpslogger'


# put your tokens here
# Remember to empty the list when going to commit to GitHub.
# Otherwise they will all be reverted and you will have to re-create them
# I would advise to create more than one token for repos with heavy commits
lstTokens = ["ghp_PJx6h9sdaffdwckl9sadfasqPdfGDYC90eafoirXI26o0Sg04g",
                "ghp_qYnsadfwM3IS5nVRLHHSQcG4dsfafdasQycPWnXwgU1MSK8B",
                "ghp_2SVVxdP4PdPiOmucvtNbuDLxsdfsdfe76XPJ1pArNr"]

dictfiles = dict()
countfiles(dictfiles, lstTokens, repo)

for filename, data in dictfiles.items():
    # Iterate over each (author, week) pair in data
    for author, week in data:
        # Increment the number of files touched by this author in this week
        author_week_files[author][week] += 1

for author, week_files in author_week_files.items():
    weeks = list(week_files.keys())
    files = list(week_files.values())
    plt.scatter(weeks, files, label=author)

plt.xlabel('Weeks')
plt.ylabel('Number of Files')
plt.title('Number of Files Touched by Each Author per Week')

plt.savefig('plot.png')