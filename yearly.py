import datetime
import pandas as pd
import dateutil
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

sns.set()

df = pd.read_csv('log.txt', sep='\t', skiprows=[1])
df['Date'] = pd.to_datetime(df['Date'])
df = df.groupby('Date').sum()
df['Date'] = df.index

years = df.Date.dt.year.unique()

legend=[]
fig, ax = plt.subplots()

# Plot 45 avg
days_of_year = np.linspace(0,366,367)

lst = []
for idx, year in enumerate(years[-5:]):
    print(year)

    dfy = df[df['Date'].dt.year == year]
    dfy['day_of_year'] = df['Date'].apply(datetime.datetime.toordinal) - datetime.datetime(year, 1, 1).toordinal() + 1

    dfy = dfy.set_index('day_of_year')
    dfy['total distance'] = np.cumsum(dfy['Distance'])

    dfy['total distance'].plot(ax=ax, linewidth=2, zorder=1)
    legend.append(str(year))

    lst.append(dfy)

for pace_per_week in [75, 55, 50, 45, 40, 35, 30, 25]:

    total_miles = pace_per_week / 7 * days_of_year
    ax.plot(days_of_year, total_miles, linestyle='-.', zorder=0)
    legend.append(f'{pace_per_week}/wk')

ax.legend(legend)
plt.show()

