%reset -f
"""¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨"""
"""¨¨¨ Setting up environment & files' path ¨¨¨"""
# Importing python libraries
import time
import pysftp
from pymediainfo import MediaInfo
import datetime
import numpy as np
import os

# Defining credentials to connect to the tails.cs.ucl.ac.uk server
Hostname = "tails.cs.ucl.ac.uk"
Username = "aavilaca"
Password = "AAT49ata"

# Disabling host key requirement (to be able to access the server) (https://stackoverflow.com/questions/38939454/verify-host-key-with-pysftp)
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None  

# Connecting to the server and moving to Griffin_dataset directory
sftp = pysftp.Connection(host=Hostname, username=Username, password=Password, cnopts=cnopts)
sftp.chdir("/cs/research/medic/surgicalvision/srv6/Griffin_dataset/2D3D VIDEOS")
"""¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨"""


"""¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨"""
"""¨¨¨ Extracting video information ¨¨¨"""
def extract_video(folder_name):
    print(f'Folder {folder_name}')
    
    # Opening folder from which to extract video data and creating array where video data will be stored
    sftp.chdir(f'{folder_name}')
    # 'video' will keep the Original name of the file, the Short form name, the Duration and the Global start time of each video
    video = np.array(sftp.listdir(), dtype=object)      # Initially, 'video' is 1D and has the names of all of the files in the folder
    video = np.transpose(np.vstack((video, video, np.full((2,len(video)), np.nan))))    # Adding 3 more columns to 'video'
    
    # Populating the rows of 'video'
    for row in range(len(video)):
        # Modifying the 'Short form' column
        video[row, 1] = video[row, 1].replace('VID00','')
        video[row, 1] = video[row, 1].replace('VID0','')
        video[row, 1] = video[row, 1].replace('.mp4','')
        video[row, 1] = video[row, 1].replace('.MP4','')
        video[row, 1] = video[row, 1].replace('_','')
        
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
    
    # Returning to '2D3D VIDEOS' folder (i.e. one level up)
    sftp.chdir('../')
    
    return video        # Giving 'video' to the function's output
"""¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨"""


"""¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨"""
"""¨¨¨ Importing folders and saving video information ¨¨¨"""
i2D3D = np.array(sftp.listdir(), dtype=object)      # 'i2D3D' has the names of all of the files (folders) in the '2D3D VIDEOS' folder (in the server)

# Changing the system working directory to save the video information in the computer on
os.chdir("C:/Users/aleja/OneDrive - University College London/Griffin Institute collaboration/Grifin_annotations/2D3D VIDEOS/Video durations")

# Looping through all of the folders in '2D3D VIDEOS', extracting the relevant video data and saving it as .npy files
for index in range(0,len(i2D3D)):
    folder_name = i2D3D[index]
    video = extract_video(folder_name)
    np.save(f'{folder_name}', video)

# Loading a single .npy file (for testing)
dur_1 = np.load('1.npy', allow_pickle=True)    