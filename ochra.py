import pandas as pd
import numpy as np
import os

import matplotlib.pyplot as plt
import matplotlib.ticker
from matplotlib.ticker import FuncFormatter
import itertools
import datetime

def is_filled(instance):
    ''' Checks whether an instance is partially filled or not.
    
    If a not NaN is found (i.e. instance is not completely empty), it returns
    True, else it gives False.

    Parameters
    ----------
    instance : ndarray or object

    Returns
    -------
    bool

    '''
    
    if isinstance(instance, np.ndarray):
        check = False in pd.isna(instance)
    else:
        check = not pd.isna(instance)
        
    return check


def check_words(words, instance):
    ''' Checks whether a string in a list can be found on another string.

    Parameters
    ----------
    words : list of strs
        Containing strings we want to test.
    instance : str

    Returns
    -------
    check : bool
        True if a word can be found on the instance, else False.

    '''
    check = False
    for word in words:
        if word in instance:
            check = True
            break
    return check    


def label_ochra(ochra, dataset):
    ''' Gives a descriptive label to each OCHRA annotation.

    The annotation is tagged either as START, ERR (Error), N.P. (Not
    Performed), N.R. (Not recorded) or DESC (Description).

    Parameters
    ----------
    ochra : 2D ndarray
        Numpy array representing the OCHRA information, as extracted using the
        spreadsheet.extract_ochra function.
    dataset : str
        Specifies whether the OCHRA information comes from from 2D3D or
        ALACART.

    Returns
    -------
    2D ndarray
        Numpy array representing updated labelled OCHRA data.

    '''

    dataset = dataset.lower()
    if dataset not in ['alacart', '2d3d']:
        raise ValueError("Selected dataset must be be either 2D3D or ALACART.")

    ## Adding an empty column to hold the labels
    ochra = np.insert(ochra, 2, np.full(len(ochra), np.nan), 1)

    ## Noting down the column numbers of each of event
    task, subtask, label, timecode, subfile, errors = 0, 1, 2, 3, 4, 5
    conseq, eem, instr, severity, loc, info = 6, 7, 8, 9, 10, 11


    ## Each event is given one of these 5 descriptive labels for easier
    ## identification later on
    if dataset == '2d3d':
        # 'start' is used to detect if an instance has the word 'Start' (or
        # similar) later on. Defining variable
        start = ['start', 'Start', 'START']

        # 'notperformed' is used to detect if an instance has the words 'Not 
        # performed' (or similar) later on. Defining variable
        notperformed = ['not performed', 'Not performed', 'not done',
                        'Not done', 'N.P.']

        # 'notrecorded' is used to detect if an instance has the words 'Not 
        # recorded' (or similar) later on. Defining variable
        notrecorded = ['Not recorded', 'not on video', 'DOCKING NOT RECORDED',
                       'Performed open']          

        # 'description' is used to detect if an instance has one of the
        # descriptive phrases included later on. Defining variable
        description = [# Descriptions with Timecode/Video subfile references
                       'End of recording',
                       'On table flexi being performed to confirm height and '
                       'make plan. Clip marked.',
                       '***Good for teaching. Right duplex ureter',
                       'Steps mixed together in this case.  Mostly file 3E',
                       'Task steps mixed in throughout this case',
                       '*****Note made of two suture oversew on conduit '
                       '?serosal tear. Must have occurred extra-corporeal'
                       '***********',
                       'Appears to be simultaneous right hemicoloectomy',
                       '?peritoneal mets anteriorly',
                       'PME performed (level of peritoneal reflection)',
      
                       # Descriptions w/o Timecode/Video subfile references
                       'Video ends',
                       'change of scope to allow 30 angulation. Scfreen '
                       'displayed 2D',
                       '*** CASE RECORDED IN 3D *** Makes assessment harder. '
                       'Chance of missing OCHRA errors',
                       'Meckels identified',
                       '4 cartridges used to divide bowel',
                       'lat to medial. Prior to pedicle',
                       'Step mixed in with others. Case moves around a lot',
                       'Adhoc splenic flexure mobilisation']       

    elif dataset == 'alacart':
        start = ['start ', 'Start ', 'START']
        notperformed = ['not performed', 'Not performed', 'N.P.']
        notrecorded = ['not recorded', 'Not recorded', 'not on video',
                       'Not on video', 'not shown', 'Not shown']
        description = ['Case appears to be converted at this point']


    ## There are some events where the 'Task Area' and 'Subtask Area' are noted
    ## but the rest of columns of the OCHRA information are empty. Assuming
    ## these cases were not performed and adding the N.P. label
    for row in range(len(ochra)):
        # Checking if instances in the row [from 'Label' column to 'Further
        # info' column] are empty or not
        check = ((is_filled(ochra[row, task]) or
                  is_filled(ochra[row, subtask]))
                 and not is_filled(ochra[row, label:info + 1]))

        # If all instances in the row are empty, a N.P. label is given
        if check:
            ochra[row, label] = 'N.P.'
            ochra[row, info] = 'ASSUMED NOT PERFORMED'  # Noting in 'Further
            # info' this event was assumed to not be performed (for clarity)


    ## There are some events where the 'Task Area', 'Subtask Area', 'Timecode'
    ## and 'Subfile' are noted but the rest of columns of the OCHRA information
    ## are empty. Assuming these are start events and adding the START label
    for row in range(len(ochra)):
        # Checking if instances in the row [from 'Tool-tissue Errors' column to
        # 'Further info' column] are empty or not
        check = ((is_filled(ochra[row, task]) or
                  is_filled(ochra[row, subtask]))
                 and is_filled(ochra[row, timecode])
                 and is_filled(ochra[row, subfile])
                 and not is_filled(ochra[row, errors:info + 1]))

        # If all instances in the row are empty, a START label is given
        if check:
            ochra[row, label] = 'START'
            ochra[row, info] = 'ASSUMED START'  # Noting in 'Further info' this
            # event was assumed to be a start event (for clarity)


    ## Marking the rest of events
    for row in range(len(ochra)):
        # Checking if instances in the row [from 'Tool-tissue Errors' column to
        # 'Location (pelvic)' column] are empty or not
        check_empty = not is_filled(ochra[row, errors:loc + 1])   

        # If all instances in the row are empty, and the 'Further info' column
        # has the 'Start' word in it, labelling as START
        if check_empty and check_words(start, ochra[row, info]):
            ochra[row, label] = 'START'

        # If all instances in the row are empty, and the 'Further info' column
        # has the 'Not performed' words in it, labelling as N.P.
        elif check_empty and check_words(notperformed, ochra[row, info]):
            ochra[row, label] = 'N.P.'

        # If all instances in the row are empty, and the 'Further info' column
        # has the 'Not recorded' words in it, labelling as N.R.
        elif check_empty and check_words(notrecorded, ochra[row, info]):
            ochra[row, label] = 'N.R.'

        # If all instances in the row are empty, and the 'Further info' column
        # has a descriptive phrase in it, labelling as DESC
        elif check_empty and check_words(description, ochra[row, info]):
            ochra[row, label] = 'DESC'

        # If the row is not fully empty, labelling as ERR
        elif not check_empty:
            ochra[row, label] = 'ERR'

    ## Marking as 'OTHER' the events that did not pass the before tests
    for row in range(len(ochra)):
        if not is_filled(ochra[row, label]):
            ochra[row, label] = 'OTHER'

    return ochra


