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

def get_Author_Date(repo, lsttokens, filename):
    authors_and_dates = []
    page = 1 # Url Page Counter
    ct = 0 # Token Counter 

    while True:
        spage = str(page) # Change page variable to a string
        commitsUrl = f'https://api.github.com/repos/{repo}/commits?path={filename}&page={spage}&per_page=100'
        jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)

        # break out of the while loop if there are no more commits in the pages
        if len(jsonCommits) == 0:
            break
        # iterate through the list of commits in spage *SHA is a unique id given to each commit
        for shaObject in jsonCommits:
            author_name = shaObject['commit']['author']['name']
            date = shaObject['commit']['author']['date']
            authors_and_dates.append([filename, author_name, date])
        page += 1
    return authors_and_dates

# GitHub repo
repo = 'scottyab/rootbeer'
# repo = 'Skyscanner/backpack' # This repo is commit heavy. It takes long to finish executing
# repo = 'k9mail/k-9' # This repo is commit heavy. It takes long to finish executing
# repo = 'mendhak/gpslogger'


# put your tokens here
# Remember to empty the list when going to commit to GitHub.
# Otherwise they will all be reverted and you will have to re-create them
# I would advise to create more than one token for repos with heavy commits
lstTokens = ["Enter_your_lstToken"]
#"16ce529bdb32263fb90a392d38b5f53c7ecb6b",
#"8cea5715051869e98044f38b60fe897b350d4a"

all_authors_and_dates = [] # Stores all authors and dates of all files (list of dictionaries)

reponame = repo.split('/')[1]
rfilename = f'data/file_{reponame}.csv' # File we want to read from
with open(rfilename, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        all_authors_and_dates.extend(get_Author_Date(repo, lstTokens, row["Filename"]))

csv_file.close()

#print(authors_dates)

wfileOutput = f'data/file_autors_dates_{reponame}.csv'
fields = ['File', 'Author', 'Date']
with open(wfileOutput, 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(fields)
    writer.writerows(all_authors_and_dates)

csv_file.close()
# file = repo.split('/')[1]
# # change this to the path of your file
# fileOutput = 'data/file_' + file + '.csv'
# rows = ["Filename", "Touches"]
# fileCSV = open(fileOutput, 'w')
# writer = csv.writer(fileCSV)
# writer.writerow(rows)

# fileCSV.close()
