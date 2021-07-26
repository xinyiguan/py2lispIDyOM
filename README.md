# A python interface for LISP IDyOM 

Last version update: July 26, 2021

Library dependency:
   - numpy
   - matplotlib
   - scipy
   - tqdm
   - mido
    

                        
## Usage Overview (brief version)

1. Change the ```configuration.py``` script to specify the training-set folder and test-set folder for the experiment.
2. Change the ```compute.lisp``` script within the lisp folder to specify the model parameters for IDyOM model. 
3. Run ```run.py``` to run LISP code of IDyOM.
4. Use the `outputs_in_mat_format.py` script to get the model outputs in ```.mat``` format.



 ## How to use (detailed version):
 
 ### 0. (*Optional*) Data preprocessing: 
 - As IDyOM is limited to the monodic melodic music, we first need to extract the melodic line from the MIDI
 files, if the MIDI has multiple parts. Refer to the `MIDI_MelodyExtractionTutorial.ipynb` for how to extract
 the melodic line from MIDI. 
 
 
 ### 1. Set/change the configurations in ```configuration.py```:
 This step is to set the input/output dataset and experiment history folder location.

In ```configuration.py```, there are 4 parameters to be set:

1.  ```'experiment_history_folder'``` where to put the experiment result folder (path specified by user)
2.  ```'train_test_path'``` specific the training set path and the testing set path here.
    - e.g. ```'train_test_path':['./dataset/bach_dataset/','./dataset/shanx_dataset/',],```
    - If you want to train and test on the same dataset, then just leave the second argument blank.
      It will automatically split the files into train and test set according to percentage ```'trainp'```.
3.  ```'trainp'``` If you only input one path in ```'train_test_path'```, you need to set the percentage of training dataset.
dataset now is randomly split into training and testing set for each experiment (each time we run the script).
If you have different training and testing path, set ```'trainp' = NONE```
4.  ```'experiment_name'``` You can name this specific experiment. The experiment_name will show up in the figures that are generated in later steps. 

Follow the template in ```configuration.py```. 

**Example:** 

```
both_train_bach_test_shanxi = {
	'train_path': bach,
	'test_path': shanx,
	'model_type': 'both',
	'target_viewpoints': 'cpitch onset dur',
	'source_viewpoints': 'cpitch onset dur',
	'k_number_of_resampling': '1',
	'experiment_history_folder': 'experiment_history/',
	'experiment_name': 'both_train_bach_test_shanx',
}
```

 ### (Optional)2. If using the customized lisp code for then experiment, set/change the IDyOM model parameters in ```compute.lisp``` in the lisp folder:
This step is to set the model parameters for IDyOM when using your own lisp script.

If you are using the general template of the lisp script, you can skip this step. You have already speicified your data/model input/parameters. 

More description of the script, see the README.md within the lisp folder.
 

 



 ### 3. Run the ```run.py```. 
 This step is to load and run the LISP version of IDyOM.

```python run.py```

##### What happens when you run ```run.py```?

- A folder (timestamp naming format: MM/DD/YY_HH.MM.SS) will be created to record information of the current experiment,
including the following:
    - the configuration file ((a script containing info of the configurations we set for this experiment))
    - the dataset input named 'experiment_input_data_folder' (duplicated from original path, which is specifiable in the ```configuration.py```)
    - the output from IDyOM named 'experiment_output_data_folder' (containing the ```.dat``` file)
    
                  
 [Comments:] *By creating an 'experiment_history' folder, we can have a record of all data and information used and the output for this experiment.
 In this way, we can have a better control over what dataset we want the model to train on and test on, 
 and we can have a record of the information we can check if we have any doubts of the output of the model.*
 
 
 ### 4. Get the model outputs in different file formats. 
 
To get the model outputs in mat format, run `outputs_in_mat_format.py`. 


Follow the 2 steps to extract the outputs: 

