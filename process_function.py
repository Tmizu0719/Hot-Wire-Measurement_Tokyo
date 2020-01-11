"""
December 26th 2019
            Author T.Mizumoto
"""
#! python 3
# ver.x4.11
# process_function.py  -  this program summarizes each proces

from Pitot import PitotData
from HWR import HWRData, fun_linearize
from graph import Graph
import matplotlib.pyplot as plt
from traverse import TraverseData
import pandas as pd
import os
import numpy as np

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
    #y_pitot[0] = 0
    y_D1, y_D2 = hwr.least_squares_M(y_pitot)
    y_D3 = hwr.D3_LSM(y_pitot)
    x_lin = np.array(hwr.df_MandF["linearize"])
    x = np.array(hwr.df_MandF["mean_ch1"])
    # sort
    y_sort = np.sort(np.array(y_pitot))
    yindex_sort = np.argsort(y_pitot)
    x_lin_sort = x_lin[yindex_sort]
    x_sort = x[yindex_sort]
    y_D1_sort = y_D1[yindex_sort]
    y_D2_sort = y_D2[yindex_sort]
    y_D3_sort = y_D3[yindex_sort]

    print("Now creating graph...")
    graph = Graph()
    graph.label = ["Pitot@Lin", "predict@D1", "predict@D2", "pred_NotLin@3", "Pitot@mean"]
    graph.mark(x_lin_sort, y_sort, 0)
    graph.line(x_lin_sort, y_D1_sort, 1)
    graph.line(x_lin_sort, y_D2_sort, 2)
    graph.line(x_sort, y_D3_sort, 3)
    graph.exp_mark(x_sort, y_sort, 4)
    graph.lim(0, 7, 0, 60)
    graph.axis_label("Voltage by HWR", "U by Pitot")
    plt.legend()

    # save
    folder_name = "Calib_dest"
    fun_mkdir(folder_name)
    outfolder_name = folder_name + "/" + output_name
    fun_mkdir(outfolder_name)
    graph.save_graph(outfolder_name + "/" + "Cg_" + output_name)
    pitot.save_csv(output_name, outfolder_name)
    hwr.save_csv(output_name, outfolder_name)
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
    #y_pitot[0] = 0
    y_D1, y_D2 = hwr.least_squares_M(y_pitot)
    y_D3 = hwr.D3_LSM(y_pitot)
    x_lin = hwr.df_MandF["linearize"]
    x = hwr.df_MandF["mean_ch1"]
    # sort
    y_sort = np.sort(np.array(y_pitot))
    yindex_sort = np.argsort(y_pitot)
    x_lin_sort = x_lin[yindex_sort]
    x_sort = x[yindex_sort]
    y_D1_sort = y_D1[yindex_sort]
    y_D2_sort = y_D2[yindex_sort]
    y_D3_sort = y_D3[yindex_sort]
    
    print("Now creating graph...")
    graph.mark(x_lin_sort, y_sort, 0)
    graph.line(x_lin_sort, y_D1_sort, 1)
    graph.line(x_lin_sort, y_D2_sort, 2)
    graph.line(x_sort, y_D3_sort, 3)
    graph.exp_mark(x_sort, y_sort, 4)
    graph.lim(0, 7, 0, 60)
    graph.axis_label("Voltage by HWR", "U by Pitot")
    plt.legend()

    # save
    folder_name = "Calib_dest"
    fun_mkdir(folder_name)
    outfolder_name = folder_name + "/" + output_name
    fun_mkdir(outfolder_name)
    graph.save_graph(outfolder_name + "/" + "Cg_" + output_name)
    pitot.save_csv(output_name, outfolder_name)
    hwr.save_csv(output_name, outfolder_name)
    graph.show()


def fun_CON(param):
    param = param
    output_name = param[4]

    # HWR
    hwr = HWRData()
    param_path = str(param[0]).split(" ")
    print(param_path)
    address, orgname = hwr.separate_csvpath(param_path[0])
    hwr.param_read(address, orgname)
    hwr.path = str(param[1]).split(" ")
    hwr.file_read()
    print(hwr.df_data)
    tag_list = ["Dimention1_", "Dimention2_", "Dimention3_"]
    tag = []
    for i in range(len(param_path)):
        for j in range(3):
            tag.append(tag_list[j] + str(i))
    df_velocity = pd.DataFrame(columns = tag)
    count = 0
    for i in param_path:
        address, orgname = hwr.separate_csvpath(i)
        hwr.param_read(address, orgname)
        hwr.path = str(param[1]).split(" ")
        hwr.cal_MandF()
        hwr.linearize_skip()
        print(hwr.df_MandF)
        velocity = hwr.convert_VtoU()
        for j in range(3):
            df_velocity[tag_list[j] + str(count)] = velocity[j]
        count += 1
        hwr.df_MandF = pd.DataFrame(columns = ["mean_ch1", "fluctuation_ch1", "mean_ch2", "fluctuation_ch2"])
    print(df_velocity)

    # mean
    for i in range(len(param_path)):
        if i == 0:
            df_velocity["D1_mean"] = df_velocity["Dimention1_0"]
            df_velocity["D2_mean"] = df_velocity["Dimention2_0"]
            df_velocity["D3_mean"] = df_velocity["Dimention3_0"]
        else:
            for j in range(1, 4):
                exec("df_velocity['D%s_mean'] = \
                    (df_velocity['D%s_mean'] + df_velocity['Dimention%s_%s']) / 2"
                    %(j, j, j, i)) 
    print(df_velocity)

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
    print("Now creating graph...")
    graph = Graph()
    mean_list = ["D1_mean", "D2_mean", "D3_mean"]
    graph.label = df_velocity.columns.tolist()
    [graph.label.remove(mean_list[i]) for i in range(3)]
    count = 0
    for i in graph.label:    
        graph.mark(df_velocity[i], coordinate, count)
        count += 1
    graph.line_NUL(df_velocity["D1_mean"], coordinate, 0, mean_list[0])
    graph.line_NUL(df_velocity["D2_mean"], coordinate, 1, mean_list[1])
    graph.line_NUL(df_velocity["D3_mean"], coordinate, 2, mean_list[2])
    graph.axis_label("velocity", "coordinate")

    plt.legend(bbox_to_anchor=(1.1, 1), borderaxespad = 0)
    plt.subplots_adjust(left = 0.2, right = 0.6)

    # save
    folder_name = "FLOW_data"
    fun_mkdir(folder_name)
    outfolder_name = folder_name + "/" + output_name
    fun_mkdir(outfolder_name)
    df_velocity["coordinate"] = coordinate
    df_velocity.to_csv(outfolder_name + "/" + output_name + ".csv")
    graph.save_graph(outfolder_name + "/" + output_name)
    graph.show_OSlegend()