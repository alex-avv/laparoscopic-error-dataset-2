import numpy as np
from datetime import datetime, date
from ochra import is_filled


def extract_ochra(analysis_xls):
    ''' Retrieves main OCHRA information from the spreadsheet.

    To find the size and position of the OCHRA data, the code loops through
    all 3rd-column rows until it finds a 'Totals' instance.

    Parameters
    ----------
    analysis_xls : 2D ndarray
        Numpy array representing the Excel OCHRA data, as imported from the
        pd.read_excel().values member variable.

    Raises
    ------
    ValueError
        Import unsuccessful: Could not find 'Totals' in 3rd column of
        analysis_xls.
    ValueError
        OCHRA data retrieved incorrectly: 'Totals' info was also extracted.

    Returns
    -------
    ochra : 2D ndarray
        Numpy array with the principal OCHRA annotations.

    Notes
    -----
    In the Excel sheets, only the first of a group of events belonging to the
    same 'Task Area' has the instance filled. The code fills out the empty
    'Task Area' instances after.

    '''

    ## Noting down the column numbers of each of event
    task, subtask, timecode, subfile, errors, conseq = 0, 1, 2, 3, 4, 5
    eem, instr, severity, loc, info = 6, 7, 8, 9, 10

    ## 'check_totals' flag will be used to confirm whether the import was
    ## successful or not. Resetting variable
    check_totals = False

    ## Looping through rows (from 3rd row to last row in the sheet)
    for totals_row in range(2, len(analysis_xls)):
        # If the instance in the 'Timecode' column says 'Totals', row number is
        # recorded and loop is exited
        if analysis_xls[totals_row, 2] == 'Totals':
            check_totals = True  # Checkpoint to confirm detection of 'Totals'
            break

    if check_totals is False:
        raise ValueError("Import unsuccessful: Could not find 'Totals' "
                         "in 3rd column of analysis_xls.")

    ## Looping through rows (from row with 'Totals' to 3rd row in the sheet)
    for ochra_last_row in reversed(range(2, totals_row)):
        # If all instances in the row (from 'Task Area' column to 'Further
        # info' column) are empty, row number is recorded and loop is exited
        if not is_filled(analysis_xls[ochra_last_row, task:info + 1]):
            break

    ## Storing the OCHRA data in a new variable using the positional
    ## information obtained earlier
    ochra_xls = analysis_xls[2:ochra_last_row, task:info + 1]

    # Sanity check to confirm the retrieved OCHRA data does not have a 'Totals'
    # instance
    if 'Totals' in ochra_xls:
        raise ValueError("OCHRA data retrieved incorrectly: 'Totals' info was "
                         "also extracted.")

    ## Copying the OCHRA data into a new variable for modification. 'ochra'
    ## will contain the adjusted OCHRA information
    ochra = np.copy(ochra_xls)

    ## Modifying the 'Task Area', 'Subtask Area', 'Timecode', 'Subfile' and
    ## 'Further Info' colums to an appropriate format
    for row in range(len(ochra)):
        # 'Task Area': If instance is not filled out, appointing value of
        # previous instance
        if not is_filled(ochra[row, task]):
            ochra[row, task] = ochra[row - 1, task]
        ochra[row, task] = int(ochra[row, task])

        # 'Subtask Area': Changing to str type
        if is_filled(ochra[row, 1]):
            ochra[row, subtask] = str(ochra[row, subtask])

        # 'Timecode': changing to datetime.timedelta format (for easier working
        # later)
        if is_filled(ochra[row, timecode]):
            ochra[row, timecode] = (datetime.combine(date.min,
                                                     ochra[row, timecode])
                                    - datetime.min)
        # 'Subfile': Changing to str type
        if is_filled(ochra[row, subfile]):
            ochra[row, subfile] = str(ochra[row, subfile])

        # 'Further info': Changing to str type
        if is_filled(ochra[row, info]):
            ochra[row, info] = str(ochra[row, info])

    return ochra
