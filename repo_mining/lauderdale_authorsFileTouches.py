import json
import requests
import csv
import pandas as pd

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

# @dictFiles, empty dictionary of files
# @lstTokens, GitHub authentication tokens
# @repo, GitHub repo
def authordate(commitList, srcFiles, lsttokens, repo):
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
                filesjson = shaDetails['files']
                for filenameObj in filesjson:
                    filename = filenameObj['filename']	
                    if filename in srcFiles:
                        author = shaDetails['commit']['author']['name'].replace(" ","")	    # get the author from commit url
                        
                        if (author[0:8] == "BIOCATCH"):	                            # take care of BIOCATCH exception
                            author = author[author.find("\\")+1:author.find(".")] + author[author.find(".")+1:]
                            
                        date = shaDetails['commit']['author']['date']               # get the date of commit from commit url
                        commitList.append([filename, author, date])	                # have a list that lists the author and date of a file commit
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
lstTokens = ["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"]

srcFilesDF = pd.read_csv('data/file_rootbeer.csv')    # convert csv file into a dataframe
srcFiles = srcFilesDF['Filename'].tolist()            # get the list of source files to check from dataframe

commitlist = list()    
authordate(commitlist, srcFiles, lstTokens, repo)    # get the authors and dates from source files, save to a list of lists

file = repo.split('/')[1]
# change this to the path of your file
fileOutput = 'data/authordate_' + file + '.csv'
rows = ["Filename", "Author", "Date"]        # set up the columns for a csv output file
fileCSV = open(fileOutput, 'w')
writer = csv.writer(fileCSV)
writer.writerow(rows)

for entry in commitlist:         # write out entries of the the commit list information to the csv file
    writer.writerow(entry)
fileCSV.close()


