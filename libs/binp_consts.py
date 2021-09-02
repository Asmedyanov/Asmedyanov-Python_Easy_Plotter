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
]
# Наименования параметров: Название: [Название, Значение по умолчанию, Размерность]
names_parametrs = {
    'Имя файла': ['По умолчанию', ''],
}
# Наименования команд: Название: [Название,Функция]
names_commands = {
    'Добавит файл': [Add_File, "Ctrl+O","<Control-o>"],
    'Очистить график': [Clear_Plot, "Ctrl+0","<Control-0>"],
}
# Наименование графиков: [Название, Подпись по Х, Подпись по Y]
names_plots = {
    'График файла':{'Заголовок':'График файла ','Подпись X':'t, мкс', 'Подпись Y':'', 'Префикс':''},
}
