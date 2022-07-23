%reset_selective -f ^(?!failed_files).*$
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
os.chdir("C:/Users/aleja/OneDrive - University College London/Griffin Institute collaboration/Grifin_annotations/2D3D VIDEOS")
# os.chdir("C:/Users/Sera Bostan/University College London/Mazomenos, Evangelos - Griffin Institute collaboration/Grifin_annotations")

# Importing Excel file, particularly the 'Analysis' sheet within the file
analysis_xls = pd.read_excel('Case 8.xls', sheet_name='Analysis').values



"""¨¨¨ Extracting and saving OCHRA information ¨¨¨"""
''' def extract_ochra(analysis_xls): '''
ochra_last_row = None     # 'ochra_last_row' is used to store the last row position of the OCHRA data lataer on. Resetting the variable
check_failed = True       # 'check_failed' is used later on. Resetting variable

# Looping through 'all' rows and columns to find the size and position of the OCHRA information
for totals_row in range(2,len(analysis_xls)):      # Looping through rows [from 3rd row to last row in the sheet]
    # If the instance in the 'Timecode' column says 'Totals', row number is recorded and loop is exited    
    if analysis_xls[totals_row, 2] == 'Totals':
        check_failed = False      # Checkpoint to confirm 'Totals' was detected
        break

if check_failed == False:
    for ochra_last_row in reversed(range(2,totals_row)):      # Looping through rows [from row with 'Totals' to 3rd row in the sheet]
        # If all instances in the row [from 'Task Area' column to 'Further info' column] are empty, row number is recorded and loop is exited
        if (False in pd.isna(analysis_xls[ochra_last_row, 0:11])) == False:
            break

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

""" Modifying fourth column ('Subfile') to an appropriate format """
for row in range(0,len(ochra)):     # Looping through all of the instances in the column
    if pd.isna(ochra[row, 3]) == False:
        ochra[row, 3] = str(ochra[row, 3])      # Changing to string type

""" Modifying last column ('Further info') to an appropriate format """
for row in range(0,len(ochra)):     # Looping through all of the instances in the column
    if pd.isna(ochra[row, 10]) == False:
        ochra[row, 10] = str(ochra[row, 10])      # Changing to string type

''' return ochra, check_failed       # Giving 'ochra' and 'check_failed' to the function's output '''



"""¨¨¨ Labelling each annotation as START, ERR (Error), N.P. (Not Performed) or DESC (Description) ¨¨¨"""
''' def label_ochra(ochra): '''
# Each event is given one of these 4 descriptive labels for easier identification later on 
start = ['start', 'Start']      # 'start' is used to detect if an instance has the word 'Start' (or similar) later on. Defining variable
notperformed = ['not performed','Not performed','not done','Not done']       # 'notperformed' is used to detect if an instance has the words 'Not performed' (or similar) later on. Defining variable

# This function checks if the words in a word array (e.g. 'np' or 'start') can be found on a selected instance
def check_words(words, instance):
    check = False
    for i in range(0,len(words)):
        if (words[i] in instance) == True:
            check = True
            break
    return check

# Adding an empty column to hold the labels
ochra = np.insert(ochra, 2, np.full(len(ochra), np.nan), 1)

# There are some events where the 'Further info' is noted but the rest of columns of the OCHRA information are empty. Assuming these are just descriptions and adding the DESC label
for row in range(0,len(ochra)):         # Looping through all rows in 'ochra'
    check_filled = False in pd.isna(ochra[row, 0:11])    # Checking if instances in the row [from 'Task Area' column to 'Location (pelvic)' column] are empty or not
    # If all instances in the row are empty, a DESC label is given
    if (pd.isna(ochra[row, 11]) == False) and (check_filled == False):
        ochra[row, 2] = 'DESC'
        
