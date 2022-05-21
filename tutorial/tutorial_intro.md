# py2lispIDyOM Tutorial

In this tutorial folder, I will walk through a sample IDyOM experiment using py2lispIDyOM to demonstrate the
functionalities of the package. For an overview of the py2lispIDyOM functionality, see the [README](README.md), and also
more [examples](examples/) on each functionality.

You will find 4 separate tutorials for each functionality.

### 1. Run IDyOM

To run the IDyOM model with py2lispIDyOM takes three steps:

1) Set experiment configuration (paths to input music files and to output experiment log)
2) Set model configuration (model parameters,
   see  [IDyOM parameters documentation](https://github.com/mtpearce/idyom/wiki/IDyOM-Parameters) for more detail)
3) run the experiment.

### 2. Extract and export the data

IDyOM writes the outputs of the modelling to a `.dat` file (with space-separated values). This file can be read in
MATLAB, R and other software for further analysis.

py2lispIDyOM also provides methods to extract certain (single or multiple) IDyOM outputs (for analysis in python)
and/or export them in different formats.

For more information about the IDyOM outputs, see [IDyOM Output](https://github.com/mtpearce/idyom/wiki/IDyOM-Output).

### 3. Visualizing IDyOM data

py2lispIDyOM provides some useful plotting tools to help visualize the IDyOM output data.

### Experiment Logger:

An experiment log folder (with the timestamp as the folder name) will be automatically created the record all data in
the current experiment in the `experiment_history/` folder
(by default, unless the users specify another path in the `experiment_history_folder_path` argument when initializing
the `IDyOMExperiment`).

This experiment log folder is structured in a way that can help researchers stay organized. It's also intended to record
all experiment data and contains all necessary data and scripts of the experiment that can be shared to
reproduce/replicate the experiment results.

In particular, the logger contains a LISP script (`compute.lisp`) which is the actual lisp script that runs the IDyOM
model.

### Structure

The structure of a typical experiment log folder follows the example below:

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