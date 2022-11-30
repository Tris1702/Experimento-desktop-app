import customtkinter as ctk
from detectoffline import DetectOffline
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import CubicSpline
from tkinter import ttk
import math
from tkinter.filedialog import asksaveasfile
import pandas as pd
import threading

class FrameOffline:

    def __init__(self, parent):
        super().__init__
        self.isMeasuring = False
        self.TEXTFONT = "Roboto Medium"
        self.detect = DetectOffline()
        self.main_frame = ctk.CTkFrame(master=parent)
        self.main_frame.grid_rowconfigure(0, weight=0)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.frame1 = ctk.CTkFrame(master=self.main_frame)
        self.frame1.grid(row=0, column=0, padx = 5, pady = 5, sticky='nsew')

        self.frame2 = ctk.CTkFrame(master=self.main_frame)
        self.frame2.grid(row=1, column=0, padx = 5, pady = 5, sticky='nsew')

        #========Frame 1==============
        self.frame1.grid_rowconfigure(0, weight=0)
        self.frame1.grid_rowconfigure(1, minsize=10)
        self.frame1.grid_rowconfigure(2, weight=0)
        self.frame1.grid_rowconfigure(3, minsize=10)
        self.frame1.grid_rowconfigure(4, weight=0)

        self.frame1.grid_columnconfigure(0, weight=0)
        self.frame1.grid_columnconfigure(1, weight=1)
        self.frame1.grid_columnconfigure(2, minsize=10)
        self.frame1.grid_columnconfigure(3, weight=0)
        
            #===First line===
        self.labelCom = ctk.CTkLabel(master=self.frame1, text="COM", text_font=(self.TEXTFONT, -16))
        self.labelCom.grid(row=0, column=0, sticky='nsw')

        self.cbCom = ctk.CTkComboBox(master=self.frame1, values =self.detect.get_coms(), text_font=(self.TEXTFONT, -16))
        self.cbCom.grid(row=0, column=1, sticky='nsew')

        self.btnRefreshCom = ctk.CTkButton(master=self.frame1, corner_radius=10, text="Refresh", text_font=(self.TEXTFONT, -14), command=lambda: self.reloadCom())
        self.btnRefreshCom.grid(row=0, column=3, sticky='nsew')

            #===Second line===
        self.labelDistance = ctk.CTkLabel(master=self.frame1, text="Distance", text_font=(self.TEXTFONT, -16))
        self.labelDistance.grid(row=2, column=0, sticky='nsw')

        self.entryDistance = ctk.CTkEntry(master=self.frame1, placeholder_text='0-30 cm', text_font=(self.TEXTFONT, -16))
        self.entryDistance.grid(row=2, column=1, sticky='nsew')

        self.btnMeasure = ctk.CTkButton(master=self.frame1, corner_radius=10, text="Measure", text_font=(self.TEXTFONT, -14), command=lambda: self.measureOnce())
        self.btnMeasure.grid(row=2, column=3, sticky='nsew')

            #===Third line===
        self.labelRepeat = ctk.CTkLabel(master=self.frame1, text="Interval", text_font=(self.TEXTFONT, -16))
        self.labelRepeat.grid(row=4, column=0, sticky='nsw')

        self.entryRepeatTimes = ctk.CTkEntry(master=self.frame1, placeholder_text='seconds', text_font=(self.TEXTFONT, -16))
        self.entryRepeatTimes.grid(row=4, column=1, sticky='nsew')

        self.btnMeasureContinuous = ctk.CTkButton(master=self.frame1, corner_radius=10, text="Measure continuous", text_font=(self.TEXTFONT, -14), command=lambda: self.measureContinuous())
        self.btnMeasureContinuous.grid(row=4, column=3, sticky='nsew')


        #========Frame2===========
        self.frame2.grid_rowconfigure(0, weight=0)
        self.frame2.grid_rowconfigure(1, minsize=10)
        self.frame2.grid_rowconfigure(2, weight=1)
        self.frame2.grid_rowconfigure(3, minsize=10)

        self.frame2.grid_columnconfigure(0, minsize=10)
        self.frame2.grid_columnconfigure(1, weight=1)
        self.frame2.grid_columnconfigure(2, minsize=10)

        self.frame3 = ctk.CTkFrame(master=self.frame2)
        self.frame3.grid(row=0, column=1, sticky='nsew')
        self.frame3.grid_rowconfigure(0, weight=1)
        self.frame3.grid_columnconfigure(0, weight=1)
        self.frame3.grid_columnconfigure(1, weight=0)
        self.frame3.grid_columnconfigure(2, minsize=5)
        self.frame3.grid_columnconfigure(3, weight=0)

        self.labelLogger = ctk.CTkLabel(master=self.frame3,text='Console Log', text_font=(self.TEXTFONT, -16))
        self.labelLogger.grid(row=0, column=0, sticky='nsw')

        self.btnDrawChart = ctk.CTkButton(master=self.frame3, text='Draw', text_font=(self.TEXTFONT, -16), command=self.drawChart)
        self.btnDrawChart.grid(row=0, column = 1, sticky='nsw')

        self.btnExport = ctk.CTkButton(master=self.frame3, text='Export', text_font=(self.TEXTFONT, -16), command=self.exportData)
        self.btnExport.grid(row=0, column = 3, sticky='nsw')

        styleTreeView = ttk.Style()
        styleTreeView.theme_use('clam')
        styleTreeView.configure("Treeview",
            highlightthickness=0,
            background="#D3D3D3",
            foreground="white",
            rowheight=25,
            fieldbackground='#292929',
            font=(self.TEXTFONT, -16)
        )
        styleTreeView.map('Treeview', background=[('selected', '#395E9C')])
        styleTreeView.configure('Treeview.Heading', background="#395E9C", foreground='white')
        self.tableLogger = ttk.Treeview(master=self.frame2, columns=(1,2,3), show='headings', height='10')
        self.tableLogger.grid(row=2, column = 1, sticky='nsew')
        
        self.tableLogger.tag_configure('odd', background='#292929', foreground='white')
        self.tableLogger.tag_configure('even', background='#3D3D3D', foreground='white')

        self.tableLogger.column(1, stretch=False, anchor='c')
        self.tableLogger.column(2, stretch=False, anchor='c')
        self.tableLogger.column(3, stretch=False, anchor='c')

        self.tableLogger.heading(1, text='ID')
        self.tableLogger.heading(2, text='Distance')
        self.tableLogger.heading(3, text='Voltage')
        
    def reloadCom(self):
        self.cbCom.configure(values=self.detect.get_coms())

    def measureContinuous(self):
        if self.isMeasuring == False:
            self.isMeasuring = True
            self.btnMeasureContinuous.configure(text="Stop",fg_color="red")
            self.measureWithInterval(self.entryRepeatTimes.get())
        else:
            self.isMeasuring = False
            self.timer_measure.cancel()
            self.btnMeasureContinuous.configure(text="Measure continuous",fg_color="#395E9C")

    def measureWithInterval(self, interval):
        self.timer_measure = threading.Timer(int(interval), lambda: self.measureWithInterval(int(interval)))
        self.timer_measure.start()
        if self.detect.SERIAL_PORT == None:
            print('set port')
            self.detect.set_serial_port(self.cbCom.get())
        self.detect.measure(self.entryDistance.get())
        if len(self.detect.history) %2 == 0:
            self.tableLogger.insert("", 0, iid=len(self.detect.history), values=(len(self.detect.history),self.detect.history[-1]['distance'],self.detect.history[-1]['voltage']), tags='even')
        else: 
            self.tableLogger.insert("", 0, iid=len(self.detect.history), values=(len(self.detect.history),self.detect.history[-1]['distance'],self.detect.history[-1]['voltage']), tags='odd')

    def measureOnce(self):
        if self.detect.SERIAL_PORT == None:
            print('set port')
            self.detect.set_serial_port(self.cbCom.get())
        self.detect.measure(self.entryDistance.get())

        if len(self.detect.history) %2 == 0:
            self.tableLogger.insert("", 0, iid=len(self.detect.history), values=(len(self.detect.history),self.detect.history[-1]['distance'],self.detect.history[-1]['voltage']), tags='even')
        else: 
            self.tableLogger.insert("", 0, iid=len(self.detect.history), values=(len(self.detect.history),self.detect.history[-1]['distance'],self.detect.history[-1]['voltage']), tags='odd')

    def drawChart(self):
        xValue=[]
        yValue=[]
        for value in self.detect.history:
            xValue.append(value['distance'])
            yValue.append(value['voltage'])
        cs = np.polyfit(xValue, yValue, len(xValue)-1)
        xvar = np.linspace(max(xValue), min(xValue))
        yvar =  np.polyval(cs, xvar)
        plt.plot(xvar, yvar,'b--', xValue, yValue, 'ro-')
        plt.xlabel('distance')
        plt.ylabel('voltage')

        plt.grid()
        plt.show()
    
    def exportData(self):
        xValue=[]
        yValue=[]
        for value in self.detect.history:
            xValue.append(value['distance'])
            yValue.append(value['voltage'])
        data = [("csv file(*.csv)","*.csv")]
        filename = asksaveasfile(filetypes = data, defaultextension = data[0], initialfile='data.csv')
        if filename != None:
            df = pd.DataFrame({'distance': xValue, 'voltage': yValue})
            df.to_csv(filename, index=True)