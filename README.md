# MAS

# Installation

pip install truc ?

# Utilization 

## I wish to use provided data 

Use the script XXXX.py and link to your folder

## I wish to use my data with the base models

Use the provided script and link to your folder. 

## I wish to use my data and changes the models

The analysis is using 2 differents inferences : 

One multianimal DeepLabCut model detecting the pup and the dam. 
One Detectron2 model detecting the nest. 

### Change maDeepLabcut model

Use the provided layout to train another maDeepLabCut model from scratch. 
How to train a maDLC model : https://deeplabcut.github.io/DeepLabCut/docs/maDLC_UserGuide.html
Once the model is satisfying, the new DLC model must be referenced in the code. 

### Change Detectron2 Nest detection model

Extract some frame from videos
Use Roboflow to label the nest, then retrieve .coco format (I NEED TO WRITE MORE ON THAT)
Train the detectron2 model using script.py
Once the nest is satisfactory, the new nest inference must be referenced in the code. 

