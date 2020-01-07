"""
December 19th 2019
            Author T.Mizumoto
"""
#! python 3
# ver.x2.10
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
    a1 = 0
    b1 = 0
    a2 = 0
    b2 = 0
    c2 = 0
    a3 = 0
    b3 = 0
    c3 = 0
    d3 = 0
    R2_1 = 0
    R2_2 = 0
    R2_3 = 0
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
        self.a1 = float(d["a1"])
        self.b1 = float(d["b1"])
        self.a2 = float(d["a2"])
        self.b2 = float(d["b2"])
        self.c2 = float(d["c2"])
        self.a3 = float(d["a3"])
        self.b3 = float(d["b3"])
        self.c3 = float(d["c3"])
        self.d3 = float(d["d3"])
        self.R2_1 = float(d["R2_1"])
        self.R2_2 = float(d["R2_2"])
        self.R2_3 = float(d["R2_3"])

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
            "dt": self.dt, "NoD": self.NoD, "E0": self.E0, "n": self.n, "m": self.m, "a1": self.a1, "b1": self.b1,\
            "a2": self.a2, "b2": self.b2, "c2": self.c2, "a3": self.a3, "b3": self.b3, "c3": self.c3, "d3": self.d3, \
            "R2_1": self.R2_1, "R2_2": self.R2_2, "R2_3": self.R2_3}
        

    def save_csv(self, name):
        with open("Cw_param_" + name + ".csv", "w", encoding = "utf-8") as f:
            fieldname = ["path", "NAME", "VULE1", "VULE2", "dt", "NoD", "E0", "n", "m", "a1", "b1", \
                "a2", "b2", "c2", "a3", "b3", "c3", "d3","R2_1", "R2_2", "R2_3"]
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
    
    # least squares method: find "a", "b"(Dimention 1) and "c"(Dimention 2)
    def least_squares_M(self, np_ylist):
        x_lin = np.array(self.df_MandF.copy()["linearize"])
        y = np.array(np_ylist)
        D1 = np.polyfit(x_lin, y, 1)
        D2 = np.polyfit(x_lin, y, 2)
        self.a1 = D1[0]
        self.b1 = D1[1]
        self.a2 = D2[0]
        self.b2 = D2[1]
        self.c2 = D2[2]
        y_D1 = [self.a1 * i + self.b1 for i in x_lin]
        y_D2 = [self.a2 * i ** 2 + self.b2 * i + self.c2 for i in x_lin]
        self.R2_1 = fun_R2(y, y_D1)
        self.R2_2 = fun_R2(y, y_D2)
        return y_D1, y_D2

    def D3_LSM(self, np_ylist):
        x = np.array(self.df_MandF.copy()["mean_ch1"])
        y = np.array(np_ylist)
        D3 = np.polyfit(x, y, 3)
        self.a3 = D3[0]
        self.b3 = D3[1]
        self.c3 = D3[2]
        self.d3 = D3[3]
        y_D3 = [self.a3 * i ** 3 + self.b3 * i ** 2 + self.c3 * i + self.d3 for i in x]
        self.R2_3 = fun_R2(y, y_D3)
        return y_D3

    # convert voltage to flow velocity
    def convert_VtoU(self):
        x_lin = np.array(self.df_MandF.copy()["linearize"])
        y = [self.a1 * i + self.b1 for i in x_lin]
        return y


if __name__ == "__main__":
    HWR = HWRData()
    for i in range(3, 10):
        path = "W_python/exp_velocity/test-data/hwr/20191113CTA1_00" + str(i) + ".tdms"
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