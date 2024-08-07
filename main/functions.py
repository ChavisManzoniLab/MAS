import pandas as pd
import math as m
import numpy as np
import cv2
from os import mkdir, path
from shapely import Polygon, Point
import random
import glob
from InferenceNest import *
import stat
import shutil
from statistics import mean
import config

def dist(B,A):
    """
    Returns the euclidean distance between two points.
    """
    X =(A[0]-B[0])**2
    Y =(A[1]-B[1])**2
    return m.sqrt(X+Y)

def mean_calculator(df):
    #outputs a dataframe with the mean coordinates of the dam and the pup for each frame.
    #if not detected, the default value is -1.
    frames = len(df)
    columns = ['t', 'damx', 'damy', 'pupx', 'pupy','damCenterx','damCentery']
    meandf = pd.DataFrame(columns = columns)
    likelihood = 0.7 #threshold on the certainty of the prediction.
    sizeList = []
    for frame in range(frames):
        meandf.loc[frame, 't'] = frame
        damx = []
        damy = []
        pupx = []
        pupy = []
        if df.iloc[frame, 3] > likelihood and df.iloc[frame, 12] > likelihood and df.iloc[frame, 18] > likelihood and df.iloc[frame, 21] > likelihood :
            nose = [df.iloc[frame,1], df.iloc[frame,2]]
            neck =[df.iloc[frame,10], df.iloc[frame,11]]
            spine = [df.iloc[frame,16], df.iloc[frame,17]]
            tail = [df.iloc[frame,19], df.iloc[frame,20]]
            mommySize = dist(nose,neck) + dist(neck, spine) + dist(spine, tail)
            sizeList.append(mommySize)
        for i in range(1, 10, 3):
            if df.iloc[frame, i+2]> likelihood:
                damx.append(df.iloc[frame, i])
                damy.append(df.iloc[frame, i+1])
        if len(damx)>1:
            meandf.loc[frame, 'damx'] = sum(damx)/len(damx)
            meandf.loc[frame, 'damy'] = sum(damy)/len(damy)
        else: 
            meandf.loc[frame, 'damx'] = -1
            meandf.loc[frame, 'damy'] = -1
        if len(damx)>1 and df.iloc[frame, 18] > likelihood:
            spine = [df.iloc[frame,16], df.iloc[frame,17]]
            meandf.loc[frame, 'damCenterx'] = (sum(damx)/len(damx) + spine[0])/2
            meandf.loc[frame, 'damCentery'] = (sum(damy)/len(damy) + spine[1])/2
        else:
            meandf.loc[frame, 'damCenterx'] = -1
            meandf.loc[frame, 'damCentery'] = -1

        for i in range(22, 39, 3):
            if df.iloc[frame, i+2]> likelihood:
                pupx.append(df.iloc[frame, i])
                pupy.append(df.iloc[frame, i+1])
                
        if len(pupx)>2:
            #if the number of detected points is less than two, the mean is not calculated
            meandf.loc[frame, 'pupx'] = sum(pupx)/len(pupx)
            meandf.loc[frame, 'pupy'] = sum(pupy)/len(pupy)
        else : 
            meandf.loc[frame, 'pupx'] = -1
            meandf.loc[frame, 'pupy'] = -1
        try : 
            meanlist = mean(sizeList)
        except:
            meanlist = 0
    return meandf, meanlist

def remove_outliers(df):
    #if the tracking was lost for one frame, the coordinates are replaced with the average between the previous frame and the next frame.
    for i in range(1, len(df)-1):
        
        if np.sign(df.loc[i, 'pupx']) != np.sign(df.loc[i-1, 'pupx']) and np.sign(df.loc[i, 'pupx']) != np.sign(df.loc[i+1, 'pupx']):
            df.loc[i, 'pupx'] = (df.loc[i-1, 'pupx'] + df.loc[i+1, 'pupx'])/2
            df.loc[i, 'pupy'] = (df.loc[i-1, 'pupy'] + df.loc[i+1, 'pupy'])/2
        if np.sign(df.loc[i, 'damx']) != np.sign(df.loc[i-1, 'damx']) and np.sign(df.loc[i, 'damx']) != np.sign(df.loc[i+1, 'damx']):
            df.loc[i, 'damx'] = (df.loc[i-1, 'damx'] + df.loc[i+1, 'damx'])/2
            df.loc[i, 'damy'] = (df.loc[i-1, 'damy'] + df.loc[i+1, 'damy'])/2
    i = len(df) -1
    if np.sign(df.loc[i, 'pupx']) != np.sign(df.loc[i-1, 'pupx']):
        df.loc[i, 'pupx'] = df.loc[i-1, 'pupx']
        df.loc[i, 'pupy'] = df.loc[i-1, 'pupy']
    if np.sign(df.loc[i, 'damx']) != np.sign(df.loc[i-1, 'damx']):
        df.loc[i, 'damx'] = df.loc[i-1, 'damx']
        df.loc[i, 'damy'] = df.loc[i-1, 'damy']
            
