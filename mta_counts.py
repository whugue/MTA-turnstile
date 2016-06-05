import csv
from collections import defaultdict
import datetime
import dateutil.parser


"""
Read-In Weekly MTA data files and combine into one master dictionary,
using CA-Unit-Station-Turnstile-Datetime as key and cumulative entries, exits as values

Use start and stop to indicate the datestamps on the first and last files you want to read in. 
Dates entries must be strings in MM/DD/YYYY format

Returned Dictionary in Format: 
{(CA,Unit,SCP,Station,Lines) : [[datetime1, cum entries 1, cum exits 1],[datetime2, cum entries2, cum exits2],...]
"""

def read_data(start,stop):
	start_date=datetime.datetime.strptime(start,"%m/%d/%Y").date()
	stop_date=datetime.datetime.strptime(stop,"%m/%d/%Y").date()
	d=defaultdict(list)
	
	#Loops through each (weekly) data file to read in
	while start_date<=stop_date:

		#Read CSV data into nested list [[Row1], [Row2], etc.]
		file_date="{:%y%m%d}".format(start_date)
		file_name="data/turnstile_"+file_date+".txt"

		f=list(csv.reader(open(file_name)))

		print "%s Imported" % (file_name)

		#Loop through rows. Create dictionary in format {(CA,Unit,Scp,Station,Lines): [DT, cum entry, cum exit]} 
		for i in range(1,len(f)):
			ca=f[i][0]
			unit=f[i][1]
			ts=f[i][2]
			station_name=f[i][3]
			station_line=f[i][4]
			date_time=dateutil.parser.parse(f[i][6]+" "+f[i][7])

			cum_entries=int(f[i][9].strip())
			cum_exits=int(f[i][10].strip())

			key=(ca,unit,ts,station_name,station_line)
			val=[date_time, cum_entries, cum_exits]
			#print key,val

			d[key].append(val)

		start_date+=datetime.timedelta(days=7)

	return d

mta_dict=read_data("04/18/2015","05/30/2015")
#print mta_dict

"""
Clean Data: 

Returned dictionary in format:
{(CA,Unit,SCP,Station,Lines) : [[audit datetime 1, entries 1, exits 1, total 1], [" "], [" "]]}
"""

def clean_data(d):
	new_d=defaultdict(list)

	for key in d:
		l=sorted(d[key], key=lambda x: x[0]) #for each key, create nested list of data. Sort by datetime (element 1)

		for i in range(1,len(l)):
			date_time=l[i][0]

			entries=l[i][1]-l[i-1][1] #Calculate Entries and Exits per audit period from cum totals
			exits=l[i][2]-l[i-1][2]
			total=entries+exits

			if entries<0 or exits<0: #if entries or exits are negative, set to 0
				entries=0
				exits=0
				total=0

			val=[date_time, entries, exits, total]
			#print key, val

			new_d[key].append(val)

	return new_d

mta_dict_clean=clean_data(mta_dict)
#print mta_dict_clean
#print mta_dict_clean.items()

"""
Aggregate voulume counts by Station-Line:

d=dictionary of to read in (produced by clean_data)
vol_ind=index of volume metric you want to aggregate (4=entries only, 5=exits only, 6=both)

Returned dictionary in format:
{(Station, Line): volume per hour}
"""

def sum_counts_total(d,vol_ind):
	new_d=defaultdict(list)
	
	for key, val in d.items():
		new_key=(key[3], key[4]) #Extract station name and line from station-turnstile key and save as new key

		for i in range(0,len(val)): #Loop through records associated with specific turnstile
			volume=val[i][vol_ind] #Exract volume (either entries, exits, or total) from each record

			new_d[new_key]=new_d.get(new_key, 0)+volume #Add volume to station total

	for key in new_d: #Scale volume into average Volume per period over entire period 
		new_d[key]=new_d[key] / (7*7*24) #number of hours in three months

	return new_d

##Create Needed Dicts
mta_count_total=sum_counts_total(mta_dict_clean,3)
#print mta_count_total


##Write out to CSV file for further analysis and exploration
def WriteOut(d,outfile):
	l=[]

	for t, v in d.items():
		station=t[0]+" ("+t[1]+")"
		l.append([station, v])

	l.sort() #sort alphabetically

	with open(outfile, "w") as f:
		writer=csv.writer(f)
		writer.writerows(l)

WriteOut(mta_count_total,"data/mta_count_total.csv")






