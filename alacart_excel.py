# %reset_selective -f ^(?!failed_files$|calcerror_files$).*
"""¨¨¨ Setting up environment & importing files ¨¨¨"""
# Importing python libraries
import sys
import os
from datetime import datetime, date
import time
import pandas as pd
import numpy as np

# 1st part of measuring time of execution of the code
# start_time = time.time()

# Moving to directory where anotations are stored
os.chdir("C:/Users/Sera Bostan/University College London/Mazomenos, Evangelos - Griffin Institute collaboration/Grifin_annotations/ALACART")
#os.chdir("C:/Users/aleja/OneDrive - University College London/Griffin Institute collaboration/Grifin_annotations/ALACART")

# Choosing file to work with later
index = "009"

# Importing Excel file, particularly the 'Analysis' sheet within the file
analysis_xls = pd.read_excel(f'{index}.xls', sheet_name='Analysis').values



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

''' return ochra, check_failed       # Giving 'ochra' and 'check_failed' to the function's output '''



"""¨¨¨ Labelling each annotation as START, ERR (Error), N.P. (Not Performed), N.R. (Not recorded) or DESC (Description) ¨¨¨"""
''' def label_ochra(ochra): '''
# Each event is given one of these 5 descriptive labels for easier identification later on 
start = ['start ','Start ','START',
         'posterior TME seems well underway at start',
         'Video starts with proximal TME posterior plane already underway',
         'Starts. TME already well underway partially left side',
         '6a starts in part 2'
         ]      # 'start' is used to detect if an instance has the word 'Start' (or similar) later on. Defining variable
notperformed = ['not performed','Not performed','N.P.']       # 'notperformed' is used to detect if an instance has the words 'Not performed' (or similar) later on. Defining variable
notrecorded = ['not recorded','Not recorded',
               'not on video','Not on video',
               'not shown','Not shown']      # 'notrecorded' is used to detect if an instance has the words 'Not recorded' (or similar) later on. Defining variable
description = ['Case appears to be converted at this point'
               ]       # 'description' is used to detect if an instance has one of the descriptive phrases included later on. Defining variable

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

# Marking the rest of events
for row in range(0,len(ochra)):     # Looping through all rows in 'ochra'
    check_filled = False in pd.isna(ochra[row, 5:11])    # Checking if instances in the row [from 'Tool-tissue Errors' column to 'Location (pelvic)' column] are empty or not
    # If all instances in the row are empty, and the 'Further info' column has the 'Start' word in it, labelling as START
    if (check_filled == False) and (check_words(start, ochra[row, 11]) == True):
        ochra[row, 2] = 'START'
    # If all instances in the row are empty, and the 'Further info' column has the 'Not performed' words in it, labelling as N.P.
    elif (check_filled == False) and (check_words(notperformed, ochra[row, 11]) == True):
        ochra[row, 2] = 'N.P.'
    # If all instances in the row are empty, and the 'Further info' column has the 'Not recorded' words in it, labelling as N.R.
    elif (check_filled == False) and (check_words(notrecorded, ochra[row, 11]) == True):
        ochra[row, 2] = 'N.R.'
    # If all instances in the row are empty, and the 'Further info' column has a descriptive phrase in it, labelling as DESC
    elif (check_filled == False) and (check_words(description, ochra[row, 11]) == True):
        ochra[row, 2] = 'DESC'
    # If the row is not fully empty, labelling as ERR
    elif check_filled == True:
        ochra[row, 2] = 'ERR'

# Marking as 'OTHER' the events that did not pass the before tests
for row in range(0,len(ochra)):
    if pd.isna(ochra[row, 2]) == True:
        ochra[row, 2] = 'OTHER'
        
''' return ochra        # Giving 'ochra' to the function's output '''



"""¨¨¨ Adding global timeline information to OCHRA and importing video data ¨¨¨"""
''' def videoinfo_ochra(ochra, index): '''
# # Opening folder with the video data stored as .npy files
# os.chdir('Video durations')

