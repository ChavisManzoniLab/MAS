from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils import visualizer
import torch
import numpy as np
import cv2
import pycocotools.mask as mask
from pycocotools.coco import COCO
import os
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
import glob
from shapely import Polygon
import pandas as pd
import math as m
import numpy as np
from os import mkdir, path
import random
import glob
import stat
import shutil
from statistics import mean
import pickle 

min_area_threshold = 250


def frameExtract(pathToVid, framePerVid = 1):
    """Extract random frames for each video in pathToVid """
    pathToVideo = str(pathToVid+"\*.mp4")
     #Clear target output directory if needed
    output = glob.glob(str(pathToVid + "/frames/")) 
    try:
        for f in output:
                os.chmod(f, stat.S_IWRITE)
                shutil.rmtree(f)
    except:
        pass
    os.makedirs(str(pathToVid + "/frames/"), exist_ok = True)
    #Create a sub-directory for each video, containing extracted frames
    for video in glob.glob(pathToVideo):
        cap = cv2.VideoCapture(video)
        FileName = str(pathToVid + "/frames/" + str(path.basename(path.normpath(video)))).replace(".mp4","")
        totalframecount= int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        try:
            mkdir(FileName)
        except: 
            pass
        segment = (totalframecount-100) / framePerVid 
        for i in range(0,framePerVid) :
            frame_id = random.randint(round(segment*i), round(segment*(i+1))) #  /!\  :)
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
            ret, frame = cap.read()
            cv2.imwrite(FileName + "/Frame_" + str(i + 1) +".jpg", frame)
        cap.release()

def polygonFromMask(maskedArr):
  # stolen from https://github.com/hazirbas/coco-json-converter/blob/master/generate_coco_json.py
  """
  Change the binary mask to polygon COCO format
  """
  contours, _ = cv2.findContours(maskedArr, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  segmentation = []
  valid_poly = 0
  for contour in contours:
     if contour.size >= 6:
        segmentation.append(contour.astype(float).flatten().tolist())
        valid_poly += 1  
  if valid_poly == 0:
     raise ValueError
  return segmentation

def predictNest(detectorPath, image_dir, visual = False, NestSimplification = 5):

    """

    Run inference from Detectron2 to detect the nest from each picture in image_dir.

    —————————
    Arguments 
    —————————

    detectorPath : Path to the detector
    image_dir : Path to one or more image in .jpg
    visual : display the nest polygon on matplotlib
    NestSimplification : Strength of Polygon.simplify(), see shapely.Polygon

    ——————————————
    Returned value 
    ——————————————

    Results are outputted as a dictonnary containing : 
    dict["id"]
    dict["video"] containing the image path
    dict["confidence"] the confidence score of the detection
    dict["polygon"] the polygon of the nest after simplification
    dict["area"] the area of the polygon before simplification
    """
    cfg=get_cfg()
    cfg.merge_from_file(os.path.join(detectorPath,'config.yaml'))
    cfg.MODEL.WEIGHTS=os.path.join(detectorPath,'model_final.pth')
    cfg.MODEL.DEVICE='cuda' if torch.cuda.is_available() else 'cpu'
    #cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
    predictor=DefaultPredictor(cfg)                         
    #image_dir = str(image_dir+"\*.jpg")
    result = []
    results = {"id" : [], "video" : [], "confidence" : [], "polygon" : [], "area" : [], 'rawpolygon' : []}
    i = 0
    for folder in glob.glob(str(image_dir +"\*")):
        mask = []
        teste =  0
        for image in glob.glob(str(folder + "\*.jpg")):
            teste += 1
            print(teste)
            inputs = cv2.imread(image)
            result = predictor(inputs)
            
            for masknb, pred_mask in enumerate(result['instances'].pred_masks.cpu()) :
                print(result['instances'].scores.cpu().numpy()[masknb])
                area = cv2.countNonZero(pred_mask.numpy().astype("uint8"))
                if result['instances'].scores.cpu().numpy()[masknb] >= 0.8 and area >= min_area_threshold: 
                    mask.append(pred_mask.numpy().astype("uint8"))
                else: print("Ignored")

        if len(mask) != 1 and len(mask) != 0:
            for maskNb in range(1, len(mask)):
                mask[0] = np.add(mask[0], mask[maskNb])
            maskAv = np.rint(np.divide(mask[0],len(mask))).astype("uint8")
        elif len(mask) == 1:
            maskAv = mask[0]
        else : 
            results["confidence"].append(0)
            results["polygon"].append(0)
            results["area"].append(0)
            continue
        poly2 = []
        poly3 = []
        poly = polygonFromMask(maskAv) #Creation of average polygon
        xcoord = poly[0][0::2]
        ycoord = poly[0][1::2]
        for j in range(0,len(xcoord)):
            poly2.append([xcoord[j], ycoord[j]])
        polygon = Polygon(poly2)

        poly2 = []
        poly = polygonFromMask(mask[len(mask)-1]) #Last polygon for comparison
        xcoord = poly[0][0::2]
        ycoord = poly[0][1::2]
        for j in range(0,len(xcoord)):
            poly3.append([xcoord[j], ycoord[j]])
        polygon2 = Polygon(poly3)

        polygon3 = (polygon.simplify(NestSimplification))
        if visual == True:
            test = plt.imread(image)
            plt.imshow(test)
            plt.plot(*polygon.exterior.xy, color = "green")
            plt.plot(*polygon2.exterior.xy, color = "red")
            #plt.plot(*polygon3.exterior.xy, color = "blue")
            plt.text(30,-30, s = str("Green estimation is an average of " + str(len(mask)) + " detections"),  fontsize =12)
            #plt.text(30,-10, s = str("Blue estimation is an simplification of  green"),  fontsize =12)
            plt.show()

        results["id"].append(i)
        results["video"].append(str(folder))
        try:
            results["confidence"].append(result['instances'].scores.cpu().numpy()[0])
            results["polygon"].append(polygon)
            results["area"].append(polygon.area)
            results["rawpolygon"].append(polygon2)
        
        except:
            results["confidence"].append(0)
            results["polygon"].append(0)
            results["area"].append(0)
        
        i += 1 
    
    filename = r'C:\Users\bs\Mas\backup'
    os.makedirs(str(filename), exist_ok=True)
    with open(filename+ '\\nestDict.pkl', 'wb') as f:
        pickle.dump(results, f)
    return results

