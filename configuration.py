import json
from dataclasses import dataclass
from typing import Literal, List, Union, Tuple, Iterable


@dataclass
class Parameters:

    def show(self):
        print(json.dumps(self, default=lambda x: x.__dict__, indent=2))  # formatting

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
    dataset_id: int
    target_viewpoints: List[SingleViewpoint]
    source_viewpoints: Union[Literal[':select'],
                             List[Union[SingleViewpoint,
                                        Tuple[SingleViewpoint]]]]

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


@dataclass
class TrainingParameters(Parameters):
    pretraining_ids: int = None
    k: Union[int, Literal['full']] = None
    resampling_indices: List[int] = None


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


@dataclass
class Configuration(Parameters):
    def __init__(self, required_parameters: RequiredParameters):
        self.required_parameters = required_parameters
        self.statistical_modelling_parameters = StatisticalModellingParameters()
        self.training_parameters = TrainingParameters()
        self.viewpoint_selection_parameters = ViewpointSelectionParameters()
        self.output_parameters = OutputParameters()
        self.caching_parameters = CachingParameters()

    def to_lisp_command(self) -> str:
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


def func():
    # config = Configuration(required_parameters=RequiredParameters(1, None, None))
    # config.show()
    statistical_modeling_parameters = StatisticalModellingParameters(models=':stm',
                                                                     stmo=ModelOptions(order_bound=4, mixtures=True))
    viewpoint_selection_parameters = ViewpointSelectionParameters(basis=BasisOption(['cpitch', 'cpint', 'contour']),
                                                                  dp=3, max_links=2)
    required_parameters = RequiredParameters(dataset_id=0, target_viewpoints=['cpitch', 'onset'],
                                             source_viewpoints=['cpitch', 'onset', ('cpitch', 'articulation')])
    # print(required_parameters.to_lisp_command())
    configuration = Configuration(required_parameters=required_parameters)
    print(configuration.to_lisp_command())


if __name__ == '__main__':
    func()
