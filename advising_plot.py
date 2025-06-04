#! /usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
from datetime import date

def main(argv,lastnames,private=False):
	source = argv[1] # file to read
	try:
		df = pd.read_excel(source)
	except OSError:
		print("Could not open/read file: " + source)
		return(0)
	
	today = date.today()
	year = today.year
	begin_year = year - 3
	
	#print(df.shape[0])
	df.fillna(0,inplace=True)
	df = df[df['Term'].apply(lambda x: int(x/10)-400+2000) >= begin_year]
	#print(df.shape[0])
	
	# Filter out to only department faculty
	if (len(lastnames) > 0):
		df = df[df['LN,FN'].apply(lambda x: x[:x.find(',')]).isin(lastnames)]
	df['Sum of Responses'] = df['Question 0'] + df['Question 1'] + df['Question 2'] + df['Question 3'] + df['Question 4'] + df['Question 5']
	df['Total Points'] = df['Question 1'] + 2*df['Question 2'] + 3*df['Question 3'] + 4*df['Question 4'] + 5*df['Question 5']
		

	
	table = df.pivot_table(index=['LN,FN'],columns=['Number'],aggfunc={'Sum of Responses': 'sum','Total Points': 'sum'})		
	table.reset_index(inplace=True)
	table['LN,FN']	= table['LN,FN'].apply(lambda x: x[:x.find(',')])
	
	fig, ax = plt.subplots(layout='constrained')
	for count,faculty in enumerate(table['LN,FN']):
		responses = []
		for question in range(1,12):
			responses.append(table.loc[count,('Total Points',question)]/table.loc[count,('Sum of Responses',question)])
		ax.plot(range(1,12),responses,label=faculty)
		if (not(private)):
			ax.text(11,table.loc[count,('Total Points',11)]/table.loc[count,('Sum of Responses',11)],faculty,fontsize='xx-small')
	#ax.legend(fontsize='xx-small',ncols=2)
	ax.set_ylabel('Average Score')
	ax.set_xlabel('Question #')
	plt.xlim([1,15])
	plt.savefig('Tables/advising_averages.png',bbox_inches='tight',pad_inches=1)
	plt.close()
	
	table['avg11'] = np.divide(table[('Total Points',11)],table[('Sum of Responses',11)])
	if (private):
		table.sort_values(by=['avg11'], inplace=True,ascending = True)
		table.reset_index(inplace=True)
		table.to_csv('advising_index.csv', sep=',', index=False, encoding='utf-8')
	
	x = np.arange(table.shape[0])  # the label locations
	width = 0.25  # the width of the bars
	multiplier = 0
	fig, ax = plt.subplots(layout='constrained')
	for question in [5,11]:
		offset = width * multiplier
		rects = ax.bar(x + offset, np.divide(table[('Total Points',question)],table[('Sum of Responses',question)]), width, label=str(question))
		multiplier += 1
	ax.bar_label(rects, padding=3,labels=table[('Sum of Responses',11)].apply(lambda x: int(x)))

	# Add some text for labels, title and custom x-axis tick labels, etc.
	ax.set_ylabel('Average Score')
	ax.set_ylim([3,5])
	if (not(private)):
		ax.set_xticks(x + width, table['LN,FN'])
	ax.legend(loc='upper left', ncols=2)
	plt.xticks(rotation = 90) # Rotates X-Axis Ticks by 45-degrees
	plt.savefig('Tables/advising5_11.png',bbox_inches='tight',pad_inches=1)
	plt.close()
	
if __name__ == "__main__":
	#lastnames = ['Helenbrook','Visser','Bazzocchi']
	lastnames = []
	main(sys.argv,lastnames)