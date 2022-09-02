import numpy as np
import datetime
import os

# Defining case number for which to save video information
folder_name = "999"

# 'vob' contains the names of the files whose duration was found out manually and their respective durations (in DD:HH:MM format)
vob = np.array([['VTS_01_1.VOB','01:00:00'],
                ['VTS_01_2.VOB','00:01:00'],
                ['VTS_01_3.VOB','00:00:01'],
                ['VTS_01_4.VOB','00:00:00'],
                ['VTS_01_5.VOB','00:00:00']], dtype=object)

# Defining path of the video files (optional)
path = np.array(np.repeat('SONY_DVD_RECORDER_VOLUME/VIDEO_TS/', len(vob), 0), dtype=object)

# Changing the durations in 'vob' to timedelta format (for easier working with later on)
for row in range(0,len(vob)):
    vob[row, 1] = datetime.timedelta(hours=int(vob[row, 1][0:2]), minutes=int(vob[row, 1][3:5]), seconds=int(vob[row, 1][6:8]))

# 'video' will keep the Path of the file, the Original name, the Short form name, the Duration and the Global start time of each video
video = np.transpose(np.vstack((path, vob[:,0], vob[:,0], vob[:,1], np.full(len(vob), np.nan))))    # Creating 'video'

# Modifying the 'Short form' column
for row in range(len(video)):
    video[row, 2] = video[row, 2].replace('VTS_0','')
    video[row, 2] = video[row, 2].replace('_','.')
    video[row, 2] = video[row, 2].replace('.VOB','')

# Modifying the 'Global start time' column
video[0, 4] = datetime.timedelta(seconds=0)     # Giving a start time of 0:00:00 to the first video in 'video'
for row in range(1,len(video)):       # The start times of the rest of videos will be the start time plus the duration of the previous video
    video[row, 4] = video[row -1, 3] + video[row -1, 4]

# Changing the system working directory to save the video information in the computer on
os.chdir("C:/Users/aleja/OneDrive - University College London/Griffin Institute collaboration/Grifin_annotations/ALACART/Video durations")

# Saving video data as .npy file
np.save(f'{folder_name}', video)

# Loading a single .npy file (for testing)
exec("dur_" + folder_name + " = np.load(f'{folder_name}.npy', allow_pickle=True)") 