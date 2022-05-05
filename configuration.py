from __future__ import annotations

import datetime
import json
import os
import shutil
from dataclasses import dataclass, field
from glob import glob
from typing import Literal, List, Union, Tuple, Iterable

from natsort import natsorted


def get_timestamp():
    today_date = datetime.date.today()
    now_time = datetime.datetime.now()
    moment = today_date.strftime('%m%d%y') + now_time.strftime('%H%M%S')
    return moment


@dataclass
class Parameters:

    def __repr__(self):
        return json.dumps(self, default=lambda x: x.__dict__, indent=2)

    def show(self):
        print(self.__repr__())  # formatting

    def to_lisp_command(self) -> str:
        convert_dict = {True: 't', False: 'nil'}
        commands = []
        for key, value in self.__dict__.items():
            if value:
                if isinstance(value, Parameters):
                    value = value.to_lisp_command()
                print_value = value
                if type(value) is bool:
                    print_value = convert_dict[value]
                sub_command = f':{key} {print_value}'
                commands.append(sub_command)
        lisp_command = ' '.join(commands)
        return lisp_command


SingleViewpoint = Literal[
    'onset', 'cpitch', 'dur', 'keysig', 'mode', 'tempo', 'pulses', 'barlength', 'deltast', 'bioi', 'phrase',
    'mpitch', 'accidental', 'dyn', 'voice', 'ornament', 'comma', 'articulation',
    'ioi', 'posinbar', 'dur-ratio', 'referent', 'cpint', 'contour', 'cpitch-class', 'cpcint', 'cpintfref', 'cpintfip', 'cpintfiph', 'cpintfb', 'inscale',
    'ioi-ratio', 'ioi-contour', 'metaccent', 'bioi-contour', 'lphrase', 'cpint-size', 'newcontour', 'cpcint-size', 'cpcint-2', 'cpcint-3', 'cpcint-4', 'cpcint-5', 'cpcint-6', 'octave', 'tessitura', 'mpitch-class',
    'registral-direction', 'intervallic-difference', 'registral-return', 'proximity', 'closure'
]


@dataclass
class RequiredParameters(Parameters):

    target_viewpoints: List[SingleViewpoint] = None
    source_viewpoints: Union[Literal[':select'],
                             List[Union[SingleViewpoint,
                                        Tuple[SingleViewpoint]]]] = None

    def _is_available(self) -> bool:
        condition = all([
            # type(self.dataset_path) is str,
            type(self.target_viewpoints) is List[SingleViewpoint],
            type(self.source_viewpoints) is Union[
                Literal[':select'], List[Union[SingleViewpoint, Tuple[SingleViewpoint]]]]
        ])
        return condition

    def viewpoint_to_string(self, viewpoint: Union[SingleViewpoint, Tuple[SingleViewpoint]]) -> str:
        if type(viewpoint) is str:
            string = str(viewpoint)
        elif type(viewpoint) is tuple:
            string = self.tuple_to_command(viewpoint)
        else:
            print(type(viewpoint))
            raise TypeError(viewpoint)
        return string

    def list_to_command(self, l: Iterable) -> str:
        list_of_string = [self.viewpoint_to_string(viewpoint=viewpoint) for viewpoint in l]
        long_string = ' '.join(list_of_string)
        command = f'\'({long_string})'
        return command

    def tuple_to_command(self, t: tuple) -> str:
        list_of_string = [self.viewpoint_to_string(viewpoint=viewpoint) for viewpoint in t]
        long_string = ' '.join(list_of_string)
        command = f'({long_string})'
        return command

    @staticmethod
    def generate_test_dataset_id():
        moment = get_timestamp()
        dataset_id = '66' + moment
        return dataset_id

    def dataset_id_to_command(self):
        command_dataset_id = self.generate_test_dataset_id()
        return command_dataset_id

    def target_viewpoints_to_command(self):
        command_target_viewpoints = self.list_to_command(self.target_viewpoints)
        return command_target_viewpoints

    def source_viewpoints_to_command(self):
        if type(self.source_viewpoints) is Literal[':select']:
            command_source_viewpoints = self.source_viewpoints
            raise NotImplementedError
        elif type(self.source_viewpoints) is list:
            command_source_viewpoints = self.list_to_command(self.source_viewpoints)
        else:
            raise TypeError(self.source_viewpoints)
        return command_source_viewpoints

    def to_lisp_command(self) -> str:
        command = f'{self.dataset_id_to_command()} {self.target_viewpoints_to_command()} {self.source_viewpoints_to_command()}'
        return command


