import pandas as pd
import math as m
import numpy as np
import cv2
from os import mkdir, path
from shapely import Polygon, Point
import random
import glob
from MAS.InferenceNest import *
import stat
import shutil
from statistics import mean
import MAS.config
from MAS.inferenceMice import *

def dist(B,A):
    """
    Returns the euclidean distance between two points.
    """
    X =(A[0]-B[0])**2
    Y =(A[1]-B[1])**2
    return m.sqrt(X+Y)

def mean_calculator(df, likelihood = 0.7):
    """
    Outputs a dataframe with the mean coordinates of the head of the dam and the pup for each frame.
    if not detected, the default value is -1.
    Also output the average size of the dam, in pixel

    —————————
    Arguments 
    —————————
    df : The CSV output from the maDLC script
    likelihood : The lowest accepted likelihood for the points.
    """

    frames = len(df)
    columns = ['t', 'damx', 'damy', 'pupx', 'pupy','damCenterx','damCentery']
    meandf = pd.DataFrame(columns = columns)
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
            #if the number of detected points is less than 3, the mean is not calculated
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
    Check if one does appear again. 
    If not return True and the start frame
    If reappearence, return False and the frame of reappearence
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

def isNestPoly(polygon, x, y):
    #Test in the point (x,y) is in the polygon 
    animal = Point(x, y)
    if polygon != 0:
        isNest = polygon.contains(animal)
        return isNest
    else: return False

def distToNestBorder(polygon, x, y):
    """
    Return the distance of a coordinate to the exterior of the nest
    —————————
    Arguments 
    —————————
        polygon : A shapely polygon object
        x, y : coordinate
    """
    animal = Point(x,y)
    return polygon.exterior.distance(animal)

