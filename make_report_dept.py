#! /usr/bin/env python3

import os
import sys
import glob
import pandas as pd
import platform
import shutil
import openpyxl


# Run this script from the Department Data folder to create annual report

# Source is faculty folder
if platform.system() == 'Windows':
	faculty_source = r"S:\departments\Mechanical & Aeronautical Engineering\Faculty"
	gathered_source = r"S:\departments\Mechanical & Aeronautical Engineering\Confidential Information\Department Data"
	sys.path.insert(0, r"S:\departments\Mechanical & Aeronautical Engineering\Faculty\_Scripts")
	sys.path.insert(0, r"S:\departments\Mechanical & Aeronautical Engineering\Confidential Information\Department Data\Scripts")
else:
	faculty_source = r"/Volumes/Mechanical & Aerospace Engineering/Faculty"
	gathered_source = r"/Volumes/Mechanical & Aerospace Engineering/Confidential Information/Department Data"
	sys.path.insert(0, r"/Volumes/Mechanical & Aerospace Engineering/Faculty/_Scripts")
	sys.path.insert(0, r"/Volumes/Mechanical & Aerospace Engineering/Confidential Information/Department Data/Scripts")

try:
	files = glob.glob('Tables_dept/*')
	for f in files:
		os.remove(f)
except:
	pass
	
# Get list of last names
FacultyNames = os.listdir(faculty_source) # For each faculty member
LastNames = []
for i,name in enumerate(FacultyNames):
	if name[0].isalnum():
		LastNames.append(name[0:name.find(",")])	
		
years = 5

import srs_plot_dept
srs_plot_dept.main(years,gathered_source +os.sep +"Proposals & Grants" +os.sep +'proposals & grants.xlsx')
import UR_plot_dept
UR_plot_dept.main(years,gathered_source +os.sep +"Undergraduate Research" +os.sep +'undergraduate research data.xlsx')
import pubs_plot_dept
pubs_plot_dept.main(years,gathered_source +os.sep +"Scholarship")
import thesis_plot_dept
thesis_plot_dept.main(years,gathered_source +os.sep +"Thesis" +os.sep +'thesis data.xlsx')
import service_plot_dept
service_plot_dept.main(years,gathered_source +os.sep +"Service" +os.sep +'service data.xlsx')
import reviewing_plot_dept
reviewing_plot_dept.main(years,gathered_source +os.sep +"Reviewing" +os.sep +'reviews data.xlsx')
import prospective_plot_dept
prospective_plot_dept.main(years,gathered_source +os.sep +"Prospective Visits" +os.sep +'prospective visits.xlsx')
import teaching_eval_plot_dept
teaching_eval_plot_dept.main(years,gathered_source +os.sep +"Teaching" +os.sep +'Teaching Eval Data.xlsx',LastNames)
import teaching_load_plot_dept
teaching_load_plot_dept.main(years,gathered_source +os.sep +"Teaching" +os.sep +'Teaching Info.xlsx',LastNames)
import advising_plot_dept
advising_plot_dept.main(years,gathered_source +os.sep +"Advising" +os.sep +'Advising Evaluation Data.xlsx',LastNames)

os.system('pdflatex annual_report_dept.tex')
os.system('pdflatex annual_report_dept.tex')
os.remove('annual_report_dept.aux')
os.remove('annual_report_dept.log')
os.remove('annual_report_dept.out')
os.remove('annual_report_dept.toc')
#os.remove('annual_report_dept-blx.bib')
#os.remove("annual_report_dept.synctex(busy)")