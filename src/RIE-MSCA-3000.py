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
	csv_filename = ''.join(ics_filename[0] + ics_filename[-1][:-4] + ".csv")
	return csv_filename


## Example CSV Row :
# A5 : 5PASNMCN MOLECULAR AND C SEM2 000001/Sem/02
# B5 : 2024-02-13 11:30:00+00:00	
# C5 : 2024-02-13 13:30:00+00:00	
# D5 : Event type: Seminar Description: Molecular and Cellular Neuroscience Location: 
#      WEC CLASSROOM 02 Date: Tuesday, 13 February 2024 Weeks: 22-26, 28-32 Staff: 
#      Mitchell , Jacqueline, Vance, Caroline Zone: Denmark Hill	
# E5 : WEC CLASSROOM 02


def main():
	convert = csv_ical.Convert()

	convert.ICS_FILE_LOCATION = find_path_GUI()
	# Prototyping: Use hard-coded path
	# Production : Use relative path
	csv_dir = "/home/minseok/Python/Projects/RIE-MSCA-3000/resources/csv_files"
	csv_filename = extract_name(convert.ICS_FILE_LOCATION)
	convert.CSV_FILE_LOCATION = os.path.join(csv_dir, csv_filename)

	convert.read_ical(convert.ICS_FILE_LOCATION)
	convert.make_csv()
	convert.save_csv(convert.CSV_FILE_LOCATION)
	# convert.save_csv('~/Python/RIE-MSCA-3000/resources/csv_files/RYUMinseok.ics')

# def todo():
# 	ics_folder = '/PATH/TO/FOLDER/'
# 	csv_folder = Csv-library.csv_from_ics(ics_folder)

#	# db name: members_lessons.db

# 	ca_all = Calendar(csv_folder, mode='ALL')
#     ca_all.init_db()
#     ca_all.merge_db()
#     ca_all.view()

#     ca_admin = Calendar(csv_folder, mode='ADMIN')
#     ca_admin.init_db()
#     ca_admin.merge_db()
#     ca_admin.view()

#     # Question: UI Drag-N-Drop Manual ?
#     ca_manual = Calendar(csv_folder, mode='MANUAL')
#     ca_manual.init_db()
#     ca_manual.merge_db()
#     ca_manual.view()

if __name__=="__main__":
	main()