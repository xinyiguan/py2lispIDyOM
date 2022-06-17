from __future__ import annotations

import datetime
import json
import os
import shutil
from abc import ABC, abstractmethod
from dataclasses import dataclass
from dataclasses import field
from glob import glob
from typing import Literal, List, Union, Tuple, Iterable, get_type_hints

from natsort import natsorted


def check_recursive_typings(obj, type_expected: type) -> bool:
    type_got = type(obj)

    if hasattr(type_expected, '__origin__'):
        type_origin = type_expected.__origin__
        if type_origin == Literal:  # type_expected is typing.Literal
            type_correct = obj in type_expected.__args__
        elif type_origin in [list, tuple]:
            arg_type = type_expected.__args__[0]
            type_correct = all([
                check_recursive_typings(obj=_, type_expected=arg_type) for _ in obj
            ])
        elif type_origin == Union:
            possible_types = type_expected.__args__
            type_correct = any([
                check_recursive_typings(obj=obj, type_expected=possible_type) for possible_type in possible_types
            ])
        else:
            raise TypeError()
    else:
        type_correct = type_got is type_expected
    return type_correct


def get_timestamp():
    today_date = datetime.date.today()
    now_time = datetime.datetime.now()
    moment = today_date.strftime('%m%d%y') + now_time.strftime('%H%M%S')
    return moment


@dataclass
class LispConvertable(ABC):
    @abstractmethod
    def to_lisp_command(self):
        pass

    def __repr__(self):
        return json.dumps(self, default=lambda x: x.__dict__, indent=2)

    def recursive_set_attr(self, key, value):
        # print(f'set {key=} {value=}')
        children_configuration = filter(lambda x: isinstance(x, Configuration), self.__dict__.values())
        children_parameter = filter(lambda x: isinstance(x, Parameters), self.__dict__.values())
        children = list(children_configuration) + list(children_parameter)

        if hasattr(self, key):
            # print(f'{self} has {key=}')
            type_hint_dict = get_type_hints(self, globalns=globals())
            if key not in type_hint_dict:
                print(f'type hint for {key} not defined')
            else:
                type_expected = type_hint_dict[key]
                type_correct = check_recursive_typings(obj=value, type_expected=type_expected)

                if type_correct:

                    self.__dict__[key] = value
                    # print('after set', self.__dict__)
                else:
                    raise TypeError(
                        f'Expect type for parameter {key} is {type_expected}, but got \'{value}\' which has type {type(value)} ')

        elif children:
            for child in children:
                child.recursive_set_attr(key, value)

    def get_surface_dict(self) -> dict:

        def expandable_component(_obj):
            expandable = [_ for _ in _obj.__dict__.values() if
                          isinstance(_, Parameters) or isinstance(_, Configuration)]

            return expandable

        def terminal_check(obj: object) -> bool:
            is_terminal = isinstance(obj, Parameters) and all((
                len(expandable_component(component)) == 0 for component in expandable_component(obj)
            ))
            return is_terminal

        def non_terminal_check(obj: object) -> bool:
            is_non_terminal = isinstance(obj, Parameters) or isinstance(obj, Configuration) and any((
                len(expandable_component(component)) != 0 for component in expandable_component(obj)
            ))
            return is_non_terminal

        children_nonterminal = filter(non_terminal_check, self.__dict__.values())
        children_terminal = filter(terminal_check, self.__dict__.values())

        children_nonterminal_dicts = [child.get_surface_dict() for child in children_nonterminal]
        children_terminal_dicts = [child.__dict__ for child in children_terminal]
        surface_dict = {}
        for d in children_nonterminal_dicts + children_terminal_dicts:
            surface_dict.update(d)
        return surface_dict


@dataclass
class Parameters(LispConvertable):

    def to_lisp_command(self) -> str:
        convert_dict = {True: 't', False: 'nil'}
        commands = []
        for key, value in self.__dict__.items():
            if value is not None:
                if isinstance(value, Parameters):
                    value = value.to_lisp_command()
                print_value = value
                if type(value) is bool:
                    print_value = convert_dict[value]
                sub_command = f':{key} {print_value}'
                commands.append(sub_command)
        lisp_command = ' '.join(commands)
        return lisp_command

    def show(self):
        print(self.__repr__())  # formatting


