import os 
import shutil
import deeplabcut

config = r'C:\Users\bs\DLC\PRT-Benj-2024-01-30\config.yaml'
videopath = r'C:\Users\bs\Desktop\zad\vidfast'
destfolder = str(os.path.dirname(videopath) + '\csvauto')


deeplabcut.analyze_videos(config = config, videos = videopath, videotype = '.mp4' , shuffle = 1, save_as_csv=True, destfolder = destfolder)

