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
	df = df.reset_index()
	
	professional = df[(df['Type'] == 'Professional')]
	professional.reset_index()
	community = df[(df['Type'] == 'Community')]
	community.reset_index()
	university = df[(df['Type'] == 'University') | (df['Type'] == 'Department')]
	university.reset_index()
	
	table = professional.pivot_table(values=['Hours/Semester'], index=['Calendar Year'], aggfunc={'Hours/Semester': 'sum'},observed=False)
	table = table.reset_index()
	table.columns=['Calendar Year','Hours']
 
	# creating the bar plot
	fig = plt.figure(figsize = (10, 5))
	plt.bar(table['Calendar Year'], table['Hours'], color ='blue',
			width = 0.4)
	plt.xticks(rotation = 90) # Rotates X-Axis Ticks by 45-degrees
	plt.xlabel("Year")
	plt.ylabel("Professional Service Hours")
	plt.savefig('Tables_dept/professional_service.png',bbox_inches='tight',pad_inches=1)
	plt.close()
	
	table = community.pivot_table(values=['Hours/Semester'], index=['Calendar Year'], aggfunc={'Hours/Semester': 'sum'},observed=False)
	table = table.reset_index()
	table.columns=['Calendar Year','Hours']
 
	# creating the bar plot
	fig = plt.figure(figsize = (10, 5))
	plt.bar(table['Calendar Year'], table['Hours'], color ='blue',
			width = 0.4)
	plt.xticks(rotation = 90) # Rotates X-Axis Ticks by 45-degrees
	plt.xlabel("Year")
	plt.ylabel("Community Service Hours")
	plt.savefig('Tables_dept/community_service.png',bbox_inches='tight',pad_inches=1)
	plt.close()
	
	table = university.pivot_table(values=['Hours/Semester'], index=['Calendar Year'], aggfunc={'Hours/Semester': 'sum'},observed=False)
	table = table.reset_index()
	table.columns=['Calendar Year','Hours']
 
	# creating the bar plot
	fig = plt.figure(figsize = (10, 5))
	plt.bar(table['Calendar Year'], table['Hours'], color ='blue',
			width = 0.4)
	plt.xticks(rotation = 90) # Rotates X-Axis Ticks by 45-degrees
	plt.xlabel("Year")
	plt.ylabel("University Service Hours")
	plt.savefig('Tables_dept/university_service.png',bbox_inches='tight',pad_inches=1)
	plt.close()
	
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='This script outputs plots of service hours in the last [YEARS] years')
	parser.add_argument('-y', '--years',default="3",type=int,help='the number of years to output')
	parser.add_argument('inputfile',help='the input excel file name')           
	args = parser.parse_args()
	
	main(args.years,args.inputfile)