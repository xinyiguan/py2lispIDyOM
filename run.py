import os
import numpy as np
import shutil
import datetime
from glob import glob
from configuration import configurations


def initialize_experiment_folder(configurations):
	"""
	initialize a folder according to configuration to record information/data for each experiment.
	folder directory is specified by configuration
	This folder has the following file structure:
	- configurations.py (a python file containing the configuration dictionary)
	- experiment_input_data_folder/
		- train/
			- ~.mid
		- test/
			- ~.mid
	- experiment_output_data_folder/
		- ~.dat
	"""

	experiment_history_folder = configurations['experiment_history_folder']
	if not os.path.exists(experiment_history_folder):
		os.makedirs(experiment_history_folder)

	# create experiment record folder
	today_date = datetime.date.today()
	now_time = datetime.datetime.now()
	this_experiment_folder = experiment_history_folder+today_date.strftime('%m-%d-%y')+'_'+now_time.strftime('%H.%M.%S')+'/'
	os.makedirs(this_experiment_folder)

	## storge the configuration of this experiment
	file = open(this_experiment_folder + 'configurations.py', 'w')
	file.write(str(configurations))

	## create input data folder
	input_data_folder = this_experiment_folder+'experiment_input_data_folder/'
	train_folder = input_data_folder+"train/"
	test_folder = input_data_folder+"test/"

	os.makedirs(input_data_folder)
	os.makedirs(train_folder)
	os.makedirs(test_folder)

	### record input data =================================================================
	"""
	(old version: prior to 06/28/2021)
	"""

	# paths = configurations['train_test_path']
	# def split_dataset(dataset_folder_path, trainp):
	# 	files = []
	# 	for file in glob(dataset_folder_path+'*'):
	# 		if file[file.rfind("."):] == ".mid":  # we are only using midi files.
	# 			files.append(file)
	# 	np.random.shuffle(files)
	# 	train = files[:int(trainp * len(files))]
	# 	test = files[int(trainp * len(files)):]
	# 	return train, test
	#
	# if len(paths) == 2:
	# 	print('using distinct training and test paths')
	# 	train_path = paths[0]
	# 	test_path = paths[1]
	# 	train=split_dataset(train_path,1)[0]
	# 	test=split_dataset(test_path,1)[0]
	#
	# elif len(paths) == 1:
	# 	print('splitting dataset')
	# 	trainp = configurations['trainp']
	# 	dataset_folder_path = paths[0]
	# 	train,test = split_dataset(dataset_folder_path, trainp)

	### end of old version =================================================================

	### Record input data ==================================================================
	"""
	new version implemented on 06/28/2021
	"""
	train_path = configurations['train_path']
	test_path = configurations['test_path']

	def get_files_from_paths(path):
		files = []
		for file in glob(path+'*'):
			if file[file.rfind("."):] == ".mid":  # we are only using midi files.
				files.append(file)
		return files

	def put_midis_in_folder(files,folder_path):
		for file in files:
			shutil.copyfile(file, folder_path + file[file.rfind("/"):])

	if train_path is None:
		pass
		print("No training set detected. Possibly using STM.")
	else:
		train = get_files_from_paths(train_path)
		print("Loaded training set")
		put_midis_in_folder(train, train_folder)
		print("Put training midi files in folder")
	test = get_files_from_paths(test_path)
	print("Loaded test set")
	put_midis_in_folder(test, test_folder)
	print("Put test midi files in folder")

	### end of new version =================================================================


	##create output data folder
	output_data_folder = this_experiment_folder + 'experiment_output_data_folder/'
	os.makedirs(output_data_folder)
	print('** Successfully created experiment folder! **')
	return this_experiment_folder


## Modify LISP code template:
""""
New version implemented on 06/28/2021.
"""

