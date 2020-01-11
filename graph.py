"""
December 7th 2019
            Author T.Mizumoto
"""
#! python3
# ver.x1.20
# graph.py  -  my graph style

import numpy
import matplotlib.pyplot as plt

class Graph:
    def __init__(self):
        plt.rcParams['font.family'] = 'Arial'
        plt.rcParams['xtick.direction'] = 'in'
        plt.rcParams['ytick.direction'] = 'in'
        plt.rcParams['xtick.major.width'] = 1.0	
        plt.rcParams['ytick.major.width'] = 1.0
        plt.rcParams['font.size'] = 15 
        plt.rcParams['axes.linewidth'] = 1.0
        plt.rcParams["legend.framealpha"] = 1.0
        plt.rcParams["legend.fancybox"] = False
        self.colorlist = ["blue", "green", "red", "orange", "magenta", "black", "blue", "green", "red", "orange", "magenta", "black"]
        self.markerlist = ['o','^','v','<','>','d','*', 'o','^','v','<','>','d','*']
        self.stylelist = ['-', '--', '-.', ':', '-', '--', '-.', ':']
        self.dashes_point = [0.8, 0.5, 2, 0.5]
        plt.figure(figsize = (6.47, 4), dpi = 200)
        plt.grid(which = "both")
        self.label = []

    # only num <= 8
    def line(self, x, y, num):
        return plt.plot(x, y, color = self.colorlist[num], ls = self.stylelist[num],\
            label = self.label[num])

    # not use self.label
    def line_NUL(self, x, y, num, label):
        return plt.plot(x, y, color = self.colorlist[num], ls = self.stylelist[num],\
            label = label)
    
    def mark(self, x, y, num):
        return plt.plot(x, y, color = self.colorlist[num], Linestyle = "None", \
            marker = self.markerlist[num], label = self.label[num])

    def exp_mark(self, x, y, num):
        return plt.plot(x,y, label = self.label[num], marker= 'o', \
            markerfacecolor ='w', color = 'k', linestyle = 'None')

    def axis_label(self, x, y):
        xlabel = plt.xlabel(x)
        ylabel = plt.ylabel(y)
        return xlabel, ylabel
    
    def show(self):
        plt.legend()
        plt.show()
    
    def show_OSlegend(self):
        plt.legend(bbox_to_anchor=(1.1, 1), borderaxespad = 0)
        plt.subplots_adjust(left = 0.2, right = 0.6)
        plt.show()
    
    def lim(self, xmin, xmax, ymin, ymax):
        plt.xlim(xmin, xmax)
        plt.ylim(ymin, ymax)
        
    def save_graph(self, name):
        plt.savefig(name + ".png")


if __name__ == "__main__":
    graph = Graph()
    x = range(1000)
    y = range(1000)
    graph.label = ["test"]

    graph.line(x, y, 0)
    graph.axis_label("time", "volum")
    graph.line_NUL(x, y, 2, "NUL")
    plt.legend()
    plt.show()