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
sftp.chdir("/cs/research/medic/surgicalvision/srv6/Griffin_dataset/2D3D VIDEOS/1")

video = np.array(sftp.listdir(), dtype=object)
video = np.transpose(np.vstack((video, video, video, np.full((2,len(video)), np.nan))))

file = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15']
subfile = ['0','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

print('Opening Video ', end='')
for row in range(len(video)):
    video[row, 1:3] = video[row, 1].replace('VID00','')
    video[row, 1:3] = video[row, 1].replace('.mp4','')
    video[row, 1:3] = video[row, 1].replace('.MP4','')
    video[row, 1:3] = video[row, 1].replace('_','')
    if (video[row, 2] in file) == True:
        video[row, 2] = video[row, 1] + '0'
    
    start_time = time.time()
    print(f'{video[row, 1]}, ', end='')
    current_video = sftp.open(video[row, 0])
    duration_ms = MediaInfo.parse(current_video).tracks[0].duration
    duration_s = duration_ms / 1000
    dur = datetime.timedelta(seconds=duration_s)
    video[row, 3] = dur
    print('Executed in %.2f seconds.' % (time.time() - start_time))

for row in range(len(video)):
    # Getting the current file name and its position within 'file' and 'subfile'
    for flag_f in range(len(file)):
        if video[row, 2][0] == file[flag_f]:
            break
    for flag1_subf in range(len(subfile)):
        if video[row, 2][1] == subfile[flag1_subf]:
            break
    
    # Getting the previous file name and its position within 'file' and 'subfile'
    if subfile[flag1_subf] == '0':
        if file[flag_f] == '1':
            sel_video = '00'
        else:
            check1_subf = True
            for flag2_subf in reversed(range(len(subfile))):
                sel_video = file[flag_f - 1] + subfile[flag2_subf]
                for n in range(len(video)):
                    if sel_video == video[n, 2]:
                        check1_subf = False
                        break
                if check1_subf == False:
                    break
    else:
        sel_video = file[flag_f] + subfile[flag1_subf - 1]
    
    
    if sel_video == '00':
        video[row, 4] = datetime.timedelta(seconds=0)
    else:
        check2_subf = False
        for row_prev in range(len(video)):
            if sel_video == video[row_prev, 2]:
                video[row, 4] = video[row_prev, 3] + video[row_prev, 4]   
                check2_subf = True
                break
        if check2_subf == False:
            print(f'Video file {sel_video} is missing')

# check_subf = False
# for row_prev in range(len(video)):
#     if sel_video == video[row2, 2]:
#         dur = dur + video[row2, 3]
#         check_subf = True
#         break
# if check_subf == False:
#     print(f'Video file {sel_video} is missing')
# video[row2, 4] = dur
            

        
# 2nd part of measuring time of execution of the code
# print('Executed in %.2f seconds.' % (time.time() - start_time))