SingleViewpoint = Literal[
    'onset', 'cpitch', 'dur', 'keysig', 'mode', 'tempo', 'pulses', 'barlength', 'deltast', 'bioi', 'phrase',
    'mpitch', 'accidental', 'dyn', 'voice', 'ornament', 'comma', 'articulation',
    'ioi', 'posinbar', 'dur-ratio', 'referent', 'cpint', 'contour', 'cpitch-class', 'cpcint', 'cpintfref', 'cpintfip', 'cpintfiph', 'cpintfb', 'inscale',
    'ioi-ratio', 'ioi-contour', 'metaccent', 'bioi-contour', 'lphrase', 'cpint-size', 'newcontour', 'cpcint-size', 'cpcint-2', 'cpcint-3', 'cpcint-4', 'cpcint-5', 'cpcint-6', 'octave', 'tessitura', 'mpitch-class',
    'registral-direction', 'intervallic-difference', 'registral-return', 'proximity', 'closure'
]


@dataclass
class RequiredParameters(Parameters):
    dataset_id: str = None
    target_viewpoints: List[SingleViewpoint] = None
    source_viewpoints: Union[Literal[':select'],
                             List[Union[SingleViewpoint,
                                        Tuple[SingleViewpoint]]]] = None

    def is_complete(self) -> bool:
        condition = all([
            # type(self.dataset_path) is str,
            bool(self.target_viewpoints),
            bool(self.source_viewpoints)
        ])
        return condition

    def viewpoint_to_string(self, viewpoint: Union[SingleViewpoint, Tuple[SingleViewpoint]]) -> str:
        if type(viewpoint) is str:
            string = str(viewpoint)
        elif type(viewpoint) is tuple:
            string = self.tuple_to_command(viewpoint)
        else:
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

    def dataset_id_to_command(self):
        command_dataset_id = self.dataset_id
        return command_dataset_id

    def target_viewpoints_to_command(self):
        command_target_viewpoints = self.list_to_command(self.target_viewpoints)
        return command_target_viewpoints

    def source_viewpoints_to_command(self):
        if self.source_viewpoints == ':select':
            command_source_viewpoints = self.source_viewpoints
            # raise NotImplementedError
        elif type(self.source_viewpoints) is list:
            command_source_viewpoints = self.list_to_command(self.source_viewpoints)
        else:
            raise TypeError(self.source_viewpoints)
        return command_source_viewpoints

    def to_lisp_command(self) -> str:
        if not self.is_complete():
            raise AssertionError(f'{self} Missing required argument')
        command = f'{self.dataset_id_to_command()} {self.target_viewpoints_to_command()} {self.source_viewpoints_to_command()}'
        return command


@dataclass
class LTMOModelOptions(Parameters):
    ltmo_order_bound: int = None
    ltmo_mixtures: bool = None
    ltmo_update_exclusion: bool = None
    ltmo_escape: Literal[':a', ':b', ':c', ':d', ':x'] = None

    def to_lisp_command(self) -> str:
        generic_command = super().to_lisp_command()
        command = f'\'({generic_command})'
        command = command.replace('ltmo_', '')
        command = command.replace('_', '-')
        return command


@dataclass
class STMOModelOptions(Parameters):
    stmo_order_bound: int = None
    stmo_mixtures: bool = None
    stmo_update_exclusion: bool = None
    stmo_escape: Literal[':a', ':b', ':c', ':d', ':x'] = None

    def to_lisp_command(self) -> str:
        generic_command = super().to_lisp_command()
        command = f'\'({generic_command})'
        command = command.replace('stmo_', '')
        command = command.replace('_', '-')
        return command


