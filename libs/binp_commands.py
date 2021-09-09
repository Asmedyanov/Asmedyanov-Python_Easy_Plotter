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
    cnst.names_plots["График файла"]['Префикс'] = str(master.array_parametrs["Имя файла"].input.get())
    master.array_plots["График файла"].tit = cnst.names_plots["График файла"]
    for k in cnst.names_file_masks:
        if fnmatch.fnmatch(short_file_name, k[0]):
            data = k[1](file_name)
            nl = 0
            for d in data:
                d=Data_cut(master,d)
                master.array_plots["График файла"].plot(k[2][nl]+short_file_name,d)
                nl += 1
    master.array_plots["График файла"].replot()


def Clear_Plot(master):
    """Очистить график"""
    for k in master.array_plots.values():
        k.clear()

def Data_cut(master,d):
    left_border=float(master.array_parametrs["Граница слева"].input.get())
    right_border=float(master.array_parametrs["Граница справа"].input.get())
    if ((d['T'][1]>left_border)&(d['T'][1]<right_border)):
        return d
    ret=d.loc[((d['T']>left_border)&(d['T']<right_border))]
    ret.index=np.arange(len(ret))
    return ret

def Smooth_Plot(master):
    smoothw=float(master.array_parametrs["Ширина сглаживания"].input.get())
    for mykey in master.array_plots["График файла"].data.keys():
        dt=np.gradient(master.array_plots["График файла"].data[mykey]['T']).mean()
        master.array_plots["График файла"].data[mykey]['T']=master.array_plots["График файла"].data[mykey]['T'].rolling(int(smoothw/dt)).mean()+0.5*smoothw
        master.array_plots["График файла"].data[mykey]['V']=master.array_plots["График файла"].data[mykey]['V'].rolling(int(smoothw/dt)).mean()
        master.array_plots["График файла"].data[mykey]=master.array_plots["График файла"].data[mykey].dropna()
        master.array_plots["График файла"].data[mykey].index=np.arange(len(master.array_plots["График файла"].data[mykey]))
    master.array_plots["График файла"].replot()

def Stack_or_legend_plot(master):
    master.array_plots["График файла"].is_stack=master.check_values['Наложение графиков'].get()
    master.array_plots["График файла"].replot()

def get_dir(a):
    alist = a.split('/')
    adir = '/'.join(alist[:-1])
    return adir

def Group_directory(master):
    Add_File(master)
    dir_name = get_dir(master.full_file_name)
    os.chdir(dir_name)
    for name in os.listdir():
        numlist = re.findall(r'\d*\.\d+|\d+', name)
        n_exper = int(numlist[0])  # +int(name[0]=='F')
        if len(numlist) == 0:
            continue
        os.makedirs('V'+str(n_exper), exist_ok=True)
        os.rename(name, 'V'+str(n_exper)+'/'+name)
