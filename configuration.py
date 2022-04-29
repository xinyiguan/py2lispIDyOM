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
    """
    for the dataset to input test dataset, we ask to provide the **PATH** to the dataset instead of an ID number.
    The py2lispIDyOM will automatically assign a unique number to the training set internaly
    """
    # dataset_id: int
    dataset_path: str = None
    target_viewpoints: List[SingleViewpoint] = None
    source_viewpoints: Union[Literal[':select'],
                             List[Union[SingleViewpoint,
                                        Tuple[SingleViewpoint]]]] = None

    def _is_available(self) -> bool:
        condition = all([
            type(self.dataset_path) is str,
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

    def dataset_path_to_dataset_id(self):
        moment = get_timestamp()
        dataset_id = '66' + moment
        return dataset_id

    def dataset_id_to_command(self):
        command_dataset_id = self.dataset_path_to_dataset_id()
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


@dataclass
class TrainingParameters(Parameters):
    """
    for the dataset to pretrain the long-term models, we ask to provide the **PATH** to the dataset instead of an ID number.
    The py2lispIDyOM will automatically assign a unique number to the training set internaly
    """
    # pretraining_ids: int = None
    pretraining_dataset_path: str = None
    k: Union[int, Literal[":full"]] = None
    resampling_indices: List[int] = None

    def pretrain_path_to_pretrain_id(self):
        moment = get_timestamp()
        pretraining_id = '99' + moment
        return pretraining_id

    def pretraining_id_to_command(self):
        command_pretraining_id = self.pretrain_path_to_pretrain_id()
        return command_pretraining_id

    def k_to_command(self):
        command_k = f':k {self.k}'
        print('k value is: ', self.k)
        return command_k

    def resampling_indices_to_command(self):
        raise NotImplementedError

    def to_lisp_command(self) -> str:
        command = f'\'({self.pretraining_id_to_command()}) {self.k_to_command()}'
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
    output_path: str = None
    detail: Literal[1, 2, 3] = None
    overwrite: bool = None  # whether to overwrite an existing output file if it exists
    separator: str = None  # a string defining the character to use for delimiting columns in the output file (default
    # is " ", use "," for CSV)


@dataclass
class CachingParameters(Parameters):
    use_resampling_set_cache: bool = None
    use_ltms_cache: bool = None


class Configuration(Parameters):
    pass


@dataclass(repr=False)
class RunModelConfiguration(Configuration):
    required_parameters: RequiredParameters = field(default_factory=RequiredParameters)
    statistical_modelling_parameters: StatisticalModellingParameters = field(default_factory=StatisticalModellingParameters)
    training_parameters: TrainingParameters = field(default_factory=TrainingParameters)
    viewpoint_selection_parameters: ViewpointSelectionParameters = field(default_factory=ViewpointSelectionParameters)
    output_parameters: OutputParameters = field(default_factory=OutputParameters)
    caching_parameters: CachingParameters = field(default_factory=CachingParameters)

    def to_lisp_command(self) -> str:
        assert self.required_parameters._is_available(), self.required_parameters
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
        command = f'(idyom: idyom {joined_commands})'
        return command


@dataclass(repr=False)
class DatabaseConfiguration(Configuration):
    file_type: Literal[':mid', ':krn']
    test_dataset_Path: RunModelConfiguration.required_parameters.dataset_path
    test_dataset_ID: RunModelConfiguration.required_parameters.dataset_path_to_dataset_id
    train_dataset_Path: RunModelConfiguration.training_parameters.pretraining_dataset_path
    train_dataset_ID: RunModelConfiguration.training_parameters.pretrain_path_to_pretrain_id
    test_dataset_Name: str = 'TEST_DATASET'
    train_dataset_Name: str = 'PRETRAIN_DATASET'

    def to_lisp_command(self) -> str:
        all_parameters = [
            self.file_type,
            self.test_dataset_Path,
            self.test_dataset_Name,
            self.test_dataset_ID,
            self.train_dataset_Path,
            self.train_dataset_Name,
            self.train_dataset_ID,
        ]
        subcommands = [parameters.to_lisp_command() for parameters in all_parameters]

        # non_empty_subcommands = [x for x in subcommands if x != '']
        # joined_commands = ' '.join(non_empty_subcommands)
        # command = f'(idyom-db:import-data {joined_commands})'
        return subcommands


def initialize_experiment_folder(RunModelConfiguration):

    def get_files_from_paths(path): # only two types files allowed: midi and kern
        files=[]
        for file in glob(path + '*'):
            if file[file.rfind("."):] == ".mid" or ".krn":
                files.append(file)
        return natsorted(files)

    def put_midis_in_folder(files, folder_path):
        for file in files:
            shutil.copyfile(file, folder_path + file[file.rfind("/"):])

    experiment_history_folder = 'experiment_history/'
    if not os.path.exists(experiment_history_folder):
        os.makedirs(experiment_history_folder)

    # read inputs from user inputs in the Configuration:
    test_dataset_path = RunModelConfiguration.required_parameters.dataset_path
    train_dataset_path = RunModelConfiguration.training_parameters.pretraining_dataset_path

    today_date = datetime.date.today()
    now_time = datetime.datetime.now()
    this_experiment_folder = experiment_history_folder+ today_date.strftime('%d-%m-%y')+'_'+ now_time.strftime('%H.%M.%S') + '/'
    os.makedirs(this_experiment_folder)

    # input data folder:
    input_data_folder = this_experiment_folder + 'experiment_input_data_folder/'
    train_folder = input_data_folder + 'train/'
    test_folder = input_data_folder + 'test/'

    os.makedirs(input_data_folder)
    os.makedirs(train_folder)
    os.makedirs(test_folder)

    if train_dataset_path is None:
        pass
        print('** No pretraining dataset detected. **')
    else:
        train = get_files_from_paths(train_dataset_path)
        put_midis_in_folder(train, train_folder)
        print("** Putting Pretraining dataset files in experiment history folder. **")

    test = get_files_from_paths(test_dataset_path)
    put_midis_in_folder(test,test_folder)
    print("** Putting Test dataset files in experiment history folder. **")

    output_data_folder = this_experiment_folder + 'experiment_output_data_folder/'
    os.makedirs(output_data_folder)

    print('** Successfully created experiment folder! **')
    return this_experiment_folder





def test():
    statistical_modeling_parameters = StatisticalModellingParameters(models=':stm',
                                                                     stmo=ModelOptions(order_bound=4, mixtures=True))

    required_parameters = RequiredParameters(dataset_path='dataset/bach_dataset',
                                             target_viewpoints=['cpitch', 'onset'],
                                             source_viewpoints=['cpitch', 'onset', ('cpitch', 'articulation')])

    training_parameters = TrainingParameters(pretraining_dataset="dataset/bach_dataset",
                                             k=1)

    output = OutputParameters(output_path="experiment_history/", detail=3, overwrite=True, separator=",")
    configuration = RunModelConfiguration(required_parameters=required_parameters,
                                          training_parameters=training_parameters)

    print(configuration.to_lisp_command())
    print('dataset_path: ', required_parameters.dataset_path)


if __name__ == '__main__':
    required_parameters = RequiredParameters(dataset_path='dataset/bach_dataset/',
                                             target_viewpoints=['cpitch', 'onset'],
                                             source_viewpoints=['cpitch', 'onset', ('cpitch', 'articulation')])

    runmodel_config = RunModelConfiguration(required_parameters=required_parameters)
    initialize_experiment_folder(runmodel_config)
