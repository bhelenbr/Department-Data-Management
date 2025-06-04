#! /usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
from datetime import date

def main(argv,lastnames):
	source = argv[1] # file to read
	try:
		df = pd.read_excel(source,sheet_name="Sheet1")
	except OSError:
		print("Could not open/read file: " + source)
		return(0)
	
	# Filter out to only department faculty
	if (len(lastnames) > 0):
		df = df[df['Advisor Name'].apply(lambda x: x[:x.find(',')]).isin(lastnames)]
		#df = df[df['Advisor Name'].isin(lastnames)]
	
	# Only plot this year
	today = date.today()
	year = int(today.year)
	df = df[df['YEAR'].apply(lambda x: int(x)) == year-1]
	
	x = np.arange(df.shape[0])  # the label locations
	width = 0.5  # the width of the bars
	fig, ax = plt.subplots(layout='constrained')
	rects = ax.bar(x, df['Count Distinct Name'], width)

	# Add some text for labels, title and custom x-axis tick labels, etc.
	ax.set_ylabel('Number of Advisees')
	ax.set_xticks(x, df['Advisor Name'])
	plt.xticks(rotation = 90) # Rotates X-Axis Ticks by 45-degrees
	plt.savefig('Tables/advisee_count.png',bbox_inches='tight',pad_inches=1)
	plt.close()
	
if __name__ == "__main__":
	lastnames = ['Helenbrook','Visser','Bazzocchi']
	#lastnames = []
	main(sys.argv,lastnames)