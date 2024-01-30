#2015-06-19
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


def weeks(startDateString, endDateString):
    # Convert string dates to datetime objects
    startDate = datetime.strptime(startDateString, '%Y-%m-%d')
    endDate = datetime.strptime(endDateString, '%Y-%m-%d')

    # Calculate the difference in days
    days = endDate - startDate

    # Calculate the number of weeks
    return days.days // 7


repo = "scottyab/rootbeer"
repoFile = repo.split('/')[1]
beginningDate = '2015-06-19'

fileInput = 'data/author_touches_' + repoFile + '.csv'
fileCSV = open(fileInput, "r")
data = fileCSV.read()

fileNameDict = {}
authorDict = {}
fileCounter = 1
authorCounter = 1

df = pd.read_csv(fileInput)

authors = df["Author"].tolist()
authorToNum = list()

files = df["Filename"].tolist()
fileToNum = list()

dates = df["Date"].tolist()
datesToWeeks = list()

for line in data.splitlines()[1:]:
    fileName = line.split(",")[0]
    if fileName not in fileNameDict:
        fileNameDict[fileName] = fileCounter
        fileCounter += 1

    author = line.split(",")[1]
    if author not in authorDict:
        authorDict[author] = authorCounter
        authorCounter += 1

    date = line.split(",")[2]

    #print(f'The file {fileName} was edited by {author}, and was edited {weeks(beginningDate, date)} weeks ago')

for author in authors:
    authorToNum.append(authorDict[author])

for file in files:
    fileToNum.append(fileNameDict[file])

for currDate in dates:
    datesToWeeks.append(weeks(beginningDate, currDate))

x = np.array(fileToNum)
y = np.array(datesToWeeks)
c = np.array(authorToNum)

plt.scatter(x, y, c=c, cmap="hsv")

plt.xlabel('File')
plt.ylabel('Weeks')
plt.title('Author Activities of scottyab/rootbeer')

plt.show()