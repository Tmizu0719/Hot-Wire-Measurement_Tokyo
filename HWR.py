"""
December 19th 2019
            Author T.Mizumoto
"""
#! python 3
# ver.x1.10
# HWR.py  -  this program read HWR data files

import numpy as np
import pandas as pd
import os, csv
from nptdms import TdmsFile
from rms_function import fun_rms
pd.set_option('mode.chained_assignment', None)

def fun_linearize(data, E0, n, m):
    return ((data - E0) / n) ** m

def fun_R2(y_org, y_pred):
    residuals = y_org - y_pred
    total = y_org - np.mean(y_org)
    # residuals sum of squares
    RSS = np.sum(residuals ** 2)
    # total sum of squares
    TSS = np.sum(total ** 2)
    R2 = 1 - (RSS / TSS)
    return R2

class HWRData:
    path = []
    NAME = ""
    VULE1 = ""
    VULE2 = ""
    E0 = 0
    n = 0
    m = 0
    dt = 0
    NoD = 0
    a = 0
    b = 0
    R2 = 0
    df_data = pd.DataFrame(index = range(NoD), columns = ["time"])
    df_MandF = pd.DataFrame(columns = ["mean_ch1", "fluctuation_ch1", "mean_ch2", "fluctuation_ch2"])
        
    def make_timelist(self):
        time_list = []
        for i in range(self.NoD):
            time = self.dt * i
            time_list.append(time)
        self.df_data["time"] = time_list
        return np.array(time_list)
    
    def param_read(self, address, orgname):
        path = address + "Cw_param_" + orgname
        with open(path, "r", encoding = "utf-8") as f:
            dic_param = csv.DictReader(f)
            for i in dic_param:
                d = dict(i)
        self.path = d["path"]
        self.NAME = d["NAME"]
        self.VULE1 = d["VULE1"]
        self.VULE2 = d["VULE2"]
        self.dt = float(d["dt"])
        self.NoD = int(d["NoD"])
        self.E0 = float(d["E0"])
        self.n = float(d["n"])
        self.m = float(d["m"])
        self.a = float(d["a"])
        self.b = float(d["b"])
        self.R2 = float(d["R2"])

    # path is Cw_...csv
    def csv_read(self, path):
        csvname = os.path.basename(path)
        orgname = csvname.lstrip("Cw_")
        MandFname = "Cw_MandF_" + orgname
        address = path.rstrip(csvname)
        MandFpath = address + MandFname
        self.df_data = pd.read_csv(path, header = 0, index_col = 0)
        self.df_MandF = pd.read_csv(MandFpath, header = 0, index_col = 0)
        self.path = list(self.df_MandF.index + ".tdms")
        self.param_read(address, orgname)

    # read from tdms files
    def file_read(self):
        ch_list = self.make_timelist()
        file_num = int(len(self.path))
        count = 1
        for i in range(file_num):
            print("No." + str(count) +" tdms file now loading...")
            basename = os.path.basename(self.path[i])
            basename = basename.rstrip(".tdms")
            # extract ch data
            tdms_file = TdmsFile(self.path[i])
            ch1 = tdms_file.object(self.NAME, self.VULE1)
            ch2 = tdms_file.object(self.NAME, self.VULE2)
            # insert into dataframe
            ch1_data = np.array(ch1.data)
            ch2_data = np.array(ch2.data)
            self.df_data[basename + "_ch1"] = ch1_data
            self.df_data[basename + "_ch2"] = ch2_data
            count += 1
        return self.df_data

    # calculate mean and fluctuation
    def cal_MandF(self):
        file_num = int(len(self.path))
        for i in range(file_num):
            MandF_list = []
            basename = os.path.basename(self.path[i])
            basename = basename.rstrip(".tdms")
            for j in range(1, 3):
                ch_basename = basename + "_ch" + str(j)
                ch_mean = np.average(self.df_data[ch_basename].values)
                ch_flu = fun_rms(self.df_data[ch_basename].values, ch_mean)
                MandF_list.append(ch_mean)
                MandF_list.append(ch_flu)
            self.df_MandF.loc[basename] = MandF_list
        self.df_MandF = self.df_MandF[["mean_ch1", "mean_ch2", "fluctuation_ch1", "fluctuation_ch2"]]
        return self.df_MandF

    def save_param(self):
        return {"path": self.path, "NAME": self.NAME, "VULE1": self.VULE1, "VULE2": self.VULE2,\
            "dt": self.dt, "NoD": self.NoD, "E0": self.E0, "n": self.n, "m": self.m, "a": self.a, "b": self.b, "R2": self.R2}
        

    def save_csv(self, name):
        with open("Cw_param_" + name + ".csv", "w", encoding = "utf-8") as f:
            fieldname = ["path", "NAME", "VULE1", "VULE2", "dt", "NoD", "E0", "n", "m", "a", "b", "R2"]
            writer = csv.DictWriter(f, fieldnames = fieldname)
            writer.writeheader()
            writer.writerow(self.save_param())
            f.close()
        self.df_data.to_csv("Cw_" + name + ".csv")
        self.df_MandF.to_csv("Cw_MandF_" + name + ".csv")

    # linearization processing 
    def linearize(self):
        HWR_ch1 = self.df_MandF.copy()["mean_ch1"]
        self.E0 = HWR_ch1[0]
        HWR_lin = []
        for i in range(len(HWR_ch1)):
            lin = fun_linearize(HWR_ch1[i], self.E0, self.n, self.m)
            HWR_lin.append(lin)
        self.df_MandF["linearize"] = HWR_lin
        self.df_MandF = self.df_MandF[["linearize", "mean_ch1", "mean_ch2", "fluctuation_ch1", "fluctuation_ch2"]]
        return self.df_MandF
    
    # least squares method: find "a" and "b"
    def least_squares_M(self, np_ylist):
        x_lin = np.array(self.df_MandF.copy()["linearize"])
        y = np.array(np_ylist)
        a_b_coefficient = np.polyfit(x_lin, y, 1)
        self.a = a_b_coefficient[0]
        self.b = a_b_coefficient[1]
        y_pred = [self.a * i + self.b for i in x_lin]
        self.R2 = fun_R2(y, y_pred)
        return y_pred

    # convert voltage to flow velocity
    def convert_VtoU(self):
        x_lin = np.array(self.df_MandF.copy()["linearize"])
        y = [self.a * i + self.b for i in x_lin]
        return y


if __name__ == "__main__":
    HWR = HWRData()
    for i in range(3, 10):
        path = "G:/W_python/exp_velocity/test-data/hwr/20191113CTA1_00" + str(i) + ".tdms"
        HWR.path.append(path)
    HWR.NAME = "名称未設定"
    HWR.VULE1 = "電圧_0"
    HWR.VULE2 = "電圧_1"
    HWR.dt = 2E-5
    HWR.NoD = 600000
    HWR.n= 0.8
    HWR.m = 2.8
    print(HWR.file_read())
    HWR.cal_MandF()
    print(HWR.linearize())
    HWR.save_csv("HWR_test")