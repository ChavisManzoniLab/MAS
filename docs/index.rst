MAS-PRT
===================================
**Machine-Automated Scoring of Pup Retrieval Test**
------------------------------------


MAS is a pipeline designed to score automatically the Pup Retrieval Test. It computes automatically multiple variables, including : 

- Time to first encounter
- Time to retrieve the pup
- Distance
- Size of the Nest

More information in *DOI*

To work, MAS uses a `DeepLabCut <http://www.mackenziemathislab.org/deeplabcut>`_ detection of both the pup and the dam, and an automated detection of the nest using `Detectron2 <https://github.com/facebookresearch/detectron2?tab=readme-ov-file#learn-more-about-detectron2>`_

Summary
------------------

.. toctree::

  install on CPU
  install on GPU
  usage
  model
  troubleshooting
