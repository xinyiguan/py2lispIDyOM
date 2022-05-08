from __future__ import annotations

import datetime
import os
import shutil
from dataclasses import dataclass, field
from glob import glob
from natsort import natsorted
from parameters import *


def get_timestamp():
    today_date = datetime.date.today()
    now_time = datetime.datetime.now()
    moment = today_date.strftime('%m%d%y') + now_time.strftime('%H%M%S')
    return moment

@dataclass
class ExperimentLogger:
    test_dataset_path: str
    pretrain_dataset_path: str
    experiment_history_folder_path: str

    def __post_init__(self):

        self.experiment_history_folder = self.generate_experiment_history_folder()
        self.this_exp_folder = self.generate_this_exp_folder()
        self.input_data_exp_folder = self.generate_input_data_exp_folder()
        self.test_dataset_exp_folder = self.generate_test_dataset_exp_folder()
        self.train_dataset_exp_folder = self.generate_pretrain_dataset_exp_folder()
        self.output_data_exp_folder = self.generate_output_data_exp_folder()

    def generate_experiment_history_folder(self):
        if self.experiment_history_folder_path is None:
            experiment_history_folder = 'experiment_history/'
            if not os.path.exists(experiment_history_folder):
                os.makedirs(experiment_history_folder)
        else:
            experiment_history_folder = self.experiment_history_folder_path
        return experiment_history_folder

    def generate_this_exp_folder(self):
        today_date = datetime.date.today()
        now_time = datetime.datetime.now()
        this_experiment_folder = self.experiment_history_folder + today_date.strftime(
            '%d-%m-%y') + '_' + now_time.strftime(
            '%H.%M.%S') + '/'
        os.makedirs(this_experiment_folder)
        return this_experiment_folder

    def generate_input_data_exp_folder(self):
        input_data_folder = self.this_exp_folder + 'experiment_input_data_folder/'
        os.makedirs(input_data_folder)
        return input_data_folder

    def generate_test_dataset_exp_folder(self):
        input_data_folder = self.input_data_exp_folder
        test_folder = input_data_folder + 'test_dataset/'
        os.makedirs(test_folder)
        print("** Putting Test dataset files in experiment history folder. **")
        test_dataset_path = self.test_dataset_path
        test = self._get_files_from_paths(test_dataset_path)
        self._put_midis_in_folder(test, test_folder)
        return test_folder

    def generate_pretrain_dataset_exp_folder(self):
        pretrain_dataset_path = self.pretrain_dataset_path
        if pretrain_dataset_path is None:
            pass
            print('** No pretraining dataset detected. **')
        else:
            input_data_folder = self.input_data_exp_folder
            pretrain_folder = input_data_folder + 'pretrain_dataset/'
            os.makedirs(pretrain_folder)
            print("** Putting Pretraining dataset files in experiment history folder. **")
            train = self._get_files_from_paths(pretrain_dataset_path)
            self._put_midis_in_folder(train, pretrain_folder)
            return pretrain_folder

    def _get_files_from_paths(self, path):  # only two types files allowed: midi and kern
        files = []
        for file in glob(path + '*'):
            if file[file.rfind("."):] == ".mid" or ".krn":
                files.append(file)
        return natsorted(files)

    def _put_midis_in_folder(self, files, folder_path):
        for file in files:
            shutil.copyfile(file, folder_path + file[file.rfind("/"):])

    def put_test_midi_in_exp_folder(self):
        print("** Putting Test dataset files in experiment history folder. **")
        test_files = self._get_files_from_paths(self.test_dataset_path)
        self._put_midis_in_folder(test_files, self.test_dataset_exp_folder)

    def put_train_midi_in_exp_folder(self):
        if self.pretrain_dataset_path is None:
            pass
            print('** No pretraining dataset detected. **')
        else:
            print("** Putting pretrain dataset files in experiment history folder. **")
            train = self._get_files_from_paths(self.pretrain_dataset_path)
            self._put_midis_in_folder(train, self.train_dataset_exp_folder)

    def generate_output_data_exp_folder(self):
        output_data_folder = self.this_exp_folder + 'experiment_output_data_folder/'
        os.makedirs(output_data_folder)
        return output_data_folder


