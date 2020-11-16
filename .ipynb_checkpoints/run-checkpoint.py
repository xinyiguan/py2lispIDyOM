import os
import numpy as np
import shutil
import datetime
import matplotlib.pyplot as plt
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

	### record input data
	paths = configurations['train_test_path']
	def split_dataset(dataset_folder_path, trainp):
		files = []
		for file in glob(dataset_folder_path+'*'):
			if file[file.rfind("."):] == ".mid":  # we are only using midi files.
				files.append(file)
		np.random.shuffle(files)
		train = files[:int(trainp * len(files))]
		test = files[int(trainp * len(files)):]
		return train, test

	if len(paths) == 2:
		print('using distinct trainning and test paths')
		train_path = paths[0]
		test_path = paths[1]
		train=split_dataset(train_path,1)[0]
		test=split_dataset(test_path,1)[0]

	elif len(paths) == 1:
		print('splitting dataset')
		trainp = configurations['trainp']
		dataset_folder_path = paths[0]
		train,test = split_dataset(dataset_folder_path, trainp)

	def put_midis_in_folder(files,folder_path):
		for file in files:
			shutil.copyfile(file, folder_path + file[file.rfind("/"):])

	put_midis_in_folder(train,train_folder)
	put_midis_in_folder(test,test_folder)

	##create output data folder
	output_data_folder = this_experiment_folder + 'experiment_output_data_folder/'
	os.makedirs(output_data_folder)
	print('** Succesfully created experiment folder! **')
	return this_experiment_folder

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
	substitutions = {
		'TRAINFOLDER': TRAINFOLDER,    # make change of dataset here: folder of dataset
		'TESTFOLDER': TESTFOLDER,
		'DATASETTITLE': 'My selected data',	#set Name of Dataset here
		'DATAOUTPUT': '\"'+DATAOUPUT+'\"',
		'TRAINID': TRAINID,
		'TESTID': TESTID,
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

def runLisp(lisp_file_path):
	"""use Shell to run IDyOM LISP code """
	print('** running lisp **')
	os.system("sbcl --noinform --load "+ lisp_file_path)
	print(' ')
	print('** we got here! done! **')



this_experiment_folder = initialize_experiment_folder(configurations)
lispfile_to_read = 'lisp/compute.lisp'
lispfile_to_run = modify_temp_lisp_file_to_run(orginal_lisp_file=lispfile_to_read,experiment_folder_path=this_experiment_folder)
runLisp(lispfile_to_run)


def RunJupyterExperiment(configurations):
    this_experiment_folder = initialize_experiment_folder(configurations)
    lispfile_to_read = 'lisp/compute.lisp'
    lispfile_to_run = modify_temp_lisp_file_to_run(orginal_lisp_file=lispfile_to_read,experiment_folder_path=this_experiment_folder)
    runLisp(lispfile_to_run)







