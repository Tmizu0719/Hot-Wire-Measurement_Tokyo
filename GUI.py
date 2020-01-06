"""
December 26th 2019
            Author T.Mizumoto
"""
#! python 3
# ver.x2.10
# GUI.py  -  this program is the GUI program for processing for hot wire measurement.

import tkinter as tk
from tkinter import filedialog
import tkinter.scrolledtext as tksc
from process_function import fun_ROWcalib, fun_CSVcalib, fun_CON

class GUI:
    def first_window(self):
        root = tk.Tk()
        root.title("処理選択")
        root.geometry("450x330+100+250")
        lb = tk.Label(text = "実行する処理を選択してください．", font = ("Arial", 16))
        bt_row = tk.Button(root, text = "熱線校正(生データより)", command = self.row_window,\
            width = 20, height = 3, font = ("Arial", 14), bg = "#bbbbff")
        bt_csv = tk.Button(root, text = "熱線校正(csvファイルより)", command = self.csv_window, \
            width = 20, height = 3, font = ("Arial", 14), bg = "#bbffbb")
        bt_con = tk.Button(root, text = "流速変換", command = self.con_window, \
            width = 20, height = 3, font = ("Arial", 14), bg = "#ffbbbb")
        
        lb.pack(fill = "x", padx = 20, pady = 5)
        for i in [bt_row, bt_csv, bt_con]:
            i.pack(fill = "x", padx = 20, pady = 5)
        root.mainloop()
    
    def row_window(self):
        row = tk.Toplevel()
        row.title("熱線校正(生データより)")
        row.geometry("+300+250")
        row.focus_set()
        row.grab_set()
        # lvm frame
        fr_lvm = tk.LabelFrame(row, text = "lvmファイル", foreground = "green", font = ("Arial", 12))
        bt_lvm = tk.Button(fr_lvm, text = "ファイルを選択してください", \
            command = lambda: self.get_filepath("lvm", "lvm"), width = 30, height = 1, font = ("Arial", 10), bg = "#bbbbff")
        self.t_lvm = tksc.ScrolledText(fr_lvm, font = ("Arial", 8), wrap = tk.WORD, height = 10)
        # tdms frame
        fr_tdms = tk.LabelFrame(row, text = "tdmsファイル", foreground = "green", font = ("Arial", 12))
        bt_tdms = tk.Button(fr_tdms, text = "ファイルを選択してください", \
            command = lambda: self.get_filepath("tdms", "tdms"), width = 30, height = 1, font = ("Arial", 10), bg = "#bbbbff")
        self.t_tdms = tksc.ScrolledText(fr_tdms, font = ("Arial", 8), wrap = tk.WORD, height = 10)
        # HWR option frame
        fr_HWR = tk.LabelFrame(row, text = "熱線の設定", foreground = "green", font = ("Arial", 12))
        lb_NAME = tk.Label(fr_HWR, text = "NAME", font = ("Arial", 10))
        self.t_NAME = tk.Entry(fr_HWR, width = 20)
        self.t_NAME.insert(tk.END, "名称未設定")
        lb_VULE1 = tk.Label(fr_HWR, text = "VULE1", font = ("Arial", 10))
        self.t_VULE1 = tk.Entry(fr_HWR, width = 20)
        self.t_VULE1.insert(tk.END, "電圧_0")
        lb_VULE2 = tk.Label(fr_HWR, text = "VULE2", font = ("Arial", 10))
        self.t_VULE2 = tk.Entry(fr_HWR, width = 20)
        self.t_VULE2.insert(tk.END, "電圧_1")
        lb_dt = tk.Label(fr_HWR, text = "時間刻み", font = ("Arial", 10))
        self.t_dt = tk.Entry(fr_HWR, width = 10)
        self.t_dt.insert(tk.END, "2E-5")
        lb_NoD = tk.Label(fr_HWR, text = "データ総数", font = ("Arial", 10))
        self.t_NoD = tk.Entry(fr_HWR, width = 10)
        self.t_NoD.insert(tk.END, "600000")
        # coefficient of linearization
        fr_lin = tk.LabelFrame(row, text = "線形化係数", foreground = "green", font = ("Arial", 12))
        lb_n = tk.Label(fr_lin, text = "n", font = ("Arial", 10))
        self.t_n = tk.Entry(fr_lin, width = 10)
        self.t_n.insert(tk.END, "0.8")
        lb_m = tk.Label(fr_lin, text = "m", font = ("Arial", 10))
        self.t_m = tk.Entry(fr_lin, width = 10)
        self.t_m.insert(tk.END, "2.8")
        # output file name
        fr_out = tk.LabelFrame(row, text = "出力ファイルの名前", foreground = "green", font = ("Arial", 12))
        self.t_out = tk.Entry(fr_out, width = 50)
        self.t_out.insert(tk.END, "output_file_name")
        # enter button
        bt_enter = tk.Button(row, text = "実行", command = self.process_ROW, width = 20, height = 1, font = ("Arial", 12), bg = "#ff6464") 

        fr_lvm.grid(row = 0, column = 0, columnspan = 2, padx = 10, pady = 5)
        fr_tdms.grid(row = 0, column = 3, columnspan = 2, padx = 10, pady = 5)
        for i in [bt_lvm, self.t_lvm, bt_tdms, self.t_tdms]:
            i.pack()
        fr_HWR.grid(row = 1, columnspan = 5)
        count = 0
        for i in [lb_NAME, lb_VULE1, lb_VULE2, lb_dt, lb_NoD, self.t_NAME, self.t_VULE1, self.t_VULE2, self.t_dt, self.t_NoD]:
            if count >= 5:
                i.grid(row = 1, column = count - 5)
            else:
                i.grid(row = 0, column = count)
            count += 1
        fr_lin.grid(row = 2, columnspan = 5)
        lb_n.grid(row = 0, column = 0)
        lb_m.grid(row = 0, column = 1)
        self.t_n.grid(row = 1, column = 0)
        self.t_m.grid(row = 1, column = 1)
        fr_out.grid(row = 3, columnspan = 5)
        self.t_out.pack()
        bt_enter.grid(row = 4, columnspan = 5)

    def csv_window(self):
        csv = tk.Toplevel()
        csv.title("熱線校正(csvファイルより)")
        csv.geometry("+300+250")
        csv.focus_set()
        csv.grab_set()
        # pitot
        fr_pitot = tk.LabelFrame(csv, text = "Pitot の校正データ", foreground = "green", font = ("Arial", 12))
        bt_pitot = tk.Button(fr_pitot, text = "ファイルを選択してください", \
            command = lambda: self.get_filepath("csv", "pitot"), width = 30, height = 1, font = ("Arial", 10), bg = "#bbffbb")
        self.t_pitot = tk.Entry(fr_pitot, font = ("Arial", 8), width = 60)
        # HWR
        fr_HWR = tk.LabelFrame(csv, text = "熱線の校正データ(Cw_)", foreground = "green", font = ("Arial", 12))
        bt_HWR = tk.Button(fr_HWR, text = "ファイルを選択してください", \
            command = lambda: self.get_filepath("csv", "HWR"), width = 30, height = 1, font = ("Arial", 10), bg = "#bbffbb")
        self.t_HWR = tk.Entry(fr_HWR, font = ("Arial", 8), width = 60)
        # coefficient of linearization
        fr_lin = tk.LabelFrame(csv, text = "線形化係数( 'pass' ならファイルを参照)", foreground = "green", font = ("Arial", 12))
        lb_n = tk.Label(fr_lin, text = "n", font = ("Arial", 10))
        self.t_n = tk.Entry(fr_lin, width = 10)
        self.t_n.insert(tk.END, "pass")
        lb_m = tk.Label(fr_lin, text = "m", font = ("Arial", 10))
        self.t_m = tk.Entry(fr_lin, width = 10)
        self.t_m.insert(tk.END, "pass")
        # output file name
        fr_out = tk.LabelFrame(csv, text = "出力ファイルの名前", foreground = "green", font = ("Arial", 12))
        self.t_out = tk.Entry(fr_out, width = 50)
        self.t_out.insert(tk.END, "output_file_name")
        # enter button
        bt_enter = tk.Button(csv, text = "実行", command = self.process_CSV, width = 20, height = 1, font = ("Arial", 12), bg = "#ff6464") 

        fr_pitot.grid(row = 0, column = 0)
        fr_HWR.grid(row = 0, column = 1)
        fr_lin.grid(row = 1, columnspan = 2)
        fr_out.grid(row = 2, columnspan = 2)
        lb_n.grid(row = 0, column = 0)
        lb_m.grid(row = 0, column = 1)
        self.t_n.grid(row = 1, column = 0)
        self.t_m.grid(row = 1, column = 1)
        self.t_out.pack()
        for i in [bt_pitot, self.t_pitot, bt_HWR, self.t_HWR]:
            i.pack()
        bt_enter.grid(row = 3, columnspan = 2)

    def con_window(self):
        con = tk.Toplevel()
        con.title("流速変換")
        con.geometry("+300+250")
        con.focus_set()
        con.grab_set()
        # HWR(calibration)
        fr_cal = tk.LabelFrame(con, text = "熱線の校正データ(Cw_)", foreground = "green", font = ("Arial", 12))
        bt_cal = tk.Button(fr_cal, text = "ファイルを選択してください", \
            command = lambda: self.get_filepath("csv", "cal"), width = 30, height = 1, font = ("Arial", 10), bg = "#ffbbbb")
        self.t_cal = tk.Entry(fr_cal, font = ("Arial", 8), width = 60)
        # HWR
        fr_HWR = tk.LabelFrame(con, text = "熱線計測データ(.tdms)", foreground = "green", font = ("Arial", 12))
        bt_HWR = tk.Button(fr_HWR, text = "ファイルを選択してください", \
            command = lambda: self.get_filepath("tdms", "HWR"), width = 30, height = 1, font = ("Arial", 10), bg = "#ffbbbb")
        self.t_HWR = tksc.ScrolledText(fr_HWR, font = ("Arial", 8), wrap = tk.WORD, height = 10)
        # Traverse
        fr_traverse = tk.LabelFrame(con, text = "座標点データ", foreground = "green", font = ("Arial", 12))
        bt_traverse = tk.Button(fr_traverse, text = "ファイルを選択してください", \
            command = lambda: self.get_filepath("csv", "traverse"), width = 30, height = 1, font = ("Arial", 10), bg = "#ffbbbb")
        self.t_traverse = tk.Entry(fr_traverse, font = ("Arial", 8), width = 60)
        # select axis
        fr_axis = tk.LabelFrame(con, text = "使用する座標軸を選択してください", foreground = "green", font = ("Arial", 12))
        self.var = tk.IntVar(fr_axis, value = 1)
        axis_list = ["x", "y", "z"]
        for i in range(3):
            radio = tk.Radiobutton(fr_axis, text = axis_list[i], value = i + 1, var = self.var)
            radio.pack(side = tk.LEFT)
        # output file name
        fr_out = tk.LabelFrame(con, text = "出力ファイルの名前", foreground = "green", font = ("Arial", 12))
        self.t_out = tk.Entry(fr_out, width = 50)
        self.t_out.insert(tk.END, "output_file_name")
        # enter button
        bt_enter = tk.Button(con, text = "実行", command = self.process_CON, width = 20, height = 1, font = ("Arial", 12), bg = "#ff6464") 

        fr_cal.grid(row = 0, column = 0)
        fr_HWR.grid(row = 0, column = 1)
        fr_traverse.grid(row = 0, column = 2)
        fr_axis.grid(row = 1, columnspan = 3)
        fr_out.grid(row = 2, columnspan = 3)
        bt_enter.grid(row = 3, columnspan = 3)
        for i in [bt_cal, self.t_cal, bt_HWR, self.t_HWR, bt_traverse, self.t_traverse, self.t_out]:
            i.pack()

    def process_ROW(self):
        param = self.get_ROWparam()
        fun_ROWcalib(param)
    
    def process_CSV(self):
        param = self.get_CSVparam()
        fun_CSVcalib(param)

    def process_CON(self):
        param = self.get_CONparam()
        fun_CON(param)

    def get_filepath(self, filetype, name):
        filetype_list = [(filetype + " file", "*." + filetype), ("all file", "*")]
        filepath = filedialog.askopenfilenames(filetype = filetype_list, title = "ファイルを選択してください．")
        filepath = list(filepath)
        exec("self.t_{}.insert(tk.END, filepath)".format(name))
    
    def get_ROWparam(self):
        param_list = [self.t_lvm, self.t_tdms, self.t_NAME, self.t_VULE1, self.t_VULE2, self.t_dt, self.t_NoD, self.t_n, self.t_m, self.t_out]
        param = []
        count = 0
        for i in param_list:
            if count <= 1:
                param.append(i.get("1.0", "end -1c"))
            else:
                param.append(i.get())
            count += 1
        return param

    def get_CSVparam(self):
        param_list = [self.t_pitot, self.t_HWR, self.t_n, self.t_m, self.t_out]
        param = []
        for i in param_list:    
            param.append(i.get())
        return param
    
    def get_CONparam(self):
        param_list = [self.t_cal, self.t_HWR, self.t_traverse, self.var, self.t_out]
        param = []
        for i in param_list:
            param.append(i.get())
        return param

if __name__ == "__main__":
    gui = GUI()
    gui.first_window()