"""
December 26th 2019
            Author T.Mizumoto
"""
#! python 3
# ver.x1.00
# traverse.py  -  this program read traverse data file.

import numpy as np
import pandas as pd
import os

class TraverseData:
    path = ""
    df_coordinate = pd.DataFrame([], columns = ["x", "y", "z"])

    def file_read(self):
        basename = os.path.basename(self.path).rsplit(".lvm")
        f = open(self.path)
        lvm_list = f.readlines()
        f.close()
        self.df_coordinate = pd.DataFrame([], columns = ["x", "y", "z"], index = range(0, len(lvm_list)))
        for i in range(len(lvm_list)):
            row = lvm_list[i].split("\t")
            row = [float(j) for j in row]
            self.df_coordinate.iloc[i, :] = row[1:]
    

if __name__ == "__main__":
    t = TraverseData()
    t.path = "D:/W_python/exp_velocity/test-data/20191226/traverse_63点_20191113 - .lvm"
    t.file_read()