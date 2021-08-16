# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 16:42:43 2020

@author: asmedyanov
"""
import libs.binp_baseclass as bc #модуль базового класса
from tkinter import * #модуль оконного интерфейса

root = Tk() #окно пользовательского интерфейса
root.wm_title("Python_Easy_Plotter Asmedianov Nikita") #закголовок окна пользовательского интерфейса
baseobject=bc.Oscilloscop(root)#создание объекта базового класса
mainloop()
# EduKudaHochu777