def isGone(XcoordList,YcoordList, start):
    """
    Check if the pup does appear again. 
    If not return True and the start frame
    If the pup reappear, return False and the frame of reappearence
    """
    X = 0
    Y = 0
    for i in range(start,len(XcoordList)):
        X =  XcoordList[i] + 1
        Y =  YcoordList[i] + 1
        if X + Y != 0:
            return False, i
    return True, start

def dam_isLost(df, frame):
    #test if the dam disappears for more than 5 frames.
    damX = 0
    damY = 0

    for i in range(frame, frame + 5):
        damX = damX + df.loc[i,'damx'] + 1
        damY = damY + df.loc[i,'damy'] + 1
        
        if damX + damY != 0:
            return False
        
    return True
    
def damAbove(df, frame, threshold = 100):
    """
    Test the proximity of the dam and the pup during frame
    threshold is excepted in euclidian distance, in pixel
    """
    pup = list((df.loc[frame-1, 'pupx'], df.loc[frame-1, 'pupy']))
    dam = list((df.loc[frame-1, 'damx'], df.loc[frame-1, 'damy']))
    return True if dist(pup,dam) <= threshold and pup != [-1, -1] and dam != [-1, -1] else False

def firstEncounter(df):
    #returns the frame of the first encounter of dam-pup.
    for frame in range(1, len(df)):
        if damAbove(df, frame, 100):
        #    if damAbove(df, frame+1, 120):
                return frame    

def dam_distance(df, nest, start = 0, stop = 0):
    """
    Returns the total distance of dam in pixel, from start to stop (in frames)
    """
    print(stop)
    if(stop == None):
        stop = len(df)
    distance = 0
    for i in range(start+1, stop):
        dam = (df.loc[i-1, 'damCenterx'], df.loc[i-1, 'damCentery'])
        dam2 = (df.loc[i, 'damCenterx'], df.loc[i, 'damCentery'])
        if dam[0] > 0 and dam2[0] > 0 and dam[1] > 0 and dam2[1] > 0 and not isNestPoly(nest, dam[0],dam[1]):
            temp = dist(dam, dam2) 
            if temp > 10 : 
                distance += temp
    return distance

def inNestRelative(df, m):
    #OBS
    #determines if the pup has crossed the x coord from the first appearenancene of the dam.
    #ie if the x coordinates of the pup are lower for 3 frames than the first x coordinate of the dam.
    e = pd.to_numeric(df['pupx'])

    f = list(pd.to_numeric(df['damx']))

    fi = [x for i, x in enumerate(f) if x > 0]
    if fi != []:
        firstApp_dam = fi[0]
    else :
        firstApp_dam = -2

    for i in range(m ,len(e)-3):
        i = i+1
        if e[i] <= firstApp_dam and e[i] != -1 :
            if e[i+1] <= firstApp_dam and e[i+1] != -1 and e[i+2] <= firstApp_dam and e[i+2] != -1:
                return i 
    return None

def isNestPoly(polygon, x, y):
    animal = Point(x, y)
    if polygon != 0:
        isNest = polygon.contains(animal)
        return isNest
    else: return False

def distToNestBorder(polygon, x, y):
    """
    Return the distance of a coordinate to the exterior of the nest

    Args : 
        polygon : A shapely polygon object
        x, y : coordinate
    """
    animal = Point(x,y)
    return polygon.exterior.distance(animal)

