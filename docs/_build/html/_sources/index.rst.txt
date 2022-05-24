py2lispIDyOM: A Python package for IDyOM
========================================

py2lispIDyOM is a Python package for the information dynamics of music (`IDyOM model <https://github.com/mtpearce/idyom/>`__).

Table of contents
-----------------

-  `Getting Started <#getting-started>`__

   -  `Prerequisite <#prerequisite>`__
   -  `Installing <#installing>`__

-  `Functionality and Usage <#functionality-and-usage>`__


Getting Started
---------------

Prerequisite
~~~~~~~~~~~~

py2lispIDyOM requires IDyOM to be installed on the local machine. To start with, please read
the `IDyOM installation page <https://github.com/mtpearce/idyom/wiki/Installation/>`__ to appropriately install IDyOM.

In addition, py2lispIDyOM also requires common packages such as `numpy`, `matplotlib`, `pandas`, `scipy`, etc.

Installing
~~~~~~~~~~
The code is compatible with >=Python 3.8.

To use py2lispIDyOM, you can download this repo or use git clone.

Functionality and Usage
-----------------------
In summary, py2lispIDyOM has three main functionalities for research workflow:

- Running the IDyOM
- Data preprocessing (extracting and exporting data)
- Visualizing IDyOM outputs

Please have a look at the `tutorial folder <tutorial/>`__, which guides you through all three basic functionalities of through an
example.

Note: I tried to make the code accessible and provide some examples in the tutorials for getting started smoothly. But
there is still lots of room for better documentation and testing. Please contact me if you have any questions or
encounter bugs!




.. toctree::
   :maxdepth: 1
   :caption: Package modules:

   run
   extract
   export
   viz


.. Indices and tables
.. ==================

.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`
