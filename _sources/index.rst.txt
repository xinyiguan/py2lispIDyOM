py2lispIDyOM: A Python package for IDyOM
========================================

A Python package for the information dynamics of music (`IDyOM <https://github.com/mtpearce/idyom/>`__) model.


Table of contents
-----------------
-  `Introduction <#introduction>`__
-  `Getting Started <#getting-started>`__

   -  `Prerequisite <#prerequisite>`__
   -  `Installing <#installing>`__

-  `Functionality and Usage <#functionality-and-usage>`__

   -  `Basic functionalities <#basic-functionalities>`__
   -  `Notebook examples <#notebook-examples>`__
   -  `Important notes <#important-notes>`__



Introduction
------------
`py2lispIDyOM` is an open-source Python package broadly aimed at researchers conducting IDyOM-based analysis in Python.
It serves as a unifying Python interface that simplifies and streamlines the research workflow for running the
information dynamics of music (`IDyOM <https://github.com/mtpearce/idyom/>`__) model and analyzing output data.
This package makes it easier to do the following two tasks: (i) configuring and running the IDyOM model,
and (ii) processing and analyzing the IDyOM output data.

Getting Started
---------------

Prerequisite
~~~~~~~~~~~~

py2lispIDyOM requires IDyOM to be installed on the local machine. To start with, please read
the (`IDyOM installation page <https://github.com/mtpearce/idyom/wiki/Installation>`__) to appropriately install IDyOM.


Installing
~~~~~~~~~~
The code is compatible with >= Python 3.9.

It can be installed using pip: ``pip install py2lispIDyOM``


Functionality and Usage
-----------------------

Basic functionalities
~~~~~~~~~~~~~~~~~~~

In summary, py2lispIDyOM has three main functionalities for research workflow:

- Running the IDyOM
- Data preprocessing (extract and export)
- Visualizing IDyOM outputs

Please have a look at the (`tutorials <https://github.com/xinyiguan/py2lispIDyOM/tree/master/tutorials/>`__),
which guides you through all three basic functionalities of through examples.


Notebook examples
~~~~~~~~~~~~~~~~~~~
- Running the IDyOM model: (`1_running_IDyOM_tutorial.ipynb <https://github.com/xinyiguan/py2lispIDyOM/blob/master/tutorials/1_running_IDyOM_tutorial.ipynb>`__)

- Data preprocessing:

  - Extracting data: (`2a_data_preprocessing_extracting.ipynb <https://github.com/xinyiguan/py2lispIDyOM/blob/master/tutorials/2a_data_preprocessing_extracting.ipynb>`__)
  - Exporting data: (`2b_data_preprocessing_exporting.ipynb <https://github.com/xinyiguan/py2lispIDyOM/blob/master/tutorials/2b_data_preprocessing_exporting.ipynb>`__)

- Visualization: (`3_visualizing_outputs.ipynb <https://github.com/xinyiguan/py2lispIDyOM/blob/master/tutorials/3_visualizing_outputs.ipynb>`__)



Important notes
~~~~~~~~~~~~~~~~~~~

To encourage an organized workflow and to improve the reproducibility of data, all data related to an experiment (used and produced)
will be logged in a structured folder, which can be shared with other researchers. A sample of the structured
experiment logger will look like:

::

    experiment_history
    └── 21-05-22_17.05.05
        ├── experiment_input_data_folder
        │   ├── pretrain_dataset
        │   └── test_dataset
        ├── experiment_output_data_folder
        │   └── 66052122170523-cpitch_onset-cpitch_onset-99052122170523-nil-melody-nil-1-both-nil-t-nil-c-nil-t-t-x-3.dat
        ├── outputs_in_csv
        │   └── chor-005.csv
        ├── compute.lisp
        ├── outputs_in_mat
        │   ├── information_content.mat
        │   └── chor001_onset.mat
        └── plots
            ├── surprisals_plots
            ├── entropy_plots
            └── pianoroll_pitch_prediction_groundtruth


I tried to make the code accessible and provide some examples in the tutorials for getting started smoothly.
But there is still lots of room for better documentation, tutorials and testing.
Please contact me if you have any questions or encounter bugs!


Developer's Guide
-----------------

.. toctree::
   :maxdepth: 1

   api_reference
   tutorials
   how_to_contribute
   LICENSE