@dataclass
class StatisticalModellingParameters(Parameters):
    models: Literal[':stm', ':ltm', ':ltm+', ':both', ':both+'] = None
    ltmo: Literal[':ltmo'] = None
    ltmo_options: LTMOModelOptions = field(default_factory=LTMOModelOptions)
    stmo: Literal[':stmo'] = None
    stmo_options: STMOModelOptions = field(default_factory=STMOModelOptions)

    def models_to_lisp_command(self) -> str:
        command = f':models {self.models}'
        return command

    def ltmo_to_lisp_command(self) -> str:
        command = self.ltmo
        return command

    def stmo_to_lisp_command(self) -> str:
        command = self.stmo
        return command

    def ltmo_options_to_lisp_command(self) -> str:
        command = self.ltmo_options.to_lisp_command()
        return command

    def stmo_options_to_lisp_command(self) -> str:
        command = self.stmo_options.to_lisp_command()
        return command

    def to_lisp_command(self) -> str:
        if self.models is not None and self.ltmo is None and self.stmo is None:
            command = f'{self.models_to_lisp_command()}'
            return command

        elif self.ltmo is not None and self.stmo is None:
            command = f'{self.models_to_lisp_command()} {self.ltmo_to_lisp_command()} {self.ltmo_options_to_lisp_command()}'
            return command

        elif self.stmo is not None and self.ltmo is None:
            command = f'{self.models_to_lisp_command()} {self.stmo_to_lisp_command()} {self.stmo_options_to_lisp_command()}'
            return command

        elif self.stmo is not None and self.ltmo is not None:
            command = f'{self.models_to_lisp_command()} {self.stmo_to_lisp_command()} {self.stmo_options_to_lisp_command()} {self.ltmo_to_lisp_command()} {self.ltmo_options_to_lisp_command()}'
            return command

        elif self.stmo is None and self.stmo_options is not None:
            raise ValueError(
                f'Please specify \':stmo\' if you want to further specify the STM optional properties {self.stmo_options_to_lisp_command()}')

        elif self.ltmo is None and self.ltmo_options is not None:
            raise ValueError(
                f'Please specify \':ltmo\' if you want to further specify the LTM optional properties {self.ltmo_options_to_lisp_command()}')


@dataclass
class TrainingParameters(Parameters):
    pretraining_id: str = None
    k: Union[int, Literal[":full"]] = 10
    resampling_indices: List[int] = None

    def pretraining_id_to_command(self) -> str:
        command = self.pretraining_id
        return command

    def k_to_command(self):
        command_k = f':k {self.k}'
        return command_k

    def resampling_indices_to_command(self):
        raise NotImplementedError

    def to_lisp_command(self) -> str:
        if self.pretraining_id:
            command = f':pretraining-ids \'({self.pretraining_id_to_command()}) {self.k_to_command()}'
            return command

        else:
            command = f'{self.k_to_command()}'
            return command


@dataclass
class BasisOption(Parameters):
    basis: Union[List[SingleViewpoint],
                 Literal[':pitch-full', ':pitch-short', ':bioi', ':onset', ':auto']] = None

    def to_lisp_command(self) -> str:
        generic_command = super().to_lisp_command()
        if generic_command:
            command = f'\'({generic_command})'
        else:
            command = ''
        return command


@dataclass
class ViewpointSelectionParameters(Parameters):
    """
    When the source viewpoint supplied is :select
    """

    basis: BasisOption = None
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


