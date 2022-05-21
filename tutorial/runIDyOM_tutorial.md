# Run IDyOM Tutorial

This tutorial will walk you through how to run the IDyOM model in py2lispIDyOM. For an overview of the py2lispIDyOM
functionality, see the [README](../README.md).

---
To run the IDyOM model with py2lispIDyOM takes three steps:

- [1. Set experiment configuration](#1-set-experiment-configuration)
- [2. Set model parameters](#2-set-model-parameters)
- [3. Run IDyOM](#3-run-idyom)

### 1. Set experiment configuration:

First, we set the IDyOM experiment configurations by providing the relevant paths.

```python3
class IDyOMExperiment(test_dataset_path,
                      pretrain_dataset_path=None,
                      experiment_history_folder_path=None)
```

**Parameters**:

- `test_dataset_path`: _str_
    - the path to your test dataset (required)


- `pretrain_dataset_path`: _str_
    - the path to your pretrain dataset


- `experiment_history_folder_path`: _str_
    - the path to which you want to save all the result data/plots
      (if leave blank, by default, a folder called **_experiment_history_** that hosts all data for the current
      experiment will be created when you run the IDyOM model).

_Example:_

```python
from py2lispIDyOM.run import IDyOMExperiment

my_experiment = IDyOMExperiment(test_dataset_path='dataset/shanx_dataset/',
                                pretrain_dataset_path='dataset/bach_dataset/')
```

Note that the `experiment_history_folder_path` is not specified here above. So by default, a folder called '
experiment_history' will be created to host experiment log folders for each experiment.
If `experiment_history_folder_path`
is specified, the experiment log folders will be saved under this path.

### 2. Set model parameters:

Next, we set the model parameters using the `set_parameters` methods.

```python3
class IDyOMExperiment.set_parameters(target_viewpoints, source_viewpoints,
models, ltmo, stmo,
k=10, resampling_indices,
basis, dp, max_links, min_links, viewpoint_selection_output,
detail, overwrite, separator,
use_resampling_set_cache, use_ltms_cache)

```

For detailed description of the model parameters, please refer to
the [IDyOM parameters documentation](https://github.com/mtpearce/idyom/wiki/IDyOM-Parameters).

Valid keyword parameters in py2lispIDyOM package are almost the same as the original one, **except** that users are not
allowed to provide `dataset_id`, `pretraining_ids` and `output_path`.

The `dataset_id` and `pretraining_ids` are automatically generated and assigned when the user specify
the `test_dataset_path` and `pretrain_dataset_path` in step 1 initialization.

- The `output_path` by default is the 'experiment_output_data_folder/' within your current experiment log folder.

If parameters are not specified by the users, py2lispIDyOM will conform to the default value in IDyOM.

_Example Continue_:

```python3
my_experiment.set_parameters(target_viewpoints=['cpitch', 'onset'],
                             source_viewpoints=['cpitch', 'onset'],
                             models=':both',
                             k=10)
```

### 3. Run IDyOM:

To run the IDyOM model, simply call the `IDyOMExperiment.run()` method.

_Example Continued:_

```python3
my_experiment.run()
```

### **_What happens then:_**

py2lispIDyOM will automatically create a folder
(with the timestamp of experiment time as the folder name) logging all data of the current experiment. For details of
the experiment log folder, see the Experiment Logger section in [README](README.md).

After finish running the model, the model output (a `.dat` file will be saved in the current experiment log folder under
'experiment_output_data_folder/').

From here on, you can extract the relevant IDyOM outputs or export them in other formats for further analysis.

#### NOTE:

See [examples](examples/) folder for more complete examples.