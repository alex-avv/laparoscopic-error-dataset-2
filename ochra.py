import pandas as pd
import numpy as np
import os


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
        Specifies whether the OCHRA information comes from 2D3D or ALACART.

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


def add_gst_ochra(ochra, labels, case, dataset):
    ''' Adds the Global Start Time (GST) to chosen tagged OCHRA annotations.

    Parameters
    ----------
    ochra : 2D ndarray
        Numpy array representing the OCHRA information, as labelled using the
        ochra.label_ochra function.
    labels: list of strs
        With the tags of the annotations for which to add the GST.
    case: str
        Case file from where the OCHRA information was extracted.
    dataset : str
        Specifies whether the OCHRA data comes from 2D3D or ALACART.

    Returns
    -------
    ochra: 2D ndarray
        Numpy array representing updated OCHRA data with GTSs.
    end_time: datetime.timedelta
        End time of the recording (in HH:MM:SS format).

    '''

    dataset = dataset.lower()
    if dataset not in ['alacart', '2d3d']:
        raise ValueError("Selected dataset must be be either 2D3D or ALACART.")

    # Noting down the column numbers of each video event
    if dataset == '2d3d':
        original, short, duration, glob_st = 0, 1, 2, 3
    elif dataset == 'alacart':
        path, original, short, duration, glob_st = 0, 1, 2, 3, 4
    
    # Loading video data for the case
    video = np.load(f'Video durations/{case}.npy', allow_pickle=True)
    
    # Discarding 'Path', 'Original name' and 'Duration' columns, keeping 'Short
    # form name' and 'Global start time' columns
    video_info = np.stack([video[:, short], video[:, glob_st]], axis=1)

    # Adding an empty column to hold the GSTs of the annotations
    ochra = np.insert(ochra, 4, np.full(len(ochra), np.nan), 1)

    # Noting down the column numbers of each event
    task, subtask, label, timecode, gst, subfile = 0, 1, 2, 3, 4, 5
    errors, conseq, eem, instr, severity, loc, info = 6, 7, 8, 9, 10, 11, 12

    def find_gst_video(video_info, simple_form):
        ''' Returns the GST of a chosen video for the case.

        Parameters
        ----------
        video : length-2 2D ndarray
            With the case videos information. The first column has the 'Short
            form' video names and the second column the respective GSTs.
        simple_form : str
            'Short form' name of the video from which to get the GST.

        Returns
        -------
        datetime.timedelta
            GST in HH:MM:SS format.

        '''
        for row in range(len(video_info)):
            if video_info[row, 0] == simple_form:
                return video_info[row, 1]

    # Adding GST to specified tagged events. This is done by summing the GST
    # of the video in the 'Subfile column' plus the time in the 'Timecode'
    # column
    for tag in labels:
        for row in range(len(ochra)):
            if ochra[row, label] == tag:
                ochra[row, gst] = (ochra[row, timecode] +
                                   find_gst_video(video_info,
                                                  ochra[row, subfile]))

    # Calculating end time of the last video
    end_time = video[-1, glob_st] + video[-1, duration]

    return ochra, end_time
