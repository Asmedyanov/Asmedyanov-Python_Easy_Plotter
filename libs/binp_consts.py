# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 16:58:46 2020

@author: asmedyanov
"""

from libs.binp_commands import *
from libs.binp_datas import *

# типы используемых файлов: [Маска,Функция открытия,Подписи к легенде]
names_file_masks = [
    ['A*.CSV', Open_A_CSV, ['P, V', 'Tr 2, V']],
    ['F*CH1.CSV', Open_F_CSV, ['I, V']],
    ['T*.CSV', Open_F_CSV, ['I, V']],
    ['*.PRN', Open_PRN, ['T, C']],
    ['*.bin', Open_bin, ['ne, V', 'U, kV', 'I, kA', 'Tr 1, %', 'Tr 2, %']],
]

# Наименования рамок в окне
names_frames = [
    'Окно графиков',
    'Окно параметров',
    'Окно команд'
]
# Наименования параметров: [Название, Значение по умолчанию, Размерность]
names_parametrs = [
    ['0. Имя файла', 'Имя файла', ''],
]
# Наименования команд: [Название,Функция]
names_commands = [
    ['Добавит файл', Add_File],
    ['Очистить график', Clear_Plot],
]
# Наименование графиков: [Название, Подпись по Х, Подпись по Y]
names_plots = [
    ['График файла ', 't, mks', '', ''],
]