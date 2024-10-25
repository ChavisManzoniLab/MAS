Launch MAS GUI
==============

To open the environment, use

.. code-block:: console

  cd MAS\\scripts\\activate

Once you are in the environment, you can launch the GUI by writing :

.. code-block:: console

  python -m MAS

The interface should open No more geek stuff for you 🥳

Functionality
==============

.. _code_directive:

.. image:: https://i.imgur.com/omAEHU3.jpeg

| Here is the MAS GUI
| I'll present every functionality offered by the MAS GUI

Main Part
-----------
1. Select folder
  | Click on the grey button to select a folder where .MP4 of PRT videos. 
  | The GUI will write down the path
  | The GUI will also write down the number of detected videos. 
  | Nested folder are not taken in account

9. RUN
  | Launch the pipeline on selected video.
  | The process can be long, especially with numerous videos or absence of a GPU
  | The result will be outputted as follow :

.. code-block:: console

 ParentFolder
 ├───csv             => CSV extraction from DLC
 ├───DLCTracking     => Video with DLC detection
 ├───results         => CSV of results
 ├───video_With_Nest => Video with Nest polygon detection
 └───VidFolder       => Folder of the video
    ├───frames       => Frames extracted for the Nest detection
    ├───Video1.MP4
    └───NestImage    => Picture of Nest detection

Usage of anterior inferences
-----------------------------

| In the case where videos where already analyzed once, MAS stores the inferences.
| It can be a gain of time in many cases : Tweaking the configs, Creating vizualitions on some videos...

2. Use stored nest 
  | Use stored nest will read the .pickle file containing a dictionary of videos and nest detection
  | The Detectron2 inference will not be done again. 
  | Will return an error if any video does not match the dict

3. Use stored DLC prediction
  | Use stored CSV outputted by the DLC inference. 
  | The DLC inference will not be done again
  | Will return an error if any video does not match the dict

Inferences config
-----------------------

4. DLC point likelihood
  | Choose the threshold for an acceptable DLC detection.
  | Every point with a likelihood inferior to the selected value will be trashed for the analysis

5. Nest border Threshold
  | Choose the pixel threshold before considering an Animal inside the nest
  | Useful for animal staying at the border of the nest for long periods.

Visualization
---------------

6. Create video with Nest
  | If selected, will draw the infered nest on each video.
  | Result are saved in a folder called video_With_Nest in the same folder where the folder selected in 1. is
  | Result will be outputted as .mp4 videos

7. Show Nest prediction
  | If selected, will draw the infered nest on an image for each videos
  | Results are saved in a folder called NestImage, located with the videos

8. Show DeepLabCut prediction on video
  | If selected, will draw the infered DLC detection on each video
  | Result are saved in a folder called DLCTracking in the same folder where the folder selected in 1. is
  | Dam is in purple
  | Pup is in red
  | Useful to spot bad detection

