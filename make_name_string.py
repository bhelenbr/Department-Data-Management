import re
import sys
from make_cv.stringprotect import abbreviate_name_list
from make_cv.stringprotect import last_first
from make_cv.stringprotect import abbreviate_name

def make_name_string(name):
	name_lf = last_first(name)
	names = name_lf.split(",")
	lastname = names[0].strip() +"/"
	firstname = names[1].strip()
	
	middle_initial = False
	if firstname.find(".") > -1:
		middle_initial = True

	
	name_lf_ab = last_first(abbreviate_name(name))
	names = name_lf_ab.split(",")
	firstname_ab = names[1].strip()
	
	# making variants
	firstname_delim = firstname.replace(" ","\\bibnamedelima ")
	firstname_delim_no_dot = firstname_delim.replace(".","")
	
	firstname_ab_delim = firstname_ab.replace(". ",".\\bibnamedelimi ")
	firstname_ab_delim_no_dot = firstname_ab.replace(". ","\\bibnamedelima ").replace(".","")

	names_string = lastname +firstname_delim
	names_string += "," +lastname +firstname_ab_delim
	names_string += "," +lastname +firstname_ab[0]

	if (middle_initial): 
		names_string += "," +lastname +firstname[:-3]
		names_string += "," +lastname +firstname_delim_no_dot
		names_string += "," +lastname +firstname_ab_delim_no_dot
		names_string += "," +lastname +firstname_ab.replace(".","").replace(" ","")
		names_string += "," +lastname +firstname_ab[0] +"."
		
	return names_string
	
def main():
	if len(sys.argv) != 2:
		print("Usage: python script.py <person's name>")
		sys.exit(1)
	
	print(make_name_string(sys.argv[1]))

if __name__ == "__main__":
	main()