class Configuration(Parameters):
    pass


@dataclass(repr=False)
class RunModelConfiguration(Configuration):
    this_exp_log_path: str
    test_dataset_id: str
    pretrain_dataset_id: str

    output_parameters: OutputParameters
    required_parameters: RequiredParameters = field(default_factory=RequiredParameters)
    statistical_modelling_parameters: StatisticalModellingParameters = field(
        default_factory=StatisticalModellingParameters)
    training_parameters: TrainingParameters = field(default_factory=TrainingParameters)
    viewpoint_selection_parameters: ViewpointSelectionParameters = field(default_factory=ViewpointSelectionParameters)
    caching_parameters: CachingParameters = field(default_factory=CachingParameters)

    def __post_init__(self):
        # after inherit the dataset ids from the IDyOMConfiguration class,
        # update ids of the required_param and train_param here

        self.required_parameters = RequiredParameters(dataset_id=self.test_dataset_id)
        self.training_parameters = TrainingParameters(pretraining_id=self.pretrain_dataset_id)

        # post init here because we want to update the out path in lisp script
        self.output_parameters = OutputParameters(output_path=self.this_exp_log_path + 'experiment_output_data_folder/')

    def to_lisp_command(self) -> str:
        # assert self.required_parameters._is_available(), self.required_parameters
        all_parameters = [
            self.required_parameters,
            self.statistical_modelling_parameters,
            self.training_parameters,
            self.viewpoint_selection_parameters,
            self.output_parameters,
            self.caching_parameters,
        ]
        subcommands = [parameters.to_lisp_command() for parameters in all_parameters]
        non_empty_subcommands = [x for x in subcommands if x != '']
        joined_commands = ' '.join(non_empty_subcommands)
        command = f'(idyom:idyom {joined_commands})'
        return command


@dataclass(repr=False)
class DatabaseConfiguration(Configuration):
    this_exp_log_path: str
    test_dataset_id: str
    pretrain_dataset_id: str = None
    test_dataset_Name: str = 'TEST_DATASET'
    pretrain_dataset_Name: str = 'PRETRAIN_DATASET'

    def __post_init__(self):
        self.test_dataset_log_path = self.this_exp_log_path + 'experiment_input_data_folder/test_dataset/'
        self.train_dataset_log_path = self.this_exp_log_path + 'experiment_input_data_folder/pretrain_dataset/'

    def get_music_files_type(self, path) -> str:
        for file in glob(path + '*'):
            if file[file.rfind("."):] == ".mid":
                return str('mid')
            if file[file.rfind("."):] == ".krn":
                return str('krn')
            else:
                print('Music file type unsupported. Please use either midi files or kern files.')

    def _oneline_import_db_to_lisp_command(self, file_type, Path, Name, ID) -> str:
        subcommands = [f':{file_type}', f'\"{Path}\"', f'\"{Name}\"', ID]
        non_empty_subcommands = [x for x in subcommands if x != '']
        joined_commands = ' '.join(non_empty_subcommands)
        command = f'(idyom-db:import-data {joined_commands})'
        return command

    def _get_command_import_db(self, path, dataset_name, dataset_id):
        file_type = self.get_music_files_type(path)
        command_import_testdb = self._oneline_import_db_to_lisp_command(file_type=file_type,
                                                                        Path=path,
                                                                        Name=dataset_name,
                                                                        ID=dataset_id)
        return command_import_testdb

    def get_command_import_testdb(self):
        command = self._get_command_import_db(path=self.test_dataset_log_path, dataset_name=self.test_dataset_Name,
                                              dataset_id=self.test_dataset_id)
        return command

    def get_command_import_traindb(self):
        command = self._get_command_import_db(path=self.train_dataset_log_path, dataset_name=self.pretrain_dataset_Name,
                                              dataset_id=self.pretrain_dataset_id)
        return command

    def to_lisp_command_import_testdb(self) -> str:
        return self.get_command_import_testdb()

    def to_lisp_command_import_traindb(self) -> str:
        return self.get_command_import_traindb()

    # def to_lisp_command(self) -> str:
    #     commands = [
    #         self.get_command_import_testdb(),
    #         self.get_command_import_traindb(),
    #     ]
    #     total_command = '\n'.join(commands)
    #     return total_command


