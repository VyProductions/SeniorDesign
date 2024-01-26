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
    # print(data.head())
    # Convert date strings to datetime objects
    data['Date'] = pd.to_datetime(data['Date'])
    
    # Week number extraction
    data['Week'] = data['Date'].dt.isocalendar().week

    # Plotting
    fig, ax = plt.subplots()
    colors = plt.cm.rainbow(data['Author'].astype('category').cat.codes / len(data['Author'].unique()))

    scatter = ax.scatter(data['Week'], data['File Name'], c=colors, label=data['Author'].unique())

    # Create a legend
    legend1 = ax.legend(*scatter.legend_elements(), loc="upper right", title="Authors")
    ax.add_artist(legend1)

    # Formatting the plot
    ax.xaxis.set_major_locator(mdates.WeekdayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%U'))
    ax.set_xlabel('Week Number')
    ax.set_ylabel('File Name')
    ax.set_title('Week vs File Variables Shaded by Author')

    plt.xticks(rotation=45)
    plt.show(block=True)

if __name__ == "__main__":
    csv_file = os.path.join('data', 'file_rootbeer.csv')
    plot_scatter(csv_file)
