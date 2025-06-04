#! /usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
from datetime import date

def main(argv,lastnames):
	source = argv[1] # file to read
	try:
		df = pd.read_excel(source,header=0)
	except OSError:
		print("Could not open/read file: " + source)
		sys.exit()
	
	today = date.today()
	year = today.year
	begin_year = year - 3
	
	df = df[(df['Date'].apply(lambda x: x.year) >= begin_year)]
	df.columns = ['Date','Time','StudentName','Area','FacultyName','Place','Notes']
	df.fillna(value={"FacultyName": "Professor No-one"},inplace=True)
	df['FacultyName'] = df['FacultyName'].apply(lambda x: x[(x.find(' ')+1):])
	df = df.reset_index()
	
	table = df.pivot_table(index=['FacultyName'], aggfunc={'StudentName': 'count'})
	table = table.reset_index()
	table.columns=['FacultyName','Count']
	
	if (len(lastnames) > 0):
		table = table[table['FacultyName'].isin(lastnames)]
	#print(table)
 
	# creating the bar plot
	fig = plt.figure(figsize = (10, 5))
	plt.bar(table['FacultyName'], table['Count'], color ='blue',
			width = 0.4)
	plt.xticks(rotation = 90) # Rotates X-Axis Ticks by 45-degrees
	plt.xlabel("Faculty")
	plt.ylabel("Student Visits")
	plt.savefig('Tables/visits.png',bbox_inches='tight',pad_inches=1)
	plt.close()

if __name__ == "__main__":
	lastnames = []
	main(sys.argv,lastnames)