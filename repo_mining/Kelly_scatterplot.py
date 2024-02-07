# Script that generates a scatter plot (using matplotlib) of
# weeks vs file variables where the points are shaded according
# to author variable (distict colors)

# NOTE: One should be able to tell a file that is touched many times
# & by whom. 

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime

# Get the dataframe from Kelly_authorsFileTouches.py
from Kelly_authorsFileTouches import data

data['Dates'] = data['Dates'].str.strip("[]'")
print(data.head(5))

# Legend
plt.title('Status Report')
plt.legend(title = "Developer", loc = "upper right")
plt.figure(figsize = (10, 8))

# Show the plot
plt.show()