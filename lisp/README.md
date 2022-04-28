# The IDyOM Lisp script explained

This section is to explained the IDyOM lisp command.
(No need to change anything here. Already implemented and good to use, this section just for record and explanation)
If you want to change the model parameters, check with Pearce instructions.

### IDyOM Lisp codes overview :

 ```` 
(start-idyom)

(idyom-db:initialise-database)    
(idyom-db:import-data :mid "TRAINFOLDER" "Train" TRAINID)    
(idyom-db:import-data :mid "TESTFOLDER" "Test" TESTID)
(idyom:idyom TESTID '(cpitch onset) '(cpitch onset) :models :ltm :pretraining-ids '(TRAINID) :k 1 :detail 3 :output-path DATAOUTPUT :overwrite t)

(quit)
````

The python script that loads and reads the this lisp script basically treats the codes as texts and pastes the it in the
terminal to run.

The capitalized words (such as `TRAINFOLDER`, `TESTID`...) are the parts to be replaced in the python script `run.py`.
NOTE: do not change these capitalized words.

If you want to inspect the parameters of the IDyOM model for the current experiment, please open the `compute_temp.lisp`
file which is generated after you run the `run.py`. Here is an example of what you will see in `compute_temp.lisp` for
one experiment:

 ```` 
(start-idyom)

(idyom-db:initialise-database)    
(idyom-db:import-data :mid "experiment_history/11-13-20_18.37.59/experiment_input_data_folder/train/" "Train" 66111320183759)    
(idyom-db:import-data :mid "experiment_history/11-13-20_18.37.59/experiment_input_data_folder/test/" "Test" 99111320183759)
(idyom:idyom 99111320183759 '(cpitch onset) '(cpitch onset) :models :ltm :pretraining-ids '(66111320183759) :k 1 :detail 3 :output-path "experiment_history/11-13-20_18.37.59/experiment_output_data_folder/" :overwrite t)

(quit)
````

The capitalized words are replaced with the actual paths/arguments that are executed. With my current setting, the
training dataset id begins with '66' and then followed by time stamp in the format of 'MMDDYYHHMMSS'. Likewise for the
testing dataset with prefix id '99'.

### Line by line explanation:

1. `(idyom-db:initialise-database)`

    - To initialize the database everytime we run our experiment. This allows us to better control and not to confuse
      ourselves with what dataset is inside our database.

2. `(idyom-db:import-data :mid "TRAINFOLDER" "Train" TRAINID)`
   `(idyom-db:import-data :mid "TESTFOLDER" "Test" TESTID)`

    - These two lines load the train and test dataset separately. So the model can train on the dataset we want it to
      train on, and test on the dataset we specify.

3. `(idyom:idyom TESTID '(cpitch onset) '(cpitch onset) :models :ltm :pretraining-ids '(TRAINID) :k 1 :detail 3 :output-path DATAOUTPUT :overwrite t)`

    - This is the main line of lisp command to configure the IDyOM for our experiment.

    - The model predicts the pitch and onset values in dataset `TESTID`, which is the dataset we input as our test
      dataset.

    - In our project and in this example, the viewpoints we are interested in are `'(cpitch onset)`

    - The model that I use, `:ltm` , is the long-term model only, which trained on the pretraining and resampling
      training data.
        - We can also use and experiment with other models.

    - The `pretraining-ids` is the dataset ids used to pretrain the long-term models. I set it to `(TRAINID)`, so now
      the dataset for *training* the model is the entire dataset we set as our training data in the `configuration.py`.

    - `:k 1` means no resampling. This is an important keyword argument. Setting k=1 makes the whole dataset of
      id `TESTID` be our test set.
      (k-fold sampling implies 1/k of our dataset to be test set)

    - `:detail 3` specifies the model outputs, containing: information content averaged over the entire dataset, and
      over each composition, and also the raw IC values for each event in each composition.

    - `:output-path DATAOUTPUT` the model output is stored in the `DATAOUTPUT`, which is the .dat file in
      experiment_history/experiment_output_data_folder/

#### Available keys in output dictionary:

dict_keys(['dataset.id', 'melody.id', 'note.id', 'melody.name', 'vertint12', 'articulation', 'comma', 'voice', 'ornament', 'dyn', 'phrase', 'bioi', 'deltast', 'accidental', 'mpitch', 'cpitch', 'barlength', 'pulses', 'tempo', 'mode', 'keysig', 'dur', 'onset', 'cpitch.order.ltm.cpitch', 'cpitch.order.stm.cpitch', 'cpitch.weight.ltm', 'cpitch.weight.stm', 'cpitch.weight.ltm.cpitch', 'cpitch.weight.stm.cpitch', 'cpitch.probability', 'cpitch.information.content', 'cpitch.entropy', 'cpitch.31', 'cpitch.34', 'cpitch.40', 'cpitch.41', 'cpitch.43', 'cpitch.44', 'cpitch.45', 'cpitch.46', 'cpitch.47', 'cpitch.48', 'cpitch.49', 'cpitch.50', 'cpitch.51', 'cpitch.52', 'cpitch.53', 'cpitch.54', 'cpitch.55', 'cpitch.56', 'cpitch.57', 'cpitch.58', 'cpitch.59', 'cpitch.60', 'cpitch.61', 'cpitch.62', 'cpitch.63', 'cpitch.64', 'cpitch.65', 'cpitch.66', 'cpitch.67', 'cpitch.68', 'cpitch.69', 'cpitch.70', 'cpitch.71', 'cpitch.72', 'cpitch.73', 'cpitch.74', 'cpitch.75', 'cpitch.76', 'cpitch.77', 'cpitch.78', 'cpitch.79', 'cpitch.80', 'cpitch.81', 'cpitch.82', 'cpitch.83', 'cpitch.84', 'cpitch.85', 'cpitch.86', 'cpitch.87', 'cpitch.88', 'cpitch.89', 'cpitch.90', 'cpitch.91', 'cpitch.92', 'cpitch.94', 'cpitch.95', 'cpitch.96', 'cpitch.97', 'cpitch.100', 'cpitch.101', 'probability', 'information.content', 'entropy', 'information.gain'])
