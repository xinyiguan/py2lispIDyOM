"""
configurations_template = {
	'train_path': ,  # absolute path to training set
	'test_path': , # absolute path to test set
	'model_type': 'both', # avaialble type: stm, ltm, ltm+, both, both+
	'target_viewpoints': 'cpitch onset',
	'source_viewpoints': 'cpitch onset',
	'k_number_of_resampling': '1',
	'experiment_history_folder': 'experiment_history/',
	'experiment_name': 'specify your experiment name here',
}
"""


bach = '/Users/guan/Desktop/Codes/IDyOM_Python_Interface/dataset/bach_dataset/'
shanx = '/Users/guan/Desktop/Codes/IDyOM_Python_Interface/dataset/shanx_dataset/'


both_train_bach_test_shanxi = {
	'train_path': bach,
	'test_path': shanx,
	'model_type': 'both',
	'target_viewpoints': 'cpitch onset',
	'source_viewpoints': 'cpitch onset',
	'k_number_of_resampling': '1',
	'experiment_history_folder': 'experiment_history/',
	'experiment_name': 'both_train_bach_test_shanx',
}

stm_test_shanxi = {
	'train_path': None,
	'test_path': shanx,
	'model_type': 'stm',
	'target_viewpoints': 'cpitch',
	'source_viewpoints': 'cpitch',
	'k_number_of_resampling': '1',
	'experiment_history_folder': 'experiment_history/',
	'experiment_name': 'stm_test_shanx',
}


configurations = stm_test_shanxi