def success(df, poly):
    """
    returns the frame of the PRT success
    
    Args : 
        df : A pandas dataframe returned from mean_calculator()
        polygon : A shapely polygon object
    """
    i = 2
    pupX = pd.to_numeric(df['pupx'])
    pupY = pd.to_numeric(df['pupy'])
    damX = pd.to_numeric(df['damx'])
    damY = pd.to_numeric(df['damy'])
    inNestList = []

    if not firstEncounter(df): # No encounter Pup-Dam result in a failure
        return None
  
    for j in range(0, len(df)):    #Add every frame where the pup is detected in the nest to a list 
        if isNestPoly(poly, pupX[j], pupY[j]):
            inNestList.append(j)
            
    #iterates through the frames until the pup has disappeared.
    while i<len(df) and not isGone(pupX, pupY, i)[0] :
        i = pupX[isGone(pupX, pupY, i)[1]:].idxmin() #Return the frame
        if i == 0:
            return None 
        if df.loc[i,'pupx'] !=-1: #if the minimum is different from -1, the pup never disappears from the video.
            for i in range(0, len(df)):
                try:
                    if i in inNestList and distToNestBorder(poly, pupX[i], pupY[i]) > 30:
                        print("PUP NEVER DISSARPEAR")
                        return i
                except: break
                
            return None
        pupgone , iter = isGone(pupX, pupY, i) #Return the next appearence as iter
        print(pupgone)
        if damAbove(df, i-1): 
            if i == iter:
                iter = len(df)
            for frame in range(i, iter):
                print("for frame")
                try:
                    if (distToNestBorder(poly, damX[frame], damY[frame]) != None and distToNestBorder(poly, damX[frame], damY[frame] ) <= 10) or isNestPoly(poly, damX[frame], damY[frame]):
                        if pupgone == True:
                            print("innest")
                            return frame
                        if isNestPoly(poly, pupX[frame], pupY[frame]) and distToNestBorder(poly, pupX[frame], pupY[frame]) > 40:
                            print("là")
                            return frame
                    if dam_isLost(df, frame):
                         #CHECK IF PUP REAPEAR AND WHERE
                        for test in range(frame,len(df)):
                            if pupX[test] > 0 and pupY[test] > 0 and not isNestPoly(poly, pupX[frame], pupY[frame]):
                                continue 
                        print('là')
                        return frame
                except: break #FAIRE QUELQUE CHOSE POUR CHECKER SI MAMAN ELLE DISPARAIT AVANT QUE LE PUP REPARRAIT
        for r in range(i, iter-5):

            if pupgone:
                if dam_isLost(df,r) or isNestPoly(poly, damX[r], damY[r]):
                    print("ehee")                                        
                    return r
        #the loop stops at the frame where the pup disappears until the end of the video.               
    if  damAbove(df, i-1) : 
        print("mhmh")
        #if the dam is near the pup when it disappears, the frame of the success of PRT is when the dam goes into the nest.
        stuck = 0
        while i<len(df) and not isGone(damX, damY, i)[0] and not stuck == 15 :
            i = damX[isGone(damX, damY, i)[1]:].idxmin()
            print("loop")
            if i < len(df)-5 and dam_isLost(df, i) or isNestPoly(poly, damX[i], damY[i]):
                return i 
            stuck = stuck + 1
    for j in inNestList:
        print("PupinNest Frame " + str(j))
        if j < firstEncounter(df):
            print("wrong pup")
            continue
        try:
            if distToNestBorder(poly, pupX[j], pupY[j]) > 30 and j < i:
                print("??")
                return j
        except: break
    return i

def timestampRead(pathToVideo, csv):
  
    # Search for the corresponding .MP4
    vidName = csv.split('_')[0]
    vidName = vidName.replace('DLC', '')
    video = pathToVideo +'\\'+ vidName + ".mp4"
    cap = cv2.VideoCapture(video)
    timestamps = []
    # Read each frame in a video to assess the corresponding timestamp
    if cap.isOpened():

        frame_rate = cap.get(cv2.CAP_PROP_FPS)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            timestamp = cap.get(cv2.CAP_PROP_POS_MSEC)/1000.0
            timestamps.append(timestamp)
    else:
        print('ISSUE WITH VIDEO %s'%vidName)
        timestamps.append("ERROR")

    return timestamps, vidName

