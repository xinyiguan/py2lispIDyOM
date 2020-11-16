"""
configurations_template = {
	'experiment_history_folder':'path to save the experiment history',
	'train_test_path':[
		'your train folder',
		'your test folder',
		], # if same, leave the second empty
	'trainp': ... # if train & test from same folder, specify split rate (#train/#total)
}
"""


bach_dataset = './dataset/bach_dataset/'
shanx_dataset = './dataset/shanx_dataset/'

train_bach_test_bach = {
	'experiment_history_folder':'experiment_history/',
	'train_test_path':[
		bach_dataset,
		],
	'trainp':0.8,
}

train_bach_test_shanx = {
	'experiment_history_folder':'experiment_history/',
	'train_test_path':[
		bach_dataset,
		shanx_dataset,
		],
	'trainp':None,
}

train_shanx_test_bach = {
	'experiment_history_folder':'experiment_history/',
	'train_test_path':[
		shanx_dataset,
		bach_dataset,
		],
	'trainp':None,
}

train_shanx_test_shanx = {
	'experiment_history_folder':'experiment_history/',
	'train_test_path':[
		shanx_dataset,
		],
	'trainp':0.8,
}

train_intentional_overfit_on_bach = {
	'experiment_history_folder':'experiment_history/',
	'train_test_path':[
		bach_dataset,
		bach_dataset,
		],
	'trainp':None,
}

testing_config = {
	'experiment_history_folder':'experiment_history/',
	'train_test_path':[
		'./dataset/bach_dataset/',
		'./dataset/shanx_dataset/',
		],
	'trainp':None,
}


configurations = testing_config