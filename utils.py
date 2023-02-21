from pandas import isna
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker
from matplotlib.ticker import FuncFormatter
import itertools
import datetime

def info_label(ochra, tag_name, total=False):
    # Notes: Checking how many phases are in the plot
    # Notes: Checking which phases are in the plot
    
    # Noting down the column numbers of the events
    task, subtask, label, timecode, subfile, errors = 0, 1, 2, 3, 4, 5
    conseq, eem, instr, severity, loc, info = 6, 7, 8, 9, 10, 11
    
    # Checking the annotations for the chosen label. If the event has the
    # specified tag, saving its 'Task-Subtask' combination
    text = []
    for row in range(len(ochra)):
        if ochra[row, label] == tag_name:            
            if not isna(ochra[row, subtask]):
                text += [str(ochra[row, task]) + ochra[row, subtask]]
            else:
                text += [str(ochra[row, task])]
    
    # Printing information on screen
    if not total:
        for word in text:
            print(f"'{word}', ", end='')
    else: 
        print(f'{len(text)}, ', end='')       
        

def info_error(ochra, err_name):
    # Notes: category on which to make the analysis
    
    # 'err_cats' contains the names of the Error categories in OCHRA 
    err_cats = ['Tool-tissue Errors', 'Consequence', 'EEM',
                'Instrument', 'Severity (a-e)', 'Location (pelvic)']

    if err_name not in err_cats:
        raise ValueError("Chosen error category must be either Tool-tissue "
                         "Errors, Consequence, EEM, Instrument, Severity "
                         "(a-e) or Location (pelvic)")

    for error_i in range(len(err_cats)):
        if err_cats[error_i] == err_name:
            break

    # Noting down the column numbers of the events
    task, subtask, label, timecode, subfile, errors = 0, 1, 2, 3, 4, 5
    conseq, eem, instr, severity, loc, info = 6, 7, 8, 9, 10, 11
    
    # Checking the annotations for the chosen Error category. If the event has
    # a 'ERR' label and a filled instance, printing the Error annotation.
    # Otherwise printing 'EMPTY'
    for row in range(len(ochra)):
        if ochra[row, label] == 'ERR' and not isna(ochra[row, errors +
                                                         error_i]):
            print(f"'{ochra[row, errors + error_i]}', ", end='')
        elif ochra[row, label] == 'ERR' and isna(ochra[row, errors +
                                                       error_i]):
            print("'EMPTY', ", end='')


