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


# list of authors
lstAuthors = []
# list of dates
lstDates = []
# list of filenames
lstFilenames = []
# lst of emails
lstEmails = []

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
                # we print shaObject to see what it looks like and what we can extract from it
                # but in the parse format for readability
                # print(json.dumps(shaObject, indent=4, sort_keys=True))
                # now we will extract the author name, email, and date
                author = shaObject['commit']['author']['name']
                date = shaObject['commit']['author']['date']
                email = shaObject['commit']['author']['email']
                # For each commit, use the GitHub commit API to extract the files touched by the commit
                shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)
                filesjson = shaDetails['files']
                for filenameObj in filesjson:
                    filename = filenameObj['filename']
                    dictfiles[filename] = dictfiles.get(filename, 0) + 1

                    # add the author, date, filename, and email to the lists
                    lstAuthors.append(author)
                    lstDates.append(date)
                    lstFilenames.append(filename)
                    lstEmails.append(email)

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
# Otherwise they will all be reverted and you will have to re-create them
# I would advise to create more than one token for repos with heavy commits
lstTokens = [""]

dictfiles = dict()
countfiles(dictfiles, lstTokens, repo)
print('Total number of files: ' + str(len(dictfiles)))

file = repo.split('/')[1]
# change this to the path of your file
fileOutput = 'data/file_' + file + '_uyen_version.csv'
# the row will contain extra info like the authors and the date they touch the file 
# rows = ["Filename", "Touches"]
#fileCSV = open(fileOutput, 'w')
#writer = csv.writer(fileCSV)
#writer.writerow(rows)

with open(fileOutput, 'w', newline='') as fileCSV:
    writer = csv.writer(fileCSV)
    writer.writerow(["Filename", "Touches", "Author", "Date", "Email"])

    # Write data to CSV
    data_rows = []
    for i in range(len(lstFilenames)):
        filename = lstFilenames[i]
        touches = dictfiles[filename]
        author = lstAuthors[i]
        date = lstDates[i]
        email = lstEmails[i]
        data_rows.append([filename, touches, author, date, email])

    # Sort data_rows by filename
    data_rows = sorted(data_rows, key=lambda row: row[2])
    for row in data_rows:
        writer.writerow(row)

    bigcount = None
    bigfilename = None
    for filename, count in dictfiles.items():
        rows = [filename, count]
        # writer.writerow(rows)
        if bigcount is None or count > bigcount:
            bigcount = count
            bigfilename = filename

    print('The file ' + bigfilename + ' has been touched ' + str(bigcount) + ' times.')

fileCSV.close()

# find and print unique authors
unique_authors = set(lstAuthors)
print(f'Total unique authors: {len(unique_authors)}')

# find and print unique files
unique_files = set(lstFilenames)
print(f'Total unique files: {len(unique_files)}')
