# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 16:58:46 2020

@author: asmedyanov
"""

from libs.binp_commands import *
from libs.binp_datas import *

# типы используемых файлов: [Маска,Функция открытия,Подписи к легенде]
names_file_masks = [
    ['A*.CSV', Open_A_CSV, ['Запуск','P, V']],
    ['F*CH1.CSV', Open_F_CSV, ['I, V']],
    ['T*.CSV', Open_F_CSV, ['I, V']],
    ['*.PRN', Open_PRN, ['Запуск','I, V']],
    ['*.bin', Open_bin, ['ne, V', 'U, kV', 'I, kA', 'Tr 1, %', 'Tr 2, %']],
]

# Наименования рамок в окне
names_frames = [
    'Окно графиков',
    'Окно параметров'
]
names_checks = {
    'Наложение': Stack_or_legend_plot,
    'Стартовые': Start_or_No_Start_plot,
    'Интерактивность': Interactive_or_No_Interactive_plot
}
# Наименования параметров: Название: [Название, Значение по умолчанию, Размерность]
names_parametrs = {
    'Имя файла': ['По умолчанию', ''],
    'Граница слева':[-1e5,'мкс'],
    'Граница справа':[1e5,'мкс'],
    'Ширина сглаживания':[10,'мкс']
}
# Наименования команд: Название: [Название,Функция]
names_commands_file = {
    'Добавит файл': [Add_File, "Ctrl+O","<Control-o>"],
    'Группировать папку по выстрелам': [Group_directory, "Ctrl+G","<Control-g>"],
    'Добавить папку': [Add_directory, "Ctrl+A","<Control-a>"],
    'Обработать папку': [Process_directory, "Ctrl+P","<Control-p>"],
}

names_commands_plot = {
    'Очистить график': [Clear_Plot, "Ctrl+0","<Control-0>"],
    'Сгладить график': [Smooth_Plot, "Ctrl+F","<Control-f>"],
    'Нормировать на себя график': [Norm_Plot, "Ctrl+N","<Control-n>"],
}

# Наименование графиков: [Название, Подпись по Х, Подпись по Y]
names_plots = {
    'График файла':{'Заголовок':'График файла ','Подпись X':'t, мкс', 'Подпись Y':'', 'Префикс':''},
}
