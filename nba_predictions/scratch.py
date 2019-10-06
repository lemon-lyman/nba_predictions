import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


file_in = "C:/Users/Nick/workspace/nba_predictions/nba_predictions/ftepy/fte_spreadsheet.csv"
df = pd.read_csv(file_in)
fig, ax = plt.subplots()
ax.scatter(df['date'].iloc[:100].values, df['carmelo_prob1'].iloc[:100].values)
plt.show()