MAS-PRT
===================================
**Machine-automated scoring of Pup retrieval test**
------------------------------------


MAS is a pipeline allowing for an automatic scoring of pup retrieval test. It computes automatically multiple variables, including 

- Time to first encounter
- Time to retrieve the pup
- Distance
- Size of the Nest

More information in *DOI*

To work, MAS utilize a `DeepLabCut <http://www.mackenziemathislab.org/deeplabcut>`_ detection of both the pup and the dam, and an automated detection of the Nest using `Detectron2 <https://github.com/facebookresearch/detectron2?tab=readme-ov-file#learn-more-about-detectron2>`_

Summary
------------------

.. toctree::

  install
  usage
  model
