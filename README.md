# A python interface for LISP IDyOM 

Last version update: Mar 5, 2021

Library dependency:
   - numpy
   - matplotlib
   - scipy
   - tqdm 
    

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
                        
## Usage Overview (brief version)

1. Change the ```configuration.py``` script to specify the training-set folder and test-set folder for our experiment.
2. Run ```run.py``` to run LISP version of IDyOM
3. Run the all-in-one ```main_analysis.py``` script to get the model outputs in ```.mat``` format and different visualizations.
**OR** You can run the three scripts (`plot_pitch_prediction_comparison.py`, 
`plot_surprise_with_pianoroll.py`, and
`outputs_in_mat_format.py`) to get the outputs separately.


 ## How to use (detailed version):
 
 ### 0. (*Optional*) Data preprocessing: 
 - As IDyOM is limited to the monodic melodic music, we first need to extract the melodic line from the MIDI
 files, if the MIDI has multiple parts. Refer to the `MIDI_MelodyExtractionTutorial.ipynb` for how to extract
 the melodic line from MIDI. 
 
 
 ### 1. Set/change the configurations in ```configuration.py```:

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
train_bach_test_shanx = {
	'experiment_history_folder':'experiment_history/',
	'train_test_path': [
		'./dataset/bach_dataset/',
		'./dataset/shanx_dataset/',
		],
	'trainp': None,
	'experiment_name' : 'train_bach_test_shanx'
}
```


 ### 2. Run the ```run.py```. 
 This step is to load and run the LISP version of IDyOM.


##### What happens when you run ```run.py```?

- A folder (timestamp naming format: MM/DD/YY_HH.MM.SS) will be created to record information of the current experiment,
including the following:
    - the configuration file ((a script containing info of the configurations we set for this experiment))
    - the dataset input named 'experiment_input_data_folder' (duplicated from original path, which is specifiable in the ```configuration.py```)
    - the output from IDyOM named 'experiment_output_data_folder' (containing the ```.dat``` file)
    
                  
 [Comments:] *By creating an 'experiment_history' folder, we can have a record of all data and information used and the output for this experiment.
 In this way, we can have a better control over what dataset we want the model to train on and test on, 
 and we can have a record of the information we can check if we have any doubts of the output of the model.*
 
 
 ### 3. Get the model outputs in different file formats. 
 
 To get the model outputs in different formats, you can either 
   - 3.1: run the ```main_analysis.py```, or 
   
   - 3.2: run `plot_pitch_prediction_comparison.py`, `plot_surprise_with_pianoroll.py`, and `outputs_in_mat_format.py` individually. 


 #### 3.1 Run the all-in-one script (```main_analysis.py```)

*You only need to manually change the path of ```selected_experiment_history_folder``` to your desired one in this script.*
 
Outputs of ```main_analysis.py```: (3 folders)

- "mat_data_outputs" folder, containing the model output data in .mat file format (with current setting, there are 4 mat files within the folder)
- "plot_pitch_prediction_comparison" folder, containing all pitch prediction vs. ground truth figures.
- "plot_surprise_with_pianoroll" folder, containing all surprise value aligned with piano roll figures. 

```main_analysis.py``` is an integrated script that runs the 3 other scripts/modules simultaneously:
`plot_pitch_prediction_comparison.py`, 
`plot_surprise_with_pianoroll.py`, and 
`outputs_in_mat_format.py`. 


##### - Notes on `outputs_in_mat_format.py`: 

The current setting for the model outputs in ```.mat ``` file format are: 

- 'melody_name'
- 'surprise'
- 'aligned_surprise_with_pitch'
- 'aligned_surprise_with_onset'

You can extract different model outputs by changing/adding different "extraction methods" in the dictionary called 
```features_method_name_dict```, and modifying the following ```my_choice_of_extraction``` accordingly in the `outputs_in_mat_format.py` script. 


#### 3.2 Run the modules and get the different outputs individually:

*You need to change the ```selected_experiment_history_folder``` at the bottom of the script to your desired one in each script.*

Example for the `outputs_in_mat_format.py`: (same for the other two)

```
# Pass your desired 'selected_experiment_history_folder' below:
if __name__ == '__main__':
    selected_experiment_history_folder = 'experiment_history/03-06-21_13.29.27/'
    export_mat_from_history_folder(selected_experiment_history_folder)
``` 






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