1. You  need to manually change the path of ```selected_experiment_history_folder``` to your desired one in this script (preferably in absolute path).

    *Example for the `outputs_in_mat_format.py`: (same for the other two plotting scripts)*

    ```
    # Pass your desired 'selected_experiment_history_folder' below:
    if __name__ == '__main__':
        selected_experiment_history_folder = 'experiment_history/03-06-21_13.29.27/'
        export_mat_from_history_folder(selected_experiment_history_folder)
    ``` 

2. Specify the **data_type_to_export**. 

Change the template ```data_type_to_export``` to output your features:

Available features for output in ```.mat ``` file format:  

- 'melody_name',
- 'overall_probability',
- 'overall_information_content',
- 'overall_entropy',
- 'cpitch_information_content',
- 'cpitch_entropy',
- 'onset_information_content',
- 'onset_entropy',
- 'duration_information_content',
- 'duration_entropy',

e.g.

    data_type_to_export = [
        'melody_name',
        'overall_information_content',
        'overall_entropy',
        'duration_information_content',
        'duration_entropy',
    ]


You can further extract different model outputs by changing/adding different "extraction methods" in the dictionary called 
```features_method_name_dict```, and modifying the following ```my_choice_of_extraction``` accordingly in the `outputs_in_mat_format.py` script. 


### 5. Get output visualizations:

*You need to change the ```selected_experiment_history_folder``` at the bottom of the script to your desired one in each script.*

- "plot_pitch_prediction_comparison" folder, containing all pitch prediction vs. ground truth figures.
- "plot_surprise_with_pianoroll" folder, containing all surprise value aligned with piano roll figures. 




```main_analysis.py``` is an integrated script that runs the 3 other scripts/modules simultaneously:
`plot_pitch_prediction_comparison.py`, 
`plot_surprise_with_pianoroll.py`, and 
`outputs_in_mat_format.py`. 


## Model Output visualization examples:


### 1. Here is an intentional underfiting example (train on distribution X test on distribution Y, with X supposed to be very different from Y):

IDyOM pitch prediction vs. ground truth:

![alt text][logo5]

[logo5]: Demo_Figs/prediction-shanx033.png

IDyOM surprise values aligned with piano roll:

![alt text][logo6]

[logo6]: Demo_Figs/surprise-shanx033.png


### 2. Here is an intentional overfitting example (train X is exactly test Y):

IDyOM pitch prediction vs. ground truth:

![alt text][logo3]

[logo3]: Demo_Figs/prediction-chor-015.png

IDyOM surprise values aligned with piano roll:

![alt text][logo4]

[logo4]: Demo_Figs/surprise-chor-015.png


### 3. Here is a normal example (train X and test Y have similar distribution and being mutually exclusive) (notice the surprise):

IDyOM pitch prediction vs. ground truth:

![alt text][logo1]

[logo1]: Demo_Figs/prediction-chor-030.png

IDyOM surprise values aligned with piano roll:

![alt text][logo2]

[logo2]: Demo_Figs/surprise-chor-030.png



## Directory Structure

- README
- `configuration.py`: *set you configurations here*
- `run.py`: *load and run the LISP IDyOM*
- `main_analysis.py`: *an integrated script to output different visualization figures and output data in .mat format,
after running the run.py.*
- `plot_pitch_prediction_comparison.py`: *make the comparison figure(s) of the predicted pitch distributions and ground truth pitches*
- `plot_surprise_with_pianoroll.py`: *make the figure(s) of surprise values aligned with piano roll reference.*
- `outputs_in_mat_format.py`: *output the data in .mat format.*
- `data_extractor.py`: *helper script to extract the data we are interested in from .dat file*

- dataset/:
    -  a bunch of folders containing midi files.
- lisp/:
    - ```compute.lisp``` *the lisp code to set and run the parameters of IDyOM*
    - ```parser.py```
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
        - plot_pitch_prediction_comparison/
            - ~.esp: *comparison figures of predicted pitch distributions and ground truth pitches*
        - plot_surprise_with_pianoroll/
            - ~.esp: *figures of surprise values aligned with piano roll reference*
        - mat_data_outputs/
            - ~.mat: *data output files in .mat format*