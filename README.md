# py2lispIDyOM: A Python interface for IDyOM

py2lispIDyOM is a Python package for the information dynamics of music ([IDyOM](https://github.com/mtpearce/idyom/))
model.

## Get Started

### Prerequisites

To start with, please read the [IDyOM installation page](https://github.com/mtpearce/idyom/wiki/Installation) to
appropriately install IDyOM on your local machine.

### Installation

Note you can also download this repo as an alternative to git clone.

## Functionality and Usage Overivew

In summary, py2lispIDyOM has four main functionalities for research workflow.

See the following tutorials for more detailed information about the three main functionalities:

- [Run IDyOM tutorial](tutorials/runIDyOM_tutorial.md)
- [Extract and export tutorial](tutorials/extract_export_tutorial.md)
- [Visualization tutorial](tutorials/visualization_tutorial.md)

See also the [examples](examples/) for more info.

### 1. Run IDyOM

To run the IDyOM model with py2lispIDyOM takes three steps:

1) Set experiment configuration (paths to input music files and to output experiment log)
2) Set model configuration (model parameters, see ... for more detail)
3) run the experiment.

### 2. Extract and export the data

IDyOM writes the outputs of the modelling to a `.dat` file (with space-separated values). This file can be read in
MATLAB, R and other software for further analysis.

py2lispIDyOM also provides methods to extract certain (single or multiple) IDyOM outputs (for analysis in python)
and export them in different formats.

For more information about the IDyOM outputs, see [IDyOM Output](https://github.com/mtpearce/idyom/wiki/IDyOM-Output).

### 3. Visualizing IDyOM data.

## About the Experiment Logger:

An experiment log folder (with the timestamp as the folder name) will be automatically created the record all data in
the current experiment in the `experiment_history/` folder
(by default, unless the users specify another path in the `experiment_history_folder_path` argument when initializing
the `IDyOMExperiment`).

This experiment log folder is structured in a way that can help researchers stay organized. It's also intended to record
all experiment data and contains all necessary data and scripts of the experiment that can be shared to
reproduce/replicate the experiment results.

The structure of the experiment log folder follows the example below:

```
experiment_history
└── 16-05-22_14.01.03
    ├── experiment_input_data_folder
    │   ├── pretrain_dataset
    │   │   ├── shanx003.mid
    │   │   │      ...
    │   │   └── shanx008.mid
    │   └── test_dataset
    │       ├── chor-008.mid
    │       │      ...
    │       └── chor-003.mid
    ├── experiment_output_data_folder
    │   └── 66051622140103-cpitch_onset-cpitch_onset-99051622140103-nil-melody-nil-1-both-nil-t-nil-c-nil-t-t-x-3.dat
    ├── outputs_in_csv
    │   ├── chor-007.csv
    │   │       ...
    │   └── chor-009.csv
    ├── compute.lisp
    ├── outputs_in_mat
    │   ├── information.content.mat
    │   │       ...
    │   └── chor001_melody_name.mat
    └── plots
        ├── simple_plot_information.content
        │   └── chor-003.png
        ├── pianoroll_groundtruth_surprisal
        │   └── chor-010.png
        ├── simple_plot_onset.entropy
        │   └── chor-001.png
        └── pianoroll_pitch_prediction_groundtruth
            └── chor-008.png
    
```