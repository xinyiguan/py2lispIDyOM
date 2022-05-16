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
from modules.extract import ExperimentInfo

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
  Access specific melodies by index or melody names and returns a list of [MelodyInfo](#2-melody-info).

### 2. Melody Info

For each melody in the experiment, all data are stored in the `MelodyInfo` class which is essentially a panda.DataFrame.
An example of

```python3
MelodyInfo()
```

**Methods:**

- `MelodyInfo.get_property_list()`  Returns a list of all valid properties of the selected melody.
  _Example:_

```python3
some
codes...
```

- `MelodyInfo.access_properties(properties))`  Returns a list of selected property values, given a list of property
  names.
  _Example:_

```python3
some
codes...
```
