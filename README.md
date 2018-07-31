### Metis Project 1: MTA Turnstile Analysis
How can we use MTA turnstile data to inform the optimal deployment of street teams for a nonprofit organization?

Please read my [blog](http://www.huguedata.com/2016/04/15/the-double-edged-sword-of-data/) to learn more on the matter.

###Program Flow
The table below provides high-level overviews of what each analysis script does. More information (including specific input/ouput data) can be found in each script's header.


Program 	| Description | 
----------- | ----------- |
01-MTA-Counts.py | Read-in raw MTA turnstile data and count the total number of entries and exits per station.
02-MTA-Graph.py | Graph the total number of entries/ exits for the top 25 busiest stations in New York City.
