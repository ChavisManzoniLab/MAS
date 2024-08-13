import os 
from os import path
import shutil
import deeplabcut
import glob
from config import *


def inferenceMice(videopath):
    destfolder = str(os.path.dirname(videopath) + '\csv')
    deeplabcut.analyze_videos(config = CONFIG, videos = videopath, videotype = '.mp4' , shuffle = 1, save_as_csv=True, destfolder = destfolder)

def showPred(videopath, pcutoff):
    CSVfolder = str(os.path.dirname(videopath) + '\csv')
    files = os.listdir(CSVfolder)
    for file in files:
        shutil.copy(os.path.join(CSVfolder, file), os.path.join(videopath, file))
    deeplabcut.create_labeled_video(config=CONFIG, videos=videopath , color_by='individual', shuffle = 1, pcutoff = pcutoff)
    for file in files:
        os.remove(os.path.join(videopath, file))
    vidList = os.listdir(videopath)
    DLCTracking = str(os.path.dirname(videopath) + '\DLCTracking')
    if not path.isdir(DLCTracking) :
        os.makedir(DLCTracking)
    for vid in vidList:
        if "shuffle" in vid:
            shutil.move(os.path.join(videopath, vid), os.path.join(DLCTracking, vid))