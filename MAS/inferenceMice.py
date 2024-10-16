import os 
from os import path
import shutil
import deeplabcut
import glob
from MAS.config import *


def inference_mice(video_path):
    destfolder = str(os.path.dirname(video_path) + '\csv')
    deeplabcut.analyze_videos(config = CONFIG, videos = video_path, videotype = '.mp4' , shuffle = 1, save_as_csv=True, destfolder = destfolder)

def show_pred(video_path, pcutoff):
    CSVfolder = str(os.path.dirname(video_path) + '\csv')
    files = os.listdir(CSVfolder)
    for file in files:
        shutil.copy(os.path.join(CSVfolder, file), os.path.join(video_path, file))
    deeplabcut.create_labeled_video(config=CONFIG, videos=video_path , color_by='individual', shuffle = 1, pcutoff = pcutoff)
    for file in files:
        os.remove(os.path.join(video_path, file))
    vidList = os.listdir(video_path)
    DLC_tracking = str(os.path.dirname(video_path) + '/DLCTracking')
    if not path.isdir(DLC_tracking) :
        os.mkdir(DLC_tracking)
    for vid in vidList:
        if "shuffle" in vid:
            shutil.move(os.path.join(video_path, vid), os.path.join(DLC_tracking, vid))