# try:
#      # Loading video data for the case and removing non-essential information
#      video = np.load(f'{index}.npy', allow_pickle=True)      # 'video' will contain the video information. Setting variable 
#      # Calculating the end time of the last video for later on
#      end = video[len(video) - 1, 2] + video[len(video) - 1, 3]
#      # Removing 'Original name' and 'Duration' columns, keeping 'Simple form name' and 'Global start time' columns
#      video = np.stack((video[:, 1], video[:, 3]), axis=1)
# except:
#      pass
 
# # Returning to original working folder (i.e. one level up)
# os.chdir('../')

# # This function finds the global start time of a chosen video using the video information loaded earlier
# def find_globalStartTime(video, simpleformname):
#     for row in range(0,len(video)):
#         if simpleformname == video[row, 0]:
#             gst = video[row, 1]         # Storing the global start time in variable 'gst'
#             break
#     return gst

# # Adding an empty column to hold the global start times of the annotated events
# ochra = np.insert(ochra, 4, np.full(len(ochra), np.nan), 1)

# """ Adding GSTs to 'START' events """
# # For each event this is done by adding the GST of the video in the 'Subfile column' plus the time in the 'Timecode' column
# for row in range(0, len(ochra)):         # Looping through all rows in 'ochra'  
#     # If event is annotated as 'START', add GST
#     if ochra[row, 2] == 'START':
#         ochra[row, 4] = ochra[row, 3] + find_globalStartTime(video, ochra[row, 5])


# """Displaying the new GST info graphically """
# # Before plotting the graph, the duration of the events has be calculated. This will be done by subtracting the global end time (GET) minus the global start time (GST) for each event
# event_timeinfo = np.empty((0,2))      # 'event_timeinfo' will hold the GSTs and GETs of certain events later on. Defining variable 

# # In this case, only the events which have the 'Task' instance filled and a 'START' label will be added to the plot
# for row in range(0, len(ochra)):         # Looping through all rows in 'ochra'
#     if (pd.isna(ochra[row, 0]) == False) and (ochra[row, 2] == 'START'):
#         # Saving the event 'Task' number and GST in the first and second columns of 'event_timeinfo', respectively
#         if pd.isna(ochra[row, 1]) == True:
#             event_timeinfo = np.vstack((event_timeinfo, np.array((str(ochra[row, 0]), ochra[row, 4]))))
#         else:
#             event_timeinfo = np.vstack((event_timeinfo, np.array((str(ochra[row, 0]) + ochra[row, 1], ochra[row, 4]))))
           
# # Sorting the events in chronological order 
# event_timeinfo = event_timeinfo[event_timeinfo[:,1].argsort()]

# # Adding two empty columns to hold the GETs and durations of the chosen events
# event_timeinfo = np.hstack((event_timeinfo, np.full((len(event_timeinfo),2), np.nan)))

# # Populating the 'GET' and 'Duration' columns
# event_timeinfo[:,2] = np.append(event_timeinfo[1:len(event_timeinfo),1], end)
# event_timeinfo[:,3] = event_timeinfo[:,2] - event_timeinfo[:,1]

# # Adding an empty column to hold the durations in seconds (i.e. not in HH:MM:SS format)
# event_timeinfo = np.hstack((event_timeinfo, np.full((len(event_timeinfo),1), np.nan)))

# # Populating the 'Duration [seconds]' column
# for row in range(0, len(event_timeinfo)):
#     event_timeinfo[row, 4] = event_timeinfo[row, 3].total_seconds()

# # Defining variables for the plot
# name = event_timeinfo[:,0]      # 'name' contains the text that will be inside the boxes in the graph 
# results = {
#     'Dictionary': event_timeinfo[:,4],      # 'results' contains the durations in seconds to plot the boxes in the graph
# }
# end = end.total_seconds()       # 'end' contains the end time of the last video in seconds

# # This function plots the graph
# def plot_timeLine(name, results, end, index):
#     # Importing Python libraries for the plot
#     import matplotlib.pyplot as plt
#     from matplotlib.ticker import FuncFormatter
    
#     # This function is to transform x-axis to time format (https://stackoverflow.com/questions/48294332/plot-datetime-timedelta-using-matplotlib-and-python)
#     def format_func(x, pos):
#         hours = int(x//3600)
#         minutes = int((x%3600)//60)
#         seconds = int(x%60)  
#         return "{:d}:{:02d}".format(hours, minutes)
#         # return "{:d}:{:02d}:{:02d}".format(hours, minutes, seconds)
#     formatter = FuncFormatter(format_func)
    
