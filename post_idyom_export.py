""""
This script exports the data in mat files for analysis in MATLAB.
Current available data types for export in mat format:

        'melody_name',
        'cpitch',
        'onset',
        'overall_probability',
        'overall_information_content',
        'overall_entropy',
        'cpitch_information_content',
        'cpitch_entropy',
        'onset_information_content',
        'onset_entropy',

"""

from helper_scripts.outputs_in_mat_format import export_mat_from_history_folder

if __name__ == '__main__':
    selected_experiment_history_folder = '/Users/xinyiguan/Desktop/Codes/IDyOM_Python_Interface/experiment_history/03-08-21_13.40.14/'  # change your desired 'selected_experiment_history_folder' here!
    data_type_to_export = [
        'melody_name',
        'cpitch',
        'onset',
        'overall_probability',
        'overall_information_content',
        'overall_entropy',
        'cpitch_information_content',
        'cpitch_entropy',
        'onset_information_content',
        'onset_entropy',
    ]

    print('Exporting mat files:')
    export_mat_from_history_folder(selected_experiment_history_folder, data_type_to_export)