# There are some events where the 'Timecode', 'Subfile' and 'Further info' are noted but the rest of columns of the OCHRA information are empty. Assuming these are just descriptions and adding the DESC label
for row in range(0,len(ochra)):         # Looping through all rows in 'ochra'
    check1_filled = False in pd.isna(ochra[row, 0:3])    # Checking if instances in the row [from 'Task Area' column to 'Label' column] are empty or not
    check2_filled = False in pd.isna(ochra[row, 5:11])    # Checking if instances in the row [from 'Tool-tissue Errors column to 'Location (pelvic)' column] are empty or not
    # If all instances in the row are empty, a DESC label is given
    if (pd.isna(ochra[row, 3]) == False) and (pd.isna(ochra[row, 4]) == False) and (pd.isna(ochra[row, 11]) == False) and (check1_filled == False) and (check2_filled == False):
        ochra[row, 2] = 'DESC'

# There are some events where the 'Task Area', 'Subtask Area', 'Timecode' and 'Subfile' are noted but the rest of columns of the OCHRA information are empty. Assuming these are start events and adding the START label
for row in range(0,len(ochra)):         # Looping through all rows in 'ochra'
    check_filled = False in pd.isna(ochra[row, 5:12])    # Checking if instances in the row [from 'Tool-tissue Errors' column to 'Further info' column] are empty or not
    # If all instances in the row are empty, a START label is given
    if ((pd.isna(ochra[row, 0]) == False) or (pd.isna(ochra[row, 1]) == False)) and (pd.isna(ochra[row, 3]) == False) and (pd.isna(ochra[row, 4]) == False) and (check_filled == False):
        ochra[row, 2] = 'START'
        ochra[row, 11] = 'ASSUMED START'       # Noting in 'Further info' this event was assumed to be a start event (for clarity)

# There are some events where the 'Task Area' and 'Subtask Area' are noted but the rest of columns of the OCHRA information are empty. Assuming these cases were not performed and adding the N.P. label
for row in range(0,len(ochra)):         # Looping through all rows in 'ochra'
    check_filled = False in pd.isna(ochra[row, 2:12])    # Checking if instances in the row [from 'Label' column to 'Further info' column] are empty or not
    # If all instances in the row are empty, a N.P. label is given
    if ((pd.isna(ochra[row, 0]) == False) or (pd.isna(ochra[row, 1]) == False)) and (check_filled == False):
        ochra[row, 2] = 'N.P.'
        ochra[row, 11] = 'ASSUMED NOT PERFORMED'       # Noting in 'Further info' this event was assumed to not be performed (for clarity)

# Marking the rest of events
for row in range(0,len(ochra)):     # Looping through all rows in 'ochra'
    check_filled = False in pd.isna(ochra[row, 5:11])    # Checking if instances in the row [from 'Tool-tissue Errors' column to 'Location (pelvic)' column] are empty or not
    # If all instances in the row are empty, and the 'Further info' column has the 'Start' word in it, labelling as START
    if (check_filled == False) and (check_words(start, ochra[row, 11]) == True):
        ochra[row, 2] = 'START'
    # If all instances in the row are empty, and the 'Further info' column has the 'Not performed' words in it, labelling as N.P.
    elif (check_filled == False) and (check_words(notperformed, ochra[row, 11]) == True):
        ochra[row, 2] = 'N.P.'
    # If the row is not fully empty, labelling as ERR
    elif check_filled == True:
        ochra[row, 2] = 'ERR'

# Marking as 'OTHER' the events that did not pass the before tests
for row in range(0,len(ochra)):
    if pd.isna(ochra[row, 2]) == True:
        ochra[row, 2] = 'OTHER'
        
''' return ochra        # Giving 'ochra' to the function's output '''



"""¨¨¨ Adding global timestamps to each annotation ¨¨¨"""
for row in range(0,len(ochra)):
    if (ochra[row, 2] == 'START') == True:
        video_file = ochra[row, 4]



# 2nd part of measuring time of execution of the code
# print('Executed in %.2f seconds.' % (time.time() - start_time))