def modify_temp_lisp_file_to_run(orginal_lisp_file,experiment_folder_path):
	input_data_folder = experiment_folder_path+'experiment_input_data_folder/'
	TRAINFOLDER = input_data_folder+"train/"
	TESTFOLDER = input_data_folder+"test/"
	DATAOUPUT = experiment_folder_path+'experiment_output_data_folder/'
	today_date = datetime.date.today()
	now_time = datetime.datetime.now()
	moment = today_date.strftime('%m%d%y')+now_time.strftime('%H%M%S')
	TRAINID= '66'+moment
	TESTID= '99'+ moment
	MODELTYPE = configurations['model_type']
	TARGETVIEWPOINTS = configurations['target_viewpoints']
	SOURCEVIEWPOINTS = configurations['source_viewpoints']
	RESAMPLENUMBER = configurations['k_number_of_resampling']

	substitutions = {
		'TRAINFOLDER': TRAINFOLDER,    # make change of dataset here: folder of dataset
		'TESTFOLDER': TESTFOLDER,
		'DATASETTITLE': 'My selected data',	#set Name of Dataset here
		'DATAOUTPUT': '\"'+DATAOUPUT+'\"',
		'TRAINID': TRAINID,
		'TESTID': TESTID,
		'MODELTYPE': MODELTYPE,
		'TARGETVIEWPOINTS': TARGETVIEWPOINTS,
		'SOURCEVIEWPOINTS': SOURCEVIEWPOINTS,
		'RESAMPLENUMBER': RESAMPLENUMBER,

	}
	find_upper_level = lambda path: path[:path.rfind("/")+1]
	temp_path = find_upper_level(orginal_lisp_file)+"compute_temp.lisp"
	shutil.copy(orginal_lisp_file,temp_path)
	def replaceinFile(file, substitutions):
		s = open(file).read()
		for key in substitutions.keys():
			tochange = key
			out = substitutions[key]
			s = s.replace(tochange, out)
		f = open(file, "w")
		f.write(s)
		f.close()
	replaceinFile(temp_path,substitutions)
	print('** Created and modified temp lisp file **')
	return temp_path

def general_modify_temp_lisp_file_to_run(orginal_lisp_file,experiment_folder_path):
	input_data_folder = experiment_folder_path+'experiment_input_data_folder/'
	TRAINFOLDER = input_data_folder+"train/"
	TESTFOLDER = input_data_folder+"test/"
	DATAOUTPUT = experiment_folder_path+'experiment_output_data_folder/'
	today_date = datetime.date.today()
	now_time = datetime.datetime.now()
	moment = today_date.strftime('%m%d%y')+now_time.strftime('%H%M%S')
	TRAINID= '66'+moment
	TESTID= '99'+ moment
	MODELTYPE = configurations['model_type']
	TARGETVIEWPOINTS = configurations['target_viewpoints']
	SOURCEVIEWPOINTS = configurations['source_viewpoints']
	RESAMPLENUMBER = configurations['k_number_of_resampling']

	substitutions = {
		'script_import_train':'idyom-db:import-data :mid \"{}\" \"Train\" {}'.format(TRAINFOLDER,TRAINID),
		'script_import_test':'idyom-db:import-data :mid \"{}\" \"Test\" {}'.format(TESTFOLDER,TESTID),
		'script_configure_model':'idyom:idyom {} \'({}) \'({}) :models :{} :pretraining-ids \'({}) :k {} :detail 3 :output-path \"{}\" :overwrite t'.format(TESTID,TARGETVIEWPOINTS,SOURCEVIEWPOINTS,MODELTYPE,TRAINID,RESAMPLENUMBER,DATAOUTPUT),
	}

	def change_substitution():
		if MODELTYPE == 'stm':
			substitutions['script_import_train'] = ''
			substitutions['script_configure_model'] = 'idyom:idyom {} \'({}) \'({}) :models :{} :k {} :detail 3 :output-path \"{}\" :overwrite t'.format(TESTID,TARGETVIEWPOINTS,SOURCEVIEWPOINTS,MODELTYPE,RESAMPLENUMBER,DATAOUTPUT)

	change_substitution()


	find_upper_level = lambda path: path[:path.rfind("/")+1]
	temp_path = find_upper_level(orginal_lisp_file)+"compute_temp.lisp"
	shutil.copy(orginal_lisp_file,temp_path)
	def replaceinFile(file, substitutions):
		s = open(file).read()
		for key in substitutions.keys():
			tochange = key
			out = substitutions[key]
			s = s.replace(tochange, out)
		f = open(file, "w")
		f.write(s)
		f.close()
	replaceinFile(temp_path,substitutions)
	print('** Created and modified temp lisp file **')
	return temp_path

def runLisp(lisp_file_path):
	"""use shell to run IDyOM LISP code """
	print('** running lisp **')
	os.system("sbcl --noinform --load "+ lisp_file_path)
	print(' ')
	print('** we got here! done! **')



this_experiment_folder = initialize_experiment_folder(configurations)
lispfile_to_read = 'lisp/compute_general.lisp'
lispfile_to_run = general_modify_temp_lisp_file_to_run(orginal_lisp_file=lispfile_to_read,experiment_folder_path=this_experiment_folder)
runLisp(lispfile_to_run)


def RunJupyterExperiment(configurations):
	this_experiment_folder = initialize_experiment_folder(configurations)
	lispfile_to_read = 'lisp/compute.lisp'
	lispfile_to_run = modify_temp_lisp_file_to_run(orginal_lisp_file=lispfile_to_read,experiment_folder_path=this_experiment_folder)
	runLisp(lispfile_to_run)