def success(df, poly, nestBorderThreshold = 10):
    """
    returns the frame of the PRT success
    —————————
    Arguments 
    —————————
        df : A pandas dataframe returned from mean_calculator()
        poly : A shapely polygon object
        nestBorderThreshold : The threshold of the nest, in pixel
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
            for i in range(0, len(df)): #Loop though everything
                try:
                    if i in inNestList and distToNestBorder(poly, pupX[i], pupY[i]) > nestBorderThreshold: 
                        return i # If The pup is in the nest return success
                except: break
                
            return None
        pupgone , iter = isGone(pupX, pupY, i) #Return the next appearence as iter
        print(pupgone)
        if damAbove(df, i-1): #If the dam is above the pup when he disappears
            if i == iter: #If pupgone return the current frame
                iter = len(df) # iter goes to the end of the dataframe
            for frame in range(i, iter):
                try:
                    if (distToNestBorder(poly, damX[frame], damY[frame]) != None and distToNestBorder(poly, damX[frame], damY[frame] ) <= nestBorderThreshold) or isNestPoly(poly, damX[frame], damY[frame]):
                        if pupgone == True: #If the pup is never seen again and the Dam enter the nest
                            return frame
                        
                        if isNestPoly(poly, pupX[frame], pupY[frame]) and distToNestBorder(poly, pupX[frame], pupY[frame]) > nestBorderThreshold:
                            return frame #If the pup is IN the nest and not close to the border
                        
                    if dam_isLost(df, frame):
                         #Check if pup reappears AND WHERE
                        for test in range(frame,len(df)):
                            if pupX[test] > 0 and pupY[test] > 0 and not isNestPoly(poly, pupX[frame], pupY[frame]):
                                continue 
                        return frame
                except: break
        for r in range(i, iter-5):

            if pupgone:
                if dam_isLost(df,r) or isNestPoly(poly, damX[r], damY[r]):                                    
                    return r
        #the loop stops at the frame where the pup disappears until the end of the video.               
    if  damAbove(df, i-1) : 
        #if the dam is near the pup when it disappears, the frame of the success of PRT is when the dam goes into the nest.
        stuck = 0
        while i<len(df) and not isGone(damX, damY, i)[0] and not stuck == 15 :
            i = damX[isGone(damX, damY, i)[1]:].idxmin()
            if i < len(df)-5 and dam_isLost(df, i) or isNestPoly(poly, damX[i], damY[i]):
                return i 
            stuck = stuck + 1
    for j in inNestList:
        print("PupinNest Frame " + str(j))
        if j < firstEncounter(df):
            print("wrong pup")
            continue
        try:
            if distToNestBorder(poly, pupX[j], pupY[j]) > nestBorderThreshold and j < i:
                print("??")
                return j
        except: break
    return i

def timestampRead(pathToVideo, csv):
  
    """
    Get the frame value in second of the video. Useful when videos are corrupted
    """
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

def outputResults(pathToCSV, pathToVideo, pathToOutput, polyDic, nestBorderThreshold, DLCThreshold):
    #Write result in a CSV file
    dataf = pd.DataFrame(columns = ('video', 'success frame','success sec', 'firstEncounter frame', 'firstEncounter sec','timeFEtoRet sec', 'distanceToFirstEncounter pixel', 'distanceFEtoRet pixel'))
 
    #Prepare the list to match CSV and video
    pathToCSV = str(pathToCSV+"\*.csv")
    CSVList = glob.glob(pathToCSV)
    CSVList_Short = []
    for csvItem in CSVList:
        vidName = csvItem.split('_')[0]
        vidName = path.basename(vidName.replace('DLC', ''))
        CSVList_Short.append(vidName)

    vids =  glob.glob(str(pathToVideo + '/*.mp4'))
    for i, file in enumerate(vids):
        video = str(path.basename(path.normpath(file))).replace(".mp4","")
        #Match the video and the nest polygon
        try:
            dictIndex = polyDic["video"].index(video)
        except ValueError: 
            print(video)
            print("NO MATCHING VIDEO FOUND IN THE NEST DICT")
            continue
        #Match the video and the CSV file
        try:   
            csvIndex = CSVList_Short.index(video)
        except ValueError: 
            print(CSVList_Short)
            print(video)
            print("NO MATCHING VIDEO FOUND FOR THE CSV")
            continue

        damSize = None
        pixcoef = None
        try:
            timestamps, vidName = timestampRead(pathToVideo, str(path.basename(path.normpath(CSVList[csvIndex]))))
            print("lentim",len(timestamps))
            df = pd.read_csv(CSVList[csvIndex], skiprows = 3)         
            meandf, damSize = mean_calculator(df, likelihood = DLCThreshold)
            remove_outliers(meandf)
            dataf.loc[i, 'video'] = vidName
            f = firstEncounter(meandf)
            dataf.loc[i, 'firstEncounter frame'] = f
            dataf.loc[i, 'damSize'] = damSize

            #Try to extrapolate the pixel to cm size via the size of the Dam
            try:
                pixcoef = 8.5/damSize
            except:
                pixcoef = None
            dataf.loc[i, 'pixelcoef'] = pixcoef
            if f != None: #If First encounter, get the frames in seconds 
                fsec = timestamps[f-1]
                dataf.loc[i, 'firstEncounter sec'] = fsec
                dataf.loc[i,'distanceToFirstEncounter pixel'] = dam_distance(meandf, stop = f, nest = polyDic["polygon"][dictIndex])
                if pixcoef :
                    dataf.loc[i,'distanceToFirstEncounter cm'] = dam_distance(meandf, stop = f, nest = polyDic["polygon"][dictIndex])*pixcoef
            else : 
                dataf.loc[i, 'firstEncounter sec'] = None
                dataf.loc[i,'distanceToFirstEncounter pixel'] = None
                dataf.loc[i,'distanceToFirstEncounter cm'] = None
            s = success(meandf, polyDic["polygon"][dictIndex], nestBorderThreshold)
            print(CSVList[csvIndex])
            print(s)
            if s != None: #If success, get the frames in seconds 
                print(s)
                dataf.loc[i, 'success frame'] = s
                dataf.loc[i, 'success sec'] = timestamps[s]
                dataf.loc[i, 'timeFEtoRet sec'] = timestamps[s] - fsec 
                dataf.loc[i,'distanceFEtoRet pixel'] = dam_distance(meandf, start = f, stop = s,nest = polyDic["polygon"][dictIndex])
                if pixcoef :
                    dataf.loc[i,'distanceFEtoRet cm'] = dam_distance(meandf, start = f, stop = s,nest = polyDic["polygon"][dictIndex])*pixcoef
            else:
                dataf.loc[i, 'success frame'] = -1
                dataf.loc[i, 'success sec'] = None
                dataf.loc[i,'distanceFEtoRet pixel'] = None
                dataf.loc[i,'distanceFEtoRet cm'] = None
            dataf.loc[i, 'distance pixel'] = dam_distance(meandf, stop = s, nest = polyDic["polygon"][dictIndex])
            if pixcoef :
                dataf.loc[i, 'distance cm'] = dam_distance(meandf, stop = s, nest = polyDic["polygon"][dictIndex])*pixcoef

            dataf.loc[i, 'Area of Nest pixel'] = polyDic["area"][dictIndex]
        
        except: 
            dataf.loc[i, 'video'] = "NOT FOUND"
            dataf.loc[i, 'success frame'] = None
            dataf.loc[i, 'success sec'] = None
            dataf.loc[i,'distanceFEtoRet pixel'] = None
            dataf.loc[i, 'firstEncounter sec'] = None
            dataf.loc[i,'distanceToFirstEncounter'] = None
            dataf.loc[i, 'firstEncounter frame'] = None
            dataf.loc[i, 'distance pixel'] = None
            dataf.loc[i, 'Area of Nest pixel'] = None
    
    fileCreated = False
    increment = 0
    while not fileCreated:
        try: 
            data = pd.ExcelWriter(pathToOutput +'/dataOutput_' + str(increment) + '.xlsx' , mode = 'x', engine='xlsxwriter') #the output file with the success
            fileCreated = True
        except:
            increment += 1
        if increment >= 30:
            raise ValueError("ANTIJAM")
    dataf.to_excel(data, sheet_name='Results', index=False)
    data.close()
    print("DONE")

def drawNestOnVid(videopath, nestPoly, outputPath= None):
    cap = cv2.VideoCapture(videopath)
    if outputPath == None :
        outputPath = str(videopath)
        outputPath = outputPath.replace(".mp4","_NestDraw.mp4")
    if not cap.isOpened():
        print("Error: Couldn't open video file.")
        return
    
    # Get video properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(outputPath, fourcc, fps, (frame_width, frame_height))
    
    # Draw polygon on every frame
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Draw polygon on the frame
        polygon_points = np.array(nestPoly.exterior.coords, np.int32)
        polygon_points = polygon_points.reshape((-1, 1, 2))
        cv2.polylines(frame, [polygon_points], isClosed=True, color=(0, 255, 120), thickness=2)
        
        # Write the frame to the output video
        out.write(frame)
        
    # Release video objects
    cap.release()
    out.release()
    cv2.destroyAllWindows()

def PRTAnalysis(videopath , detectorPath = NESTDETECTOR,  useBackup = False, showNest = False, useCSV = False, drawDLCpred = False,  drawNest = False, nestBorderThreshold = 10 , DLCThreshold = 0.7):
    """
    The main function
    Launch the detection of the nest via detectron2
    Launch the detection of the mice via maDLC
    Pass the result through the MAS pipeline and output results in results folders

    —————————
    Arguments 
    —————————
    pathToVid : The path to the video folder. Videos must be in MP4    
    detectorPath : Path to the Detectron2 detector 
    useBackup => Boolean : Use the .pickle file to gain time. Use only if videos are the same
    showNest : display the nest polygon on matplotlib
    useCSV => Boolean : Use the .CSV outputted from maDLC.  
    drawNest => Boolean : Create a video with the estimated polygon nest drawn on the video. Outputted in video_With_Nest folder
    nestBorderThreshold : Threshold in pixel to consider a point inside the nest, and not in border of it
    """
    files =  glob.glob(str(videopath + '/*.mp4'))
    if useBackup : 
        with open( ROOT + '/models/nestDict.pkl', 'rb') as f:
            nestDict = pickle.load(f)    
    else:
        frameExtract(pathToVid=videopath, framePerVid = 20)
        nestDict = predictNest(detectorPath , str(videopath + "/frames"), visual = showNest )
    if not useCSV :
        inferenceMice(videopath)
    pathToOutput = str(os.path.dirname(videopath) + '/results')
    if not os.path.isdir(pathToOutput):
        os.makedirs(pathToOutput)
    destfolder = str(os.path.dirname(videopath) + '/csv')
    outputResults(pathToCSV = destfolder, pathToVideo=videopath, pathToOutput = pathToOutput, polyDic = nestDict, nestBorderThreshold = nestBorderThreshold, DLCThreshold = DLCThreshold)
    if drawNest :
        print('Drawing the nest detection on each video')
        for file in files:
            video = str(path.basename(path.normpath(file))).replace(".mp4","")
            try:
                dictIndex = nestDict["video"].index(video)
            except ValueError: 
                print(video)
                print("NO MATCHING VIDEO FOUND IN THE NEST DICT")
                continue
            try: 
                drawNestOnVid(file, nestDict["polygon"][dictIndex])
            except: 
                print('DRAWING ERROR')
                continue
        vidList = os.listdir(videopath)
        vidNest = str(os.path.dirname(videopath) + '/video_With_Nest')
        if not path.isdir(vidNest) :
            os.mkdir(vidNest)
        for vid in vidList:
            print(vid)
            if "NestDraw" in vid:
                shutil.move(os.path.join(videopath, vid), os.path.join(vidNest, vid))
    if drawDLCpred:
        print('Drawing the DLC detection on each video')
        showPred(videopath, pcutoff = DLCThreshold)