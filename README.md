# py2lispIDyOM: A Python interface for IDyOM

py2lispIDyOM is a Python package for the information dynamics of music ([IDyOM](https://github.com/mtpearce/idyom/))
model.

## Getting Started

### Prerequisites

To start with, please read the [IDyOM installation page](https://github.com/mtpearce/idyom/wiki/Installation) to
appropriately install IDyOM on your local machine.

### Installation

Note you can also download this repo as an alternative to git clone.

## Functionality and Usage

In summary, py2lispIDyOM has four main functionalities for research workflow.

See the following files for more detailed information about the three main functionalities:

- [Run IDyOM tutorial](notebooks/runIDyOM_tutorial.md)
- [Extract tutorial](notebooks/extract_tutorial.md)
- [Export tutorial](notebooks/export_tutorial.md)
- [Visualization tutorial](notebooks/visualization_tutorial.md)

Examples and tutorial files can be found in the [example](examples) directory.

### 1. Run IDyOM

To run the IDyOM model with py2lispIDyOM takes three steps:

1) Set experiment configuration (paths to input music files and to output experiment log)
2) Set model configuration (model parameters, see ... for more detail)
3) run the experiment.

### 2. Extract/Access to output data

### 3. Export Data in other formats

IDyOM outputs can be extracted and exported in `.mat` or `.csv` format.

### 4. Visualizing IDyOM data.

methods available:

- `plot_pianoroll_pitch_distribution_groundtruth`
- `plot_pianoroll_surprisal`



## Experiment Logger:

An experiment log folder (with the timestamp as the folder name) will be automatically 
created the record all data in the current experiment in the `experiment_history/` folder 
(by default, unless the users specify another path in the `experiment_history_folder_path` argument 
when initializing the `IDyOMExperiment`). 

The structure of the experiment log folder follows the example below:

**_(insert folder tree here)_**

```
experiment_history
└── 04-05-22_14.35.26
    ├── experiment_input_data_folder
    │   ├── test
    │   └── train
    ├── experiment_output_data_folder
    │   └── 66050422143526-cpitch_onset-cpitch_onset-99050422143526-nil-melody-nil-1-both+-nil-t-nil-c-nil-t-t-x-3.dat
    ├── outputs_in_csv
    ├── compute.lisp
    ├── outputs_in_mat
    │   ├── cpitch.mat
    │   └── onset.mat
    └── plots
    
```