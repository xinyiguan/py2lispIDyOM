# Mar2021 IDyOM (LISP) with Python Interface experiment documentation:

Using the python interface (last update Mar 4, 2021)

Notes: As the entire dataset is too large, I partitioned the dataset into 5 smaller ones (see following section), and 
ran the model 5 times. The results/model outputs should be the same.

### Dataset:

Training: '/Users/guan/LocalMusicDataset/mixed2/'  (953 midi files)

Testing: '/Users/guan/LocalMusicDataset/midi1/'
         '/Users/guan/LocalMusicDataset/midi2/'
         '/Users/guan/LocalMusicDataset/midi3/'
         '/Users/guan/LocalMusicDataset/midi4/'
         '/Users/guan/LocalMusicDataset/midi5/'
         
(35105 midi files in total, 7021 file for each folder)


### Model configurations:

Viewpoint: pitch (default)

Type of model: long term and short term (both)

k = 1 (no cross validation)


### LISP code script:

```
(start-idyom)

(idyom-db:initialise-database)
(idyom-db:import-data :mid "experiment_history/03-06-21_13.29.27/experiment_input_data_folder/train/" "Train" 66030621132945)
(idyom-db:import-data :mid "experiment_history/03-06-21_13.29.27/experiment_input_data_folder/test/" "Test" 99030621132945)
(idyom:idyom 99030621132945 '(cpitch) '(cpitch) :models :both :pretraining-ids '(66030621132945) :k 1 :detail 3 :output-path "experiment_history/03-06-21_13.29.27/experiment_output_data_folder/" :overwrite t)

(quit)


```

NOTE: the spaces within the MIDI file names are filled with "-"

### Experiment outputs:

For each of the five experiments, the program outputs 3 folders:

- mat_data_outputs/    (containing relevant data in .mat format)
    - surprise.mat
    - melody_name.mat
    - aligned_surprise_with_pitch.mat
    
- plot_pitch_prediction_comparison/     (all the pitch prediction vs. ground truth comparison figures)

- plot_surprise_with_pianoroll/         (all the surprise aligned with pianoroll figures)

*Notes: the two figure folders are insanely large.*