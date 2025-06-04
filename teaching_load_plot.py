#! /usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
from datetime import date

def main(argv,lastnames):
	source = argv[1] # file to read
	try:
		df = pd.read_excel(source,sheet_name="Data")
	except OSError:
		print("Could not open/read file: " + source)
		return(0)
	
	today = date.today()
	year = today.year
	twodigityear = year-int(year/100)*100
	# Spring ends in 2, Fall ends in 9
	if ((today.month > 1) & (today.month < 9)):
		semester = 2
	else:
		semester = 9
	term = 4000+ twodigityear*10 +semester
	# beginterm is 3 years before
	begin_term = term -3*10
	
	df = df[df['Term'].apply(lambda x: (x > begin_term) & (x <= term))]
	df.fillna(value={"PI": ""},inplace=True)
	# Filter out to only department faculty
	if (len(lastnames) > 0):
		df = df[df['PI'].apply(lambda x: x[:x.find(',')]).isin(lastnames)]
	
	# Merge distance sections with section 01
	df['Section'] = df['Section'].apply(lambda x: x.replace('D','0')[0:2])
	df.fillna(value={'Enrollment':0},inplace=True)
	
	# Get only lecture sections
	lectures = df[df['Component'].apply(lambda x: x == 'LEC')]	
	#others = df[df['Component'].apply(lambda x: not(x == 'LEC'))]
		
	sections = lectures.pivot_table(index=['PI','Term','Course Nbr','Section'],aggfunc={'Enrollment': 'sum'})	
	sections.reset_index(inplace=True)
	sections.columns = ['PI','Term','Course Nbr','Section','Enrollment']
	section_counts = sections[['PI']].value_counts(sort=False).reset_index()
	
	
	classes = lectures.pivot_table(index=['PI','Term','Course Nbr'],aggfunc={'Enrollment': 'sum'})	
	classes.reset_index(inplace=True)
	classes.columns = ['PI','Term','Course Nbr','Enrollment']
	class_counts = classes[['PI']].value_counts(sort=False).reset_index()
	
	x = np.arange(section_counts.shape[0])  # the label locations
	width = 0.25  # the width of the bars
	multiplier = 0

	fig, ax = plt.subplots(layout='constrained')
	offset = width * multiplier
	rects = ax.bar(x + offset, section_counts['count'], width, label='sections')
	multiplier += 1
	offset = width * multiplier
	rects = ax.bar(x + offset, class_counts['count'], width, label='classes')
	multiplier += 1	
	
	# Add some text for labels, title and custom x-axis tick labels, etc.
	ax.set_ylabel('Sections / Classes Taught')
	ax.set_xticks(x+width/2, section_counts['PI'])
	#ax.set_yticks(range(20))
	ax.legend(loc='upper left', ncols=2)
	plt.xticks(rotation = 90) # Rotates X-Axis Ticks by 45-degrees
	plt.savefig('Tables/teaching_counts.png',bbox_inches='tight',pad_inches=1)
	plt.close()
	
	enrollments = lectures.pivot_table(index=['PI'],aggfunc={'Enrollment': 'sum'})
	enrollments.reset_index(inplace=True)
	enrollments.columns=['PI','Enrollment']
	
	x = np.arange(enrollments.shape[0])  # the label locations
	width = 0.25  # the width of the bars
	fig, ax = plt.subplots(layout='constrained')
	rects = ax.bar(x, enrollments['Enrollment'], width, label='Enrollment')

	

	# Add some text for labels, title and custom x-axis tick labels, etc.
	ax.set_ylabel('Students Taught')
	ax.set_xticks(x, enrollments['PI'])
	plt.xticks(rotation = 90) # Rotates X-Axis Ticks by 45-degrees
	plt.savefig('Tables/class_enrollments.png',bbox_inches='tight',pad_inches=1)
	plt.close()
	
	
if __name__ == "__main__":
	lastnames = ['Helenbrook','Ahmadi','Aidun','Issen']
	main(sys.argv,lastnames)