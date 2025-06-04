#! /usr/bin/env python3

import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
from datetime import date

def main(years,inputfile):
	for name in ['journal','refereed','patent','conference','book','invited']:
		source = inputfile +os.sep +name +".xlsx"
		try:
			df = pd.read_excel(source,header=0)
		except OSError:
			print("Could not open/read file: " + source)
			continue

		today = date.today()
		year = today.year
		begin_year = year - years

		df = df[(df['year'] >= begin_year)]
		df = df.reset_index()
		if (df.shape[0] > 0):
			table = df.pivot_table(values=['ID'], index=['year'], aggfunc={'ID': 'count'},observed=False)
			table = table.reset_index()
			table.columns=['year','Count']

			# creating the bar plot
			fig = plt.figure(figsize = (10, 5))
			plt.bar(table['year'], table['Count'], color ='blue',
					width = 0.4)
			plt.xticks(rotation = 90) # Rotates X-Axis Ticks by 45-degrees
			plt.xlabel("Year")
			plt.ylabel("Count")
			plt.savefig('Tables_dept' +os.sep +name +'.png',bbox_inches='tight',pad_inches=1)
			plt.close()

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='This script outputs plots of publication activity in the last [YEARS] years')
	parser.add_argument('-y', '--years',default="3",type=int,help='the number of years to output')
	parser.add_argument('inputfile',help='the input excel file name')           
	args = parser.parse_args()
	main(args.years,args.inputfile)