import json


class Parameters:
    def show(self):
        print(json.dumps(self, default=lambda x: x.__dict__, indent=2))  # formatting


class RequiredParameters(Parameters):
    def __init__(self, dataset_id: int, target_viewpoints, source_viewpoints):
        """
        :param dataset_id: int
        :param target_viewpoints: str
        :param source_viewpoints: str
        """
        self.dataset_id = dataset_id
        self.target_viewpoints = target_viewpoints
        self.source_viewpoints = source_viewpoints


class StatisticalModellingParameters(Parameters):
    def __init__(self, models=None, order_bound=None, mixtures=None, update_exclusion=None, escape=None):
        """
        :param models: [stm, ltm, ltm+, both, both+]
        :param order_bound: int
        :param mixtures:
        :param update_exclusion:
        :param escape:
        """

        self.models = models
        self.order_bound = order_bound
        self.mixtures = mixtures
        self.update_exclusion = update_exclusion
        self.escape = escape


class TrainingParameters(Parameters):
    def __init__(self, pretraining_ids=None, k=None, resampling_indices=None):
        """
        :param pretraining_ids: int
        :param k: int or str = "full"
        :param resampling_indices: list of int
        """
        self.pretraining_ids = pretraining_ids
        self.k = k
        self.resampling_indices = resampling_indices


class ViewpointSelectionParameters(Parameters):
    """
    When the source viewpoint supplied is :select
    """

    def __init__(self, basis=None, dp=None, max_links=None, min_links=None, viewpoint_selection_output=None):
        """
        :param basis: [pitch_full, pitch_short, bioi, onset, auto]
        :param dp: int
        :param max_links: int
        :param min_links: int
        :param viewpoint_selection_output: str
        """
        self.basis = basis
        self.dp = dp
        self.max_links = max_links
        self.min_links = min_links
        self.viewpoint_selection_output = viewpoint_selection_output


class OutputParameters(Parameters):
    def __init__(self, output_path=None, detail=None, overwrite=None, separator=None):
        """
        :param output_path: str
        :param detail: [1, 2, 3]
        :param overwrite: [nil, t]
        :param separator: [" ", ","]
        """
        self.output_path = output_path
        self.detail = detail
        self.overwrite = overwrite
        self.separator = separator


class CachingParameters(Parameters):
    def __init__(self, use_resampling_set_cache=None, use_ltms_cache=None):
        """
        :param use_resampling_set_cache: [t, nil]
        :param use_ltms_cache: [t, nil]
        """
        self.use_resampling_set_cache = use_resampling_set_cache
        self.use_ltms_cache = use_ltms_cache


class Configuration(Parameters):
    def __init__(self, required_parameters: RequiredParameters):
        self.required_parameters = required_parameters
        self.statistical_modelling_parameters = StatisticalModellingParameters()
        self.training_parameters = TrainingParameters()
        self.viewpoint_selection_parameters = ViewpointSelectionParameters()
        self.output_parameters = OutputParameters()
        self.caching_parameters = CachingParameters()

    def to_lisp_command(self):
        pass




def func():
    config = Configuration(required_parameters=RequiredParameters(1, None, None))
    config.show()


if __name__ == '__main__':
    func()
