import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

csv_file = 'data/file_rootbeer_touches.csv'
df = pd.read_csv(csv_file)

df['Date'] = pd.to_datetime(df['Date'])

# find earliest commit date
earliest_date = df['Date'].min()

# calc the number of weeks since the earliest commit date
df['Weeks'] = df['Date'].apply(lambda x: (x - earliest_date).days // 7)


authors = df['Author'].unique() # get list of unique authors
colors = plt.cm.rainbow(np.linspace(0, 1, len(authors)))
author_color_map = dict(zip(authors, colors)) # assign each a color

# assign each unique file a unique number for x-coord
unique_files = df['Filename'].unique()
file_map = {file: i for i, file in enumerate(unique_files)}
df['FileIndex'] = df['Filename'].map(file_map)


plt.figure(figsize=(14, 8))

for author in authors:
    author_data = df[df['Author'] == author]
    plt.scatter(author_data['FileIndex'], author_data['Weeks'], color=author_color_map[author], label=author, alpha=0.6, edgecolors='w', s=100)

plt.xlabel('Files')
plt.ylabel('Weeks')
plt.title('File Touches by Week and Author')
plt.legend(loc='upper right', bbox_to_anchor=(1.15, 1))
plt.xticks(ticks=np.arange(0, len(unique_files), 10), labels=np.arange(0, len(unique_files), 10))
plt.show()
