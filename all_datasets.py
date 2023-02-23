### Setting up environment
import os
import pandas as pd

# Importing custom modules
from ochra import extract_ochra, label_ochra, add_gst_ochra
from testing import test_ochra
from utils import info_label, info_error

## Chosing dataset to work with (either 2D3D or ALACART)
dataset = '2D3D'
assert dataset in ['2D3D', 'ALACART']

# Moving to directory where anotations are stored
annotations_dir = [('C:/Users/aleja/OneDrive - University College London/'
                    'Griffin Institute collaboration/Grifin_annotations/'),
                   ('C:/Users/Sera Bostan/University College London/'
                    'Mazomenos, Evangelos - Griffin Institute collaboration/'
                    'Grifin_annotations/')]
for i in range(len(annotations_dir)):
    if dataset == '2D3D':
        annotations_dir[i] += f'{dataset} VIDEOS'
    elif dataset == 'ALACART':
        annotations_dir[i] += f'{dataset}'
os.chdir(annotations_dir[0])

### Importing files & testing if OCHRA information is in correct format
# 'files' has the names of all the Excel files with anotations for the chosen
# dataset
if dataset == '2D3D':
    files = os.listdir()[1:-1]
elif dataset == 'ALACART':
    files = os.listdir()[:-3]

missing_files = ''  # 'missing_files' is used to store the cases whos' Excel
# anotations can't be opened
failed_files = ''  # 'failed_files' is used to store the cases whos' OCHRA data
# extraction is unsuccessful
time_err_files = ''  # 'time_err_files' is used to store the cases where trying
# to do calculations on the OCHRA times gives errors

## Choosing type of statistical analysis for events
analysis = 'errors'
assert analysis in ['labels', 'errors']
if analysis == 'labels':
    # Allows to select whether to use the 'total' flag or not
    info_ochra = (lambda ochra, statistical_category:
                  info_label(ochra, statistical_category, total=False))
elif analysis == 'errors':
    info_ochra = info_error

_, statistical_category = 'START', 'Tool-tissue Errors'
print(f'{statistical_category} -- ', end='')

## Looping through all of the cases' Excel files in the Griffin dataset
for file_name in files:
    # Getting the case number
    if dataset == '2D3D':
        case = file_name.replace('Case ', '').replace('.xls', '')
    elif dataset == 'ALACART':
        case = file_name.replace('.xls', '')

    # Resetting checkpoints (used later)
    check_missing, check_failed, check_time_err = True, True, True

    try:
        # Importing Excel file, particularly the 'Analysis' spreadsheet
        analysis_xls = pd.read_excel(file_name, sheet_name='Analysis').values
        check_missing = False
    except:
        # If it is not possible to import the file, the case number is recorded
        missing_files = missing_files + f', {case}'

    if check_missing is False:
        try:
            # Extracting and testing the OCHRA data using our preset functions
            # defined earlier
            ochra = extract_ochra(analysis_xls)
            ochra = label_ochra(ochra, dataset)
            test_ochra(ochra, dataset)

            ## Making statistical analysis of events
            print(f'Case {case}: ', end='')  # Comment this line if
            # quantitying the results with statistical_analysis module
            info_ochra(ochra, statistical_category)
        except:
            # If it is not possible to (correctly) retrieve the OCHRA data, the
            # case number is recorded
            failed_files = failed_files + f', {case}'

    if check_failed is False:
        try:
            # Adding the Global Start Time (GST) to the events in OCHRA using
            # our preset function defined earlier
            ochra, end_hms = add_gst_ochra(ochra, ['START'], case, dataset)
            check_time_err = False
        except:
            # If it is not possible to successfully add the GSTs, the case
            # number is recorded
            time_err_files = time_err_files + f', {case}'

## Printing on screen the files that are missing and/or with failed OCHRA data
## extraction
missing_files, failed_files = missing_files[2:], failed_files[2:]
time_err_files = time_err_files[2:]
if True:
    print('\n', end='')
    if missing_files:
        print(f'\nCases {missing_files} are missing')
    if failed_files:
        print(f'\nCases {failed_files} have inappropriate OCHRA data')
