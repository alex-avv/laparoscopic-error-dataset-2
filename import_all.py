%reset -f
"""¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨"""
"""¨¨¨ Setting up environment & files' path ¨¨¨"""
# Importing python libraries
import sys
import os
from datetime import datetime, date
import time
import pandas as pd
import numpy as np

# Moving to directory where anotations are stored
os.chdir("C:/Users/aleja/OneDrive - University College London/Griffin Institute collaboration/Grifin_annotations/2D3D VIDEOS")
"""¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨"""


"""¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨"""
"""¨¨¨ Extracting and saving OCHRA information ¨¨¨"""
def extract_ochra(analysis_xls):
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
    
    return ochra, check_failed       # Giving 'ochra' and 'check_failed' to the function's output
"""¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨"""


"""¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨"""
"""¨¨¨ Labelling each annotation as START, ERR (Error), N.P. (Not Performed) or DESC (Description) ¨¨¨"""
def label_ochra(ochra):
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

    # There are some events where the 'Task Area' and 'Subtask Area' are noted but the rest of columns of the OCHRA information are empty. Assuming these cases were not performed and adding the N.P. label
    for row in range(0,len(ochra)):         # Looping through all rows in 'ochra'
        check_filled = False in pd.isna(ochra[row, 2:12])    # Checking if instances in the row [from 'Label' column to 'Further info' column] are empty or not
        # If all instances in the row are empty, a N.P. label is given
        if ((pd.isna(ochra[row, 0]) == False) or (pd.isna(ochra[row, 1]) == False)) and (check_filled == False):
            ochra[row, 2] = 'N.P.'
            ochra[row, 11] = 'ASSUMED NOT PERFORMED'       # Noting in 'Further info' this event was assumed to not be performed (for clarity)

    # There are some events where the 'Task Area', 'Subtask Area', 'Timecode' and 'Subfile' are noted but the rest of columns of the OCHRA information are empty. Assuming these are start events and adding the START label
    for row in range(0,len(ochra)):         # Looping through all rows in 'ochra'
        check_filled = False in pd.isna(ochra[row, 5:12])    # Checking if instances in the row [from 'Tool-tissue Errors' column to 'Further info' column] are empty or not
        # If all instances in the row are empty, a START label is given
        if ((pd.isna(ochra[row, 0]) == False) or (pd.isna(ochra[row, 1]) == False)) and (pd.isna(ochra[row, 3]) == False) and (pd.isna(ochra[row, 4]) == False) and (check_filled == False):
            ochra[row, 2] = 'START'
            ochra[row, 11] = 'ASSUMED START'       # Noting in 'Further info' this event was assumed to be a start event (for clarity)

    # There are some events where the 'Task Area', 'Subtask Area', 'Timecode', 'Subfile' and 'Further info' are noted but the rest of columns of the OCHRA information are empty. Assuming these are just descriptions and adding the DESC label
    for row in range(0,len(ochra)):         # Looping through all rows in 'ochra'
        check_filled = False in pd.isna(ochra[row, 5:11])    # Checking if instances in the row [from 'Tool-tissue Errors column to 'Location (pelvic)' column] are empty or not
        # If all instances in the row are empty, a DESC label is given
        if (pd.isna(ochra[row, 3]) == False) and (pd.isna(ochra[row, 4]) == False) and (pd.isna(ochra[row, 11]) == False) and (check_filled == False) and (check_words(start, ochra[row, 11]) == False) and (check_words(notperformed, ochra[row, 11]) == False):
            ochra[row, 2] = 'DESC'

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

    return ochra        # Giving 'ochra' to the function's output
"""¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨"""


