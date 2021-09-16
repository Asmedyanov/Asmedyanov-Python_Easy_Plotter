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


def get_filename(master):
    file_name = fd.askopenfilename()  # узнать полное имя файла из диалога
    master.full_file_name = file_name
      # записать полное имя файла в
    short_file_name = file_name.split('/')[-1]
    master.array_parametrs["Имя файла"].print(
    short_file_name)  # Записать новое имя файла
    cnst.names_plots["График файла"]['Префикс'] = str(
        master.array_parametrs["Имя файла"].input.get())
    master.array_plots["График файла"].tit = cnst.names_plots["График файла"]

def Add_File_str(master, file_name):
    master.array_plots["График файла"].stat_flag=False
    short_file_name = file_name.split('/')[-1]
    for k in cnst.names_file_masks:
        if fnmatch.fnmatch(short_file_name, k[0]):
            data = k[1](file_name)
            nl = 0
            for d in data:
                d = Data_cut(master, d)
                master.array_plots["График файла"].plot(
                    k[2][nl]+' '+short_file_name, d)
                nl += 1


def Add_File(master):
    """Добавить файл на график"""
    get_filename(master)
    Add_File_str(master, master.full_file_name)
    master.array_plots["График файла"].replot()


def Clear_Plot(master):
    """Очистить график"""
    for k in master.array_plots.values():
        k.clear()


def Data_cut(master, d):
    left_border = float(master.array_parametrs["Граница слева"].input.get())
    right_border = float(master.array_parametrs["Граница справа"].input.get())
    if ((d['T'][1] > left_border) & (d['T'][1] < right_border)):
        return d
    ret = d.loc[((d['T'] > left_border) & (d['T'] < right_border))]
    ret.index = np.arange(len(ret))
    return ret


def Smooth_Plot(master):
    smoothw = float(master.array_parametrs["Ширина сглаживания"].input.get())
    for mykey in master.array_plots["График файла"].data.keys():
        dt = np.gradient(
            master.array_plots["График файла"].data[mykey]['T']).mean()
        master.array_plots["График файла"].data[mykey]['T'] = master.array_plots["График файла"].data[mykey]['T'].rolling(
            int(smoothw/dt)).mean()+0.5*smoothw
        master.array_plots["График файла"].data[mykey]['V'] = master.array_plots["График файла"].data[mykey]['V'].rolling(
            int(smoothw/dt)).mean()
        master.array_plots["График файла"].data[mykey] = master.array_plots["График файла"].data[mykey].dropna()
        master.array_plots["График файла"].data[mykey].index = np.arange(
            len(master.array_plots["График файла"].data[mykey]))
    master.array_plots["График файла"].replot()


def Stack_or_legend_plot(master):
    master.array_plots["График файла"].is_stack = not(
        master.check_values['Наложение'].get())
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
        n_exper = int(numlist[0])
        if len(numlist) == 0:
            continue
        os.makedirs('V'+str(n_exper), exist_ok=True)
        os.rename(name, 'V'+str(n_exper)+'/'+name)

def Add_directory_str(master,dir_name):
    os.chdir(dir_name)
    for t_name in os.listdir():
        Add_File_str(master,t_name)


def Add_directory(master):
    get_filename(master)
    dir_name = get_dir(master.full_file_name)
    Add_directory_str(master,dir_name)
    master.array_plots["График файла"].replot()


def Start_or_No_Start_plot(master):
    master.array_plots["График файла"].have_start = master.check_values['Стартовые'].get()

    data_t = master.array_plots["График файла"].data
    master.array_plots["График файла"].clear()
    for k, v in data_t.items():
        master.array_plots["График файла"].plot(k, v)
    master.array_plots["График файла"].replot()

def Process_data_pmi27(data,dataout):
    for key, v in data.items():
            if key[0] == 'I':
                When_Current = v.loc[v['V'] > 1]
                if len(When_Current) == 0:
                    dataout["Current_position"].append(0)
                    dataout["Current_length"].append(0)
                else:
                    dataout["Current_position"].append(When_Current['T'].min())
                    dataout["Current_length"].append(
                        When_Current['T'].max()-When_Current['T'].min())
            if key[0] == 'P':
                When_Pressure = v.loc[((v['T'] > 2000) & (v['T'] < 8000))]
                Pressure_pic_amplitude=np.max(When_Pressure['V'])
                dataout['Pressure_pic_amplitude'].append(Pressure_pic_amplitude)
                Pressure_pic_time = When_Pressure['T'].loc[When_Pressure['V']
                                                           == Pressure_pic_amplitude].min()
                dataout['Pressure_pic_time'].append(float(Pressure_pic_time))

def Process_plot_pmi27(stattable, master):
    argument_key='Current_length'
    function_keys=['Pressure_pic_amplitude','Pressure_pic_time']
    stattable= stattable.sort_values(argument_key)
    for mykey in function_keys:
        data=pd.DataFrame()
        data['T']=stattable[argument_key]
        data['V']=stattable[mykey]
        master.array_plots["График файла"].plot(mykey, data)
    master.array_plots["График файла"].replot()

