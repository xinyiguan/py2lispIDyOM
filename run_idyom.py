import os
import shutil
import datetime
from glob import glob
import configuration


def initialize_experiment_folder(experiment_history_folder):

    if not os.path.exists(experiment_history_folder):
        os.makedirs(experiment_history_folder)

    # create experiment record folder
    today_date = datetime.date.today()
    now_time = datetime.datetime.now()
    this_experiment_folder = experiment_history_folder + today_date.strftime('%m-%d-%y') + '_' + now_time.strftime(
        '%H.%M.%S') + '/'
    os.makedirs(this_experiment_folder)

    ## create input data folder
    input_data_folder = this_experiment_folder + 'experiment_input_data_folder/'
    train_folder = input_data_folder + "train/"
    test_folder = input_data_folder + "test/"

    os.makedirs(input_data_folder)
    os.makedirs(train_folder)
    os.makedirs(test_folder)

    ## Record input data =====================
    train_path = configuration.TrainingParameters.pretraining_dataset
    test_path = configuration.RequiredParameters.dataset_path

    def get_files_from_paths(path):
        files = []
        for file in glob(path + '*'):
            if file[file.rfind("."):] == ".mid":  # we are only using midi files.
                files.append(file)
        return files

    def put_midis_in_folder(files, folder_path):
        for file in files:
            shutil.copyfile(file, folder_path + file[file.rfind("/"):])

    if train_path is None:
        pass
        print("** No training set detected. Possibly using STM.**")
    else:
        train = get_files_from_paths(train_path)
        print(" ** Loaded training set **")
        put_midis_in_folder(train, train_folder)
        print("** Put training midi files in experiment history folder **")
    test = get_files_from_paths(test_path)
    print("** Loaded test set **")
    put_midis_in_folder(test, test_folder)
    print("** Put test midi files in experiment history folder **")

    ## create output data folder
    output_data_folder = this_experiment_folder + 'experiment_output_data_folder/'
    os.makedirs(output_data_folder)
    print('** Successfully created experiment folder! **')
    return this_experiment_folder


# def generate_IDyOM_LISP_script(outpath):
#     IDyOM_Lisp_script = open('./experiment_history.IDyOM_Lisp_script.lisp', 'w')
#     lisp_start_idyom = '(start-idyom)'
#     lisp_import_test_dataset =
#
#     IDyOM_Lisp_script.write(lisp_script)


# def runLisp(lisp_file_path):
#     """use shell to run IDyOM LISP code """
#     print('** running lisp **')
#     os.system("sbcl --noinform --load " + lisp_file_path)
#     print(' ')
#     print('** we got here! done! **')

if __name__ == '__main__':
    initialize_experiment_folder(experiment_history_folder='new_exp_folder')
