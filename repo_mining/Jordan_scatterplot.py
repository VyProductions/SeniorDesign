import csv
import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime

#Read the CSV file
csv_file = 'data/file_authors_dates_sorted.csv'  # Assuming this is the file with the provided data

#Dictionary to store author-color mapping
author_color_mapping = {}

#Dictionary to store author-week-file mapping
author_week_file_mapping = defaultdict(lambda: defaultdict(int))

#Lists to store data for scatter plot
authors = []
weeks = []
files_touched = []

#Read CSV file and extract data
with open(csv_file, 'r') as file:
    reader = csv.DictReader(file)
    
    # Extract the earliest date
    earliest_date_str = next(reader)['Date']
    earliest_date = datetime.strptime(earliest_date_str, '%Y-%m-%d')

    for row in reader:
        author = row['Author']
        date_str = row['Date']
        filename = row['Filename']

        #Assign color
        if author not in author_color_mapping:
            author_color_mapping[author] = len(author_color_mapping)

        #Calculate the week number
        current_date = datetime.strptime(date_str, '%Y-%m-%d')
        week = int((current_date - earliest_date).days / 7)

        #Increment the number of files touched for the given author
        author_week_file_mapping[author][week] += 1

#Prepare data for the scatter plot
for author, week_file_mapping in author_week_file_mapping.items():
    for week, files_touched_count in week_file_mapping.items():
        authors.append(author)
        weeks.append(week)
        files_touched.append(files_touched_count)

scatter = plt.scatter(files_touched, weeks, c=[author_color_mapping[author] for author in authors], cmap='viridis', marker='o')

#Add labels and title
plt.title('Files Touched by Authors Each Week')
plt.xlabel('Number of Files Touched')
plt.ylabel('Week')
plt.show()