def Statistic_plot_pmi27(stattable,master):
    argument_key='Current_length'
    stattable= stattable.sort_values('Num')
    stattable.index=stattable['Num']
    refval=dict()
    deltalist=['Pressure_pic_amplitude','Pressure_pic_time']
    for mykey in deltalist:
        refval[mykey]=0
        stattable[mykey+'_delta']=0
    for i in stattable['Num']:
        for mykey in deltalist:
            if stattable[argument_key][i]==0: refval[mykey]=stattable[mykey][i]
            stattable[mykey+'_delta'][i]=stattable[mykey][i]-refval[mykey]
    statlist=['_avg','_std']
    statkeys=['Current_length','Pressure_pic_amplitude_delta','Pressure_pic_time_delta']
    statSubset=dict()
    statSubsettemp=dict()
    for mykey in statkeys:
        statSubset[mykey]=list()
        statSubsettemp[mykey]=list()
    #Выполним разбиение на подмассивы
    Nzeros=4
    Countzeros=0
    for i in stattable['Num']:
        if stattable[argument_key][i]==0:
            if (i!=stattable['Num'].max())&(stattable[argument_key][i+1]==0):
                continue
            if Countzeros==Nzeros:
                Countzeros=0
                for mykey in statkeys:
                    statSubset[mykey].append(statSubsettemp[mykey])
                    statSubsettemp[mykey]=list()
            Countzeros+=1
        else:
            for mykey in statkeys:
                statSubsettemp[mykey].append(stattable[mykey][i])
            if i==stattable['Num'].max():
                for mykey in statkeys:
                    statSubset[mykey].append(statSubsettemp[mykey])
                    statSubsettemp[mykey]=list()
    
    statDict=dict()
    for mykey in statkeys:
        statDict[mykey+'_avg']=list()
        statDict[mykey+'_std']=list()
        for sublist in statSubset[mykey]:
            statDict[mykey+'_avg'].append(np.mean(sublist))
            statDict[mykey+'_std'].append(np.std(sublist))
    function_keys=['Pressure_pic_amplitude_delta','Pressure_pic_time_delta']
    for mykey in function_keys:
        data=pd.DataFrame()
        for st in statlist:
            data['T'+st]=statDict[argument_key+st]
            data['V'+st]=statDict[mykey+st]
        master.array_plots["График файла"].plot(mykey, data)
        print(data)
    master.array_plots["График файла"].stat_flag=True
    master.array_plots["График файла"].replot()
    
    return stattable

    """ for mykey in function_keys:
        data=pd.DataFrame()
        data['T']=stattable[argument_key]
        data['V']=stattable[mykey]
        master.array_plots["График файла"].plot(mykey, data)
    master.array_plots["График файла"].replot() """
    
        


def Process_directory(master):
    # Открыть папку с выстрелами
    file_name = fd.askopenfilename()  # узнать имя файла из диалога
    master.full_file_name = file_name
    dir_path = file_name.split('/')
    dir_outer = '/'.join(dir_path[:-2])

    os.chdir(dir_outer)
    # Создать папку PHOTO
    os.makedirs('PHOTO', exist_ok=True)
    os.makedirs('STAT', exist_ok=True)

    # Составить список выстрелов
    dataout_heads=['Num','Current_length','Current_position','Pressure_pic_amplitude','Pressure_pic_time']
    dataout={mykey:[] for mykey in dataout_heads}
    master.array_plots["График файла"].output_flag=False
    for folder_name in os.listdir():
        numlist = re.findall(r'\d+', folder_name)
        if len(numlist) == 0:
            continue
        dataout['Num'].append(int(numlist[0]))
        master.array_parametrs["Имя файла"].print(numlist[0])
        cnst.names_plots["График файла"]['Префикс'] = folder_name.split(
            '/')[-1]
        master.array_plots["График файла"].tit = cnst.names_plots["График файла"]
        Add_directory_str(master,folder_name)
        Smooth_Plot(master)
        Process_data_pmi27(master.array_plots["График файла"].data,dataout)
        os.chdir(dir_outer+'/PHOTO')
        master.array_plots["График файла"].fig.savefig(folder_name)
        Clear_Plot(master)
        os.chdir(dir_outer)


    # создадим таблицу статистики
    master.array_plots["График файла"].output_flag=True
    stattable = pd.DataFrame()
    for mykey in dataout_heads:
        stattable[mykey]=dataout[mykey]
    #Process_plot_pmi27(stattable, master)
    os.chdir(dir_outer+'/STAT')
    #stattable= stattable.sort_values('Num')
    stattable=Statistic_plot_pmi27(stattable,master)
    stattable.to_csv('Statist.txt', sep=' ')
    os.chdir(dir_outer)
    master.array_plots["График файла"].fig.savefig('Stat_Res')
    print("Process is finished\n")


def Norm_Plot(master):
    data = master.array_plots["График файла"].data
    master.array_plots["График файла"].clear()
    for k, v in data.items():
        v['V'] = v['V']-v['V'].loc[v['T'] < 0].mean()
        maxv = np.abs(v['V']).max()
        v['V'] = 100.0*v['V']/maxv
        data[k] = v
        master.array_plots["График файла"].plot(k+' %', v)
    master.array_plots["График файла"].replot()

def Interactive_or_No_Interactive_plot(master):
    master.array_plots["График файла"].interactive_flag = master.check_values['Интерактивность'].get()
    master.array_plots["График файла"].activate_interactiv(master)
