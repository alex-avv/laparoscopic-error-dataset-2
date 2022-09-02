%reset -f
import time
import pysftp
from pymediainfo import MediaInfo
import datetime
import numpy as np
import os

# Defining credentials to connect to the tails.cs.ucl.ac.uk server
Hostname = "tails.cs.ucl.ac.uk"
Username = "sbostan"
Password = "TdT28ete"

# Disabling host key requirement (to be able to access the server) (https://stackoverflow.com/questions/38939454/verify-host-key-with-pysftp)
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

# Connecting to the server and moving to Griffin_dataset directory
sftp = pysftp.Connection(host=Hostname, username=Username, password=Password, cnopts=cnopts)
sftp.chdir("/cs/research/medic/surgicalvision/srv6/Griffin_dataset/ALACART/All Lap surgical Videos")

# Choosing folder to work with later
folder_name = "009"

# Opening folder from which to extract video data
sftp.chdir(folder_name)

# 'extension' will be used to retrieve the files with either of the video extensions given and their location within the chosen folder later on
extension = ['.mpg','.avi','.wmv','.mp4']

path = []       # 'path' will keep the locations of the video files detected
file_name = []      # 'file_name' will keep the names of the video files detected

# This function detects if a file has a video extension and saves its name and path
def store_files_name(fname):
    if (fname[len(fname) -4:len(fname)] in extension) == True:
        path.append(fname[2:len(fname)])
        for fname_last_position in reversed(range(0,len(fname))):
            if fname[fname_last_position] == '/':
                break
        fname = fname[fname_last_position +1:len(fname)]
        file_name.append(fname) 

# This function (empty) is needed later on (for the sftp.walktree() method)
def emptyFunction(nothing):
    pass

# Scanning all of the files in the chosen SFTP folder and storing information about those which are videos
sftp.walktree(".", store_files_name, emptyFunction, emptyFunction, recurse=True)
print(file_name)

# Changing 'path' and 'file_name' to numpy arrays of type object
path = np.array(path, dtype=object)
file_name = np.array(file_name, dtype=object)

# 'video' will keep the Path of the file, the Original name, the Short form name, the Duration and the Global start time of each video
video = np.transpose(np.vstack((path, file_name, file_name, np.full((2,len(file_name)), np.nan))))    # Creating 'video'

# =============================================================================
# with sftp.cd('/cs/research/medic/surgicalvision/srv6/Griffin_dataset/ALACART/All Lap surgical Videos'):
#     all_files = sftp.listdir()
#     video = sftp.chdir("150")
#     for video in all_files :
#         if (video [-2:] == '.mp4'):
#             print(video, 'downloaded successfully!')
# =============================================================================
            
# =============================================================================
# targetPattern = r"all_files\*.avi*"
# glob.glob(targetPattern)            
# 
# 
# # Opening folder from which to extract video data and creating array where video data will be stored
# =============================================================================

# =============================================================================
# df = df.drop(labels='subfile name', axis=1)
# =============================================================================

# 'substitute' contains the characters which have to be replaced from the Original name of the file to get the Short form name.
# A single string in an entry of the dictionary deletes those characters later on
# An array with two strings in an entry of the dictionary replaces the characters of the first with the characters of the second
# For example, '009':['0',['_','.']] deletes zeroes and replaces underscores with full stops
substitute = {'009':['0'], '013':['0'], '016':['0'], '022':['0'], '026':['0'],
              '033':['0'],
              '070':['ANDREWS_JAMES_Laparoscopic surg_20120329_'], '074':['0'],
              '077':['RA 077 - video ','RA 077 video '], '080':['ch1_video_0'],
              '087':['0'], '098':['0000000'], '099':['ch1_video_0'],
              '115':['ch1_video_0'], '130':['ch1_video_0'],
              '132':['ch2_video_0','pip_video_0'], '144':['0'],
              '146':['PDH 146 - video '], '147':['0'], '150':['0'],
              '153':['ch1_video_0'], '157':['0'], '161':['ch1_video_0'],
              '162':['ch1_video_0'],
              '190':['Botica__Colorectal laparo_20130321_'], '200':['0']
              }

# Populating the rows of 'video'
for row in range(len(video)):
    # Modifying the 'Short form' column
    for m in range(0,len(substitute[folder_name])):         # Removing first part of file name
        if len(substitute[folder_name][m]) == 2:
            video[row, 2] = video[row, 2].replace(substitute[folder_name][m][0], substitute[folder_name][m][1])
        else:
            video[row, 2] = video[row, 2].replace(substitute[folder_name][m],'')
    for n in range(0,len(extension)):       # Removing file extension
        video[row, 2] = video[row, 2].replace(f'{extension[n]}','')
        
    # Modifying the 'Duration' column
    print(f'~ {video[row, 2]}', end='')
    start_time = time.time()
    current_video = sftp.open(video[row, 0])
    duration_ms = MediaInfo.parse(current_video).tracks[0].duration
    duration_s = duration_ms / 1000
    dur = datetime.timedelta(seconds=duration_s)
    print(', %.2f seconds' % (time.time() - start_time))
    video[row, 3] = dur
        
# Ordering entries in numerical order
video = video[video[:,2].argsort()]

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
