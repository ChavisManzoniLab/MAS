MAS GUI (Graphical User Interface)
==============

To open the environment, use

.. code-block:: console

  cd MAS\\scripts\\activate

Once you are in the environment, you can launch the GUI by writing :

.. code-block:: console

  python -m MAS

The interface should open. No more geek stuff for you 🥳

Functionality
**************

.. _code_directive:

.. image:: https://i.imgur.com/omAEHU3.jpeg

| Here is the MAS GUI
| Every functionality offered by the MAS GUI are described below

Main
-----------
1. Select folder
  | Click on the grey button to select a folder where .MP4 of PRT videos. 
  | The GUI will write down the path
  | The GUI will also write down the number of detected videos. 
  | Nested folder are not taken in account

9. RUN
  | Launch the pipeline on selected video.
  | The process can be long, especially with numerous videos or absence of a GPU
  | The result will be outputted as shown in `Arborescence <https://mas.readthedocs.io/en/latest/usage.html#id4>`_

Usage of anterior inferences
-----------------------------

| In the case where videos where already analyzed once, MAS stores the inferences.
| It can be a gain of time in many cases : Tweaking the configs, creating vizualisations on parts of the videos...

2. Use stored nest 
  | Use stored nest will read the .pickle file containing a dictionary of videos and nest detection
  | The Detectron2 inference will not be done again. 
  | Will return an error if any video does not match the stored information

3. Use stored DLC prediction
  | Use stored CSV outputted by the DLC inference. 
  | The DLC inference will not be done again
  | Will return an error if any video does not match the stored information

Inferences config
-----------------------

4. DLC point likelihood
  | Choose the threshold for an acceptable DLC detection.
  | Every point with a likelihood inferior to the selected value will be trashed for the analysis
  | Range : 0-1

5. Non-border pixel threshold
  | Choose the pixel threshold before considering an Animal inside the nest
  | Useful for animal staying at the border of the nest for longer periods.
  | Range : ≥0

Visualization
---------------

6. Create video with Nest
  | If selected, will draw the infered nest on each video.
  | Results are saved in video_With_Nest, see `Arborescence <https://mas.readthedocs.io/en/latest/usage.html#id4>`_
  | Results will be outputted as .mp4 videos

.. image:: https://i.imgur.com/JzdKvP2.jpeg
   :width: 600

7. Show Nest prediction
  | If selected, will draw the infered nest on an image for each video
  | Results are saved in NestImage, see `Arborescence <https://mas.readthedocs.io/en/latest/usage.html#id4>`_

8. Show DeepLabCut prediction on video
  | If selected, will draw the infered DLC detection on each video
  | Results are saved in DLCTracking, see `Arborescence <https://mas.readthedocs.io/en/latest/usage.html#id4>`_

.. image:: https://i.imgur.com/GObPK5s.jpeg
   :width: 600

.. note::
   Dam will be labeled in purple 

   Pup will be labeled in red

   Useful to spot bad detection


Arborescence
**************

.. code-block:: console

 ParentFolder
 ├───csv             => CSV extraction from DLC
 ├───DLCTracking     => Video with DLC detection (8)
 ├───results         => CSV of results 
 ├───video_With_Nest => Video with Nest polygon detection (6)
 └───VidFolder       => Folder of the video (selected in 1)
    ├───frames       => Frames extracted for the nest detection
    ├───Models       => Store the .pickle of the nest detection
    ├───Video1.MP4
    └───NestImage    => Picture of the nest detection (7)

