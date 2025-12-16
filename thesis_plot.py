#! /usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
from datetime import date

def main(argv,years):
	source = argv[1] # file to read
	try:
		df = pd.read_excel(source,header=0)
	except OSError:
		print("Could not open/read file: " + source)
		sys.exit()
	
	today = date.today()
	year = today.year
	begin_year = year - years

	df = df[(df['Year'] >= begin_year)]
	df = df.reset_index()

	table = df.pivot_table(values=['Student'], index=['FacultyName'], columns=['Degree'], aggfunc={'Student': 'count'},observed=False,fill_value=0)

	x = np.arange(table.shape[0])  # the label locations
	width = 0.25  # the width of the bars
	multiplier = 0

	fig, ax = plt.subplots(layout='constrained')

	for program in ["MS","PhD"]:
		offset = width * multiplier
		rects = ax.bar(x + offset, table[('Student',   program)], width, label=program)
		#ax.bar_label(rects, padding=3)
		multiplier += 1

	# Add some text for labels, title and custom x-axis tick labels, etc.
	ax.set_ylabel('Theses')
	ax.set_xticks(x + width, table.index)
	ax.legend(loc='upper left', ncols=2)
	plt.xticks(rotation = 90) # Rotates X-Axis Ticks by 45-degrees
	plt.savefig('Tables/thesis.png',bbox_inches='tight',pad_inches=1)
	plt.close()
	
	table = table[[('Student','MS'),('Student','PhD')]]
	table.columns=['MS Theses','PhD Theses']

	return(table)

if __name__ == "__main__":
	main(sys.argv,3)