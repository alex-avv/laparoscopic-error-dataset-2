# %reset_selective -f ^(?!failed_files$|time_err_files$).*

## Setting up environment & importing files
import os
import pandas as pd

# Importing custom modules
from ochra import extract_ochra, label_ochra, add_gst_ochra
from utils import info_label, info_error, visualise_gsts
from testing import test_ochra

# Moving to directory where anotations are stored
annotations_dir = [('C:/Users/aleja/OneDrive - University College London/'
                    'Griffin Institute collaboration/Grifin_annotations/'
                    'ALACART'),
                   ('C:/Users/Sera Bostan/University College London/'
                    'Mazomenos, Evangelos - Griffin Institute collaboration/'
                    'Grifin_annotations/ALACART')]
os.chdir(annotations_dir[0])

# Choosing file to work with later
case = '009'

# Importing Excel file, particularly the 'Analysis' spreadsheet
analysis_xls = pd.read_excel(f'{case}.xls', sheet_name='Analysis').values

## Extracting and saving OCHRA information
ochra = extract_ochra(analysis_xls)

## Labelling each annotation as START, ERR (Error), N.P. (Not Performed), N.R.
## (Not recorded) or DESC (Description)
ochra = label_ochra(ochra, dataset='alacart')
print(f'START -- Case {case}: ', end='')
info_label(ochra, 'START', total=False)

## Making statistical analysis of ERR (Error) events
error_category = 'Tool-tissue Errors'
print(f'\n{error_category} -- Case {case}: ', end='')
info_error(ochra, error_category)

## Checking OCHRA data is as expected
test_ochra(ochra, 'alacart')

## Adding global timeline information to OCHRA
ochra, end_hms = add_gst_ochra(ochra, ['START'], case, 'alacart')
visualise_gsts(ochra, ['START'], case, end_hms)