@dataclass
class ExperimentLogger:
    test_dataset_path: str
    pretrain_dataset_path: str
    experiment_history_folder_path: str
    experiment_logger_name: str

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
        if self.experiment_logger_name is None:
            today_date = datetime.date.today()
            now_time = datetime.datetime.now()
            timestamp_str = today_date.strftime('%d-%m-%y') + '_' + now_time.strftime('%H.%M.%S')
            this_experiment_folder = self.experiment_history_folder + timestamp_str + '/'
        else:
            this_experiment_folder = self.experiment_history_folder + self.experiment_logger_name + '/'
        os.makedirs(this_experiment_folder)
        return this_experiment_folder

    def generate_input_data_exp_folder(self):
        input_data_folder = self.this_exp_folder + 'experiment_input_data_folder/'
        os.makedirs(input_data_folder)
        return input_data_folder

    def _get_files_from_paths(self, path):  # only two types files allowed: midi and kern
        files = []
        for file in glob(path + '*'):
            if file[file.rfind("."):] == ".mid" or ".krn":
                files.append(file)
        return natsorted(files)

    def _put_midis_in_folder(self, files, folder_path):
        for file in files:
            shutil.copyfile(file, folder_path + file[file.rfind("/"):])

    def generate_test_dataset_exp_folder(self):
        input_data_folder = self.input_data_exp_folder
        test_folder = input_data_folder + 'test_dataset/'
        os.makedirs(test_folder)
        test_dataset_path = self.test_dataset_path
        test_files = self._get_files_from_paths(test_dataset_path)
        self._put_midis_in_folder(test_files, test_folder)
        if not os.listdir(test_folder):
            raise AssertionError(f'test_dataset folder is empty!')
        else:
            print("** Putting Test dataset files in experiment history folder. **")

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
            train_files = self._get_files_from_paths(pretrain_dataset_path)
            self._put_midis_in_folder(train_files, pretrain_folder)
            if not os.listdir(pretrain_folder):
                raise AssertionError(f'pretrain_dataset folder is empty!')
            else:
                print("** Putting Pretraining dataset files in experiment history folder. **")
            return pretrain_folder

    # def put_test_midi_in_exp_folder(self):
    #     print("** Putting Test dataset files in experiment history folder. **")
    #     test_files = self._get_files_from_paths(self.test_dataset_path)
    #     self._put_midis_in_folder(test_files, self.test_dataset_exp_folder)

    # def put_train_midi_in_exp_folder(self):
    #     if self.pretrain_dataset_path is None:
    #         pass
    #         print('** No pretraining dataset detected. **')
    #     else:
    #         print("** Putting pretrain dataset files in experiment history folder. **")
    #         train = self._get_files_from_paths(self.pretrain_dataset_path)
    #         self._put_midis_in_folder(train, self.train_dataset_exp_folder)

    def generate_output_data_exp_folder(self):
        output_data_folder = self.this_exp_folder + 'experiment_output_data_folder/'
        os.makedirs(output_data_folder)
        return output_data_folder


@dataclass
class Configuration(LispConvertable, ABC):
    pass


@dataclass(repr=False)
class RunModelConfiguration(Configuration):
    this_exp_log_path: str = None
    test_dataset_id: str = None
    pretrain_dataset_id: str = None

    output_parameters: OutputParameters = field(default_factory=OutputParameters)
    required_parameters: RequiredParameters = field(default_factory=RequiredParameters)
    statistical_modelling_parameters: StatisticalModellingParameters = field(
        default_factory=StatisticalModellingParameters)
    training_parameters: TrainingParameters = field(default_factory=TrainingParameters)
    viewpoint_selection_parameters: ViewpointSelectionParameters = field(default_factory=ViewpointSelectionParameters)
    caching_parameters: CachingParameters = field(default_factory=CachingParameters)

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


@dataclass
class DatabaseConfiguration(Configuration):
    this_exp_log_path: str = None
    test_dataset_id: str = None
    pretrain_dataset_id: str = None
    test_dataset_Name: str = 'TEST_DATASET'
    pretrain_dataset_Name: str = 'PRETRAIN_DATASET'

    def to_lisp_command(self):
        if self.pretrain_dataset_id:
            commands = [
                self.get_command_import_testdb(),
                self.get_command_import_traindb(),
            ]
        else:
            commands = [
                self.get_command_import_testdb(),
            ]
        total_command = '\n'.join(commands)
        return total_command

    @property
    def test_dataset_log_path(self):
        test_dataset_log_path = self.this_exp_log_path + 'experiment_input_data_folder/test_dataset/'
        return test_dataset_log_path

    @property
    def train_dataset_log_path(self):
        train_dataset_log_path = self.this_exp_log_path + 'experiment_input_data_folder/pretrain_dataset/'
        return train_dataset_log_path

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
class IDyOMConfiguration(Configuration):
    database_configuration: DatabaseConfiguration = field(default_factory=DatabaseConfiguration)
    run_model_configuration: RunModelConfiguration = field(default_factory=RunModelConfiguration)

    def to_lisp_command(self) -> str:
        if self.run_model_configuration.training_parameters.pretraining_id:
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