"""¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨"""
"""¨¨¨ Testing OCHRA information is in the correct format ¨¨¨"""
def test_ochra(ochra):
    check_failed = False       # 'check_failed' is used later on. Resetting variable
    
    # 'file' and 'subfile' are used to test the 'Subfile' column later on. Setting variables
    file = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15']
    subfile = ['0','AA','AB','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

    
    """ Checking 'Task Area' column) """
    col_taskarea = 0
    # Confirming all instances in the column are between 1-10
    for row in range(0,len(ochra)):
        if pd.isna(ochra[row, col_taskarea]) == False:
            if (ochra[row, col_taskarea] in [1,2,3,4,5,6,7,8,9,10]) == False:       # If an instance is not in the available options, test fails
                check_failed = True
                break
            
    """ Checking 'Subtask Area' column """
    col_subtaskarea = 1
    # Confirming all instances in the column are between a-d
    for row in range(0,len(ochra)):
        if pd.isna(ochra[row, col_subtaskarea]) == False:
            if (ochra[row, col_subtaskarea] in ['a','b','c','d']) == False:       # If an instance is not in the available options, test fails
                check_failed = True
                break
    
    """ Checking 'Label' column """
    col_label = 2
    # Confirming all instances in the column are either 'START', 'ERR', 'N.P.' or 'DESC'
    for row in range(0,len(ochra)):
        if pd.isna(ochra[row, col_label]) == False:
            if (ochra[row, col_label] in ['START','ERR','N.P.','DESC']) == False:       # If an instance is not in the available options, test fails
                check_failed = True
                break
        elif pd.isna(ochra[row, col_label]) == True:
            check_failed = True
            break
            
    
    """ Checking 'Subfile' column """
    col_subfile = 4
    # Confirming all instances in the column are between 1-15 (1st character in most cases) & B-Z (2nd charecter in most cases)
    for row in range(0,len(ochra)):
        if pd.isna(ochra[row, col_subfile]) == False:
            if len(ochra[row, col_subfile]) == 1:         # Testing when instance only has 1 character (e.g. '1')
                if (ochra[row, col_subfile] in file) == False:       # If an instance is not in the available options, test fails
                    check_failed = True
                    break
            elif len(ochra[row, col_subfile]) == 2:       # Testing when instance has 2 characters (e.g. '1B' or '10')
                if ((ochra[row, col_subfile][0] in file) == False) or ((ochra[row, col_subfile][1] in subfile) == False):       # If an instance is not in the available options, test fails
                    if (ochra[row, col_subfile][0:2] in file) == False:
                        check_failed = True
                        break
            elif len(ochra[row, col_subfile]) == 3:       # Testing when instance has 3 characters (e.g. '10B or 1AB')
                if ((ochra[row, col_subfile][0:2] in file) == False) or ((ochra[row, col_subfile][2] in subfile) == False):       # If an instance is not in the available options, test fails
                    if ((ochra[row, col_subfile][0] in file) == False) or ((ochra[row, col_subfile][1:3] in subfile) == False):
                        check_failed = True
                        break    
            else:       # Any other options
                check_failed = True
                break
    
    return check_failed      # Returning the value of 'check_failed' to the function's output
"""¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨"""


"""¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨"""
"""¨¨¨ Importing files & testing if OCHRA information is in correct format ¨¨¨"""
# 1st part of measuring time of execution of the code
start_time = time.time()

missing_files = ''      # 'missing_files' is used to store the cases whos' anotations are missing later on. Resetting variable
failed_files = ''       # 'failed_files' is used to store the cases whos' OCHRA data extraction is unsuccessful later on. Resetting variable

# Looping through all of the cases' spreadsheets in the Griffin dataset 
for index in range(1,91):
    analysis_xls = None
    file_name = f'Case {index}.xls'        # 'file_name' is used for the name of the file to be imported later on. Setting variable
    
    try:        # Importing Excel file, particularly the 'Analysis' sheet within the file
        analysis_xls = pd.read_excel(file_name, sheet_name='Analysis').values
        check_missing = False
    except:     # If it is not possible to find the file, the case number is recorded 
        missing_files = missing_files + f', {index}'
        check_missing = True
  
    if check_missing == False:
        try:        # Extracting and testing the OCHRA data using our preset functions defined earlier
            ochra, check_failed = extract_ochra(analysis_xls)
            ochra = label_ochra(ochra)
            if check_failed == True:    # If localisation of the OCHRA data in the Excel sheet is not successful, the case number is recorded 
                failed_files = failed_files + f', {index}'
            else:
                if test_ochra(ochra) == True:          # If the check fails, the case number is recorded
                    failed_files = failed_files + f', {index}'
        except:     # If it is not possible to retrieve the OCHRA data from the file, the case number is recorded 
            failed_files = failed_files + f', {index}'
    

# Printing on screen the files that are missing and with failed OCHRA data extraction
# print(f'\nCases {missing_files[2:]} are missing')
# print(f'Cases {failed_files[2:]} have inappropriate/failed OCHRA data ')

# 2nd part of measuring time of execution of the code
# print('Executed in %.2f seconds.' % (time.time() - start_time))

