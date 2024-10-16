import pandas as pd
import math as m
import numpy as np
import cv2
from matplotlib import pyplot as plt
from os import mkdir, path
from shapely import Polygon, Point
import random
import glob
from InferenceNest import *
import stat
import shutil
from statistics import mean

incr = list(range(5,101,5))
incr.insert(0,4)
incr.insert(0,3)
incr.insert(0,2)
incr.insert(0,1)

pathToVid = r'C:\Users\bs\Desktop\zad\vido'
detectorPath = r"C:\Users\bs\LabGym\Lib\site-packages\LabGym\detectors\Nest10"
dicolist = []

for i in incr:
    frame_extract(video_path=pathToVid, frame_per_vid = i)
    Nestdict = predict_nest(detectorPath, str(pathToVid + "/frames"), visual = False )
    dicolist.append(Nestdict)

resultdic = {'video' : [], 'areadiff' : []}

for vid in dicolist[0]['id']:
    resultlist = []
    print(vid)
    poly100 = dicolist[-1]['area'][vid]
    i = -1
    while poly100 == 0:
        i = i-1
        poly100 = dicolist[i]['area'][vid]
    for i, j in enumerate(incr) :
        poly = dicolist[i]['area'][vid] 
        result = abs(((poly100 - poly) / poly100)) * 100
        resultlist.append(result)
    resultdic['video'].append(vid)
    resultdic['areadiff'].append(resultlist)

print(resultdic.items())

for video in resultdic["video"]:
    plt.plot(incr,resultdic['areadiff'][video], label=video)

plt.xlabel('Iter')
plt.axhline(y=0, color='black', linestyle='--')
plt.ylabel('Result')
plt.title('Results of Videos')
plt.legend()
plt.show()