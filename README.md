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

To train another Detectron2 model, I would strongly suggest to use the method offered by LabGym. 

https://github.com/umyelab/LabGym?tab=readme-ov-file#2-use-trained-detectors

2 frames should be enough, depending on the quantity of video you have
Once your model is satistying, you should modify the detectorPath accordingly with yours. 

Now that you have LabGym on your computer, feel free to try it out ! 
It's a formidable tool for quantifying behavior on videos :)

