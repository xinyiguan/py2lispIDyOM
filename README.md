# A python interface for IDyOM 

Last version update: Jun 28, 2021

This project provides a python interface for IDyOM model by Marcus Pearce. 

Need to install IDyOM first. Follow instructions here: https://github.com/mtpearce/idyom/wiki/Installation 

Python library dependency:
   - numpy
   - matplotlib
   - scipy
   - tqdm
   - mido
 
                        
## Usage Steps Overview (brief version):

1. Define inputs and set the model configurations for your experiment in the ```configuration.py``` script.
2. Execute ```run.py``` to run LISP version of IDyOM.
3. (optional) Run the all-in-one ```main_analysis.py``` script to get the model outputs in ```.mat``` format and different visualizations.

    **OR** run the following three scripts to get the outputs separately: 

    - `plot_pitch_prediction_comparison.py`, 
    - `plot_surprise_with_pianoroll.py`, 
    - `outputs_in_mat_format.py` 
   


 ## Usage Steps (detailed version):
 
 ### 0. (*Optional*) Data preprocessing: 
 
Notes: 

 1. As IDyOM is limited to the monodic melodic music, you may want to extract the melodic line from the MIDI
 files, if the MIDI has multiple parts. Refer to the `MIDI_MelodyExtractionTutorial.ipynb` for how to extract
 the melodic line from MIDI. 
 
 2. The file names for each input MIDI files should **NOT** contain space.
 
 
 ### 1. Define Inputs and Set Parameters
 
In the ```configuration.py``` script, define your input datasets and set the model configurations for your experiment by following the template.

**Example:** 

```
both_train_bach_test_shanxi = {
	'train_path': '/Users/xinyiguan/Desktop/Codes/IDyOM_Python_Interface/dataset/bach_dataset/',
	'test_path': '/Users/xinyiguan/Desktop/Codes/IDyOM_Python_Interface/dataset/shanx_dataset/',
	'model_type': 'both',
	'target_viewpoints': 'cpitch onset',
	'source_viewpoints': 'cpitch onset',
	'k_number_of_resampling': '1',
	'experiment_history_folder': 'experiment_history/',
	'experiment_name': 'both_train_bach_test_shanx',
}
```



 ### 2. Execute the ```run.py```. 
 This step is to load and run the LISP version of IDyOM.

In your terminal, type the following code:


    python run.py


##### What happens when you run ```run.py```?

- A folder (timestamp naming format: MM/DD/YY_HH.MM.SS) will be created to record information of the current experiment,
including the following:
    - the configuration file ((a script containing info of the configurations we set for this experiment))
    - the dataset input named 'experiment_input_data_folder' (duplicated from original path, which is specifiable in the ```configuration.py```)
    - the output from IDyOM named 'experiment_output_data_folder' (containing the ```.dat``` file)
    
                  
 [Comments:] *The 'experiment_history' folder contains all data and information used and the outputs for each of the current experiment. 
 It should have all the necessary details to replicate the same experiments if needed.*
 
 
 ### 3. Get the model outputs in mat file format and different visualizations. 
 
 All data outputs here are extracted from the .dat file. 
 
 ##### 1. Get the model outputs in mat file format
 
  - To get the model outputs in mat file format, jump to the **helper_scripts/outputs_in_mat_format.py** script.
  
  - Pass the absolute path of the your desired experiment_history folder for the `selected_experiment_history_folder`
  
  - The current implementation for the model outputs in `.mat` file format are the melodic names, 3 overall metrics and 4 melodic expectation features :
    - melody_name,
    - overall_probability,
    - overall_information_content,
    - overall_entropy,
    - cpitch_information_content,
    - cpitch_entropy,
    - onset_information_content,
    - onset_entropy,
  
  You can extract different model outputs by changing/adding different "extraction methods" in the dictionary called `features_method_name_dict`, 
  and modifying the following `my_choice_of_extraction` accordingly in the `outputs_in_mat_format.py` script.
  
 
 ##### 2. Get outputs visualizations
 
   - To get the model outputs visualizations, jump to the **helper_scripts/plot_pitch_prediction_comparison.py** and **helper_scripts/plot_surprise_with_pianoroll.py** scripts.
  
 #### You can also get 1 &2 with the all-in-one script (```main_analysis.py```)

   - You only need to manually change the path of ```selected_experiment_history_folder``` to your desired one in this script.
 
```main_analysis.py``` is an integrated script that runs the 3 other scripts/modules simultaneously:
`plot_pitch_prediction_comparison.py`, 
`plot_surprise_with_pianoroll.py`, and 
`outputs_in_mat_format.py`. 

You will find all output files within the corresponding experiment history folder.

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