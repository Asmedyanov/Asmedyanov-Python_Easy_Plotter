# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 13:14:34 2020

@author: asmedyanov
"""

# модуль работ с матрицами
import numpy as np
# модуль баз данных
import pandas as pd
# модуль бинарных файлов
import pickle as pk

mks = 1.0e6


def Open_A_CSV(a):
    """
    Открытие файла типа A*.CSV по строке a
    """
    data = pd.read_csv(a, skiprows=2, error_bad_lines=False,
                       names=['T', 'V1', 'V2'])
    stmin = data['V1'].min()
    stmax = data['V1'].max()
    st = 0.5*(stmax-stmin)
    t0 = data['T'].loc[data['V1'] < st].values.min()*1.0e6
    data1 = pd.DataFrame()
    data1['T'] = data['T']*1.0e6-t0
    data1['V'] = data['V1']
    data2 = pd.DataFrame()
    data2['T'] = data['T']*1.0e6-t0
    data2['V'] = data['V2']
    return [data1, data2]

def Open_F_CSV(a):
    """
    Открытие файла типа F*.CSV по строке a
    """
    data = pd.read_csv(a, skiprows=19, error_bad_lines=False, names=[
                       'T', 'V', 'e'], skipinitialspace=True)
    data["T"] *= mks
    ret = []
    ret.append(pd.DataFrame())
    ret[0]['T'] = data['T']
    ret[0]['V'] = data['V']
    return ret


def Open_PRN(a):
    """
    Открытие файла типа *.PRN по строке a
    """
    parametr_data = pd.read_csv(a, nrows=29, error_bad_lines=False,
                                names=['P', 'V1', 'V5'])
    namesch = ['CH'+str(i) for i in range(1, 5)]
    CHDisplay = np.array(
        parametr_data.loc[parametr_data['P'].str.contains('Disp')].V1 == 'On')
    t0 = float(parametr_data[parametr_data['P'] == 'Trigger Address']['V1'])
    dt = float(parametr_data[parametr_data['P'] == 'Delta(second)']['V1'])*mks
    data = pd.read_csv(a, sep=' ', skiprows=30,
                       error_bad_lines=False,
                       names=namesch)
    data["T"] = [(i-t0)*dt for i in range(len(data))]
    data_ret = []
    for k in range(len(CHDisplay)):
        if CHDisplay[k] == True:
            data_t = pd.DataFrame()
            data_t['T'] = data['T']
            data_t['V'] = data['CH'+str(k+1)]
            data_ret.append(data_t)
    return [data_ret[0],data_ret[1]] 


def Open_bin(a):
    """
    Открытие файла типа *.bin по строке a
    """
    f = open(a, 'rb')
    value0 = np.fromfile(f, dtype='>i2').byteswap().newbyteorder()
    dt = 0.1
    Nsemp = (value0[0] << 16)+value0[1]
    time = np.arange(Nsemp)*dt+2.3-310.0-300
    data_ret = []
    mult = [1.0,
            0,
            2.0e4*1.0e-3,
            -1.0e-3*10*132*8/0.1,
            1,
            1]
    for k in [0, 2, 3, 4, 5]:
        tdata = pd.DataFrame()
        tdata['T'] = time
        tdata['V'] = (value0[4+k::16]-(1 << 11))*(1.6/(1 << 11))*mult[k]
        data_ret.append(tdata)
    return data_ret


def Open_tek_csv(a):
    """
    Открытие файла типа tek*.CSV по строке a
    """
    data = pd.read_csv(a, skiprows=20)
    time = data['TIME']*1.0e6
    data_ret = []
    data_ret.append(pd.DataFrame())
    data_ret[0]['T'] = time
    data_ret[0]['V'] = data['CH2']
    data_ret.append(pd.DataFrame())
    data_ret[1]['T'] = time
    data_ret[1]['V'] = data['CH3']
    data_ret.append(pd.DataFrame())
    data_ret[2]['T'] = time
    data_ret[2]['V'] = data['CH4']
    return data_ret
