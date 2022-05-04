import os
from dataclasses import dataclass

import pandas as pd
import scipy.io
from extraction import getDictionary, ExperimentInfo, MelodyInfo

@dataclass
class Exportation:
    exp_file_path: str

    # def __init__(self, exp_file_path: str):
    #     self.file_path = exp_file_path
    #     self.file = os.path.basename(exp_file_path)
    #     self.file_name = os.path.splitext(self.file)[0]
    #     self.file_type = os.path.splitext(self.file)[1]

    def dat2mat(self, file_path):
        whole_dict = getDictionary(file_path)
        print(whole_dict)
        # scipy.io.savemat(output_path+self.file_name+'.mat', mdict=whole_dict)
        # print('Exported data to '+output_path + '!')


if __name__ == '__main__':
    dat_file_path = '/Users/xinyiguan/Codes/IDyOM_Interface_paper/99030821134014-cpitch_onset-cpitch_onset-66030821134014-nil-melody-nil-1-both-nil-t-nil-c-nil-t-t-x-3.dat'

    Exportation(dat_file_path)
