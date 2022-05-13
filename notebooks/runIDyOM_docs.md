# Run IDyOM documentation

`class IDyOMExperiment`

Keyword arguments:

- `test_dataset_path`:
    - type: str
    - the path to your test dataset (required)
- `pretrain_dataset_path`:
    - type: str
    - the path to your pretrain dataset
- `experiment_history_folder_path`:
    - type: str
    - the path to which you want to save all the result data/plots
      (if leave blank, by default, a folder called **_experiment_history_** that hosts all data for the current
      experiment will be created when you run the IDyOM model).

### 1. Initialize Experiment

First, we initialize the IDyOM Experiment by providing the relevant paths. For example,

_Example_:

```
my_experiment = IDyOMExperiment(test_dataset_path = 'dataset/shanx_dataset/',
                                pretrain_dataset_path = 'dataset/bach_dataset/')
```
Note that the `experiment_history_folder_path` is not specified here above. So by default, a folder called '
experiment_history' will be created to host experiment log folders for each experiment.

### 2. Set model parameters:

For detailed description of the model parameters, please refer to
the [IDyOM parameters documentation](https://github.com/mtpearce/idyom/wiki/IDyOM-Parameters)

Valid keyword parameters in py2lispIDyOM package are almost the same as the original one, **except** that users are not
allowed to provide `dataset_id`, `pretraining_ids` and `output_path`.

The `dataset_id` and `pretraining_ids` are automatically generated and assigned when the user specify
the `test_dataset_path` and `pretrain_dataset_path` in step 1 initialization.

- The `output_path` by default is the 'experiment_output_data_folder/' within your current experiment log folder.

Valid keyword parameters are:

`target_viewpoints`, `source_viewpoints`,
`models`, `ltmo`, `stmo`,
`k`, `resampling_indices`,
`basis`, `dp`, `max_links`, `min_links`, `viewpoint_selection_output`,
`detail`, `overwrite`, `separator`,
`use_resampling_set_cache`, `use_ltms_cache`

_Example_:

Now, we need to set all the model parameters by using `set_parameters` method.

```
my_experiment.set_parameters(target_viewpoints=['cpitch', 'onset'],
                             source_viewpoints=['cpitch', 'onset'],
                             models=':both',
                             k=10)
```

### 3 Run IDyOM:

To run the IDyOM model, simply do the following:

```
my_experiment.run()
```

#### NOTE:

See example folder for more complete examples and tutorials.