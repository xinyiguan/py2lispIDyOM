# py2lispIDyOM: A Python package for IDyOM

![build](https://github.com/xinyiguan/py2lispIDyOM/workflows/build/badge.svg)
![tests](https://github.com/xinyiguan/py2lispIDyOM/workflows/tests/badge.svg)
[![docs](https://github.com/xinyiguan/py2lispIDyOM/actions/workflows/docs.yml/badge.svg)](https://xinyiguan.github.io/py2lispIDyOM/)

[![DOI](https://zenodo.org/badge/313182306.svg)](https://zenodo.org/badge/latestdoi/313182306)
[![PyPI version](https://badge.fury.io/py/py2lispIDyOM.svg)](https://badge.fury.io/py/py2lispIDyOM)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


py2lispIDyOM is a Python package for the information dynamics of music ([IDyOM](https://github.com/mtpearce/idyom/))
model.

## Table of Content

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installing](#installing)


- [Functionality and Usage](#functionality-and-usage)

---

## Getting Started

### Prerequisites

py2lispIDyOM requires IDyOM to be installed on the local machine. To start with, please read
the [IDyOM installation page](https://github.com/mtpearce/idyom/wiki/Installation) to appropriately install IDyOM.

In addition, py2lispIDyOM also requires common packages such as `numpy`, `matplotlib`, `pandas`, `scipy`, etc.

### Installing

The code is compatible with >=Python 3.9.

It can be installed using pip or directly from the source code. 
Basic installation options include:

- From PyPI using pip: `pip install py2lispIDyOM`
- Download or gitclone this repository

## Functionality and Usage

In summary, py2lispIDyOM has three main functionalities for research workflow:

- Running the IDyOM
- Data preprocessing
- Visualizing IDyOM outputs

Please have a look at the [tutorial](tutorials/), which guides you through all three basic functionalities of through an
example.

### Notebook examples

- Running the IDyOM model: [1_running_IDyOM_tutorial.ipynb](tutorials/1_running_IDyOM_tutorial.ipynb)
- Data preprocessing: 
  - Extracting data: [2a_data_preprocessing_extracting.ipynb](tutorials/2a_data_preprocessing_extracting.ipynb)
  - Exporting data: [2b_data_preprocessing_exporting.ipynb](tutorials/2b_data_preprocessing_exporting.ipynb)
- Visualization: [3_visualizing_outputs.ipynb](tutorials/3_visualizing_outputs.ipynb)

Note: I tried to make the code accessible and provide some examples in the tutorials for getting started smoothly. But
there is still lots of room for better documentation, tutorials and testing. Please contact me if you have any questions or
encounter bugs!

