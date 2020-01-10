"""
December 19th 2019
            Author T.Mizumoto
"""
#! python 3
# ver.x1.10
# Pitot.py  -  this program read pitot data files

import numpy as np
import pandas as pd
from lvm_read import read
import os

class PitotData:
    path = []
    df_data = pd.DataFrame(columns = ["U [m/s]", "press [Pa]", "temp. [degree]", "rho[kg/m3]", "U_true[m/s]"] )
    
    def U_corection(self, np_data):
        if np_data[1] < 0 or np_data[3] < 0:
            U_true = 0
        else:
            U_true = np.sqrt(2 * np_data[1] * 1000 /np_data[3])
        np_data = np.append(np_data, U_true)
        return np_data

    # read from lvm files
    def file_read(self):
        file_num = int(len(self.path))
        for i in range(file_num):
            basename = os.path.basename(self.path[i])
            basename = basename.rstrip(".lvm")
            # extract ch data
            lvm_file = read(self.path[i])
            nessesary = lvm_file[0]["data"][0, 0:4]
            # corection and appende U
            add_U_true = self.U_corection(nessesary)
            # insert into dataframe
            self.df_data.loc[basename] = (add_U_true)
        return self.df_data
    
    def csv_read(self, path):
        self.df_data = pd.read_csv(path, header = 0, index_col = 0)
        self.path = list(self.df_data.index + ".lvm")
        
    def save_csv(self, name, folder):
        return self.df_data.to_csv(folder + "/" + "Cp_" + name + ".csv")


if __name__ == "__main__":
    PD = PitotData()
    for i in range(4, 11):
        path = "D:/W_python/exp_velocity/test-data/pitot/20191113_VEL_00" + str(i) + ".lvm"
        if i >= 10:
            path = "D:/W_python/exp_velocity/test-data/pitot/20191113_VEL_0" + str(i) + ".lvm"
        PD.path.append(path)
    #PD.path = ["exp_velocity/test-data/pitot/20191113_VEL_005.lvm", "exp_velocity/test-data/pitot/20191113_VEL_006.lvm"]
    print(PD.file_read())
    PD.save_csv("Pitot_test")
