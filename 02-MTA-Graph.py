"""
Script:     01-MTA-Counts.py
Purpose:    Read-in raw MTA turnstile data and count the total number of entries and exits per station.
Input:      data/mta_count_total.csv
Output:     graphics/BusiestSubwayStops.png
"""

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


#Read In MTA Count Data
df=pd.read_csv("data/mta_count_total.csv", names=["station_line","volume_per_hour"])


#Sort
df=df.sort_values(by="volume_per_hour", ascending=True)
df=df.reset_index(drop=True)


#Clean
df.ix[df.volume_per_hour<100,"volume_per_hour"] = np.nan
df.ix[df.volume_per_hour>11000,"volume_per_hour"] = np.nan
df.ix[df.station_line=="9TH STREET (1)", "volume_per_hour"] = np.nan
df=df.dropna()
df=df.reset_index(drop=True)


#Plot
station_line=df[-20:]["station_line"].tolist()
volume_per_hour=df[-20:]["volume_per_hour"].tolist()

width=0.5
colors=["b"]*9+["g"]*4+["y"]*5+["r"]*2

plt.figure(figsize=(25,15))
plt.barh([x for x in range(0,20)],volume_per_hour,width,color=colors)
plt.yticks([(x+(width/2)) for x in range(0,20)], station_line)

plt.tick_params(axis="x", labelsize=26)
plt.tick_params(axis="y", labelsize=13)

plt.title("Busiest 20 MTA Stops by Average Hourly Traffic", fontweight="bold", fontsize=32)
#plt.ylabel("Station",fontweight="bold",fontsize=28)
plt.xlabel("Entries/ Exits per Hour",fontweight="bold",fontsize=28)
plt.savefig("graphics/BusiestSubwayStops.png")
#plt.show()