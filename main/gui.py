import tkinter as tk
from tkinter import  *
from tkinter import filedialog
import glob
from functions import *

path = 'No path selected'

outpath = r'C:\Users\bs\Desktop\zad\mdr2.mp4'
pathTobox = r'C:\Users\bs\Desktop\zad\vido\2023-06-05 C4 T4 Masdig.mp4'
pathToVid = r'C:\Users\bs\Desktop\zad\vidNew'
detectorPath = r"C:\Users\bs\LabGym\Lib\site-packages\LabGym\detectors\Nest10"
pathToCSV = r'C:\Users\bs\Desktop\zad/csv1'
pathToOuput = r'C:\Users\bs\Desktop\zad/output/'


def browseFiles():
    global path
    path = filedialog.askdirectory(title = "Select a folder")
    vidlist = glob.glob(path + '/*.mp4')
    if len(vidlist) != 1:
       nicetext =  ' videos found'
    else:
        nicetext = ' video found'
    pathway['text'] = path + "\n" + '——————'+ "\n" + str(len(vidlist)) + nicetext

def launchAnalyze(pathway):
    print(pathway) 
    useBackup = storedNest.get()
    visual = showPred.get()
    if not glob.glob(pathway + '/*.mp4'):
        quit()
    try:
        PRTAnalysis(pathToVid = pathway , detectorPath = detectorPath, pathToCSV = pathToCSV, pathToOuput = pathToOuput, useBackup=useBackup, visual = visual) 
    except:
        print("WRONG PATH")

window = tk.Tk()
window.title('WELCOME TO MAS')
window.resizable(width=False, height=False)



buttonpath = tk.Button(
    master = window,
    text= "Click here to select " + "\n" + "the folder of the videos",
    width=20,
    height=3,
    bg="grey",
    fg="black",
    command = browseFiles
    )
buttonpath.grid(row = 0, column = 0,  padx = 1, pady = 2, )

pathway = tk.Label( master = window,text=path)

pathway.grid(row = 0, column = 1)

pathway = tk.Label( master = window,text=path)

pathway.grid(row = 0, column = 1)



button = tk.Button(
    master = window,
    text="Launch Analysis",
    width=20,
    height=3,
    bg="limegreen",
    fg="black",
    command = lambda: launchAnalyze(path)
)

button.grid(row = 4, column = 0, padx = 1, pady = 1)

storedNest = tk.BooleanVar()
showPred = tk.BooleanVar()
drawNest = tk.BooleanVar()

Checkbutton(master = window, text="Use stored nest", variable=storedNest).grid(row=2, column = 0, sticky=W)
Checkbutton(master = window, text="Show nest prediction (SLOW)", variable=showPred).grid(row=2, column = 1, sticky=W)
Checkbutton(master = window, text="Draw nest on each analyzed video", variable=drawNest).grid(row=3, column = 0, sticky=W)


Button(master = window, text='Quit', command=window.quit).grid(row=5, column = 1, pady=4)

window.mainloop()