@dataclass
class ModelOptions(Parameters):
    order_bound: int = None
    mixtures: bool = None
    update_exclusion: str = None
    escape: Literal[':a', ':b', ':c', ':d', ':x'] = None

    def to_lisp_command(self) -> str:
        generic_command = super().to_lisp_command()
        command = f'\'({generic_command})'
        return command


@dataclass
class StatisticalModellingParameters(Parameters):
    models: Literal[':stm', ':ltm', ':ltm+', ':both', ':both+'] = None
    ltmo: ModelOptions = None
    stmo: ModelOptions = None

    def to_lisp_command(self) -> str:
        command = super().to_lisp_command()
        return command


@dataclass
class TrainingParameters(Parameters):

    k: Union[int, Literal[":full"]] = None
    resampling_indices: List[int] = None

    @staticmethod
    def generate_pretrain_dataset_id():
        moment = get_timestamp()
        pretrain_dataset_id = '99' + moment
        return pretrain_dataset_id

    def pretraining_id_to_command(self) -> str:
        command = self.generate_pretrain_dataset_id()
        return command

    def k_to_command(self):
        command_k = f':k {self.k}'
        return command_k

    def resampling_indices_to_command(self):
        raise NotImplementedError

    def to_lisp_command(self) -> str:
        command = f':pretraining-ids \'({self.pretraining_id_to_command()}) {self.k_to_command()}'
        return command


@dataclass
class BasisOption(Parameters):
    basis: Union[List[SingleViewpoint],
                 Literal[':pitch-full', ':pitch-short', ':bioi', ':onset', ':auto']] = None

    def to_lisp_command(self) -> str:
        generic_command = super().to_lisp_command()
        command = f'\'({generic_command})'
        return command


@dataclass
class ViewpointSelectionParameters(Parameters):
    """
    When the source viewpoint supplied is :select
    """

    basis: Literal[':pitch-full', ':pitch-short', ':bioi', ':onset', ':auto'] = None
    dp: int = None
    max_links: int = None
    min_links: int = None
    viewpoint_selection_output: str = None  # a filepath to write output for every viewpoint system considered during viewpoint selection.
    # The default is nil meaning that no files are written.


@dataclass
class OutputParameters(Parameters):
    detail: Literal[1, 2, 3] = 3
    output_path: str = None
    overwrite: bool = False  # whether to overwrite an existing output file if it exists
    separator: str = None  # a string defining the character to use for delimiting columns in the output file

    def detail_to_command(self) -> str:
        command_detail = f':detail {self.detail}'
        return command_detail

    # the default output path in py2lispIDyOM is experiment_history/THIS_EXP/experiment_output_data_folder/
    def output_path_to_command(self) -> str:
        command_outpath = f':output-path \"{self.output_path}\"'
        return command_outpath

    def overwrite_to_command(self) -> str:
        convert_dict = {True: 't', False: 'nil'}
        if self.overwrite is True:
            command_overwrite = f':overwrite {convert_dict[True]}'
            return command_overwrite
        if self.overwrite is False:
            command_overwrite = f':overwrite {convert_dict[False]}'
            return command_overwrite

    def to_lisp_command(self) -> str:
        command = f'{self.detail_to_command()} {self.output_path_to_command()} {self.overwrite_to_command()}'
        return command


@dataclass
class CachingParameters(Parameters):
    use_resampling_set_cache: bool = None
    use_ltms_cache: bool = None


class Configuration(Parameters):
    pass


@dataclass(repr=False)
class RunModelConfiguration(Configuration):
    this_exp_log_path: str
    output_parameters: OutputParameters
    required_parameters: RequiredParameters = field(default_factory=RequiredParameters)
    statistical_modelling_parameters: StatisticalModellingParameters = field(
        default_factory=StatisticalModellingParameters)
    training_parameters: TrainingParameters = field(default_factory=TrainingParameters)
    viewpoint_selection_parameters: ViewpointSelectionParameters = field(default_factory=ViewpointSelectionParameters)
    # output_parameters: OutputParameters
    caching_parameters: CachingParameters = field(default_factory=CachingParameters)

    def __post_init__(self):
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
    train_dataset_id: str
    test_dataset_id: str
    test_dataset_Name: str = 'TEST_DATASET'
    train_dataset_Name: str = 'PRETRAIN_DATASET'

    def __post_init__(self):
        self.test_dataset_log_path = self.this_exp_log_path + 'experiment_input_data_folder/test/'
        self.train_dataset_log_path = self.this_exp_log_path + 'experiment_input_data_folder/train/'

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
        command = self._get_command_import_db(path=self.train_dataset_log_path, dataset_name=self.train_dataset_Name,
                                              dataset_id=self.train_dataset_id)
        return command

    def to_lisp_command(self) -> str:
        commands = [
            self.get_command_import_testdb(),
            self.get_command_import_traindb(),
        ]
        total_command = '\n'.join(commands)
        return total_command


