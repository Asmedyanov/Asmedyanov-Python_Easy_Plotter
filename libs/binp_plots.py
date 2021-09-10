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
        self.is_stack=True
        self.have_start=False
    
    def replot(self):
        if self.is_stack:
            self.replot_stack()
        else:
            self.replot_legend()
    def replot_legend(self):
        """Перестроить график"""
        self.fig.clf()#Очистить график
        self.fig.subplots(1)
        for k,v in self.data.items():
            self.fig.axes[0].plot(v['T'],v['V'],label=k)
        self.fig.axes[0].legend()
        self.fig.axes[0].grid()
        self.fig.axes[0].set_xlabel(self.tit['Подпись X']) # Подписать горизонтальную ось
        self.fig.axes[0].set_title(self.tit["Заголовок"]+self.tit['Префикс']) # Подписать заголовок
        self.fig.axes[0].set_ylabel("У. Е.") #Подписать вертикальные оси
        self.fig.canvas.draw()
        
        
    def replot_stack(self):
        """Перестроить график"""
        self.fig.clf()#Очистить график
        n=len(self.data)#Длина массива баз данных каналов
        if (n==0): return
        gs = self.fig.add_gridspec(n, hspace=0.05)
        axes=gs.subplots(sharex=True)# массив графиков
        
        for k in self.data.keys():
            data_t=self.data[k] # ВрЕменная база данных
            i=list(self.data.keys()).index(k)
            axes[i].plot(data_t['T'],data_t['V']) #Построить каждый канал в соостветствующем графике
            axes[i].minorticks_on() #Включить вспомогательные засечки на шкалах
            
            #  Определяем внешний вид линий основной сетки:
            axes[i].grid(
                which='major', #Основная сетка
                    color = 'k', #цвет сетки
                    linewidth = 1) #Ширина линии сетки
            #  Определяем внешний вид линий вспомогательной сетки:
            axes[i].grid(
                which='minor', # Вспомогрательная сетка
                    color = 'k', # Цвет сетки
                    linestyle = ':') # Пунктирный стиль
            axes[i].tick_params(direction='in', top=True, right=True)
            axes[i].set_ylabel(k) #Подписать вертикальные оси
        axes[n-1].set_xlabel(self.tit['Подпись X']) # Подписать горизонтальную ось
        axes[0].set_title(self.tit["Заголовок"]+self.tit['Префикс']) # Подписать заголовок
        self.fig.canvas.draw() #Рисовать график
    def plot(self,key,data):
        if self.have_start:
            self.plot_all(key,data)
        else:
            self.plot_no_start(key,data)
    
    def plot_no_start(self,key,data):
        """Пристроить канал к графику"""
        if key.split(' ')[0]=="Запуск": return
        self.data[key]=data#добавить таблицу канала в список каналов
    def plot_all(self,key,data):
        """Пристроить канал к графику"""
        self.data[key]=data#добавить таблицу канала в список каналов
    def clear(self):
        """Очистить график"""
        self.fig.clf()#Очистить график
        self.data=dict() #Очистить список каналов графика
        self.fig.canvas.draw() #Нарисовать пустой график
        