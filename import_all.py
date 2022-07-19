%reset -f
""" Setting up environment & files' path """
# Importing python libraries
import sys
import os
from datetime import datetime, date
import time
import pandas as pd
import numpy as np

# Moving to directory where anotations are stored
os.chdir("C:/Users/aleja/OneDrive - University College London/Griffin Institute collaboration/Grifin_annotations")


""" Extracting and saving OCHRA information """
def extract_ochra(analysis_xls):
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
        
    # Storing the OCHRA data in a new variable using the positional information obtained earlier
    ochra_xls = analysis_xls[2:ochra_last_row, 0:11]
    
    # Sanity check to confirm the retrieved OCHRA data does not have the 'Totals' (shown below in the Excel sheet)
    if ('Totals' in ochra_xls) == True:
        sys.exit("OCHRA data retrieved incorrectly. 'Totals' info was also extracted")
        
    # Copying the OCHRA data into a new variable for modification, keeping the original OCHRA data
    ochra = np.copy(ochra_xls)      # 'ochra' will contain the adjusted OCHRA information. Setting the variable
    
    """ Filling first column ('Task Area') approppriately """
    # Only the first of a group of annotations belonging to the same Task Area has the first column filled (shown in Excel sheet). Filling out the rest of empty instances
    for row in range(0,len(ochra)):     # Looping through all of the instances in the column
        if pd.isna(ochra[row, 0]) == True:      # If instance is not filled out, appointing value of previous instance
            ochra[row, 0] = ochra[row - 1, 0]
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
    
    return ochra       # Giving 'ochra' to the function's output


""" Testing OCHRA information is in the correct format"""
def test_ochra(ochra):
    check21 = True       # 'check21' is used later on. Resetting variable
    
    """ Checking first column ('Task Area') """
    # Confirming all instances in the column are between 1-10
    for row in range(0,len(ochra)):
        if (ochra[row, 0] in [1,2,3,4,5,6,7,8,9,10]) == False:       # If an instance is not in the appropriate format, case number is recorded
            check21 = False
            
    """ Checking second column ('Subtask Area') """
    # Confirming all instances in the column are between a-d
    for row in range(0,len(ochra)):
        if pd.isna(ochra[row, 1]) == False:
            if (ochra[row, 1] in ['a','b','c','d']) == False:       # If an instance is not in the appropriate format, case number is recorded
                check21 = False
    
    return check21      # Returning the value of 'check21' to the function's output


""" Adding a  OCHRA information is in the correct format"""
def test_ochra(ochra):
    check21 = True       # 'check21' is used later on. Resetting variable
    
    """ Checking first column ('Task Area') """
    # Confirming all instances in the column are between 1-10
    for row in range(0,len(ochra)):
        if (ochra[row, 0] in [1,2,3,4,5,6,7,8,9,10]) == False:       # If an instance is not in the appropriate format, case number is recorded
            check21 = False
            
    """ Checking second column ('Subtask Area') """
    # Confirming all instances in the column are between a-d
    for row in range(0,len(ochra)):
        if pd.isna(ochra[row, 1]) == False:
            if (ochra[row, 1] in ['a','b','c','d']) == False:       # If an instance is not in the appropriate format, case number is recorded
                check21 = False
    
    return check21      # Returning the value of 'check21' to the function's output


""" Importing files & testing if OCHRA information is in correct format """
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
        check1 = True
    except:     # If it is not possible to find the file, the case number is recorded 
        missing_files = missing_files + f', {index}'
        check1 = False
  
    if check1 == True:
        try:        # Extracting and testing the OCHRA data using our preset functions defined earlier
            ochra = extract_ochra(analysis_xls)
            if test_ochra(ochra) == False:          # If the check fails, the case number is recorded
                failed_files = failed_files + f', {index}'
        except:     # If it is not possible to retrieve the OCHRA data from the file, the case number is recorded 
            failed_files = failed_files + f', {index}'
    

# Printing on screen the files that are missing and with failed OCHRA data extraction
# print(f'\nCases {missing_files[2:]} are missing')
# print(f'Cases {failed_files[2:]} have inappropriate/failed OCHRA data ')

# 2nd part of measuring time of execution of the code
# print('Executed in %.2f seconds.' % (time.time() - start_time))

