# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 16:48:32 2020

@author: asmedyanov
"""

from tkinter import *  # модуль оконного интерфейса
import pandas as pd  # модуль баз банных
from libs.binp_consts import *  # модуль констант
from libs.binp_plots import *  # Модуль графиков
from libs.binp_parametrs import *  # модуль параметров


class Oscilloscop:  # базовый класс
    def __init__(self, master):
        self.menubar=Menu(master)

        self.filemenu=Menu(self.menubar)
        for k in names_commands_file.keys():
            self.filemenu.add_command(
                label=k,
                command=lambda k=k: names_commands_file[k][0](self),
                accelerator=names_commands_file[k][1])
        self.menubar.add_cascade(label="Файл", menu=self.filemenu)

        self.plotmenu=Menu(self.menubar)
        for k in names_commands_plot.keys():
            self.plotmenu.add_command(
                label=k,
                command=lambda k=k: names_commands_plot[k][0](self),
                accelerator=names_commands_plot[k][1])
        self.menubar.add_cascade(label="График", menu=self.plotmenu)

        master.config(menu=self.menubar)
        for mykey in names_commands_file.keys():
            self.filemenu.bind_all(names_commands_file[mykey][2],lambda event, mykey=mykey:names_commands_file[mykey][0](self))
        for mykey in names_commands_plot.keys():
            self.plotmenu.bind_all(names_commands_plot[mykey][2],lambda event, mykey=mykey:names_commands_plot[mykey][0](self))
        # массив рамок в окне интерфейса
        self.array_frames = {k: LabelFrame(
            master, text=k) for k in names_frames}
        self.array_plots = {k: Embaded_Plot(
            self.array_frames["Окно графиков"], v) for k,v in names_plots.items()}  # массив графиков
        self.array_parametrs = {k: Parametr(
            self.array_frames["Окно параметров"], [k]+v) for k,v in names_parametrs.items()}  # массив параметров
        self.full_file_name = ''
        for k in self.array_frames.values():
            k.pack(side=LEFT, fill=BOTH)
        self.array_frames["Окно графиков"].pack(side=TOP, fill=BOTH, expand=1)
