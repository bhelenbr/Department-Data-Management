#! /usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
from datetime import date

def main(years,inputfile):
	source = inputfile # file to read
	try:
		df = pd.read_excel(source,header=0)
	except OSError:
		print("Could not open/read file: " + source)
		sys.exit()
	
	today = date.today()
	year = today.year
	begin_year = year - years

	df = df[(df['Calendar Year'] >= begin_year)]
	df.sort_values(by=['Calendar Year','Term'], inplace=True, ascending = [False,True])
	df = df.reset_index()

	table = df.pivot_table(values=['Students'], index=['Calendar Year'], aggfunc={'Students': 'count'},observed=False)
	table = table.reset_index()
	table.columns=['Year','Count']
 
	# creating the bar plot
	fig = plt.figure(figsize = (10, 5))
	plt.bar(table['Year'], table['Count'], color ='blue',
			width = 0.4)
	plt.xticks(rotation = 90) # Rotates X-Axis Ticks by 45-degrees
	plt.xlabel("Year")
	plt.ylabel("Undergraduate Projects Advised")
	plt.savefig('Tables_dept/UR.png',bbox_inches='tight',pad_inches=1)
	plt.close()

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='This script outputs plots of undergraduate research activity in the last [YEARS] years')
	parser.add_argument('-y', '--years',default="3",type=int,help='the number of years to output')
	parser.add_argument('inputfile',help='the input excel file name')           
	args = parser.parse_args()
	main(args.years,args.inputfile)