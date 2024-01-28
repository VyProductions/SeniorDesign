
import csv
import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime

def read_csv(file_path):
    with open(file_path, 'r') as file:
        return list(csv.DictReader(file))

def map_author_colors(authors):
    return {author: index for index, author in enumerate(authors)}

def calculate_weeks_and_files_touched(data):
    author_color_mapping = {}
    author_week_file_mapping = defaultdict(lambda: defaultdict(int))

    earliest_date_str = data[0]['Date']
    earliest_date = datetime.strptime(earliest_date_str, '%Y-%m-%d')

    for row in data:
        author = row['Author']
        date_str = row['Date']

        if author not in author_color_mapping:
            author_color_mapping[author] = len(author_color_mapping)

        current_date = datetime.strptime(date_str, '%Y-%m-%d')
        week = int((current_date - earliest_date).days / 7)

        author_week_file_mapping[author][week] += 1

    return author_color_mapping, author_week_file_mapping

def prepare_scatter_data(author_week_file_mapping, author_color_mapping):
    authors, weeks, files_touched = [], [], []

    for author, week_file_mapping in author_week_file_mapping.items():
        for week, files_touched_count in week_file_mapping.items():
            authors.append(author)
            weeks.append(week)
            files_touched.append(files_touched_count)

    return authors, weeks, files_touched, [author_color_mapping[author] for author in authors]

def plot_scatter(authors, weeks, files_touched, colors):
    scatter = plt.scatter(files_touched, weeks, c=colors, cmap='viridis', marker='o')
    plt.title('Files Touched by Authors Each Week')
    plt.xlabel('Number of Files Touched')
    plt.ylabel('Week')
    plt.show()

def main():
    csv_file_path = 'data/file_authors_dates_sorted.csv'
    data = read_csv(csv_file_path)

    author_color_mapping, author_week_file_mapping = calculate_weeks_and_files_touched(data)

    authors, weeks, files_touched, colors = prepare_scatter_data(author_week_file_mapping, author_color_mapping)

    plot_scatter(authors, weeks, files_touched, colors)

if __name__ == "__main__":
    main()

