#! /usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
from datetime import date
import argparse

def main(years,inputfile,lastnames):
	source = inputfile # file to read
	try:
		df = pd.read_excel(source,sheet_name="Data")
	except OSError:
		print("Could not open/read file: " + source)
		return(0)
	
	today = date.today()
	year = today.year
	begin_year = year - years
	
	df['Year'] = df['term'].apply(lambda x: int(x[-4:]))
	df = df[(df['Year'] >= begin_year)]

	# Filter out to only department faculty
	if (len(lastnames) > 0):
		df = df[df['INSTR_NA'].apply(lambda x: x[:x.find(',')]).isin(lastnames)]
		
	table = df.pivot_table(index=['Year'],columns=['question'],aggfunc={'enrollment': 'sum','Weighted Average': 'sum', 'count_evals':'sum'})		
	table = table.fillna(0)
	table.sort_values(by=['Year'], inplace=True,ascending = True)
	table = table.reset_index()


	# creating the bar plot
	q19av = np.divide(table[('Weighted Average',19)],table[('count_evals',19)])
	q20av = np.divide(table[('Weighted Average',20)],table[('count_evals',20)])
	
	x = np.arange(len(q19av))  # the label locations
	width = 0.25  # the width of the bars
	multiplier = 0

	fig, ax = plt.subplots(layout='constrained')

	for question,data in [("Q19",q19av),("Q20",q20av)]:
		offset = width * multiplier
		rects = ax.bar(x + offset, data, width, label=question)
		#ax.bar_label(rects, padding=3)
		multiplier += 1

	# Add some text for labels, title and custom x-axis tick labels, etc.
	ax.set_ylabel('Weighted Average Teaching Evaluation')
	ax.set_xticks(x + width, table['Year'])
	ax.legend(loc='upper left', ncols=2)
	plt.xticks(rotation = 90) # Rotates X-Axis Ticks by 45-degrees
	plt.xlabel("Year")
	plt.savefig('Tables_dept/teaching_averages.png',bbox_inches='tight',pad_inches=1)
	plt.close()
	
if __name__ == "__main__":
	lastnames = []
	parser = argparse.ArgumentParser(description='This script outputs plots of teaching evaluations in the last [YEARS] years')
	parser.add_argument('-y', '--years',default="3",type=int,help='the number of years to output')
	parser.add_argument('inputfile',help='the input excel file name')           
	args = parser.parse_args()
	main(args.years,args.inputfile,lastnames)
