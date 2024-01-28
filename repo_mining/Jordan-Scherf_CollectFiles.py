import json
import requests
import csv
import os

if not os.path.exists("data"):
    os.makedirs("data")

# GitHub Authentication function - Yoinked from the Proffessor
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
def count_source_files(dictfiles, lsttokens, repo):
    ipage = 1  # url page counter
    ct = 0  # token counter

    source_file_extensions = ['.java', '.py', '.cpp', '.h']  # not sure if kotlin is considered a source file or not

    try:
        # loop through all the commit pages until the last returned empty page
        while True:
            spage = str(ipage)
            commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?page=' + spage + '&per_page=100'
            jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)

            # break out of the while loop if there are no more commits on the pages
            if len(jsonCommits) == 0:
                break
            # iterate through the list of commits on spage
            for shaObject in jsonCommits:
                sha = shaObject['sha']
                # For each commit, use the GitHub commit API to extract the files touched by the commit
                shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)
                filesjson = shaDetails['files']
                for filenameObj in filesjson:
                    filename = filenameObj['filename']
                    # Check if the file has a source file extension
                    if any(filename.endswith(ext) for ext in source_file_extensions): # added this just to get the source files -Jordan
                        dictfiles[filename] = dictfiles.get(filename, 0) + 1
                        print(filename)
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
# Otherwise, they will all be reverted, and you will have to re-create them
# I would advise creating more than one token for repos with heavy commits
lstTokens = ["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"]

dictfiles = dict()
count_source_files(dictfiles, lstTokens, repo)
print('Total number of source files: ' + str(len(dictfiles)))

file = repo.split('/')[1]
# change this to the path of your file
fileOutput = 'data/file_src_' + file + '.csv'
rows = ["Filename", "Touches"]
fileCSV = open(fileOutput, 'w')
writer = csv.writer(fileCSV)
writer.writerow(rows)

bigcount = None
bigfilename = None
for filename, count in dictfiles.items():
    rows = [filename, count]
    writer.writerow(rows)
    if bigcount is None or count > bigcount:
        bigcount = count
        bigfilename = filename
fileCSV.close()
print('The source file ' + bigfilename + ' has been touched ' + str(bigcount) + ' times.')
