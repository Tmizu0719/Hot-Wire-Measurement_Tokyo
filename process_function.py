"""
December 26th 2019
            Author T.Mizumoto
"""
#! python 3
# ver.x3.20
# process_function.py  -  this program summarizes each proces

from Pitot import PitotData
from HWR import HWRData, fun_linearize
from graph import Graph
import matplotlib.pyplot as plt
from traverse import TraverseData
import pandas as pd
import os

def fun_mkdir(name):
    cwd_name = os.getcwd()
    judge_path = os.path.exists(cwd_name + "/" + name)
    if judge_path == False:
        os.makedirs(cwd_name + "/" + name)
    

def fun_ROWcalib(param):
    param = param
    # enter the parameter
    pitot = PitotData()
    pitot.path = str(param[0]).split(" ")
    hwr = HWRData()
    count = 1
    hwr.path = str(param[1]).split(" ")
    hwr.NAME = param[2]
    hwr.VULE1 = param[3]
    hwr.VULE2 = param[4]
    hwr.dt = float(param[5])
    hwr.NoD = int(param[6])
    hwr.n = float(param[7])
    hwr.m = float(param[8])
    output_name = param[9]
    
    # pitot
    pitot.file_read()
    #pitot.save_csv(output_name)
    print(pitot.df_data)

    # HWR
    hwr.file_read()
    print(hwr.df_data)
    hwr.cal_MandF()
    hwr.linearize()
    print(hwr.df_MandF)

    # graph
    y_pitot = pitot.df_data.astype({"U_true[m/s]": float})
    y_pitot = y_pitot["U_true[m/s]"]
    y_pitot[0] = 0
    y_D1, y_D2 = hwr.least_squares_M(y_pitot)
    y_D3 = hwr.D3_LSM(y_pitot)
    x_lin = hwr.df_MandF["linearize"]
    x = hwr.df_MandF["mean_ch1"]
    graph = Graph()
    graph.label = ["Pitot@Lin", "predict@D1", "predict@D2", "pred_NotLin@3", "Pitot@mean"]
    graph.mark(x_lin, y_pitot, 0)
    graph.line(x_lin, y_D1, 1)
    graph.line(x_lin, y_D2, 2)
    graph.line(x, y_D3, 3)
    graph.exp_mark(x, y_pitot, 4)
    graph.lim(0, 7, 0, 60)
    graph.axis_label("Voltage by HWR", "U by Pitot")
    plt.legend()

    # save
    folder_name = "Calib_dest"
    fun_mkdir(folder_name)
    graph.save_graph(folder_name + "/" + "Cg_" + output_name)
    pitot.save_csv(output_name, folder_name)
    hwr.save_csv(output_name, folder_name)
    graph.show()

def fun_CSVcalib(param):
    param = param
    output_name = param[4]
    
    # pitot
    pitot = PitotData()
    pitot.csv_read(param[0])
    print(pitot.df_data)
    
    # HWR
    hwr = HWRData()
    hwr.csv_read(param[1])
    print(hwr.df_MandF)
    if param[2] == "pass":
        pass
    else:
        hwr.n = float(param[2])
    if param[3] == "pass":
        pass
    else:
        hwr.m = float(param[3])
    hwr.linearize()
    
    # graph
    graph = Graph()
    graph.label = ["Pitot@Lin", "predict@D1", "predict@D2", "pred_NotLin@D3", "Pitot@mean"]
    y_pitot = pitot.df_data.astype({"U_true[m/s]": float})
    y_pitot = pitot.df_data["U_true[m/s]"]
    y_pitot[0] = 0
    y_D1, y_D2 = hwr.least_squares_M(y_pitot)
    y_D3 = hwr.D3_LSM(y_pitot)
    x_lin = hwr.df_MandF["linearize"]
    x = hwr.df_MandF["mean_ch1"]
    graph.mark(x_lin, y_pitot, 0)
    graph.line(x_lin, y_D1, 1)
    graph.line(x_lin, y_D2, 2)
    graph.line(x, y_D3, 3)
    graph.exp_mark(x, y_pitot, 4)
    graph.lim(0, 7, 0, 60)
    graph.axis_label("Voltage by HWR", "U by Pitot")
    plt.legend()

    # save
    folder_name = "Calib_dest"
    graph.save_graph(folder_name + "/" + "Cg_" + output_name)
    pitot.save_csv(output_name, folder_name)
    hwr.save_csv(output_name, folder_name)
    graph.show()

def fun_CON(param):
    param = param
    output_name = param[4]

    # HWR
    hwr = HWRData()
    hwr.csv_read(param[0])
    hwr.path = str(param[1]).split(" ")
    hwr.file_read()
    print(hwr.df_data)
    hwr.cal_MandF()
    hwr.linearize()
    print(hwr.df_MandF)
    velocity = hwr.convert_VtoU()

    # Traverse
    tr = TraverseData()
    tr.path = param[2]
    tr.file_read()
    axis = param[3]
    if axis == 1:
        axis = "x"
    elif axis == 2:
        axis = "y"
    elif axis == 3:
        axis = "z"
    coordinate = tr.df_coordinate[axis]

    # graph
    graph = Graph()
    graph.axis_label = ["measured"]
    graph.mark(velocity, coordinate, 0)
    graph.axis_label("velocity", "coordinate")
    plt.legend()

    # save
    df_VandC = pd.DataFrame([velocity, coordinate], columns = ["velocity", "coordinate"], index = range(len(velocity)))
    df_VandC.to_csv(output_name + "csv")
    graph.save_graph(output_name + "png")
    graph.show()