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
    def __init__(self,master,tit):
        self.data=[]
        self.is_interactiv=False
        self.tit=tit
        self.frame=Frame(master)
        self.fig =Figure(figsize=(5, 4), dpi=100)
        t = np.arange(0, 3, .01)
        self.fig.add_subplot(111,
                             title=str(tit[0]),
                             xlabel=str(tit[1]),
                             ylabel=str(tit[2])
                             ).plot(t, 2 * np.sin(2 * np.pi * t))
        self.canvas = FigureCanvasTkAgg(self.fig, self.frame)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=2)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=2)
        self.frame.pack(side=TOP,fill=BOTH,expand=1)
        self.cursor=0
        self.ids_interactiv=[]
        
        self.current_clicks=[]
        self.text=Text(self.frame,height=2)
    
        
        
    
    
    def replot(self):
        self.fig.clf()#Очистить график
        n=len(self.data)
        subplotarray=np.array(self.fig.subplots(n,sharex=True))
        
        for i in range(n):
            data_t=self.data[i]
            self.fig.axes[i].plot(data_t['T'],data_t['V'])
            self.fig.axes[i].minorticks_on()
            
            #  Определяем внешний вид линий основной сетки:
            self.fig.axes[i].grid(which='major',
                    color = 'k', 
                    linewidth = 1)
            #  Определяем внешний вид линий вспомогательной
            #  сетки:
            self.fig.axes[i].grid(which='minor', 
                    color = 'k', 
                    linestyle = ':')
            self.fig.axes[i].tick_params(direction='in', top=True, right=True)
            self.fig.axes[i].set_ylabel(data_t['label'][0])
        self.fig.axes[n-1].set_xlabel(self.tit[1])
        self.fig.axes[0].set_title(self.tit[0]+self.tit[3])
        self.fig.canvas.draw()
        
    def plot(self,data):
        self.data.append(data)
        return self.replot()
       
    def on_move(self,event,master):
        xdata=str(getattr(event, 'xdata'))
        if xdata=='None': return
        master.array_parametrs[2+(self.cursor % 2)].print('%3.2f'%float(xdata))
    
    def on_click(self,event,master):
        xdata=str(getattr(event, 'xdata'))
        if xdata=='None': return
        dbl=getattr(event, 'dblclick')
        if dbl:
            self.cursor+=1
            n0=int(len(names_clicks)-1)
            self.current_clicks.append('%3.2f'%float(xdata))
            self.text.delete(1.0,END)
            self.text.insert(1.0,str(self.cursor)+' / '+str(n0))
            if self.cursor==n0:
                n=int(len(names_clicks)/3)
                for i in range(n):
                    t1=float(self.current_clicks[i])
                    t2=float(self.current_clicks[i+n])
                    tcur=abs(t2-t1)
                    self.current_clicks.append('%3.2f'%tcur)
                self.data_clicks.loc[len(self.data_clicks)]=self.current_clicks
                self.text.delete(1.0,END)
                self.text.insert(1.0,str(self.data_clicks))
                self.clear_cursor()
                
    def clear_cursor(self):
        self.cursor=0
        self.current_clicks=[]
        
    def activate_interactiv(self,master):
        if len(self.ids_interactiv)!=0: return
        id_click=self.fig.canvas.mpl_connect(
            'button_press_event',
            lambda event, master=master:
                self.on_click(event,master))
        self.ids_interactiv.append(id_click)
        id_move=self.fig.canvas.mpl_connect(
            'motion_notify_event',
            lambda event, master=master:
                self.on_move(event,master))
        self.ids_interactiv.append(id_move)
        self.text.pack(fill=BOTH,expand=1)
    def clear(self):
        self.fig.clf()#Очистить первый график
        self.data=[]
        self.fig.canvas.draw()
    def clear_last_click(self):
        self.clear_cursor()
        self.data_clicks=self.data_clicks[:-1]
        self.text.delete(1.0,END)
        self.text.insert(1.0,str(self.data_clicks))
        