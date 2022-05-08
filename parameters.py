import json
from dataclasses import dataclass
from typing import Literal, List, Union, Tuple, Iterable


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
    """ user-level interaction class """
    dataset_id: str
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

    def dataset_id_to_command(self):
        command_dataset_id = self.dataset_id
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
    pretraining_id: str = None
    k: Union[int, Literal[":full"]] = None
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
        elif self.pretraining_id is None:
            command = f'{self.k_to_command()}'
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
