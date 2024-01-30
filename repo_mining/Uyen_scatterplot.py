import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load data
df = pd.read_csv('./data/file_rootbeer_uyen_version.csv')

# Count total number of unique source files
total_files = df['Filename'].nunique()
print(f'Total unique source files: {total_files}')

# Count total number of unique authors
total_authors = df['Author'].nunique()
print(f'Total unique authors: {total_authors}')

# Convert 'Date' to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Calculate number of weeks since the earliest date
earliest_date = df['Date'].min()
df['Week'] = ((df['Date'] - earliest_date) / pd.Timedelta(1, unit='W')).round()

# Group data by 'Week' and 'Author' and count unique 'Filename' values
df_grouped = df.groupby(['Week', 'Author'])['Filename'].nunique().reset_index(name='Files')

# How much work is being done?
total_commits = df.shape[0]
print(f'Total commits: {total_commits}')

commits_per_author = df.groupby('Author').size().sort_values(ascending=False)
print(f'Commits per author:\n{commits_per_author}\n')

# Who is doing the most work on the files that have the most work?
commits_per_file = df.groupby('Filename').size().sort_values(ascending=False)
print(f'Commits per file:\n{commits_per_file}\n')

# find which file has most commits and then find the author who has most commits on that file
most_commits_file = commits_per_file.index[0]
print(f'Most commits file: {most_commits_file}\n')

df_most_commitF = df[df['Filename'] == most_commits_file]
commit_per_authos_mcf = df_most_commitF.groupby('Author').size().sort_values(ascending=False)
print(f'Commits per author on most commits file:\n{commit_per_authos_mcf}\n')

# make a dict like author and then list of files they have touched
author_files_dict = {}
print("Author files dict:")
for author in df['Author'].unique():
    author_files_dict[author] = df[df['Author'] == author]['Filename'].unique()

# for author, files in author_files_dict.items():
    # print(f'{author}: {files}\n')

# find which author has touched the most files
def get_num_files_touched(author):
    return len(author_files_dict[author])

most_files_touched_author = max(author_files_dict, key=get_num_files_touched)
print(f'Most files touched author: {most_files_touched_author}\n')

# find recent commits per author 
recent_commits_per_author = df[df['Week'] >= 100].groupby('Author').size().sort_values(ascending=False)
print(f'Recent commits per author:\n{recent_commits_per_author}\n')

# Which developer could have left the project?
# find authors who have not committed in the last 100 weeks and have commit count less than 3
inactive_authors = df[df['Week'] >= 100].groupby('Author').size()
inactive_authors = inactive_authors[inactive_authors < 3]
print(f'Authors who could have left the project:\n{inactive_authors}\n')

# What types of things are they doing?
# find most common file extensions
file_extensions = df['Filename'].str.split('.').str[-1]
file_extensions = file_extensions.value_counts()
print(f'Most common file extensions:\n{file_extensions}\n')


# Create color map for authors
authors = df_grouped['Author'].unique()
colors = plt.get_cmap('tab20', len(authors))
color_map = {author: colors(i) for i, author in enumerate(authors)}
df_grouped['Color'] = df_grouped['Author'].map(color_map)

# Plot data
for author in authors:
    df_author = df_grouped[df_grouped['Author'] == author]
    plt.scatter(df_author['Files'], df_author['Week'], color=color_map[author], label=author)

# Set title and labels
plt.title('Number of Files vs Weeks')
plt.xlabel('Number of Files')
plt.ylabel('Week')

# Create legend
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

# Show plot
plt.show()

