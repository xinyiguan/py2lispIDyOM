# py2lispIDyOM: A Python interface for IDyOM

py2lispIDyOM is a Python package for the information dynamics of music ([IDyOM](https://github.com/mtpearce/idyom/))
model.

## Getting Started

### Prerequisites

To start with, please read the [IDyOM installation page](https://github.com/mtpearce/idyom/wiki/Installation) to
appropriately install IDyOM on your local machine.

### Installation

## Functionality and Usage


In summary, py2lispIDyOM currently has three main functionalities:

### 1. Run IDyOM

The first step is to define all necessary parameters for the IDyOM model.

```
some sample codes here...
```


#### _Notes:_

When you run the IDyOM experiment, py2lispIDyOM will automatically create a folder
(with the timestamp of experiment time as the folder name) logging all data of the
current experiment. For details of the experiment log folder, see the 
**_Experiment Logger_** section.

### 2. Export the IDyOM outputs in `.mat` or `.csv` format

Given that IDyOM outputs are available (check if `.dat` file exists under the path `experiment_output_data_folder/`
in the current experiment log folder), users can extract and export certain features in 
`.mat` and/or `.csv` formats with the methods `export2mat()` and `export2csv()` respectively.

A quick example of export the "melody_name", "onset" and "cpitch" data of the two melodies
'"shanx002"', '"shanx008"' in the experiment `04-05-22_14.35.26` in `.mat` format will look like:
```
from export import Export

# define the parameters for the export
export_mat = Export(experiment_folder_path='experiment_history/04-05-22_14.35.26/',
                   features_to_export=['onset', 'cpitch', 'melody_name'],
                   melody_names=['"shanx002"', '"shanx008"'])
                   
export_mat.export2mat()
```


### 3. Plotting for IDyOM data. 




### Detailed Functionality

See the following files for more detailed information about the three main functionalities:

- [Run IDyOM documentation](notebooks/runIDyOM_docs.ipynb)
- [Export documentation](notebooks/export_docs.ipynb)
- [Visualization documentation](notebooks/visualization_docs.ipynb)

Examples and tutorial files can be found in the [example](examples) directory.


## Experiment Logger:

An experiment log folder (with the timestamp as the folder name) will be automatically 
created the record all data in the current experiment in the `experiment_history/` folder 
(by default, unless the users specify another path in the `experiment_history_folder_path` argument 
when initializing the `IDyOMExperiment`). 

The structure of the experiment log folder follows the example below:

**_(insert folder tree here)_**

