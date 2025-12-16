import re
import sys
from make_cv.stringprotect import abbreviate_name_list
from make_cv.stringprotect import last_first
from make_cv.stringprotect import abbreviate_name

def extract_experience(latex_file):
	with open(latex_file, "r", encoding="utf-8") as f:
		content = f.read()
	
	# Extract the EXPERIENCE section
	experience_match = re.search(r"\\section\*{EXPERIENCE}(.*?)(?=\\section\*|$)", content, re.DOTALL)
	if not experience_match:
		raise ValueError("EXPERIENCE section not found in the LaTeX file.")
	
	experience_content = experience_match.group(1).strip()
	
	# Extract each job entry
	job_entries = re.findall(r"{\\bf (.+?)}\s*\\hspace\*{\\fill}\s*(.*?)\\\\\s*{\\em (.+?)}\s*\\hfill\s*{\\em (.+?)}", experience_content, re.DOTALL)
	
	return job_entries

def format_experience(job_entries, output_file):
	with open(output_file, "w", encoding="utf-8") as f:
		f.write("\\begin{rubric}{Employment History}\n\n")
		
		for institution, location, title, dates in job_entries:
			dates_formatted = dates.replace("Present", "\\textit{Present}")
			f.write(f"\\entry*[{dates_formatted}] ")
			f.write(f"\\textbf{{{title},}} {institution}, {location}.\n")
			
		f.write("\\end{rubric}\n")

def extract_education(latex_file):
	with open(latex_file, "r", encoding="utf-8") as f:
		content = f.read()
	
	# Extract the EDUCATION section
	education_match = re.search(r"\\section\*{EDUCATION}(.*?)(?=\\section\*|$)", content, re.DOTALL)
	if not education_match:
		raise ValueError("EDUCATION section not found in the LaTeX file.")
	
	education_content = education_match.group(1).strip()
	
	# Extract each education entry
	education_entries = re.findall(r"{\\bf (.+?)}\s*\\hspace\*{\\fill}\s*(.*?)\\\\\s*{\\em (.+?)}", education_content, re.DOTALL)
	
	return education_entries

def format_education(education_entries, output_file):
	with open(output_file, "w", encoding="utf-8") as f:
		f.write("\\begin{rubric}{Education}\n\n")
		
		for institution, location, year in education_entries:
			f.write(f"\\entry*[{year}] ")
			f.write(f"\\textbf{{{institution},}} {location}.\n")
			
		f.write("\\end{rubric}\n")

def extract_contact_info(latex_file):
	with open(latex_file, "r", encoding="utf-8") as f:
		content = f.read()
	
	name_match = re.search(r"\\Large{\\bf (.+?)}", content)
	phone_match = re.search(r"\(\d{3}\) \d{3}-\d{4}", content)
	email_match = re.search(r"\\em\{(.+?@.+?)\}", content)
	
	name = name_match.group(1) if name_match else "Unknown Name"
	phone = phone_match.group(0) if phone_match else "Unknown Phone"
	email = email_match.group(1) if email_match else "Unknown Email"
	
	return name, phone, email

def format_contact_info(name, phone, email, output_file):
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

	names_string = lastname +firstname_ab[0]

	with open(output_file, "w", encoding="utf-8") as f:
		f.write(r"""% Specify you last name/first initial to have it be bold in the author list
% if you have changed your name or if you need to highlight multiple authors, you can specify multiple names separated by a comma {Doe/J,Smith/T} """)
		f.write(f"\n\\mynames{{{names_string}}}\n\n")
		f.write(f"%% Photo is only shown if \"usePhoto\" is true\n")
		f.write(r"\setboolean{usePhoto}{true}")
		f.write("\n\n\\leftheader{%\n")
		f.write(f"  {{\\LARGE\\bfseries\\sffamily {name}, Ph.D.}}\\\\\n")
		f.write(f"  Clarkson University, Potsdam, NY 13699-5725, {phone}\\\\\n")
		f.write(f"  \\makefield{{\\faEnvelope[regular]}}{{\\href{{mailto:{email}}}{{\\texttt{{{email}}}}}}}\n")
		f.write(r"""  \makefield{\faLinkedin}{\href{http://www.linkedin.com/in/example/}{\texttt{LinkedIn}}}
  \makefield{\faGlobe}{\href{http://example.example.org/}{\texttt{Webpage}}}""")
		f.write("\n}\n")

def main():
	if len(sys.argv) != 2:
		print("Usage: python script.py <latex_file>")
		sys.exit(1)
	
	latex_file = sys.argv[1]
	employment_file = "employment.tex"
	education_file = "education.tex"
	contact_file = "contact_info.tex"
	
	#job_entries = extract_experience(latex_file)
	#format_experience(job_entries, employment_file)
	
	#education_entries = extract_education(latex_file)
	#format_education(education_entries, education_file)
	
	name, phone, email = extract_contact_info(latex_file)
	format_contact_info(name, phone, email, contact_file)
	
	print(f"Employment history successfully written to {employment_file}")
	print(f"Education history successfully written to {education_file}")
	print(f"Contact information successfully written to {contact_file}")

if __name__ == "__main__":
	main()
