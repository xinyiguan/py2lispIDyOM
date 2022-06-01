*************
Run IDyOM model
*************

.. currentmodule:: py2lispIDyOM.run
.. toctree::

To run the IDyOM model with `py2lispIDyOM`, the `IDyOMExperiment` object is
provided to configure the model. You will set all the dataset paths, model parameters here.

.. autoclass:: IDyOMExperiment
   :members:


Parameters to configure the IDyOM model are almost the same as the those listed and described in the
`IDyOM parameters documentation, <https://github.com/mtpearce/idyom/wiki/IDyOM-Parameters>`__
EXCEPT that users are not allowed to assign `dataset-id` and `pretraining-ids`, and `output-path` in `py2lispIDyOM`.

Instead, users need to supply the relevant dataset paths for the test dataset and pretrain dataset,
and unique dataset ID will automatically then be assigned to those user-specified dataset respectively.
The output file of the IDyOM model are saved to the corresponding experiment logger.

Valid parameters to configure the IDyOM model are:

**Required parameters**:
    - `target_viewpoints`: List[SingleViewpoint]
    - `source_viewpoints`: Union[Literal[':select'], List[Union[SingleViewpoint, Tuple[SingleViewpoint]]]]

**Statistical modelling parameters**:
    - `models`: Literal[':stm', ':ltm', ':ltm+', ':both', ':both+']
    - `ltmo`: Literal[':ltmo']
    - `stmo`: Literal[':stmo']
    - `ltmo_order_bound``stmo_order_bound`: int
    - `ltmo_mixtures`, `stmo_mixtures`: bool
    - `ltmo_update_exclusion`, `stmo_update_exclusion`: bool
    - `ltmo_escape`, `stmo_escape`: Literal[':a', ':b', ':c', ':d', ':x']

**Training parameters**:
    - `k`: Union[int, Literal[":full"]], default is 10
    - `resampling_indices`: List[int]

**Viewpoint selection parameters**:
    - `basis`:  Union[List[SingleViewpoint], Literal[':pitch-full', ':pitch-short', ':bioi', ':onset', ':auto']]
    - `dp`: int
    - `max_links`: int
    - `min_links`: int
    - `viewpoint_selection_output`: str

**Output parameters**:
    - `detail`: Literal[1, 2, 3]
    - `overwrite`: bool
    - `separator`: str

**Caching parameters**:
    - `use_resampling_set_cache`: bool
    - `use_ltms_cache`: bool


For more examples on how to configure and run the IDyOM model,
please see the `tutorial <https://github.com/xinyiguan/py2lispIDyOM/blob/master/tutorials/1_running_IDyOM_tutorial.ipynb>`__.

