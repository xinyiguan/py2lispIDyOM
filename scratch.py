"""
scratches for module in development

"""
import helper_scripts.data_extractor as data_extractor

dat_file_path = '/Users/xinyiguan/Desktop/Codes/IDyOM_Python_Interface/experiment_history/03-08-21_13.40.14/experiment_output_data_folder/99030821134014-cpitch_onset-cpitch_onset-66030821134014-nil-melody-nil-1-both-nil-t-nil-c-nil-t-t-x-3.dat'

all_song_dict = data_extractor.get_all_song_dict_from_dat(dat_file_path)


