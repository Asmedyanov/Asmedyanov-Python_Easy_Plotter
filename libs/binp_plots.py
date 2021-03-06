# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 17:44:08 2020

@author: asmedyanov
"""
from tkinter import * #модуль оконного интерфейса
#модули построения графиков
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk) # Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
#модуль работ с матрицами
import numpy as np
import pandas as pd
from libs.binp_consts import *

class Embaded_Plot:
    """Класс графиков, адаптированный по Tkinter"""
    def __init__(self,master,tit):
        self.data=dict() # список баз данных
        self.tit=tit #установка заголовков и подписей
        self.frame=Frame(master) # Рабочая рамка
        self.fig =Figure(figsize=(5, 4), dpi=100) #График в рабочей рамке
        t = np.arange(0, 3, .01) #Шкала времени демонстрационного графика
        self.fig.add_subplot(111,
                             title=str(tit["Заголовок"]),
                             xlabel=str(tit['Подпись X']),
                             ylabel=str(tit['Подпись Y'])
                             ).plot(t, 2 * np.sin(2 * np.pi * t))# добавление домнстационного графика
        self.canvas = FigureCanvasTkAgg(self.fig, self.frame)  # A tk.DrawingArea. область рисования
        self.canvas.draw() #Рисуем график
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=2) #расположение области рисования в окне
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame) # Панель навигации (больще/меньше/влево/вправо/сохранить)
        self.toolbar.update() #Обновить панель навигации
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=2) # Расположение панели навигации в окне
        self.frame.pack(side=TOP,fill=BOTH,expand=1) #Расположение рабочей рамки в окне
    
    def replot(self):
        """Перестроить график"""
        self.fig.clf()#Очистить график
        n=len(self.data)#Длина массива баз данных каналов
        subplotarray=np.array(self.fig.subplots(n,sharex=True))# массив графиков
        
        for k in self.data.keys():
            data_t=self.data[k] # ВрЕменная база данных
            i=list(self.data.keys()).index(k)
            self.fig.axes[i].plot(data_t['T'],data_t['V']) #Построить каждый канал в соостветствующем графике
            self.fig.axes[i].minorticks_on() #Включить вспомогательные засечки на шкалах
            
            #  Определяем внешний вид линий основной сетки:
            self.fig.axes[i].grid(
                which='major', #Основная сетка
                    color = 'k', #цвет сетки
                    linewidth = 1) #Ширина линии сетки
            #  Определяем внешний вид линий вспомогательной сетки:
            self.fig.axes[i].grid(
                which='minor', # Вспомогрательная сетка
                    color = 'k', # Цвет сетки
                    linestyle = ':') # Пунктирный стиль
            self.fig.axes[i].tick_params(direction='in', top=True, right=True)
            self.fig.axes[i].set_ylabel(k) #Подписать вертикальные оси
        self.fig.axes[n-1].set_xlabel(self.tit['Подпись X']) # Подписать горизонтальную ось
        self.fig.axes[0].set_title(self.tit["Заголовок"]+self.tit['Префикс']) # Подписать заголовок
        self.fig.canvas.draw() #Рисовать график
        
    def plot(self,key,data):
        """Пристроить канал к графику"""
        self.data[key]=data#добавить таблицу канала в список каналов
        return self.replot()#Перестроить график
    def clear(self):
        """Очистить график"""
        self.fig.clf()#Очистить график
        self.data=[] #Очистить список каналов графика
        self.fig.canvas.draw() #Нарисовать пустой график
        