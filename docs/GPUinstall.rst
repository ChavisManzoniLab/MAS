Installation for GPU
=================

Install Git : https://git-scm.com/downloads 

Install Visual Studio C++ : `Visual Studio <https://visualstudio.microsoft.com/fr/thank-you-downloading-visual-studio/?sku=Community&channel=Release&version=VS2022&source=VSFeaturesPage&passive=true&tailored=cplus&cid=2031#cplusplus>`_

.. image:: https://i.imgur.com/deCNAyX.png
  :width: 800

Install Python x64 3.9 https://www.python.org/downloads/release/python-3913/ (INSTALL x64)

.. _code_directive:

.. figure:: https://i.imgur.com/8pWVNwr.png
   
    When installing Python, check the "Add Python to PATH"

| Open the terminal 
| In the terminal => 

1. Create an environnement using venv command in python. 

.. code-block:: console

 mypythonpath -m venv MAS

.. warning:: 
   Do not write mypythonpath, but link but your python 3.9.XX executable instead

   *By default, mypythonpath should be here : C:/Users/Your user name/AppData/Local/Programs/Python/Python39/python*

2. Activate the environnement you just created :

.. code-block:: console

 cd MAS
 scripts\activate
 
3. Install the packages 

.. code-block:: console

 pip install git+https://github.com/ChavisManzoniLab/MAS.git

4. Install detectron2

.. code-block:: console

 python -m pip install git+https://github.com/facebookresearch/detectron2.git

5. Install CUDA

| A GPU is highly recommanded to speed up the analysis. To make use of the analysis with GPU, CUDA must be installed on your machine. 
| I recommand trying with Cuda 11 at first
| https://developer.nvidia.com/cuda-11-8-0-download-archive
| 

.. figure:: https://i.imgur.com/IRh68fu.png
   :width: 500
   This message might appear, just ignore it 

.. note:: 
  Beware, Cuda version may be dependent of your GPU


6. Install the good version of Torch 

See https://pytorch.org/get-started/locally/ to find the version that suit your CUDA

.. code-block:: console

 pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 

7. Install Cudnn

Go to https://developer.nvidia.com/rdp/cudnn-archive

.. image:: https://i.imgur.com/k8PAL0g.jpeg
   :width: 700

| Select this version

