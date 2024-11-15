import os 
from os import path
import shutil
import deeplabcut
from MAS.config import *
import glob


def inference_mice(video_path):
    dest_folder = str(os.path.dirname(video_path) + '\csv')
    vids =  glob.glob(str(video_path + '/*.mp4')) 
    for vid in vids:
        try:
            deeplabcut.analyze_videos(config = DLCDETECTOR, videos = vid, videotype = '.mp4' , shuffle = 1, save_as_csv=True, destfolder = dest_folder)
        except OSError:
            continue

def show_pred(video_path, pcutoff):
    csv_folder = str(os.path.dirname(video_path) + '\csv')
    files = os.listdir(csv_folder)
    for file in files:
        shutil.copy(os.path.join(csv_folder, file), os.path.join(video_path, file))
    deeplabcut.create_labeled_video(config=DLCDETECTOR, videos=video_path , color_by='individual', shuffle = 1, pcutoff = pcutoff)
    for file in files:
        os.remove(os.path.join(video_path, file))
    vidList = os.listdir(video_path)
    DLC_tracking = str(os.path.dirname(video_path) + '/DLCTracking')
    if not path.isdir(DLC_tracking) :
        os.mkdir(DLC_tracking)
    for vid in vidList:
        if "shuffle" in vid:
            shutil.move(os.path.join(video_path, vid), os.path.join(DLC_tracking, vid))