@dataclass
class ExperimentLogger:
    train_dataset_path: str
    test_dataset_path: str
    experiment_history_folder_path: str

    def __post_init__(self):

        self.experiment_history_folder = self.generate_experiment_history_folder()
        self.this_exp_folder = self.generate_this_exp_folder()
        self.input_data_exp_folder = self.generate_input_data_exp_folder()
        self.test_dataset_exp_folder = self.generate_test_dataset_exp_folder()
        self.train_dataset_exp_folder = self.generate_train_dataset_exp_folder()
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
        test_folder = input_data_folder + 'test/'
        os.makedirs(test_folder)
        print("** Putting Test dataset files in experiment history folder. **")
        test_dataset_path = self.test_dataset_path
        test = self._get_files_from_paths(test_dataset_path)
        self._put_midis_in_folder(test, test_folder)
        return test_folder

    def generate_train_dataset_exp_folder(self):
        input_data_folder = self.input_data_exp_folder
        train_folder = input_data_folder + 'train/'
        os.makedirs(train_folder)
        train_dataset_path = self.train_dataset_path
        if train_dataset_path is None:
            pass
            print('** No pretraining dataset detected. **')
        else:
            print("** Putting Pretraining dataset files in experiment history folder. **")
            train = self._get_files_from_paths(train_dataset_path)
            self._put_midis_in_folder(train, train_folder)
        return train_folder

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
        if self.train_dataset_path is None:
            pass
            print('** No pretraining dataset detected. **')
        else:
            print("** Putting Pretraining dataset files in experiment history folder. **")
            train = self._get_files_from_paths(self.train_dataset_path)
            self._put_midis_in_folder(train, self.train_dataset_exp_folder)

    def generate_output_data_exp_folder(self):
        output_data_folder = self.this_exp_folder + 'experiment_output_data_folder/'
        os.makedirs(output_data_folder)
        return output_data_folder


@dataclass
class IDyOMConfiguration:
    required_parameters: RunModelConfiguration.required_parameters
    statistical_modelling_parameters: RunModelConfiguration.statistical_modelling_parameters
    training_parameters: RunModelConfiguration.training_parameters
    viewpoint_selection_parameters: RunModelConfiguration.viewpoint_selection_parameters
    output_parameters: RunModelConfiguration.output_parameters
    caching_parameters: RunModelConfiguration.caching_parameters

    this_exp_log_path: str

    def __post_init__(self):
        self.database_configuration = DatabaseConfiguration(this_exp_log_path=self.this_exp_log_path,
                                                            train_dataset_id=self.generate_train_dataset_id(),
                                                            test_dataset_id=self.generate_test_dataset_id()
                                                            )
        self.run_model_configuration = RunModelConfiguration(required_parameters=self.required_parameters,
                                                             statistical_modelling_parameters=self.statistical_modelling_parameters,
                                                             training_parameters=self.training_parameters,
                                                             viewpoint_selection_parameters=self.viewpoint_selection_parameters,
                                                             output_parameters=self.output_parameters,
                                                             caching_parameters=self.caching_parameters,
                                                             this_exp_log_path=self.this_exp_log_path)

    def generate_test_dataset_id(self):
        moment = get_timestamp()
        dataset_id = '66' + moment
        return dataset_id

    def generate_train_dataset_id(self):
        moment = get_timestamp()
        dataset_id = '99' + moment
        return dataset_id

    def total_lisp_command(self) -> str:
        commands = [
            self.start_idyom_command(),
            self.import_datasets_command(),
            self.run_model_command(),
            self.quit_command()
        ]
        total_command = '\n'.join(commands)
        return total_command

    def start_idyom_command(self) -> str:
        command = '(start-idyom)'
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