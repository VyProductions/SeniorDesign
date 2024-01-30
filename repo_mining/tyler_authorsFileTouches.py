import json
import requests
import csv

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

def authordate(lsttokens, repo, files):
    output = []
    ct = 0  # token counter

    try:
        # loop though all the commit pages until the last returned empty page
        for file in files:
            logUrl = 'https://api.github.com/repos/' + repo + '/commits?path=' + file
            jsonLog, ct = github_auth(logUrl, lsttokens, ct)

            # break out of the while loop if there are no more log in the pages
            if len(jsonLog) == 0:
                break

            for shaObject in jsonLog:
                if "author" not in shaObject or shaObject["author"] is None:
                    continue
                print(file, shaObject["author"]["login"], shaObject["commit"]["author"]["date"].split('T')[0])
                output.append((file, shaObject["author"]["login"], shaObject["commit"]["author"]["date"].split('T')[0]))
    except Exception as error:
        print("Error receiving data", error)
        exit(0)

    return output

repo = "scottyab/rootbeer"
lstTokens = [""]

repoFile = repo.split('/')[1]
fileInput = 'data/file_' + repoFile + '.csv'

fileCSV = open(fileInput, "r")
data = fileCSV.read()

files = []

for line in data.splitlines()[1:]:
    filename = line.split(",")[0]
    files.append(filename)

#rows = authordate(lstTokens, repo, files)

fileOutput = 'data/author_touches_' + repoFile + '.csv'
rows = ["Filename", "Author", "Date"]
fileCSV = open(fileOutput, 'w')
writer = csv.writer(fileCSV)
writer.writerow(rows)

for filename, author, date in authordate(lstTokens, repo, files):
    rows = [filename, author, date]
    writer.writerow(rows)

fileCSV.close()