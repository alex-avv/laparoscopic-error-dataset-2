# laparoscopic-error-dataset

## Overview

The code aims to extract information from a laparoscopic colorectal error dataset constituting Excel files. The error annotations were taken following the OCHRA and task analaysis TME guidelines. A visualisation and statistical testing of the surgery events was made possible, helping in the database understanding. The end purpose of the project is to develop AI technology to detect moments of errors in the videos.

## Usage

To examine individual cases, open the `single_2d3d` or `single_alacart` scripts, choose the desired case, and run the file. You may need to manually add the Grifin annotation spreadsheets' path.

Similarly, to analyse the whole dataset, open the `all_datasets` file, select the desired parameters, and execute it. The statistical investigation of the events can be carried out using the `statistical_analysis` module.

## Notes

In order to get the event global times for visualisation, the video time-spans were extracted with the scripts in the `video_durations` folder. The 2D3D durations were extracted all at once, where as for ALACART this was done one by one. To retrieve the .VOB durations, the files were downloaded and manually inspected.