#     # Defining colours for the plot
#     bg_color = 'white'     #'xkcd:dark gray'
#     cover_color = 'black'
    
#     # Plotting the times (code from: https://matplotlib.org/3.1.1/gallery/lines_bars_and_markers/horizontal_barchart_distribution.html#sphx-glr-gallery-lines-bars-and-markers-horizontal-barchart-distribution-py)
#     labels = list(results.keys())
#     data = np.array(list(results.values()))
#     data_cum = data.cumsum(axis=1)
#     category_colors = plt.get_cmap('tab20b')(np.linspace(0, 1, len(name)))
#     #
#     fig, ax = plt.subplots(figsize=(5, 1), dpi=1000)     # Defining figure size and resolution
#     #
#     for i, (colname, color) in enumerate(zip(name, category_colors)):
#         widths = data[:, i]
#         starts = data_cum[:, i] - widths
#         #
#         thr = 0.0555      # This threshold is to determine if the graph label will be inside the box or in the legend
#         if (len(name[i]) == 2) and (widths/end > thr):
#             ax.barh(labels, widths, left=starts, height=1, label='_nolegend_', color=color)
#         elif (len(name[i]) == 1) and (widths/(2*end) > thr):
#             ax.barh(labels, widths, left=starts, height=1, label='_nolegend_', color=color)
#         else:
#             ax.barh(labels, widths, left=starts, height=1, label=colname, color=color)
#         #
#         xcenters = starts + widths / 2
#         xcenters2 = starts + widths
#         #
#         if widths/end > thr:
#             r, g, b, _ = color
#             text_color = 'white' if r * g * b < 0.5 else 'black'
#             for y, (x, c) in enumerate(zip(xcenters, widths)):
#                 ax.text(x, y, name[i], ha='center', va='center', color=text_color, fontsize='medium')
#         plt.autoscale(enable=True, axis='x', tight=True)      # Tightening the axes of the graph
            
#     # Ordering legend labels from left to right (https://stackoverflow.com/questions/10101141/matplotlib-legend-add-items-across-columns-instead-of-down)
#     import itertools
#     def flip(items, ncol):
#         return itertools.chain(*[items[i::ncol] for i in range(ncol)])
#     handles, labels = ax.get_legend_handles_labels()
#     ax.legend(flip(handles, 5), flip(labels, 5), ncol=5, loc='lower left',
#               bbox_to_anchor=(0.035, 1), fontsize='small')
        
#     # Modifying x-axis to appropriate time format
#     ax.tick_params(axis='y', colors=bg_color)  
#     plt.xticks(np.linspace(0, end, len(ax.get_xticks()) - 1))
#     ax.xaxis.set_major_formatter(formatter)
    
#     # Ignoring warning
#     import warnings
#     with warnings.catch_warnings():
#         warnings.simplefilter("ignore")
#         ax.set_yticklabels([f'Surgery\nTimeline\nCase {index}'], color=cover_color)
    
#     # Embellishing plot
#     fig.patch.set_facecolor(bg_color)
#     ax.set_facecolor(bg_color)
#     ax.spines['bottom'].set_color(cover_color)
#     ax.spines['top'].set_color(bg_color)
#     ax.spines['left'].set_color(cover_color)
#     ax.spines['right'].set_color(cover_color)
#     ax.tick_params(axis='x', colors=cover_color)
#     plt.show()

# # Producing the plot using the function defined earlier
# plot_timeLine(name, results, end, index)

# # Checking how many phases are in the plot
# number_events = len(name)
# print(f'Case {index}: ', end='')
# print(f'{number_events}, ', end='')

# # Checking which phases are in the plot
# print(f'Case {index}: ', end='')
# for n in range(0, len(name)):
#     print(f"'{name[n]}', ", end='')

''' return ochra        # Giving 'ochra' to the function's output '''

# 2nd part of measuring time of execution of the code
# print('Executed in %.2f seconds.' % (time.time() - start_time))
