%reset -f
import time
import pysftp
from pymediainfo import MediaInfo
import datetime
import numpy as np

# 1st part of measuring time of execution of the code
start_time = time.time()

# Defining credentials to connect to the tails.cs.ucl.ac.uk server
Hostname = "tails.cs.ucl.ac.uk"
Username = "aavilaca"
Password = "AAT49ata"

# Disabling host key requirement (to be able to access the server) (https://stackoverflow.com/questions/38939454/verify-host-key-with-pysftp)
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None  

# Connecting to the server and moving to Griffin_dataset directory
sftp = pysftp.Connection(host=Hostname, username=Username, password=Password, cnopts=cnopts)
# print('Connection successfully established ...')
sftp.chdir("/cs/research/medic/surgicalvision/srv6/Griffin_dataset/2D3D VIDEOS/24")

video = np.array(sftp.listdir(), dtype=object)
video = np.transpose(np.vstack((video, video, np.full((2,len(video)), np.nan))))

for row in range(len(video)):
    video[row, 1] = video[row, 1].replace('VID00','')
    video[row, 1] = video[row, 1].replace('.mp4','')
    video[row, 1] = video[row, 1].replace('.MP4','')
    video[row, 1] = video[row, 1].replace('_','')
    
    print(f'~ {video[row, 1]}', end='')
    start_time = time.time()
    current_video = sftp.open(video[row, 0])
    duration_ms = MediaInfo.parse(current_video).tracks[0].duration
    duration_s = duration_ms / 1000
    dur = datetime.timedelta(seconds=duration_s)
    print(', %.2f seconds' % (time.time() - start_time))
    video[row, 2] = dur
    

video[0, 3] = datetime.timedelta(seconds=0)

for row in range(1,len(video)):
    video[row, 3] = video[row - 1, 2] + video[row - 1, 3]
    
# 2nd part of measuring time of execution of the code
# print('Executed in %.2f seconds.' % (time.time() - start_time))