%reset_selective -f ^(?!failed_files$|calcerror_files$).*

## Setting up environment & importing files
import os
import pandas as pd

# Importing custom modules
os.chdir('../')
from spreadsheet import extract_ochra
from ochra import label_ochra, add_gst_ochra
from utils import info_label, info_error, visualise_gsts
os.chdir('2D3D')

# Moving to directory where anotations are stored
annotations_dir = [('C:/Users/aleja/OneDrive - University College London/'
                    'Griffin Institute collaboration/Grifin_annotations/2D3D '
                    'VIDEOS'),
                   ('C:/Users/Sera Bostan/University College London/'
                    'Mazomenos, Evangelos - Griffin Institute collaboration/'
                    'Grifin_annotations/2D3D VIDEOS')]
os.chdir(annotations_dir[0])

# Choosing file to work with later
case = 5

# Importing Excel file, particularly the 'Analysis' sheet within the file
analysis_xls = pd.read_excel(f'Case {case}.xls', sheet_name='Analysis').values

## Extracting and saving OCHRA information
ochra = extract_ochra(analysis_xls)

## Labelling each annotation as START, ERR (Error), N.P. (Not Performed), N.R.
## (Not recorded) or DESC (Description)
ochra = label_ochra(ochra, dataset='2d3d')
print(f'START -- Case {case}: ', end='')
info_label(ochra, 'START', total=False)

## Making statistical analysis of ERR (Error) events
error_category = 'Tool-tissue Errors'
print(f'\n{error_category} -- Case {case}: ', end='')
info_error(ochra, error_category)

## Adding global timeline information to OCHRA
ochra, end_hms = add_gst_ochra(ochra, ['START'], case, '2d3d')
visualise_gsts(ochra, ['START'], case, end_hms)
