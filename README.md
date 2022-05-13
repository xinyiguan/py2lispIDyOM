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

In summary, py2lispIDyOM currently has four main functionalities:

### 1. Run IDyOM

To start with, you need to 1) initialize the experiment, 2) set model parameters, and 3) run the model.

**_Notes:_**

When you run the IDyOM experiment, py2lispIDyOM will automatically create a folder
(with the timestamp of experiment time as the folder name) logging all data of the current experiment. For details of
the experiment log folder, see the
**_Experiment Logger_** section.

After finish running the model, the model output (a `.dat` file will be saved in the current experiment log folder under
'experiment_output_data_folder/').

From here, you can extract the relevant IDyOM outputs or export them in other formats for further analysis.

### 2. Extract/Access to output data

### 3. Export Data in other formats

IDyOM outputs can be extracted and exported in `.mat` or `.csv` format.

### 4. Plotting for IDyOM data.

methods available:

- `plot_pianoroll_pitch_distribution_groundtruth`
- `plot_pianoroll_surprisal`

#### Detailed Functionality

See the following files for more detailed information about the three main functionalities:

- [Run IDyOM documentation](notebooks/runIDyOM_docs.md)
- [Extract documentation](notebooks/extract_docs.md)
- [Export documentation](notebooks/export_docs.md)
- [Visualization documentation](notebooks/visualization_docs.md)

Examples and tutorial files can be found in the [example](examples) directory.


## Experiment Logger:

An experiment log folder (with the timestamp as the folder name) will be automatically 
created the record all data in the current experiment in the `experiment_history/` folder 
(by default, unless the users specify another path in the `experiment_history_folder_path` argument 
when initializing the `IDyOMExperiment`). 

The structure of the experiment log folder follows the example below:

**_(insert folder tree here)_**

