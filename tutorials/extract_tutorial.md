# Extracting Data

This tutorial will cover how to extract the IDyOM outputs in py2lispIDyOM. For an overview of the py2lispIDyOM
functionality, see the [README](README.md).

### Content

- [Experiment Information](#1-experiment-info)
- [Melody Infomration](#2-melody-info)

----

### 1. Experiment Info

To start, users need to indicate the experiment log folder that you want to work with by providing the log
path `experiment_folder_path`.

```python3
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
from modules.extract import ExperimentInfo

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

```python3
MelodyInfo()
```

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