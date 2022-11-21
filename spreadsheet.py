"""¨¨¨ Setting up environment ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨"""
# Importing python libraries
import sys
import pandas as pd
import numpy as np
from datetime import datetime, date
"""¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨"""


"""¨¨¨ Extracting and saving OCHRA information ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨"""
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

    """ Filling first column ('Task Area') approppriately """
    # Only the first of a group of annotations belonging to the same 'Task Area' has the instance filled (shown in Excel sheet). Filling out the empty instances after
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
