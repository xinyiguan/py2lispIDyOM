# Extracting and exporting Tutorial

IDyOM writes the outputs of the modelling to a `.dat` file (with space-separated values). This file should be under
the 'experiment_output_data_folder' in the experiment log folder. The `.dat` file can be read in MATLAB, R and other
software.

For more information about the IDyOM outputs, see [IDyOM Output](https://github.com/mtpearce/idyom/wiki/IDyOM-Output).

This tutorial will cover how to extract certain IDyOM outputs (for analysis in python) and export them in different
formats in py2lispIDyOM. For an overview of the py2lispIDyOM functionality, see the [README](../README.md).

### Content

I. [Extracting Data](#i-extracting-data)
<br>
II. [Exporting Data](#ii-exporting-data)

----

## I. Extracting Data

py2lispIDyOM provides methods to extract certain properties of the IDyOM outputs. The extract module is helpful for
analysis in python.

#### Content <br>

1. [Experiment Information](#1-experiment-info)
2. [Melody Infomration](#2-melody-info)

### 1. Experiment Info

To start, users need to indicate the experiment log folder that you want to work with by providing the log
path `experiment_folder_path`.

``` python3
ExperimentInfo(experiment_folder_path)
```

**Parameters:**

- `experiment_folder_path`: _str_
  - the path to the experiment log folder.

**Attributes:**

- `melodies_dict`  Dictionary of all melodies in the experiment with melody name as the key and the
  corresponding [MelodyInfo](#2-melody-info) as the value.

- `pitch_range`  Returns a tuple of pitch range of the entire dataset.

**Methods:**

- `access_melodies(starting_index=None, ending_index=None, melody_names=None)`  
  Access specific melodies by index or melody names and returns a list of [MelodyInfo](#2-melody-info) objects.

Example:

```python3
from py2lispIDyOM.extract import ExperimentInfo

my_experiment = ExperimentInfo(experiment_folder_path='examples/1_sample_experiment/16-05-22_14.01.03/')

# Access the melody named '"chor-012"':
selected_melody_1 = my_experiment.melodies_dict['"chor-012"']

# Another way to do the same:
selected_melody_1 = my_experiment.access_melodies(melody_names=['"chor-012'])

# Access the melody (or melodies) by index. Here we access the first 10 melodies:
selected_melody_2 = my_experiment.access_melodies(starting_index=0,
                                                  ending_index=9)

```

### 2. Melody Info

For each melody in the experiment, all data are stored in the `MelodyInfo` class which is essentially a panda.DataFrame.
To create an instance of `MelodyInfo`, we can use `ExperimentInfo.melodies_dict`, or `ExperimentInfo.access_melodies` as
showed above.

**Methods:**

- `MelodyInfo.get_property_list()`  Returns a list of all valid properties (IDyOM results) of the selected melody.
  _Example:_

```python3
# first, access the melody:
selected_melody = my_experiment.melodies_dict['"chor-012"']

# get a list of valid properties for this selected_melody:
property_list = selected_melody.get_property_list()
```

- `MelodyInfo.access_properties())`  Returns a list of selected property values, given a list of property names.
  _Example:_

```python3
# first, access the melody:
selected_melody = my_experiment.melodies_dict['"chor-012"']

# we access the folllowing three properties/results: 'information.content', 'cpitch.information.content', 'onset.information.content' 
property_list = selected_melody.access_properties(
  ['information.content', 'cpitch.information.content', 'onset.information.content'])
```

For more examples, see also the [Jupyter Notebook examples](examples/1_sample_experiment/2_extract_data.ipynb)


---

## II. Exporting data

py2lispIDyOM also provides methods to **export** certain properties of the IDyOM outputs in different formats (`.mat`
and `.csv`).

``` python3
Export(experiment_folder_path,
       properties_to_export,
       melody_names=None)
```

**Parameters:**

- `experiment_folder_path`: _str_
  - This is the experiment log folder path which contains the data you want to export (the folder name by default is the
    timestamp of the experiment time)
- `properties_to_export`: _list of str_, e.g., `properties_to_export = ['melody.name', 'cpitch']`
  - The list of properties to be exported. For available properties to export,
    see [IDyOM Output](https://github.com/mtpearce/idyom/wiki/IDyOM-Output).
- `melody_names`: _list of str_
  - The list of melodies of which properties to be exported. If not specified, the selected properties of all melodies
    data will be exported.

**Methods:**

- `export2mat()`  Export the values of selected properties of selected melodies in `.mat` files.
- `export2csv()`  Export the values of selected properties of selected melodies in `.csv` files.

A quick example of export the "melody_name", "onset" and "cpitch" data of the two melodies
'"chor-001"', '"chor-002"' in the experiment `16-05-22_14.01.03' `to `.mat` format will look like:

```python3
from py2lispIDyOM.export import Export

# define the parameters for the export
export_mat = Export(experiment_folder_path='examples/1_sample_experiment/16-05-22_14.01.03/',
                    properties_to_export=['onset', 'cpitch', 'melody_name'],
                    melody_names=['"chor-001"', '"chor-002"'])

export_mat.export2mat()
```

The exported files will be saved in then experiment logger under the folder 'outputs_in_mat/' or 'outputs_in_csv/'








