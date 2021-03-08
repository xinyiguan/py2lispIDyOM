"""
configurations_template = {
	'experiment_history_folder':'path to save the experiment history',
	'train_test_path':[
		'your train folder',
		'your test folder',
		], # if same, leave the second empty
	'trainp': ... # if train & test from same folder, specify split rate (#train/#total)
	'experiment_name': ... # Name your experiment for later reference
}
"""


bach_dataset = './dataset/bach_dataset/'
shanx_dataset = './dataset/shanx_dataset/'

train_bach_test_bach = {
	'experiment_history_folder': 'experiment_history/',
	'train_test_path': [
		bach_dataset,
		],
	'trainp': 0.8,
	'experiment_name': 'train_bach_test_bach'
}

train_bach_test_shanx = {
	'experiment_history_folder':'experiment_history/',
	'train_test_path': [
		bach_dataset,
		shanx_dataset,
		],
	'trainp': None,
	'experiment_name' : 'train_bach_test_shanx'
}

train_shanx_test_bach = {
	'experiment_history_folder':'experiment_history/',
	'train_test_path': [
		shanx_dataset,
		bach_dataset,
		],
	'trainp': None,
}

train_shanx_test_shanx = {
	'experiment_history_folder': 'experiment_history/',
	'train_test_path': [
		shanx_dataset,
		],
	'trainp': 0.8,
}

train_intentional_overfit_on_bach = {
	'experiment_history_folder':'experiment_history/',
	'train_test_path': [
		bach_dataset,
		bach_dataset,
		],
	'trainp': None,
}

mixed2 = '/Users/guan/LocalMusicDataset/mixed2/'
midi1 = '/Users/guan/LocalMusicDataset/midi1/'
midi2 = '/Users/guan/LocalMusicDataset/midi2/'
midi3 = '/Users/guan/LocalMusicDataset/midi3/'
midi4 = '/Users/guan/LocalMusicDataset/midi4/'
midi5 = '/Users/guan/LocalMusicDataset/midi5/'
smallmixed2 = '/Users/guan/LocalMusicDataset/smallmixed2/'
smallmidi = '/Users/guan/LocalMusicDataset/smallmidi/'

train_smallmixed2_test_smallmidi = {
	'experiment_history_folder':'experiment_history/',
	'train_test_path': [
		smallmixed2,
		smallmidi,
		],
	'trainp': None,
	'experiment_name': 'train_smallmixed2_test_smallmidi'
}

train_mixed2_test_midi1 = {
	'experiment_history_folder':'experiment_history/',
	'train_test_path': [
		mixed2,
		midi1,
		],
	'trainp': None,
	'experiment_name': 'train_mixed2_test_midi1',
}

train_mixed2_test_midi2 = {
	'experiment_history_folder':'experiment_history/',
	'train_test_path': [
		mixed2,
		midi2,
		],
	'trainp': None,
	'experiment_name': 'train_mixed2_test_midi2',
}

train_mixed2_test_midi3 = {
	'experiment_history_folder':'experiment_history/',
	'train_test_path': [
		mixed2,
		midi3,
		],
	'trainp': None,
	'experiment_name': 'train_mixed2_test_midi3',
}

train_mixed2_test_midi4 = {
	'experiment_history_folder':'experiment_history/',
	'train_test_path': [
		mixed2,
		midi4,
		],
	'trainp': None,
	'experiment_name': 'train_mixed2_test_midi4',
}

train_mixed2_test_midi5 = {
	'experiment_history_folder':'experiment_history/',
	'train_test_path': [
		mixed2,
		midi5,
		],
	'trainp': None,
	'experiment_name': 'train_mixed2_test_midi5',
}


configurations = train_bach_test_shanx