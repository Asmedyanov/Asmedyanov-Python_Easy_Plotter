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
        # массив рамок в окне интерфейса
        self.array_frames = {k: LabelFrame(
            master, text=k) for k in names_frames}
        self.array_plots = {k: Embaded_Plot(
            self.array_frames["Окно графиков"], names_plots[k]) for k in names_plots.keys()}  # массив графиков
        self.array_parametrs = {k: Parametr(
            self.array_frames["Окно параметров"], names_parametrs[k]) for k in names_parametrs.keys()}  # массив параметров
        self.array_buttons = {k: Button(self.array_frames['Окно команд'], text=str(k),
                                        command=lambda k=k: names_commands[k][1](self)) for k in names_commands.keys()}  # массив кнопок
        self.full_file_name = ''
        for k in self.array_buttons.values():
            k.pack(fill=BOTH)
        for k in self.array_frames.values():
            k.pack(side=LEFT, fill=BOTH)
        self.array_frames["Окно графиков"].pack(side=TOP, fill=BOTH, expand=1)
