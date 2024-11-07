Installation
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

All done ! 

4. Install detectron2

.. code-block:: console

 python -m pip install git+https://github.com/facebookresearch/detectron2.git
