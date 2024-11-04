import os


#Setup
FIRST_START = 1
ROOT = os.path.dirname(__file__)

#Model path
DLCDETECTOR = os.path.join(ROOT, r'Models\PRT-Benj-2024-01-30\config.yaml')
NESTDETECTOR = os.path.join(ROOT, r'Models\Nest10')

#Misc
DAMSIZECM = 8.5
MIN_AREA_THRESHOLD = 250
NEST_BORDER_THRESHOLD = 10
DLC_THRESHOLD = 0.7