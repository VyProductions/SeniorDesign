from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

filesDF = pd.read_csv('data/authordate_rootbeer.csv')    # save information from csv to dataframe

fileToId = dict()
idCount = 0
fileList = list()

for file in filesDF["Filename"].tolist():   # give a file a unique id to create the x coordinate for plot
    if file not in fileToId:
        fileToId[file] = idCount
        idCount += 1
    fileList.append(fileToId[file])

# print(fileList)

rawTimes = filesDF['Date'].tolist()
dayTimes = list()
scaledTimes = list()

for time in rawTimes:                       # convert a time string into a time format for comparison
    timeBySeconds = time[0:time.find("T")] + " " + time[time.find("T")+1:time.find("Z")]
    day = datetime.strptime(timeBySeconds, "%Y-%m-%d %H:%M:%S")
    dayTimes.append(day)

earliestTime = min(dayTimes)    # find the earliest time of all dates of file commits

for time in dayTimes:           # convert from the date of a commit to how many weeks away from the earliest commit
    diff = time - earliestTime
    scaledTimes.append(diff.total_seconds()/604800)    # saved times serve as y coordinate for plot

authors = list(filesDF["Author"].tolist())    # get a list of author names (no spaces) from the dataframe

for i in range(len(authors)):                 # loop checks each author for a capital letter of last name to put a space before it
    needSpace = 0
    for j, k in enumerate(authors[i]):        # inner loop finds location to put space between first and last name
        if k.isupper() and j != 0:
            needSpace = j
            break
    if needSpace != 0:                        # if a location is found, a space is placed
        authors[i] = authors[i][:needSpace] + " " + authors[i][needSpace:]

# print(authors)

authorToId = dict()
idCount = 0
idList = list()

for author in authors:
    if author not in authorToId:              # gives an author a unique id to create the a color variable for coordinates
        authorToId[author] = idCount
        idCount += 1
    idList.append(authorToId[author])

# print(idList)

x = np.array(fileList)                        # the x, y, and color of the scatterplot or set
y = np.array(scaledTimes)
a = np.array(idList)

plt.figure(figsize=(10,6))                    # the initial scatterplot is sized to provide the best ratio to view the information
scatter = plt.scatter(x, y, c=a, cmap="hsv")  # the scatterplot is created, with an "hsv" color map for a nice visual variety

legend_handles = [Line2D([0], [0], marker='o', color='w', markerfacecolor=scatter.to_rgba(author_id), markersize=8, label=author)
                  for author, author_id in authorToId.items()]    # custom legend handles created using Line2D

plt.legend(handles=legend_handles, title='Authors', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout(pad=2)                       # legend is added to the plot with custom handles

plt.title("Author and Date Acess per File")   # the title and axis labels are written
plt.xlabel("Files")
plt.ylabel("Weeks")

plt.show()    # the scatterplot is drawn in a separate window