@dataclass
class IDyOMConfiguration:
    required_parameters: RunModelConfiguration.required_parameters
    statistical_modelling_parameters: RunModelConfiguration.statistical_modelling_parameters
    training_parameters: RunModelConfiguration.training_parameters
    viewpoint_selection_parameters: RunModelConfiguration.viewpoint_selection_parameters
    output_parameters: RunModelConfiguration.output_parameters
    caching_parameters: RunModelConfiguration.caching_parameters

    this_exp_log_path: str
    test_dataset_path: str
    test_dataset_id: str
    pretrain_dataset_path: str
    pretrain_dataset_id: str

    def __post_init__(self):

        self.database_configuration = DatabaseConfiguration(this_exp_log_path=self.this_exp_log_path,
                                                            pretrain_dataset_id=self.pretrain_dataset_id,
                                                            test_dataset_id=self.test_dataset_id
                                                            )

        self.run_model_configuration = RunModelConfiguration(required_parameters=self.required_parameters,
                                                             statistical_modelling_parameters=self.statistical_modelling_parameters,
                                                             training_parameters=self.training_parameters,
                                                             viewpoint_selection_parameters=self.viewpoint_selection_parameters,
                                                             output_parameters=self.output_parameters,
                                                             caching_parameters=self.caching_parameters,
                                                             this_exp_log_path=self.this_exp_log_path,
                                                             test_dataset_id=self.test_dataset_id,
                                                             pretrain_dataset_id=self.pretrain_dataset_id
                                                             )

    def total_lisp_command(self) -> str:
        if os.path.exists(self.this_exp_log_path + 'experiment_input_data_folder/train/'):
            commands = [
                self.start_idyom_command(),
                self.import_test_dataset_command(),
                self.import_train_dataset_command(),
                self.run_model_command(),
                self.quit_command()
            ]
            total_command = '\n'.join(commands)
            return total_command
        else:
            commands = [
                self.start_idyom_command(),
                self.import_test_dataset_command(),
                self.run_model_command(),
                self.quit_command()
            ]
            total_command = '\n'.join(commands)
            return total_command

    def start_idyom_command(self) -> str:
        command = '(start-idyom)'
        return command

    def import_test_dataset_command(self) -> str:
        command = self.database_configuration.to_lisp_command_import_testdb()
        return command

    def import_train_dataset_command(self) -> str:
        command = self.database_configuration.to_lisp_command_import_traindb()
        return command

    def import_datasets_command(self) -> str:
        command = self.database_configuration.to_lisp_command()
        return command

    def describe_database_command(self) -> str:
        command = '(idyom-db:describe-database)'
        return command

    def describe_detailed_database_command(self) -> str:
        command = '(idyom-db:describe-database :verbose t)'
        return command

    def run_model_command(self) -> str:
        command = self.run_model_configuration.to_lisp_command()
        return command

    def quit_command(self) -> str:
        command = '(quit)'
        return command

    def run_start_idyom_command(self):
        print('** Starting IDyOM in SBCL **')
        os.system('sbcl')
        os.system(self.start_idyom_command())

    def generate_lisp_script(self):
        path_to_file = self.this_exp_log_path
        lisp_file_path = path_to_file + 'compute.lisp'
        lisp_command = self.total_lisp_command()
        with open(lisp_file_path, "w") as f:
            f.write(lisp_command)
        return str(lisp_file_path)

    def run(self):
        """use shell to run IDyOM LISP code """
        print('** running lisp script **')
        os.system("sbcl --noinform --load " + self.generate_lisp_script())
        print(' ')
        print('** Finished! **')