def outputResults(pathToCSV, pathToVideo, pathToOuput, polyDic):
    #Write TOUT to CSV
    dataf = pd.DataFrame(columns = ('video', 'success','success sec', 'firstEncounter', 'firstEncounter sec','timeFEtoRet', 'distanceToFirstEncounter', 'distanceFEtoRet'))
    pathToCSV = str(pathToCSV+"\*.csv")
    files = glob.glob(pathToCSV)

    for i, csv in enumerate(files):
        damSize = None
        pixcoef = None
        try:
            timestamps, vidName = timestampRead(pathToVideo, str(path.basename(path.normpath(csv))))
            print("lentim",len(timestamps))
            df = pd.read_csv(csv, skiprows = 3)         
            meandf, damSize = mean_calculator(df)
            remove_outliers(meandf)
            dataf.loc[i, 'video'] = vidName
            f = firstEncounter(meandf)
            dataf.loc[i, 'firstEncounter'] = f
            dataf.loc[i, 'damSize'] = damSize
            try:
                pixcoef = 8.5/damSize
            except:
                pixcoef = None
            dataf.loc[i, 'pixelcoef'] = pixcoef
            if f != None: #If First encounter, get the frames in seconds 
                fsec = timestamps[f-1]
                dataf.loc[i, 'firstEncounter sec'] = fsec
                dataf.loc[i,'distanceToFirstEncounter'] = dam_distance(meandf, stop = f, nest = polyDic["polygon"][i])
                if pixcoef :
                    dataf.loc[i,'distanceToFirstEncounter cm'] = dam_distance(meandf, stop = f, nest = polyDic["polygon"][i])*pixcoef
            else : 
                dataf.loc[i, 'firstEncounter sec'] = None
                dataf.loc[i,'distanceToFirstEncounter'] = None
                dataf.loc[i,'distanceToFirstEncounter cm'] = None
            s = success(meandf, polyDic["polygon"][i])
            print(csv)
            print(s)
            if s != None: #If success, get the frames in seconds 
                print(s)
                dataf.loc[i, 'success'] = s
                dataf.loc[i, 'success sec'] = timestamps[s]
                dataf.loc[i, 'timeFEtoRet'] = timestamps[s] - fsec 
                dataf.loc[i,'distanceFEtoRet'] = dam_distance(meandf, start = f, stop = s,nest = polyDic["polygon"][i])
                if pixcoef :
                    dataf.loc[i,'distanceFEtoRet cm'] = dam_distance(meandf, start = f, stop = s,nest = polyDic["polygon"][i])*pixcoef
            else:
                dataf.loc[i, 'success'] = -1
                dataf.loc[i, 'success sec'] = None
                dataf.loc[i,'distanceFEtoRet'] = None
                dataf.loc[i,'distanceFEtoRet cm'] = None
            dataf.loc[i, 'distance'] = dam_distance(meandf, stop = s, nest = polyDic["polygon"][i])
            if pixcoef :
                dataf.loc[i, 'distance cm'] = dam_distance(meandf, stop = s, nest = polyDic["polygon"][i])*pixcoef

            dataf.loc[i, 'Area of Nest'] = polyDic["area"][i]
        
        except: 
            dataf.loc[i, 'video'] = "NOT FOUND"
            dataf.loc[i, 'success'] = None
            dataf.loc[i, 'success sec'] = None
            dataf.loc[i,'distanceFEtoRet'] = None
            dataf.loc[i, 'firstEncounter sec'] = None
            dataf.loc[i,'distanceToFirstEncounter'] = None
            dataf.loc[i, 'firstEncounter'] = None
            dataf.loc[i, 'distance'] = None
            dataf.loc[i, 'Area of Nest'] = None
        
    #print(csv, success(meandf, polyDic["polygon"][i]), dam_distance(meandf, stop = s), firstEncounter(meandf))
    #/!\ CHANGER NOM FICHIER
    data = pd.ExcelWriter(pathToOuput +'dataOutput_C2.xlsx', engine='xlsxwriter') #the output file with the success
    dataf.to_excel(data, sheet_name='Sheet1', index=False)
    data.close()
    print("DONE")

def draw_polygon_on_video(polygon, input_video_path, output_video_path):
    cap = cv2.VideoCapture(input_video_path)
    if not cap.isOpened():
        print("Error: Couldn't open video file.")
        return
    
    # Get video properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))
    
    # Draw polygon on every frame
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Draw polygon on the frame
        polygon_points = np.array(polygon.exterior.coords, np.int32)
        polygon_points = polygon_points.reshape((-1, 1, 2))
        cv2.polylines(frame, [polygon_points], isClosed=True, color=(0, 255, 120), thickness=2)
        
        # Write the frame to the output video
        out.write(frame)
        
    # Release video objects
    cap.release()
    out.release()
    cv2.destroyAllWindows()

outpath = r'C:\Users\bs\Desktop\zad\mdr2.mp4'
pathTobox = r'C:\Users\bs\Desktop\zad\vido\2023-06-05 C4 T4 Masdig.mp4'
pathToVid = r'C:\Users\bs\Desktop\zad\vidNew'
detectorPath = r"C:\Users\bs\LabGym\Lib\site-packages\LabGym\detectors\Nest10"
pathToCSV = r'C:\Users\bs\Desktop\zad/csv1'
pathToOuput = r'C:\Users\bs\Desktop\zad/output/'

def PRTAnalysis(pathToVid , detectorPath, pathToCSV, pathToOuput, useBackup = False):
    frameExtract(pathToVid=pathToVid, framePerVid = 20)
    if useBackup :
        with open('backup/nestDict.pkl', 'rb') as f:
            Nestdict = pickle.load(f)    
    else:
        Nestdict = predictNest(detectorPath, str(pathToVid + "/frames"), visual = False )
        
    outputResults(pathToCSV, pathToVideo=pathToVid, pathToOuput = pathToOuput, polyDic = Nestdict)
    #draw_polygon_on_video(Nestdict["polygon"][0], pathTobox, outpath)

PRTAnalysis(pathToVid , detectorPath, pathToCSV, pathToOuput, useBackup=False) 