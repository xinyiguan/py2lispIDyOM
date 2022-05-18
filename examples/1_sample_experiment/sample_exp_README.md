# Sample Experiment

This is a walk-through of a sample IDyOM experiment using py2lispIDyOM to demonstrate the functionalities of the
package. For an overview of the py2lispIDyOM functionality, see the [README](README.md), and also
the [tutorials](tutorials/) for more details on each functionality.

There are 4 sample script/jupyter notebooks that provides examples for how you can use the py2lispIDyOM:

- [1_run_idyom.py](1_run_idyom.py)
- [2a_extract_data.ipynb](2a_extract_data.ipynb)
- [2b_export_data.ipynb](2b_export_data.ipynb)
- [4_viz.ipynb](4_viz.ipynb)

The `1_sample_experiment/` folder resembles a typical folder for IDyOM experiment using py2lispIDyOM.

All experiment outputs, files, figures are saved in the experiment log folder `16-05-22_14.01.03/`.

### Folder structure of the experiment logger `16-05-22_14.01.03`

```
16-05-22_14.01.03
├── experiment_input_data_folder
│   ├── pretrain_dataset
│   │   ├── shanx003.mid
│   │   ├── shanx002.mid
│   │   ├── shanx014.mid
│   │   ├── shanx015.mid
│   │   ├── shanx001.mid
│   │   ├── shanx005.mid
│   │   ├── shanx011.mid
│   │   ├── shanx010.mid
│   │   ├── shanx004.mid
│   │   ├── shanx012.mid
│   │   ├── shanx006.mid
│   │   ├── shanx007.mid
│   │   ├── shanx013.mid
│   │   ├── shanx009.mid
│   │   └── shanx008.mid
│   └── test_dataset
│       ├── chor-008.mid
│       ├── chor-009.mid
│       ├── chor-007.mid
│       ├── chor-013.mid
│       ├── chor-012.mid
│       ├── chor-006.mid
│       ├── chor-010.mid
│       ├── chor-004.mid
│       ├── chor-005.mid
│       ├── chor-011.mid
│       ├── chor-015.mid
│       ├── chor-001.mid
│       ├── chor-014.mid
│       ├── chor-002.mid
│       └── chor-003.mid
├── experiment_output_data_folder
│   └── 66051622140103-cpitch_onset-cpitch_onset-99051622140103-nil-melody-nil-1-both-nil-t-nil-c-nil-t-t-x-3.dat
├── outputs_in_csv
│   ├── chor-007.csv
│   ├── chor-013.csv
│   ├── chor-012.csv
│   ├── chor-006.csv
│   ├── chor-010.csv
│   ├── chor-004.csv
│   ├── chor-005.csv
│   ├── chor-011.csv
│   ├── chor-015.csv
│   ├── chor-001.csv
│   ├── chor-014.csv
│   ├── chor-002.csv
│   ├── chor-003.csv
│   ├── chor-008.csv
│   └── chor-009.csv
├── compute.lisp
├── outputs_in_mat
│   ├── information.content.mat
│   ├── chor003_melody_name.mat
│   ├── chor001_information_content.mat
│   ├── chor003_entropy.mat
│   ├── melody.name.mat
│   ├── chor003_information_content.mat
│   ├── entropy.mat
│   ├── chor001_entropy.mat
│   └── chor001_melody_name.mat
└── plots
    ├── simple_plot_information.content
    │   └── chor-003.png
    ├── pianoroll_groundtruth_surprisal
    │   ├── chor-011.png
    │   └── chor-010.png
    ├── simple_plot_onset.entropy
    │   ├── chor-002.png
    │   └── chor-001.png
    └── pianoroll_pitch_prediction_groundtruth
        ├── chor-007.eps
        └── chor-008.png
```




