# A python interface for LISP IDyOM 

This is a still work in progress...


## Directory Structure

- README
- `configuration.py`: *set you configurations here*
- `run.py`: *load and run the LISP IDyOM*
- `data_extractor.py`: *extract the data we are interested in from .dat file*
- `DataExtractionTutorial.ipynb`: *a Jupyter Notebook tutorial to show how to use functions in `data_extractor.py`*
- `midi_melody_extractor.py` : *extract the melodic line from midi*
- `MIDI_MelodyExtractionTutorial.ipynb` : *a Jupyter Notebook tutorial to show how to use extract melody from MIDI files*
- `analyze_output_data.py`: *a playground for any other tasks (plotting, analyzing output data ...)*
- dataset/:
    -  a bunch of folders containing midi files 
- lisp/:
    - compute.lisp *the lisp code to set the parameters of IDyOM*
    - parser.py
- experiment_history/:
    - folders(naming format: MM-DD-YY_HH.MM.SS) *containing information for each experiment run*
        - `configurations.py`
        - experiment_input_data_folder/
            - train/
                - ~.mid
            - test/
                - ~.mid
        - experiment_output_data_folder/
            - ~.dat: *LISP IDyOM model output*

## Usage (brief version)

1. Change the ```configuration.py``` file to specify the training-set folder and test-set folder for our experiment.
2. Run ```run.py``` to run LISP version of IDyOM
3. Customize your processing of the IDyOM output in ```analyze_output_data.py```. You can use functions in `data_extractor.py`
4. Run ```analyze_output_data.py``` (This is an example of extracting experiment output data from the saved experiment result, and using it for plotting)

Here is an intentional underfiting example (train on distribution X test on distribution Y with X being very different from Y) (notice the surprise):
![alt text][logo1]

[logo1]: Demo_figures/train_bach_test_shanx/shanx019.mid.png

Here is an intentional overfiting example (train X is exactly test Y) (notice the surprise):
![alt text][logo2]

[logo2]: Demo_figures/train_intentional_overfit_on_bach/chor-003.mid.png

Here is a normal example (train X and test Y have similar distribution and being mutually exclusive) (notice the surprise):
![alt text][logo3]

[logo3]: Demo_figures/train_bach_test_bach/chor-004.mid.png

- Do whatever you want to do in ```analyze_output_data.py```. 
- Done!


 ## How to use (detailed version):
 
 #### 0. (*Optional*) Data preprocessing: 
 - As IDyOM is limited to the monodic melodic music, we first need to extract the melodic line from the MIDI
 files, if the MIDI has multiple parts. Refer to the `MIDI_MelodyExtractionTutorial.ipynb` for how to extract
 the melodic line from MIDI. 
 
 
 #### 1. Set/change the configuration in ```configuration.py```:
-  In ```configuration.py```, there are 2 parameters to be set:
    - ```'experiment_history_folder'``` where to put the experiment result folder (path specified by user)
    - ```'train_test_path'``` specific the training set path and the testing set path here. 
        - e.g. ```'train_test_path':['./dataset/bach_dataset/','./dataset/shanx_dataset/',],```
        - If you want to train and test on the same dataset, then just leave the second argument blank.
          It will automatically split the files into train and test set according to percentage ```'trainp'```.
    - ```'trainp'``` If you only input one path in ```'train_test_path'```, you need to set the percentage of training dataset.
    dataset now is randomly split into training and testing set for each experiment (each time we run the script).
    If you have different training and testing path, set ```'trainp' = NONE```

 #### 2. Run the ```run.py```. 
 This step is to load and run the LISP version of IDyOM.


##### What happens when you run ```run.py```

- A folder (naming format: MM/DD/YY_HH.MM.SS) will be created to record information of the current experiment,
including the following:
    - the configuration file ((a script containing info of the configurations we set for this experiment))
    - the dataset input named 'experiment_input_data_folder' (duplicated from original path, which is specifiable in the ```configuration.py```)
    - the output from IDyOM named 'experiment_output_data_folder' (containing the ```.dat``` file)
    
                  
 [Comments:] *By creating an 'experiment_history' folder, we can have a record of all data and information used and the output for this experiment.
 In this way, we can have a better control over what dataset we want the model to train on and test on, 
 and we can have a record of the information we can check if we have any doubts of the output of the model.*
 
 #### 3. Play around with the model output in ```analyze_output_data.py```. 
 You can look up the functions in `data_extractor.py` (probably will add more). 
 This script contains the helper functions that extract the data from the IDyOM model output (`.dat` file)
 An example of how to use this script is provided in later section and in the `DataExtractionTutorial.ipynb`
 


## IDyOM command to separate train and test (Already implemented)
#####Refer to the `README` in the lisp directory for more details on the model parameters. 

IDyOM Lisp codes: (no need to change anything in here.)
 ```` 
    (start-idyom)
    (idyom-db:initialise-database)    
    (idyom-db:import-data :mid "TRAINFOLDER" "Train" TRAINID)    
    (idyom-db:import-data :mid "TESTFOLDER" "Test" TESTID)
    (idyom:idyom TESTID '(cpitch onset) '(cpitch onset) :models :ltm :pretraining-ids '(TRAINID) :k 1 :detail 3 :output-path DATAOUTPUT :overwrite t)
    
    (quit)
````


## Example on how to use data_extractor.py to extract data of interest from .dat file
Please look up the Jupyter Notebook `DataExtractionTutorial.ipynb` for detailed tutorial. 
The following codes are just a simple example. 
    
 
    import data_extractor
    
    all_song_dict = data_extractor.get_all_song_dict_from_dat(dat_file_path)

```all_song_dict``` is python dictionary contain info from the dat.file

for demonstration purpose, we choose data for a specific song from the of the ```all_song_dict```

    song_dict_of_interest= list(all_song_dict.values())[0]


    
    note_distribution = data_extractor.get_note_distribution_from_song_dict(song_dict_of_interest)
    onset_sequence = data_extractor.get_onset_from_song_dict(song_dict_of_interest)
    
    print('note_distribution.shape: ',note_distribution.shape)
    print('note_distribution: ',note_distribution)
    print('onset_sequence.shape: ',onset_sequence.shape)
    print('onset_sequence: ',onset_sequence)   

 terminal print result:
    
    note_distribution.shape:  (26, 44)
    note_distribution:  [[0.         0.         0.         ... 0.02287778 0.02107164 0.0192655 ]
     [0.         0.         0.         ... 0.01175776 0.01082951 0.00990127]
     [0.         0.         0.         ... 0.00356255 0.0032813  0.00300005]
     ...
     [0.         0.         0.         ... 0.00830964 0.00765362 0.00699759]
     [0.         0.         0.         ... 0.01286343 0.0118479  0.01083237]
     [0.         0.         0.         ... 0.01452397 0.01337734 0.01223071]]
    onset_sequence.shape:  (26,)
    onset_sequence:  [  0.  12.  24.  48.  66.  72.  84.  96. 108. 114. 120. 132. 144. 192.
     204. 216. 240. 258. 264. 276. 288. 300. 306. 312. 324. 336.]

 the number in the ```oneset_sequence``` is the time location for each event (useful for modeling rhythm)
 
 length of a quarter note is 24 by default