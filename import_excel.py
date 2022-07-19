%reset -f
"""¨¨¨ Setting up environment & importing files ¨¨¨"""
# Importing python libraries
import sys
import os
from datetime import datetime, date
import time
import pandas as pd
import numpy as np

# 1st part of measuring time of execution of the code
start_time = time.time()

# Moving to directory where anotations are stored
# os.chdir("C:/Users/aleja/OneDrive - University College London/Griffin Institute collaboration/Grifin_annotations")
os.chdir("C:/Users/Sera Bostan/University College London/Mazomenos, Evangelos - Griffin Institute collaboration/Grifin_annotations")

# Importing Excel file, particularly the 'Analysis' sheet within the file
analysis_xls = pd.read_excel('Case 3.xls', sheet_name='Analysis').values


"""¨¨¨ Extracting and saving OCHRA information ¨¨¨"""
ochra_last_row = None     # 'ochra_last_row' is used to store the last row position of the OCHRA data lataer on. Resetting the variable

# Looping through 'all' rows and columns to find the size and position of the OCHRA information
for row in range(2,len(analysis_xls)):      # Looping through rows [from 3rd row to last row in the sheet]
    check11 = True       # 'check11' is used later on. Resetting variable
    empty_boolean = pd.isna(analysis_xls[row, 0:11])     # Checking if instances in the row [from 'Task Area' column to 'Location (pelvic)' column] are empty or not
    for col in range(0,11):
        if empty_boolean[col] == False:       # If a single instance in the row is not empty, current loop iteration is broken and next row is checked
            check11 = False
            break
    if check11 == True:       # If all instances in the row are empty, row number is recorded and loop is exited
        ochra_last_row = row
        break

for n in range(0, 11):
    x = 1
    
# Storing the OCHRA data in a new variable using the positional information obtained earlier
ochra_xls = analysis_xls[2:ochra_last_row, 0:11]

# Sanity check to confirm the retrieved OCHRA data does not have the 'Totals' (shown below in the Excel sheet)
if ('Totals' in ochra_xls) == True:
    sys.exit("OCHRA data retrieved incorrectly. 'Totals' info was also extracted")
    
# Copying the OCHRA data into a new variable for modification, keeping the original OCHRA data
ochra = np.copy(ochra_xls)      # 'ochra' will contain the adjusted OCHRA information. Setting the variable

""" Modifying first column ('Task Area') labels to an appropriate format """
for row in range(0,len(ochra)):     # Looping through all of the instances in the column
    if pd.isna(ochra[row, 0]) == False:
        ochra[row, 0] = int(ochra[row, 0])      # Changing to integer type

""" Modifying second column ('Subtask Area') labels to an appropriate format """
for row in range(0,len(ochra)):     # Looping through all of the instances in the column
    if pd.isna(ochra[row, 1]) == False:
        ochra[row, 1] = str(ochra[row, 1])      # Changing to string type

""" Modifying third column ('Timecode') times to an appropriate format """
for row in range(0,len(ochra)):     # Looping through all of the instances in the column
    if pd.isna(ochra[row, 2]) == False:
        ochra[row, 2] = datetime.combine(date.min, ochra[row, 2]) - datetime.min      # Changing to .timedelta format (for easier working with later)

""" Modifying last column ('Further info') to an appropriate format """
for row in range(0,len(ochra)):     # Looping through all of the instances in the column
    if pd.isna(ochra[row, 10]) == False:
        ochra[row, 10] = str(ochra[row, 10])      # Changing to string type


""" Labelling each annotation as START, ERR (Error) or N.P. (Not Performed) """
# Each event is given one of these 3 descriptive labels for easier identification and working with later on 
ochra = np.insert(ochra, 2, np.full(len(ochra), np.nan), 1)         # Adding an empty column to hold the labels

# There are some events where the 'Task Area' is noted but the rest of columns of the OCHRA information are empty. Assuming these cases were not performed and adding the N.P. label
for row in range(0,len(ochra)):         # Looping through rows 
    check31 = True       # 'check31' is used later on. Resetting variable
    empty_boolean = pd.isna(ochra[row, 1:12])     # Checking if instances in the row [from 'Subtask Area' column to 'Further info' column] are empty or not
    for col in range(0,11):
        if empty_boolean[col] == False:       # If a single instance in the row is not empty, current loop iteration is broken and next row is checked
            check31 = False
            break
    if check31 == True:      # If all instances in the row are empty, labelling as N.P.
        ochra[row, 2] = 'N.P.'
        ochra[row, 11] = 'ASSUMED NOT PERFORMED'       # Noting in 'Further info' this event was assumed to not be performed

# Marking rest of cases
for row in range(0,len(ochra)):     # Looping through rows
    check32 = True       # 'check32' is used later on. Resetting variable
    empty_boolean = pd.isna(ochra[row, 5:11])     # Checking if instances in the row [from 'Tool-tissue Errors' column to 'Location (pelvic)' column] are empty or not
    for col in range(0,6):
        if empty_boolean[col] == False:       # If a single instance in the row is not empty, noting it down
            check32 = False
            break
    # If all instances in the row are empty, and the 'Further info' column has the 'Start' word in it, labelling as START
    if check32 == True and (('start' in ochra[row, 11]) == True or ('Start' in ochra[row, 11])):
        ochra[row, 2] = 'START'
    # If all instances in the row are empty, and the 'Further info' column has the 'Not performed' words in it, labelling as N.P.
    elif check32 == True and (('not performed' in ochra[row, 11]) == True or ('Not performed' in ochra[row, 11])):
        ochra[row, 2] = 'N.P.'
        pass
    elif check32 == False:      # If row is not empty, labelling as ERR
        ochra[row, 2] = 'ERR'


"""¨¨¨ Adding global timestamps to each annotation ¨¨¨"""
for row in range(0,len(ochra)):
    if (ochra[row, 2] == 'START') == True:
        video_file = ochra[row, 4]

# I commented this

# 2nd part of measuring time of execution of the code
# print('Executed in %.2f seconds.' % (time.time() - start_time))
