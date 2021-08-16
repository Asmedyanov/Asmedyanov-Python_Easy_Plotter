# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 12:09:26 2020

@author: asmedyanov
"""

from tkinter import * #модуль оконного интерфейса

class Parametr:
    def __init__(self, master,userstr):
        self.frame=Frame(master)
        self.name=Label(self.frame,text=str(userstr[0]))
        self.input=Entry(self.frame)
        self.input.insert(0,str(userstr[1]))
        self.dimension=Label(self.frame,text=str(userstr[2]))
        self.name.pack(side=LEFT,fill=X)
        self.input.pack(side=LEFT,fill=X,expand=1)
        self.dimension.pack(side=LEFT,fill=X)
        self.frame.pack(fill=X)
    def print(self,s):
        self.input.delete(0,END)#очистить старое имя файла
        self.input.insert(0, s)#Записать новое имя файла
