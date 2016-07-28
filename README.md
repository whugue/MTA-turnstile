### Metis Project 1: MTA Turnstile Analysis

How can we use MTA turnstile data to inform the optimal deployment of street teams for a nonprofit organization?

Please read my [blog](http://www.huguedata.com/2016/04/15/the-double-edged-sword-of-data/) to learn more on the matter.

### Code Dependencies
* Collections
* CSV
* Datetime/ Dateutil
* Numpy
* Pandas
* Matplotlib

### Data
MTA Turnstile Counts were obtained [here](http://web.mta.info/developers/turnstile.html). The raw weekly data files used in analysis are saved to the *data/* folder in the format *turnstile_YYMMDD.txt*. The **data/** folder also contains an aggregated datafile of the total entry/ exit counts per station, saved as *mta_counts_total.csv*.

### Python Scripts and Program Flow:
* **mta_counts.py**: Read-in raw MTA turnstile data and count the total number of entries and exits per station.
* **mta_graph.ph**: Graph the total number of entries/ exits for the top 25 busiest stations in New York City.

### Other Fun Stuff:
* **graphics/**: Graph of Entries/ Exits of 25 busiest subway stops in New York.



