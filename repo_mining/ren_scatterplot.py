import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timezone
import math

df = pd.read_csv('./data/file_autors_dates_rootbeer.csv') # Read the file

numauth = df['Author'].nunique() # Counts number of unique authors
numfile = df['File'].nunique() # Counts number of unique files

df['Date'] = pd.to_datetime(df['Date']) # Convert timestamp to datetime


# Calculate which week each commit was
weeks = (df['Date'].max() - df['Date'].min()) / np.timedelta64(1, 'W') # Calculate number of weeks since the earliest commit to the latest commit
weeks = math.floor(weeks)
df['Week'] = ((df['Date'] - df['Date'].min()) / np.timedelta64(7, 'D')).astype(int)


# Map each File into numbers
df['Number'] = df.groupby(['File']).ngroup()

# Map each Author into numbers
df['ID'] = df.groupby(['Author']).ngroup()

#Draw Scatter Plot
plt.scatter(df['Number'], df['Week'], c=df['ID'], cmap='viridis')
plt.title("Authors Activities over Time of each File")
plt.xlabel("File")
plt.ylabel("Weeks")
plt.show()