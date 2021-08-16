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
        self.array_frames = [LabelFrame(master, text=k) for k in names_frames]
        self.array_plots = [Embaded_Plot(
            self.array_frames[0], k) for k in names_plots]  # массив графиков
        self.array_parametrs = [Parametr(
            self.array_frames[1], k) for k in names_parametrs]  # массив параметров
        self.array_buttons = [Button(self.array_frames[2], text=str(
            k[0]), command=lambda k=k: k[1](self)) for k in names_commands]  # массив кнопок
        self.full_file_name = ''
        for k in self.array_buttons:
            k.pack(fill=BOTH)
        for k in self.array_frames:
            k.pack(side=LEFT, fill=BOTH)
        self.array_frames[0].pack(side=TOP, fill=BOTH, expand=1)
