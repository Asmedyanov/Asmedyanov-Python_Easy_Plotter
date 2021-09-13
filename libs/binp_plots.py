# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 17:44:08 2020

@author: asmedyanov
"""
from tkinter import *  # модуль оконного интерфейса
# модули построения графиков
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)  # Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
# модуль работ с матрицами
import numpy as np
import pandas as pd
from libs.binp_consts import *


class Embaded_Plot:
    """Класс графиков, адаптированный по Tkinter"""

    def __init__(self, master, tit):
        self.data = dict()  # список баз данных
        self.tit = tit  # установка заголовков и подписей
        self.frame = Frame(master)  # Рабочая рамка
        self.fig = Figure(figsize=(5, 4), dpi=100)  # График в рабочей рамке
        t = np.arange(0, 3, .01)  # Шкала времени демонстрационного графика
        self.fig.add_subplot(111,
                             title=str(tit["Заголовок"]),
                             xlabel=str(tit['Подпись X']),
                             ylabel=str(tit['Подпись Y'])
                             ).plot(t, 2 * np.sin(2 * np.pi * t))  # добавление домнстационного графика
        # A tk.DrawingArea. область рисования
        self.canvas = FigureCanvasTkAgg(self.fig, self.frame)
        self.canvas.draw()  # Рисуем график
        # расположение области рисования в окне
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=2)
        # Панель навигации (больще/меньше/влево/вправо/сохранить)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame)
        self.toolbar.update()  # Обновить панель навигации
        # Расположение панели навигации в окне
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=2)
        # Расположение рабочей рамки в окне
        self.frame.pack(side=TOP, fill=BOTH, expand=1)
        self.is_stack = True
        self.have_start = False
        self.interactive_flag = False
        self.textlist = []

    def replot(self):
        self.clear_annotations()
        if self.is_stack:
            self.replot_stack()
        else:
            self.replot_legend()

    def replot_legend(self):
        """Перестроить график"""
        self.fig.clf()  # Очистить график
        self.fig.subplots(1)
        for k, v in self.data.items():
            self.fig.axes[0].plot(v['T'], v['V'], label=k)
        self.fig.axes[0].legend()
        self.fig.axes[0].grid()
        # Подписать горизонтальную ось
        self.fig.axes[0].set_xlabel(self.tit['Подпись X'])
        self.fig.axes[0].set_title(
            self.tit["Заголовок"]+self.tit['Префикс'])  # Подписать заголовок
        self.fig.axes[0].set_ylabel("У. Е.")  # Подписать вертикальные оси
        self.fig.axes[0].ticklabel_format(style='sci')
        self.fig.canvas.draw()

    def replot_stack(self):
        """Перестроить график"""
        self.fig.clf()  # Очистить график
        n = len(self.data)  # Длина массива баз данных каналов
        if (n == 0):
            return
        if (n == 1):
            self.replot_legend()
            return
        gs = self.fig.add_gridspec(n, hspace=0.05)
        axes = gs.subplots(sharex=True)  # массив графиков

        for k in self.data.keys():
            data_t = self.data[k]  # ВрЕменная база данных
            i = list(self.data.keys()).index(k)
            # Построить каждый канал в соостветствующем графике
            axes[i].plot(data_t['T'], data_t['V'])
            # Включить вспомогательные засечки на шкалах
            axes[i].minorticks_on()

            #  Определяем внешний вид линий основной сетки:
            axes[i].grid(
                which='major',  # Основная сетка
                color='k',  # цвет сетки
                linewidth=1)  # Ширина линии сетки
            #  Определяем внешний вид линий вспомогательной сетки:
            axes[i].grid(
                which='minor',  # Вспомогрательная сетка
                color='k',  # Цвет сетки
                linestyle=':')  # Пунктирный стиль
            axes[i].tick_params(direction='in', top=True, right=True)
            axes[i].set_ylabel(k)  # Подписать вертикальные оси
            axes[i].ticklabel_format(style='sci')
        # Подписать горизонтальную ось
        axes[n-1].set_xlabel(self.tit['Подпись X'])
        # Подписать заголовок
        axes[0].set_title(self.tit["Заголовок"]+self.tit['Префикс'])

        self.fig.canvas.draw()  # Рисовать график

    def plot(self, key, data):
        if self.have_start:
            self.plot_all(key, data)
        else:
            self.plot_no_start(key, data)

    def plot_no_start(self, key, data):
        """Пристроить канал к графику"""
        if key.split(' ')[0] == "Запуск":
            return
        self.data[key] = data  # добавить таблицу канала в список каналов

    def plot_all(self, key, data):
        """Пристроить канал к графику"""
        self.data[key] = data  # добавить таблицу канала в список каналов

    def clear(self):
        """Очистить график"""
        self.fig.clf()  # Очистить график
        self.data = dict()  # Очистить список каналов графика
        self.clear_annotations()
        self.fig.canvas.draw()  # Нарисовать пустой график

    def clear_annotations(self):
        if len(self.textlist) == 0:
            return
        for k in self.textlist:
            k.remove()
        self.textlist = []
        

    def activate_interactiv(self, master):
        if (self.interactive_flag == 0):
            self.clear_annotations()
            self.fig.canvas.mpl_disconnect(self.id_click)
            self.fig.canvas.draw()
            return
        # Рисовать график
        self.id_click = self.fig.canvas.mpl_connect(
            'button_press_event',
            lambda event, master=master:
                self.on_click(event, master))

    def on_click(self, event, master):
        if event.dblclick != 1:
            return
        xdata = float(getattr(event, 'xdata'))
        ydata = float(getattr(event, 'ydata'))
        outputstring = '№ %d ( %3.2e , %3.2e )' % (
            len(self.textlist)+1, xdata, ydata)
        for axis in self.fig.axes:
            if axis == event.inaxes:
                labelshiftx = (axis.get_xlim()[1]-axis.get_xlim()[0])*0.05
                labelshifty = (axis.get_ylim()[1]-axis.get_ylim()[0])*0.05
                self.textlist.append(axis.annotate(outputstring,
                                                   xy=(xdata,
                                                       ydata), xycoords='data',
                                                   xytext=(xdata+labelshiftx, ydata+labelshifty), textcoords='data',
                                                   arrowprops=dict(arrowstyle="-|>",
                                                                   connectionstyle="arc3"),
                                                   bbox=dict(
                                                       boxstyle="round", fc="w"),
                                                   ))
        self.fig.canvas.draw()
