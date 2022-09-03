
#%reset -f
import time
import pysftp
from pymediainfo import MediaInfo
import datetime
import numpy as np
import  os
import glob

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

# Opening folder from which to extract video data and creating array where video data will be stored
sftp.chdir("146")
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

# 'video' will keep the Original name of the file, the Short form name, the Duration and the Global start time of each video
video = np.array(sftp.listdir(), dtype=object)      # Initially, 'video' is 1D and has the names of all of the files in the folder
video = np.transpose(np.vstack((video, video, np.full((2,len(video)), np.nan))))    # Adding 3 more columns to 'video'

# Populating the rows of 'video'
for row in range(len(video)):
    # Modifying the 'Short form' column
        video[row, 1] = video[row, 1].replace('PDH','')
        video[row, 1] = video[row, 1].replace('146','')
        video[row, 1] = video[row, 1].replace('.wmv','')
        video[row, 1] = video[row, 1].replace('-','')

# =============================================================================
# for row in range(len(video)):
#     video[row, 1] = video[row, 1].replace('.mpg')
#     
# =============================================================================

    
    # Modifying the 'Duration' column
print(f'~ {video[row, 1]}', end='')
start_time = time.time()
current_video = sftp.open(video[row, 0])
duration_ms = MediaInfo.parse(current_video).tracks[0].duration
duration_s = duration_ms / 1000
dur = datetime.timedelta(seconds=duration_s)
print(', %.2f seconds' % (time.time() - start_time))
video[row, 2] = dur
    
# Modifying the 'Global start time' column
video[0, 3] = datetime.timedelta(seconds=0)     # Giving a start time of 0:00:00 to the first video in 'video'
for row in range(1,len(video)):       # The start times of the rest of videos will be the start time plus the duration of the previous video
    video[row, 3] = video[row - 1, 2] + video[row - 1, 3]
    
