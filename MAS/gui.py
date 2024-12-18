import tkinter as tk
from tkinter import  *
from tkinter import filedialog
import glob
from MAS.functions import *
import tkinter.ttk
from MAS.inferenceMice import *
import time
path = ' '

def GUI():
    def validate_float(var, min, max):
        new_value = var.get()
        try:
            new_value == '' or float(new_value)
            flnew_value = float(new_value)
            if flnew_value < min or flnew_value >max:
                raise
            validate_float.old_value = new_value

        except:
            var.set(validate_float.old_value)


    def browseFiles():
        global path
        path = filedialog.askdirectory(title = "Select a folder")
        vidlist = glob.glob(path + '/*.mp4')
        if len(vidlist) != 1:
            nicetext =  ' videos found'
        else:
            nicetext = ' video found'
        pathway['text'] = path + "\n" + '——————'+ "\n" + str(len(vidlist)) + nicetext

    def launch_analyze(pathway):
        start_time = time.time()
        print('STARTING')
        print(pathway) 
        use_backup = storedNest.get()
        use_CSV = storedCSV.get()
        visual = showNestPred.get()
        draw_pred = drawDLConVid.get()
        draw_nest_pred = drawNest.get()
        try:
            new_nest_threshold = float(Nestthreshold.get())
            new_DLC_threshold = float(threshold.get())
        except:
            print("WRONG ENTRY")
            window.quit
        if not glob.glob(pathway + '/*.mp4'):
            quit()
        PRTAnalysis(video_path = pathway , use_backup=use_backup, show_nest = visual, use_CSV = use_CSV, draw_DLC_pred = draw_pred,
                    nest_border_threshold = new_nest_threshold, DLC_threshold = new_DLC_threshold , draw_nest = draw_nest_pred) 
        print("--- %s seconds ---" % (time.time() - start_time))

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


    storedNest = tk.BooleanVar()
    storedCSV = tk.BooleanVar()

    tk.ttk.Separator(master = window, orient = HORIZONTAL).grid(column = 0, row = 2 , columnspan=100, sticky="ew" )
    storedText = tk.Label( master = window,text="Use anterior inferences :")
    storedText.grid(row = 3, column = 0)
    Checkbutton(master = window, text="Use stored nest", variable=storedNest).grid(row=4, column = 0, sticky=W)
    Checkbutton(master = window, text="Use stored DLC prediction", variable=storedCSV).grid(row=4, column = 1, sticky=W)
    tk.ttk.Separator(master = window, orient = HORIZONTAL).grid(column = 0, row = 5 , columnspan=100, sticky="ew" )

    pipeLine_Config = tk.Label( master = window,text="Inferences Config :").grid(row = 6)
    likelihoodText = tk.Label( master = window,text="DLC point Likelihood").grid(row = 7, column =0 )
    threshold = StringVar()
    threshold.trace('w', lambda nm, idx, mode, var=threshold: validate_float(var, 0 , 1)) 
    threshold.set(0.7)
    likelihoodTh = tk.Entry(master = window ,textvariable=threshold).grid(row = 7, column = 1 ,padx = 1, pady = 4, )

    likelihoodText = tk.Label( master = window,text="Nest border Threshold (in Pixel)").grid(row = 8, column =0 )
    Nestthreshold = StringVar()
    Nestthreshold.trace('w', lambda nm, idx, mode, var=Nestthreshold: validate_float(var, 0 , 10000))
    Nestthreshold.set(10)
    likelihoodTh = tk.Entry(master = window ,textvariable=Nestthreshold).grid(row = 8, column = 1,  padx = 1, pady = 4, )
    tk.ttk.Separator(master = window, orient = HORIZONTAL).grid(column = 0, row = 9 , columnspan=100, sticky="ew" )


    storedText = tk.Label( master = window,text="Visualization :")
    storedText.grid(row = 15, column = 0)

    showNestPred = tk.BooleanVar()
    Checkbutton(master = window, text="Show nest prediction (slow)", variable=showNestPred).grid(row=16, column = 1, sticky=W)

    drawNest = tk.BooleanVar()
    Checkbutton(master = window, text="Create video with Nest (VERY slow)", variable=drawNest).grid(row=16, column = 0, sticky=W)

    drawDLConVid = tk.BooleanVar()
    Checkbutton(master = window, text="Show DeepLabCut prediction on video (VERY slow)", variable=drawDLConVid).grid(row=17, column = 0, sticky=W)

    tk.ttk.Separator(master = window, orient = HORIZONTAL).grid(column = 0, row = 30 , columnspan=100, sticky="ew" )

    buttonAnalyze = tk.Button( master = window, text="RUN", width=20,
        height=3, bg="limegreen", fg="black", command = lambda: launch_analyze(path) )
    buttonAnalyze.grid(row = 31, column = 0, padx = 1, pady = 1)

    Button(master = window, text='Quit', command=window.quit).grid(row=32, column = 1, pady=4)

    window.mainloop()