# AUTHOR      : Minseok Ryu
# DATA CREATED: 15/12/2023

# https://medium.com/@bobbie.wxy/how-to-convert-calendar-ics-to-csv-excel-using-python-3-steps-ca3903530aa3

import os
import re
import csv_ical
import tkinter
from tkinter.filedialog import askopenfilename

def find_path_GUI():
	tkinter.Tk().withdraw() # we don't want a full GUI, so keep root window from appearing
	filename = askopenfilename()
	return filename

# 'KURUPPU MUDIYANSELAGE, Jineth.ics' --> JinethKURUPPU.csv
def extract_name(filepath):
	ics_filename = filepath.split("/")[-1]
	ics_filename = re.findall(r'\s|,|[^,\s]+', ics_filename)
	csv_filename = ''.join(ics_filename[-1] + ics_filename[0] + ".csv")
	print(csv_filename)
	return csv_filename

def main():
	convert = csv_ical.Convert()

	convert.ICS_FILE_LOCATION = find_path_GUI()
	csv_dir = "~/Python/RIE-MSCA-3000/resources/csv_files"
	csv_filename = extract_name(convert.ICS_FILE_LOCATION)
	convert.CSV_FILE_LOCATION = os.path.join(csv_dir, csv_filename)

	convert.read_ical(convert.ICS_FILE_LOCATION)
	convert.make_csv()
	convert.save_csv(convert.CSV_FILE_LOCATION)

if __name__=="__main__":
	main()