def plot_timeline(text, bar_widths, end, case):
    ''' Visualises the GSTs of the chosen events in a timeline.

    Parameters
    ----------
    text : list of str
         'Task-Subtask' of the annotations, which will be inside the graph's
         boxes.
    bar_widths : TYPE
        Duration of the annotations (in s), which will plot the graph's boxes.
    end : TYPE
        End time of the recording (in s), for re.
    case : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''
    # 'name' contains the text that will be inside the boxes in the graph
    # 'results' contains the durations in seconds to plot the boxes in the graph
    # 'end' contains the end time of the last video in seconds

    # This function is to transform x-axis to time format (https://
    # stackoverflow.com/questions/48294332/plot-datetime-timedelta-using-
    # matplotlib-and-python)
    def format_func(x, pos):
        hours = int(x//3600)
        minutes = int((x%3600)//60)
        # seconds = int(x%60)  
        return "{:d}:{:02d}".format(hours, minutes)
        # return "{:d}:{:02d}:{:02d}".format(hours, minutes, seconds)
    formatter = FuncFormatter(format_func)

    # Defining colours for the plot
    bg_color = 'white'  # 'xkcd:dark gray'
    cover_color = 'black'

    # Plotting the times (code from: https://matplotlib.org/3.1.1/gallery/
    # lines_bars_and_markers/horizontal_barchart_distribution.html#sphx-glr-
    # gallery-lines-bars-and-markers-horizontal-barchart-distribution-py)
    labels = list(bar_widths.keys())
    data = np.array(list(bar_widths.values()))
    data_cum = data.cumsum(axis=1)
    category_colors = plt.get_cmap('tab20b')(np.linspace(0, 1, len(text)))

    # If the first event is an empty event, plotting an invisible bar
    if len(text) > 0:
        if text[0] == '':       
            category_colors = np.vstack((np.array((1, 1, 1, 0)),
                                         category_colors[0:-1]))

    # Figure size and resolution
    fig, ax = plt.subplots(figsize=(5, 1), dpi=1000)     
    for i, (colname, color) in enumerate(zip(text, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths

        thr = 0.0555  # This threshold is to determine if the graph label
        # will be inside the box or in the legend
        if (len(text[i]) == 2) and (widths/end > thr):
            ax.barh(labels, widths, left=starts, height=1, label='_nolegend_',
                    color=color)
        elif (len(text[i]) == 1) and (widths/(2 * end) > thr):
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
                ax.text(x, y, text[i], ha='center', va='center',
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

    # Adding title to plot (in ytick location)
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
    

def visualise_gsts(ochra, labels, case, end_time):
    ''' Displays graphically the GST of the chosen tagged OCHRA annotations.
        
    Parameters
    ----------
    ochra : 2D ndarray
        Numpy array representing the OCHRA information, as with the GSTs from
        using the ochra.add_gst_ochra function.
    labels: list of strs
        With the tags of the annotations for which to plot the GST.
    case: str
        Case file from where the OCHRA information was extracted.
    end_time: datetime.timedelta
        End time of the surgery recording (in HH:MM:SS format).
    more_info: length-2 tuple of bools
        Specifies whether to print the total number of phases 

    Returns
    -------
    None.
    
    Notes
    -----
    Before plotting the timeline, the duration of the events was calculated.
    This was done by subtracting the Global End Time (GET) minus the Global
    Start Time (GST) for each event.

    '''
    
    ## Noting down the column numbers of the events
    task, subtask, label, timecode, gst, subfile = 0, 1, 2, 3, 4, 5
    errors, conseq, eem, instr, severity, loc, info = 6, 7, 8, 9, 10, 11, 12 
    
    ## 'event_times' will hold the event GSTs and GETs in the following loop
    event_times = np.empty((0, 2), dtype=object)  
    
    ## In this case, only the events with the 'Task' instance filled and with
    ## one of the specified tags will be added to the plot
    for row in range(len(ochra)):
        if not isna(ochra[row, task]) and ochra[row, label] in labels:
            # Saving the event 'Task-Subtask' and GST in the first and second
            # columns of 'event_times', respectively
            if not isna(ochra[row, subtask]):
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
    if (len(event_times) == 0
        or event_times[0, 1] != datetime.timedelta(seconds=0)):   
        event_times = np.vstack([event_times,
                                 np.array(['',
                                           datetime.timedelta(seconds=0)])])

    ## Sorting the events in chronological order 
    event_times = event_times[event_times[:, 1].argsort()]
    
    # Adding two empty columns to hold the GETs and durations of the
    # chosen events
    event_times = np.hstack([event_times,
                             np.full((len(event_times), 2), np.nan)])

    # Populating the 'GET' and 'Duration' columns
    event_times[:, 2] = np.append(event_times[1:len(event_times), 1], end_time)
    event_times[:, 3] = event_times[:, 2] - event_times[:, 1]
    
    # Adding an empty column to hold the durations in seconds (i.e. not in
    # HH:MM:SS format)
    event_times = np.hstack([event_times,
                             np.full((len(event_times), 1), np.nan)])
    # Populating the 'Duration [seconds]' column
    for row in range(len(event_times)):
        event_times[row, 4] = event_times[row, 3].total_seconds()

    ## Defining variables for the plot
    text = event_times[:, 0]  # With the 'Task-Subtask' of the annotations
    bar_widths = {'Durations (in s)': event_times[:, 4]}
    end = end_time.total_seconds()  # End time of the surgery in seconds

    plot_timeline(text, bar_widths, end, case)
    
    ## Removing the first event in 'area' if it is an empty event
    if len(text) > 0:
        if text[0] == '':
            text = text[1:len(text)]
    