%reset -f
"""¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨"""
## Setting up environment & importing files
import sys
import os
from datetime import datetime, date
import time
import pandas as pd
import numpy as np

# Importing custom modules
os.chdir('../')
from spreadsheet import extract_ochra
from ochra import label_ochra
os.chdir('ALACART')

# Moving to directory where anotations are stored
annotations_dir = [('C:/Users/aleja/OneDrive - University College London/'
                    'Griffin Institute collaboration/Grifin_annotations/2D3D '
                    'VIDEOS'),
                   ('C:/Users/Sera Bostan/University College London/'
                    'Mazomenos, Evangelos - Griffin Institute collaboration/'
                    'Grifin_annotations/2D3D VIDEOS')]
os.chdir(annotations_dir[0])
"""¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨"""


"""¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨"""
"""¨¨¨ Adding global timeline information to OCHRA and importing video data ¨¨¨"""
def videoinfo_ochra(ochra, index):
    # Opening folder with the video data stored as .npy files
    os.chdir('Video durations')

    try:
        # Loading video data for the case and removing non-essential information
        video = np.load(f'{index}.npy', allow_pickle=True)      # 'video' will contain the video information. Setting variable 
        # Calculating the end time of the last video for later on
        end = video[len(video) -1, 3] + video[len(video) -1, 4]
        # Removing 'Path', 'Original name' and 'Duration' columns, keeping 'Simple form name' and 'Global start time' columns
        video = np.stack((video[:, 2], video[:, 4]), axis=1)
    except:
        pass
     
    # Returning to original working folder (i.e. one level up)
    os.chdir('../')

    # This function finds the global start time of a chosen video using the video information loaded earlier
    def find_globalStartTime(video, simpleformname):
        for row in range(0,len(video)):
            if simpleformname == video[row, 0]:
                gst = video[row, 1]         # Storing the global start time in variable 'gst'
                break
        return gst

    # Adding an empty column to hold the global start times of the annotated events
    ochra = np.insert(ochra, 4, np.full(len(ochra), np.nan), 1)

    """ Adding GSTs to 'START' events """
    # For each event this is done by adding the GST of the video in the 'Subfile column' plus the time in the 'Timecode' column
    for row in range(0, len(ochra)):         # Looping through all rows in 'ochra'  
        # If event is annotated as 'START', add GST
        if ochra[row, 2] == 'START':
            ochra[row, 4] = ochra[row, 3] + find_globalStartTime(video, ochra[row, 5])


    """Displaying the new GST info graphically """
    # Before plotting the graph, the duration of the events has be calculated. This will be done by subtracting the global end time (GET) minus the global start time (GST) for each event
    event_timeinfo = np.empty((0,2), dtype=object)      # 'event_timeinfo' will hold the GSTs and GETs of certain events later on. Defining variable 

    # In this case, only the events which have the 'Task' instance filled and a 'START' label will be added to the plot
    for row in range(0, len(ochra)):         # Looping through all rows in 'ochra'
        if (pd.isna(ochra[row, 0]) == False) and (ochra[row, 2] == 'START'):
            # Saving the event 'Task' number and GST in the first and second columns of 'event_timeinfo', respectively
            if pd.isna(ochra[row, 1]) == True:
                event_timeinfo = np.vstack((event_timeinfo, np.array((str(ochra[row, 0]), ochra[row, 4]))))
            else:
                event_timeinfo = np.vstack((event_timeinfo, np.array((str(ochra[row, 0]) + ochra[row, 1], ochra[row, 4]))))

    # If there is no event to map or if the first event's GST is not zero, adding an empty event so the timeline plots correctly later on
    import datetime      # 'datetime' library is needed later on
    if len(event_timeinfo) == 0:
        event_timeinfo = np.vstack((event_timeinfo, np.full((1,2), np.nan)))    # Adding an empty row to hold the empty event    
        event_timeinfo[len(event_timeinfo) -1,:] = np.stack(('',datetime.timedelta(seconds=0)))      # Populating the empty event
    elif event_timeinfo[0, 1] != datetime.timedelta(seconds=0):
        event_timeinfo = np.vstack((event_timeinfo, np.full((1,2), np.nan)))    # Adding an empty row to hold the empty event    
        event_timeinfo[len(event_timeinfo) -1,:] = np.stack(('',datetime.timedelta(seconds=0)))      # Populating the empty event
        
    # Sorting the events in chronological order 
    event_timeinfo = event_timeinfo[event_timeinfo[:,1].argsort()]

    # Adding two empty columns to hold the GETs and durations of the chosen events
    event_timeinfo = np.hstack((event_timeinfo, np.full((len(event_timeinfo),2), np.nan)))

    # Populating the 'GET' and 'Duration' columns
    event_timeinfo[:,2] = np.append(event_timeinfo[1:len(event_timeinfo),1], end)
    event_timeinfo[:,3] = event_timeinfo[:,2] - event_timeinfo[:,1]

    # Adding an empty column to hold the durations in seconds (i.e. not in HH:MM:SS format)
    event_timeinfo = np.hstack((event_timeinfo, np.full((len(event_timeinfo),1), np.nan)))

    # Populating the 'Duration [seconds]' column
    for row in range(0, len(event_timeinfo)):
        event_timeinfo[row, 4] = event_timeinfo[row, 3].total_seconds()

    # Defining variables for the plot
    name = event_timeinfo[:,0]      # 'name' contains the text that will be inside the boxes in the graph 
    results = {
        'Dictionary': event_timeinfo[:,4],      # 'results' contains the durations in seconds to plot the boxes in the graph
    }
    end = end.total_seconds()       # 'end' contains the end time of the last video in seconds

    # This function plots the graph
    def plot_timeLine(name, results, end, index):
        # Importing Python libraries for the plot
        import matplotlib.pyplot as plt
        from matplotlib.ticker import FuncFormatter
        
        # This function is to transform x-axis to time format (https://stackoverflow.com/questions/48294332/plot-datetime-timedelta-using-matplotlib-and-python)
        def format_func(x, pos):
            hours = int(x//3600)
            minutes = int((x%3600)//60)
            seconds = int(x%60)  
            return "{:d}:{:02d}".format(hours, minutes)
            # return "{:d}:{:02d}:{:02d}".format(hours, minutes, seconds)
        formatter = FuncFormatter(format_func)
        
        # Defining colours for the plot
        bg_color = 'white'     #'xkcd:dark gray'
        cover_color = 'black'
        
        # Plotting the times (code from: https://matplotlib.org/3.1.1/gallery/lines_bars_and_markers/horizontal_barchart_distribution.html#sphx-glr-gallery-lines-bars-and-markers-horizontal-barchart-distribution-py)
        labels = list(results.keys())
        data = np.array(list(results.values()))
        data_cum = data.cumsum(axis=1)
        category_colors = plt.get_cmap('tab20b')(np.linspace(0, 1, len(name)))
        if len(name) > 0:       # If the first event is an empty event, plotting an invisible bar
            if name[0] == '':       
                category_colors = np.vstack((np.array((1,1,1,0)), category_colors[0:len(category_colors) -1]))
        #
        fig, ax = plt.subplots(figsize=(5, 1), dpi=1000)     # Defining figure size and resolution
        #
        for i, (colname, color) in enumerate(zip(name, category_colors)):
            widths = data[:, i]
            starts = data_cum[:, i] - widths
            #
            thr = 0.0555      # This threshold is to determine if the graph label will be inside the box or in the legend
            if (len(name[i]) == 2) and (widths/end > thr):
                ax.barh(labels, widths, left=starts, height=1, label='_nolegend_', color=color)
            elif (len(name[i]) == 1) and (widths/(2*end) > thr):
                ax.barh(labels, widths, left=starts, height=1, label='_nolegend_', color=color)
            else:
                ax.barh(labels, widths, left=starts, height=1, label=colname, color=color)
            #
            xcenters = starts + widths / 2
            xcenters2 = starts + widths
            #
            if widths/end > thr:
                r, g, b, _ = color
                text_color = 'white' if r * g * b < 0.5 else 'black'
                for y, (x, c) in enumerate(zip(xcenters, widths)):
                    ax.text(x, y, name[i], ha='center', va='center', color=text_color, fontsize='medium')
            plt.autoscale(enable=True, axis='x', tight=True)      # Tightening the axes of the graph
                
        # Ordering legend labels from left to right (https://stackoverflow.com/questions/10101141/matplotlib-legend-add-items-across-columns-instead-of-down)
        import itertools
        def flip(items, ncol):
            return itertools.chain(*[items[i::ncol] for i in range(ncol)])
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(flip(handles, 5), flip(labels, 5), ncol=5, loc='lower left',
                  bbox_to_anchor=(0.035, 1), fontsize='small')
            
        # Modifying x-axis to appropriate time format
        ax.tick_params(axis='y', colors=bg_color)  
        plt.xticks(np.linspace(0, end, len(ax.get_xticks()) - 1))
        ax.xaxis.set_major_formatter(formatter)
        
        # Ignoring warning
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            ax.set_yticklabels([f'Surgery\nTimeline\nCase {index}'], color=cover_color)
        
        # Embellishing plot
        fig.patch.set_facecolor(bg_color)
        ax.set_facecolor(bg_color)
        ax.spines['bottom'].set_color(cover_color)
        ax.spines['top'].set_color(bg_color)
        ax.spines['left'].set_color(cover_color)
        ax.spines['right'].set_color(cover_color)
        ax.tick_params(axis='x', colors=cover_color)
        plt.show()

    # Producing the plot using the function defined earlier
    # plot_timeLine(name, results, end, index)

    # Removing the first event in 'name' if it is an empty event
    if len(name) > 0:
        if name[0] == '':
            name = name[1:len(name)]
        
    # Checking how many phases are in the plot
    # number_events = len(name)
    # print(f'Case {index}: ', end='')
    # print(f'{number_events}, ', end='')

    # Checking which phases are in the plot
    # print(f'Case {index}: ', end='')
    # for n in range(0, len(name)):
    #     print(f"'{name[n]}', ", end='')
    
    return ochra        # Giving 'ochra' to the function's output
"""¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨"""


"""¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨"""
"""¨¨¨ Testing OCHRA information is in the correct format ¨¨¨"""
def test_ochra(ochra):
    check_failed = False       # 'check_failed' is used later on. Resetting variable
    
    # 'file' and 'subfile' are used to test the 'Subfile' column later on. Setting variables
    file = ['x']
    subfile = ['y']


    """ Checking 'Task Area' column) """
    col_taskarea = 0
    # Confirming all instances in the column are between 6-10
    for row in range(0,len(ochra)):
        if pd.isna(ochra[row, col_taskarea]) == False:
            if (ochra[row, col_taskarea] in [6,7,8,9,10]) == False:       # If an instance is not in the available options, test fails
                check_failed = True
                break
        elif pd.isna(ochra[row, col_taskarea]) == True:
            check_failed = True
            break
        
    # Checking the column has at least one of the instances in 6-10
    if check_failed == False:
        if (6 in ochra[:, col_taskarea]) == False:      # If the column doesn't have a 6 in it, test fails. Likewise for 7-10
            check_failed = True
        elif (7 in ochra[:, col_taskarea]) == False:
            check_failed = True
        elif (8 in ochra[:, col_taskarea]) == False:
            check_failed = True
        elif (9 in ochra[:, col_taskarea]) == False:
            check_failed = True
        elif (10 in ochra[:, col_taskarea]) == False:
            check_failed = True
            
    """ Checking 'Subtask Area' column """
    col_subtaskarea = 1
    # Confirming all instances in the column are between a-c
    for row in range(0,len(ochra)):
        if pd.isna(ochra[row, col_subtaskarea]) == False:
            if (ochra[row, col_subtaskarea] in ['a','b','c']) == False:       # If an instance is not in the available options, test fails
                check_failed = True
                break
    
    """ Checking 'Label' column """
    col_label = 2
    # Confirming all instances in the column are either 'START', 'ERR', 'N.P.', 'N.R.' or 'DESC'
    for row in range(0,len(ochra)):
        if pd.isna(ochra[row, col_label]) == False:
            if (ochra[row, col_label] in ['START','ERR','N.P.','N.R.','DESC']) == False:       # If an instance is not in the available options, test fails
                check_failed = True
                break
        elif pd.isna(ochra[row, col_label]) == True:
            check_failed = True
            break
            
    """ Checking 'Subfile' column """
    col_subfile = 4
    # Not necessary for ALACART as videos are named in different ways/formats
            
    # """ Checking 'Further info' column """
    # col_furtherinfo = 11
    # # Checking instances in the column are equal to the chosen word(s)
    # for row in range(0,len(ochra)):
    #     if pd.isna(ochra[row, col_furtherinfo]) == False:
    #         if ochra[row, col_furtherinfo] == 'ASSUMED START':       # If an instance is not in the available options, test fails
    #             check_failed = True
    #             break
            
    return check_failed      # Returning the value of 'check_failed' to the function's output
"""¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨"""


"""¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨"""
"""¨¨¨ Importing files & testing if OCHRA information is in correct format ¨¨¨"""
# 1st part of measuring time of execution of the code
start_time = time.time()

iALACART = np.array(os.listdir(), dtype=object)      # 'iALACART' has the names of all the Excel files files with anotations in the 'ALACART' folder

missing_files = ''      # 'missing_files' is used to store the cases whos' Excel anotations can't be opened later on. Resetting variable
failed_files = ''       # 'failed_files' is used to store the cases whos' OCHRA data extraction is unsuccessful later on. Resetting variable
calcerror_files = ''    # 'calcerror_files' is used to store the cases where trying to do calculations on the OCHRA data gives errors later on. Resetting variable

# Looping through all of the cases' spreadsheets in the Griffin dataset 
for n in range(0,len(iALACART)-3):
    analysis_xls = None
    file_name = iALACART[n]        # 'file_name' is used for the name of the file to be imported later on. Setting variable
    index = file_name.replace(".xls","")
    
    try:        # Importing Excel file, particularly the 'Analysis' sheet within the file
        analysis_xls = pd.read_excel(file_name, sheet_name='Analysis').values
        check_missing = False
    except:     # If it is not possible to import the file, the case number is recorded 
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
                    check_failed = True
        except:     # If it is not possible to retrieve the OCHRA data from the file, the case number is recorded 
            failed_files = failed_files + f', {index}'
            check_failed = True
    
    if (check_missing == False) and (check_failed == False):
        try:      # Adding the global start times to the events in OCHRA using our preset function defined earlier
            ochra = videoinfo_ochra(ochra, index)
            check_calcerror = False
        except:      # If it is not possible to successfully add the global start times, the case number is recorded
            calcerror_files = calcerror_files + f', {index}'
            check_calcerror = True

# Printing on screen the files that are missing and with failed OCHRA data extraction
# print(f'\nCases {missing_files[2:]} are missing')
# print(f'Cases {failed_files[2:]} have inappropriate/failed OCHRA data ')

# 2nd part of measuring time of execution of the code
# print('Executed in %.2f seconds.' % (time.time() - start_time))
