# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 12:48:46 2020

@author: asmedyanov
"""
from scipy.fftpack import rfft, irfft, fftfreq
import re
from scipy import signal
import libs.binp_consts as cnst
from tkinter import *  # модуль оконного интерфейса
from tkinter import filedialog as fd  # модуль файлового диалога
# модуль масок строк
import fnmatch
import numpy as np
import pandas as pd
import os
from scipy.signal import argrelextrema
from matplotlib.animation import FuncAnimation

import warnings
warnings.filterwarnings("ignore")

mks = 1.0e6


def Add_File(master):
    """Добавить файл на график"""
    file_name = fd.askopenfilename()  # узнать полное имя файла из диалога
    master.full_file_name = file_name #записать полное имя файла в 
    short_file_name = file_name.split('/')[-1]
    master.array_parametrs["Имя файла"].print(
        short_file_name)  # Записать новое имя файла
    cnst.names_plots["График файла"][3] = str(master.array_parametrs["Имя файла"].input.get())
    master.array_plots["График файла"].tit = cnst.names_plots["График файла"]
    for k in cnst.names_file_masks:
        if fnmatch.fnmatch(short_file_name, k[0]):
            data = k[1](file_name)
            nl = 0
            for d in data:
                d['label'] = k[2][nl]
                master.array_plots["График файла"].plot(d)
                nl += 1


def Clear_Plot(master):
    """Очистить график"""
    for k in master.array_plots.values():
        k.clear()
