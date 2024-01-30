import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

# Replace with your first name
script_name = 'your_firstname_scatterplot.py'

def plot_scatter(csv_file):
    # Read the CSV file
    data = pd.read_csv(csv_file)

    print(data.head())
    
    # Convert date strings to datetime objects
    data['Date'] = pd.to_datetime(data['Date'])
    
    # Week number extraction
    data['Week'] = data['Date'].dt.isocalendar().week

    # Convert file names to numerical values
    file_name_mapping = {name: i for i, name in enumerate(data['File Name'].unique())}
    data['File Number'] = data['File Name'].map(file_name_mapping)

    # Plotting
    fig, ax = plt.subplots()

    # Assign colors for each unique author
    unique_authors = data['Author'].unique()
    print(f'There are {len(unique_authors)} unique authors for this repository')
    # colors = plt.cm.rainbow(range(len(unique_authors)))
    color_map = plt.cm.get_cmap('rainbow', len(unique_authors))

    # Create a scatter plot for each author to allow for legend creation
    for i, author in enumerate(unique_authors):
        author_data = data[data['Author'] == author]
        ax.scatter(author_data['File Number'], author_data['Week'], color=color_map(i), label=author)

    # Create a legend
    ax.legend(title="Authors", loc='center left', bbox_to_anchor=(1, 0.5))

    # Adjust layout to make room for the legend
    plt.subplots_adjust(right=0.75)

    # Formatting the plot
    ax.set_xlabel('File Number')
    ax.set_ylabel('Week Number')
    ax.set_title('File vs Week Shaded by Author')

    plt.xticks(rotation=45)
    plt.show(block=True)

if __name__ == "__main__":
    csv_file = os.path.join('data', 'file_rootbeer.csv')
    # csv_file = os.path.join('data', 'file_gpslogger.csv')
    plot_scatter(csv_file)
