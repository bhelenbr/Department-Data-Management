#! /usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
from datetime import date

def main(argv):
	source = argv[1] # file to read
	try:
		df = pd.read_excel(source,header=0)
	except OSError:
		print("Could not open/read file: " + source)
		sys.exit()
	
	today = date.today()
	year = today.year
	begin_year = year - 3

	df = df[(df['Calendar Year'] >= begin_year)]
	df = df.reset_index()
	
	professional = df[(df['Type'] == 'Professional')]
	professional.reset_index()
	community = df[(df['Type'] == 'Community')]
	community.reset_index()
	university = df[(df['Type'] == 'University') | (df['Type'] == 'Department')]
	university.reset_index()
	
	table = professional.pivot_table(values=['Hours/Semester'], index=['FacultyName'], aggfunc={'Hours/Semester': 'sum'},observed=False)
	table = table.reset_index()
	table.columns=['FacultyName','Hours']
 
	# creating the bar plot
	fig = plt.figure(figsize = (10, 5))
	plt.bar(table['FacultyName'], table['Hours'], color ='blue',
			width = 0.4)
	plt.xticks(rotation = 90) # Rotates X-Axis Ticks by 45-degrees
	plt.xlabel("Faculty")
	plt.ylabel("Professional Service Hours")
	plt.ylim([0,300])
	plt.savefig('Tables/professional_service.png',bbox_inches='tight',pad_inches=1)
	plt.close()
	
	table = community.pivot_table(values=['Hours/Semester'], index=['FacultyName'], aggfunc={'Hours/Semester': 'sum'},observed=False)
	table = table.reset_index()
	table.columns=['FacultyName','Hours']
 
	# creating the bar plot
	fig = plt.figure(figsize = (10, 5))
	plt.bar(table['FacultyName'], table['Hours'], color ='blue',
			width = 0.4)
	plt.xticks(rotation = 90) # Rotates X-Axis Ticks by 45-degrees
	plt.xlabel("Faculty")
	plt.ylabel("Community Service Hours")
	plt.savefig('Tables/community_service.png',bbox_inches='tight',pad_inches=1)
	plt.close()
	
	table = university.pivot_table(values=['Hours/Semester'], index=['FacultyName'], aggfunc={'Hours/Semester': 'sum'},observed=False)
	table = table.reset_index()
	table.columns=['FacultyName','Hours']
 
	# creating the bar plot
	fig = plt.figure(figsize = (10, 5))
	plt.bar(table['FacultyName'], table['Hours'], color ='blue',
			width = 0.4)
	plt.xticks(rotation = 90) # Rotates X-Axis Ticks by 45-degrees
	plt.xlabel("Faculty")
	plt.ylabel("University Service Hours")
	plt.ylim([0,1000])
	plt.savefig('Tables/university_service.png',bbox_inches='tight',pad_inches=1)
	plt.close()
	
if __name__ == "__main__":
	main(sys.argv)