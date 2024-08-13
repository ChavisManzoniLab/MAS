# MAS-PRT

Machine-automated scoring of Pup retrieval test

Mas is a pipeline allowing for an automatic scoring of pup retrieval test. It computes automatically multiple variables, including 

- Time to first encounter
- Time to retrieve the pup
- Distance
- Size of the Nest

More information in *DOI*

To work, Mas utilize a DeepLabCut detection of both the pup and the dam, and an automated detection of the Nest using Detectron2

# Suggested Installation

I suggest installing python 3.9 https://www.python.org/downloads/release/python-3913/ (I didn't try with other version, feel free to try)\
Create an environnement using venv command in python. 

`mypythonpath -m venv /path/to/new/virtual/environment`

**Do not write mypythonpath, but link but your python 3.9.XX executable instead**

`pip install MasPRT`\
`python -m pip install torch==2.0.1+cu118 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118` \
**/!\ THE ONE ABOVE MAY VARY DEPENDING ON YOUR GPU** \
`python -m pip install git+https://github.com/facebookresearch/detectron2.git` 



A GPU is highly recommanded to speed up the analysis. To make use of the analysis with GPU, CUDA must be installed on your machine. \
Beware, Cuda version will be dependent of your GPU

# Use 

## I wish to use provided data 

To open the environnment, use 

`cd MYENVIRONNEMENTPATH`\
`scripts\activate`

Once you are in the environnment, you can launch the GUI by writing :

`cd main`\
`python -m gui.py`

The interface should open
No more geek stuff for you 🥳

## I wish to use my data with the base models

Use the provided script and link to your folder. 

## I wish to use my data and changes the models

The analysis is using 2 differents inferences : 

One multianimal DeepLabCut model detecting the pup and the dam. \
One Detectron2 model detecting the nest. 

### Change maDeepLabcut model

To change the maDeepLabCut model, I highly encourage to follow my tutorial to not recode my entire pipeline. 
<details>
  **<summary> Expand by clicking on the arrow to see the tutorial </summary>**
  
  First, Create a new maDeepLabCut project 
  
  ![NewProject](https://github.com/user-attachments/assets/e0a40bd6-364e-4307-9a73-c4a921ce16aa)

  Open the config.yaml with any text editor. It should look like this
  ![Yaml](https://github.com/user-attachments/assets/149162f3-ddec-4df1-918c-5cebbd0dd02f)

  Now, delete everything below the red line. \
  Copy and paste the layout.yaml located in main/DLC/Layout into your config.yaml\
  /!\ Do not erase the first part, before the red line

  Now, you can extract some frames, and try to start label frame.

  IF your manipulation was good, the keypoint selection in Napari (down right) should look like the picture  
  ![Success](https://github.com/user-attachments/assets/826ed7f4-d582-4940-bbb8-21c60e8e715c)

  
  This is how I label my frames.\
  Dam is the dam\
  single is the pup\
  The point names are self-explanatory, see image below. 
  ![image](https://github.com/user-attachments/assets/60d822fa-b52d-49e4-9b2c-7a3776c0e1d2)
  ![image](https://github.com/user-attachments/assets/5091cffd-0e47-4c6d-8cc6-ccf81732f8e0)
  ![image](https://github.com/user-attachments/assets/c349c316-2b01-49af-b9f0-47eb65d51e2b)

  (Don't be afraid if you have differents colors than me, It changes)
  
  Now, it's up to you! Happy training !\
  See how to train a maDLC model : https://deeplabcut.github.io/DeepLabCut/docs/maDLC_UserGuide.html\
  Once the model is satisfying, the new DLC model must be referenced in the code. 

  
</details>



### Change Detectron2 Nest detection model

To train another Detectron2 model, I would strongly suggest to use the method offered by LabGym. 

https://github.com/umyelab/LabGym?tab=readme-ov-file#2-use-trained-detectors

2 frames should be enough, depending on the quantity of video you have\
Once your model is satistying, you should modify the detectorPath accordingly with yours. 

Now that you have LabGym on your computer, feel free to try it out ! \
It's a formidable tool for quantifying behavior on videos :)

