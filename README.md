# MAS-PRT

Machine-automated scoring of Pup retrieval test

Mas is a pipeline allowing for an automatic scoring of pup retrieval test. It computes automatically multiple variables, including 

- Time to first encounter
- Time to retrieve the pup
- Distance
- Size of the Nest

More information in *DOI*

To work, Mas utilize a DeepLabCut detection of both the pup and the dam, and an automated detection of the Nest using Detectron2

# Installation

I suggest installing python 3.9 https://www.python.org/downloads/release/python-3913/ (I didn't try with other version, feel free to try)
creating an environnement using venv command in python. 

`mypythonpath -m venv /path/to/new/virtual/environment`

**Do not write mypythonpath, but link but your python 3.9.XX executable instead**

`pip install MasPRT`

A GPU is highly recommanded to speed up the analysis. To make use of the analysis with GPU, CUDA must be installed on your machine. 
Beware, Cuda version will be dependent of your GPU

# Use 

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