def plot_timeline(name, results, end, case):
    # 'name' contains the text that will be inside the boxes in the graph
    # 'results' contains the durations in seconds to plot the boxes in the graph
    # 'end' contains the end time of the last video in seconds
    
    # This function plots the graph

    # This function is to transform x-axis to time format (https://
    # stackoverflow.com/questions/48294332/plot-datetime-timedelta-using-
    # matplotlib-and-python)
    def format_func(x, pos):
        hours = int(x//3600)
        minutes = int((x%3600)//60)
        seconds = int(x%60)  
        return "{:d}:{:02d}".format(hours, minutes)
        # return "{:d}:{:02d}:{:02d}".format(hours, minutes, seconds)
    formatter = FuncFormatter(format_func)

    # Defining colours for the plot
    bg_color = 'white'  #'xkcd:dark gray'
    cover_color = 'black'

    # Plotting the times (code from: https://matplotlib.org/3.1.1/gallery/
    # lines_bars_and_markers/horizontal_barchart_distribution.html#sphx-glr-
    # gallery-lines-bars-and-markers-horizontal-barchart-distribution-py)
    labels = list(results.keys())
    data = np.array(list(results.values()))
    data_cum = data.cumsum(axis=1)
    category_colors = plt.get_cmap('tab20b')(np.linspace(0, 1, len(name)))

    # If the first event is an empty event, plotting an invisible bar
    if len(name) > 0:
        if name[0] == '':       
            category_colors = np.vstack((np.array((1, 1, 1, 0)),
                                         category_colors[0:-1]))

    # Figure size and resolution
    fig, ax = plt.subplots(figsize=(5, 1), dpi=1000)     
    for i, (colname, color) in enumerate(zip(name, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths

        thr = 0.0555  # This threshold is to determine if the graph label
        # will be inside the box or in the legend
        if (len(name[i]) == 2) and (widths/end > thr):
            ax.barh(labels, widths, left=starts, height=1, label='_nolegend_',
                    color=color)
        elif (len(name[i]) == 1) and (widths/(2 * end) > thr):
            ax.barh(labels, widths, left=starts, height=1, label='_nolegend_',
                    color=color)
        else:
            ax.barh(labels, widths, left=starts, height=1, label=colname,
                    color=color)

        xcenters = starts + widths / 2

        if widths/end > thr:
            r, g, b, _ = color
            text_color = 'white' if r * g * b < 0.5 else 'black'
            for y, (x, c) in enumerate(zip(xcenters, widths)):
                ax.text(x, y, name[i], ha='center', va='center',
                        color=text_color, fontsize='medium')
        # Tightening the axes of the graph
        plt.autoscale(enable=True, axis='x', tight=True)

    # Ordering legend labels from left to right (https://stackoverflow.com/
    # questions/10101141/matplotlib-legend-add-items-across-columns-
    # instead-of-down)
    def flip(items, ncol):
        return itertools.chain(*[items[i::ncol] for i in range(ncol)])
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(flip(handles, 5), flip(labels, 5), ncol=5, loc='lower left',
              bbox_to_anchor=(0.035, 1), fontsize='small')

    # Modifying x-axis to appropriate time format
    ax.tick_params(axis='y', colors=bg_color)  
    plt.xticks(np.linspace(0, end, len(ax.get_xticks()) - 1))
    ax.xaxis.set_major_formatter(formatter)

    # Adding title to plot
    ticks_loc = ax.get_yticks()
    ax.yaxis.set_major_locator(matplotlib.ticker.FixedLocator(ticks_loc))
    ax.set_yticklabels([f'Surgery\nTimeline\nCase {case}'], color=cover_color)

    # Embellishing plot
    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)
    ax.spines['bottom'].set_color(cover_color)
    ax.spines['top'].set_color(bg_color)
    ax.spines['left'].set_color(cover_color)
    ax.spines['right'].set_color(cover_color)
    ax.tick_params(axis='x', colors=cover_color)
    plt.show()


def time_info(ochra, labels, case, dataset, visualise=False):
    """¨¨¨ Adds global timeline information to OCHRA 
    
    Imports video data
    ¨¨¨"""
    
    # This function finds the global start time of a chosen video using the video information loaded earlier
    def find_video_gst(video, simpleformname):
        for row in range(0,len(video)):
            if simpleformname == video[row, 0]:
                video_gst = video[row, 1]         # Storing the global start time in variable 'gst'
                break
        return video_gst
    
    dataset = dataset.lower()
    if dataset not in ['alacart', '2d3d']:
        raise ValueError("Selected dataset must be be either 2D3D or ALACART.")
        
    ## Opening folder with the video data stored as .npy files
    os.chdir('Video durations')

    ## Noting down the column numbers of each video event
    if dataset == '2d3d':
        original, short, duration, glob_st = 0, 1, 2, 3
    elif dataset == 'alacart':
        path, original, short, duration, glob_st = 0, 1, 2, 3, 4

    ## Loading video data for the case and only keeping essential information        
    video = np.load(f'{case}.npy', allow_pickle=True)
    # Discarding 'Path', 'Original name' and 'Duration' columns, keeping 'Short
    # form name' and 'Global start time' columns
    video_info = np.stack([video[:, short], video[:, glob_st]], axis=1)

    ## Returning to original working folder (i.e. one level up)
    os.chdir('../')

    ## Adding an empty column to hold the global start times of the annotations
    ochra = np.insert(ochra, 4, np.full(len(ochra), np.nan), 1)
    
    ## Noting down the column numbers of each event
    task, subtask, label, timecode, gst, subfile = 0, 1, 2, 3, 4, 5
    errors, conseq, eem, instr, severity, loc, info = 6, 7, 8, 9, 10, 11, 12    

    ## Appending Global Start Time (GST) to specified tagged events
    # This is done by adding the GST of the video in the 'Subfile column' plus
    # the time in the 'Timecode' column
    for tag in labels:
        for row in range(len(ochra)):
            if ochra[row, label] == tag:
                ochra[row, gst] = (ochra[row, timecode] + 
                                   find_video_gst(video_info,
                                                  ochra[row, subfile]))

    ## Displaying the new GST info graphically
    # Before plotting the graph, the duration of the events has be calculated.
    # This will be done by subtracting the Global End Time (GET) minus the GST
    # for each event
    if visualise:
        # Calculating the end time of the last video for later on
        end = video[-1, glob_st] + video[-1, duration]
        
        event_times = np.empty((0, 2), dtype=object)  # 'event_times' will
        # hold the GSTs and GETs of certain events later on 
        
        ## In this case, only the events with the 'Task' instance filled and
        ## with one of the specified tags will be added to the plot
        for row in range(len(ochra)):
            if is_filled(ochra[row, task]) and ochra[row, label] in labels:
                # Saving the event 'Task/Subtask Area' and GST in the first and
                # second columns of 'event_times', respectively
                if is_filled(ochra[row, subtask]):
                    event_times = np.vstack([event_times,
                                             np.array([str(ochra[row, task]) +
                                                       ochra[row, subtask],
                                                       ochra[row, gst]])])
                else:
                    event_times = np.vstack([event_times,
                                             np.array([str(ochra[row, task]),
                                                       ochra[row, gst]])])
        
        ## If there is no event to map or if the first event's GST is not zero,
        ## adding an empty event so the timeline plots correctly later on
        if len(event_times) == 0 or (event_times[0, 1] !=
                                     datetime.timedelta(seconds=0)):   
            event_times = np.vstack([event_times,
                                     np.array(['', datetime.timedelta(seconds=
                                                                      0)])])

        ## Sorting the events in chronological order 
        event_times = event_times[event_times[:, 1].argsort()]
        
        # Adding two empty columns to hold the GETs and durations of the
        # chosen events
        event_times = np.hstack([event_times,
                                 np.full((len(event_times), 2), np.nan)])
        # Populating the 'GET' and 'Duration' columns
        event_times[:, 2] = np.append(event_times[1:len(event_times), 1], end)
        event_times[:, 3] = event_times[:, 2] - event_times[:, 1]
        
        # Adding an empty column to hold the durations in seconds (i.e. not in
        # HH:MM:SS format)
        event_times = np.hstack([event_times,
                                 np.full((len(event_times), 1), np.nan)])
        # Populating the 'Duration [seconds]' column
        for row in range(len(event_times)):
            event_times[row, 4] = event_times[row, 3].total_seconds()

        ## Defining variables for the plot
        area = event_times[:, 0]  # 'area' contains the 'Task/Subtask Area'
        # text
        durations = {'Durations (in s)': event_times[:, 4]}  # 'durations'
        # has the times to plot the boxes of the graph
        end = end.total_seconds()  # 'end' is the end time of the last
        # video in seconds

        plot_timeline(area, durations, end, case)
        
        ## Removing the first event in 'area' if it is an empty event
        if len(area) > 0:
            if area[0] == '':
                area = area[1:len(area)]
        
        # Checking how many phases are in the plot
        number_events = len(area)
        print(f'Case {case}: ', end='')
        print(f'{number_events}, ', end='')
        
        # Checking which phases are in the plot
        print(f'Case {case}: ', end='')
        for n in range(len(area)):
            print(f"'{area[n]}', ", end='')
        
    return ochra, area
