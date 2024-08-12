import os 
import shutil
import deeplabcut
from config import *


def inferenceMice(videopath = VIDEOPATH):
    print('here')
    destfolder = str(os.path.dirname(videopath) + '\csv')
    deeplabcut.analyze_videos(config = CONFIG, videos = videopath, videotype = '.mp4' , shuffle = 1, save_as_csv=True, destfolder = destfolder)

