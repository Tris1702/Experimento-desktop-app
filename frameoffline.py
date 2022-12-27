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
from constance import Constance
import xlsxwriter

class FrameOffline:
    def __init__(self, parent):
        super().__init__
        self.isMeasuring = False
        self.TEXTFONT = "Roboto Medium"
        self.optionMeasure = 0
        self.detect = DetectOffline(option= self.optionMeasure)
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
        self.labelCom = ctk.CTkLabel(master=self.frame1, text="Cổng kết nối", text_font=(self.TEXTFONT, -16))
        self.labelCom.grid(row=0, column=0, sticky='nsw')

        self.cbCom = ctk.CTkComboBox(master=self.frame1, values =self.detect.get_coms(), text_font=(self.TEXTFONT, -16))
        self.cbCom.grid(row=0, column=1, sticky='nsew')

        self.btnRefreshCom = ctk.CTkButton(master=self.frame1, corner_radius=10, text="Cập nhật", text_font=(self.TEXTFONT, -14), command=lambda: self.reloadCom())
        self.btnRefreshCom.grid(row=0, column=3, sticky='nsew')

            #===Second line===
        self.comboType = ctk.CTkComboBox(master=self.frame1, values=["A-V", "V-cm", "V-t"], text_font=(self.TEXTFONT, -16), command=self.changeOptionMeasure)
        self.comboType.grid(row=2, column=0, sticky='nsw')

        self.entryValue = ctk.CTkEntry(master=self.frame1, text_font=(self.TEXTFONT, -16))
        self.entryValue.grid(row=2, column=1, sticky='nsew')

        self.btnMeasure = ctk.CTkButton(master=self.frame1, corner_radius=10, text="Đo", text_font=(self.TEXTFONT, -14), command=self.measureOnce)
        self.btnMeasure.grid(row=2, column=3, sticky='nsew')

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
        self.frame3.grid_columnconfigure(4, minsize=5)
        self.frame3.grid_columnconfigure(5, weight=0)
        self.frame3.grid_columnconfigure(6, minsize=5)
        self.frame3.grid_columnconfigure(8, weight=0)

        self.labelLogger = ctk.CTkLabel(master=self.frame3,text='Kết quả', text_font=(self.TEXTFONT, -16))
        self.labelLogger.grid(row=0, column=0, sticky='nsw')

        self.btnDrawChart = ctk.CTkButton(master=self.frame3, text='Vẽ', text_font=(self.TEXTFONT, -16), command=lambda: self.drawChart(self.optionMeasure, self.btnIP.get()))
        self.btnDrawChart.grid(row=0, column = 1, sticky='nsw')

        self.btnExport = ctk.CTkButton(master=self.frame3, text='Xuất file', text_font=(self.TEXTFONT, -16), command=self.exportData)
        self.btnExport.grid(row=0, column = 3, sticky='nsw')

        self.btnIP = ctk.CTkSwitch(master=self.frame3, text="Nội suy", text_font=(self.TEXTFONT, -16), onvalue="on", offvalue="off", command=None)

        self.btnExport = ctk.CTkButton(master=self.frame3, text='Xóa dữ liệu', text_font=(self.TEXTFONT, -16), command=self.clearData)
        self.btnExport.grid(row=0, column = 5, sticky='nsw')

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
        self.tableLogger.heading(2, text='Voltage')
        self.tableLogger.heading(3, text='Ampe')
        
    def reloadCom(self):
        self.cbCom.configure(values=self.detect.get_coms())

    def measureContinuous(self):
        if self.isMeasuring == False:
            self.isMeasuring = True
            self.btnMeasure.configure(text="Ngừng",fg_color="red")
            self.measureWithInterval(self.entryValue.get(), timer = 0)
        else:
            self.isMeasuring = False
            self.timer_measure.cancel()
            self.btnMeasure.configure(text="Đo",fg_color="#395E9C")

    def measureWithInterval(self, interval, timer):
        
        self.timer_measure = threading.Timer(int(interval), lambda: self.measureWithInterval(int(interval), timer+int(interval)))
        self.timer_measure.start()
        
        if self.detect.SERIAL_PORT == None:
            print('set port')
            self.detect.set_serial_port(self.cbCom.get())
        self.detect.measure(self.entryValue.get(), timer)
        if self.optionMeasure == 0:
            self.tableLogger.insert("", 0, iid=len(Constance.historyAV), values=(len(Constance.historyAV),Constance.historyAV[-1]['ampe'],Constance.historyAV[-1]['voltage']), tags='odd' if len(Constance.historyAV)%2 else 'even')
        elif self.optionMeasure == 1:
            self.tableLogger.insert("", 0, iid=len(Constance.historyCV), values=(len(Constance.historyCV),Constance.historyCV[-1]['centimeter'],Constance.historyCV[-1]['voltage']), tags='odd' if len(Constance.historyCV)%2 else 'even')
        else:
            self.tableLogger.insert("", 0, iid=len(Constance.historyTV), values=(len(Constance.historyTV),Constance.historyTV[-1]['timepoint'],Constance.historyTV[-1]['voltage']), tags='odd' if len(Constance.historyTV)%2 else 'even')
    def measureOnce(self):
        if self.detect.SERIAL_PORT == None:
            print('set port')
            self.detect.set_serial_port(self.cbCom.get())
        self.detect.measure(self.entryValue.get())

        if self.optionMeasure == 0:
            self.tableLogger.insert("", 0, iid=len(Constance.historyAV), values=(len(Constance.historyAV),Constance.historyAV[-1]['ampe'],Constance.historyAV[-1]['voltage']), tags='odd' if len(Constance.historyAV)%2 else 'even')
        elif self.optionMeasure == 1:
            self.tableLogger.insert("", 0, iid=len(Constance.historyCV), values=(len(Constance.historyCV),Constance.historyCV[-1]['centimeter'],Constance.historyCV[-1]['voltage']), tags='odd' if len(Constance.historyCV)%2 else 'even')
        else:
            self.tableLogger.insert("", 0, iid=len(Constance.historyTV), values=(len(Constance.historyTV),Constance.historyTV[-1]['timepoint'],Constance.historyTV[-1]['voltage']), tags='odd' if len(Constance.historyTV)%2 else 'even')
    

    def drawChart(self, option, drawIP):
        xValue=[]
        yValue=[]
        if self.optionMeasure == 0:
            for value in Constance.historyAV:
                yValue.append(value['voltage'])
                xValue.append(value['ampe'])
            plt.xlabel('Voltage')
            plt.ylabel('Ampe')
        elif self.optionMeasure == 1:
            for value in Constance.historyCV:
                yValue.append(value['voltage'])
                xValue.append(value['centimeter'])
            plt.xlabel('Centimeter')
            plt.ylabel('Voltage')
        else:
            for value in Constance.historyTV:
                yValue.append(value['voltage'])
                xValue.append(value['timepoint'])
            plt.xlabel('Time')
            plt.ylabel('Voltage')
        if drawIP == "on":
            cs = np.polyfit(xValue, yValue, len(xValue)-1)
            xvar = np.linspace(max(xValue), min(xValue))
            yvar =  np.polyval(cs, xvar)
            plt.plot(xvar, yvar,'b--', xValue, yValue, 'ro-')
        else:
            plt.plot(xValue, yValue, 'ro-')
        plt.grid()
        plt.show()
    
    def exportData(self):
        xValue=[]
        yValue=[]
        if self.optionMeasure == 0:
            for value in Constance.historyAV:
                yValue.append(value['ampe'])
                xValue.append(value['voltage'])
        elif self.optionMeasure == 1:
            for value in Constance.historyCV:
                yValue.append(value['voltage'])
                xValue.append(value['centimeter'])
        else:
            for value in Constance.historyTV:
                yValue.append(value['voltage'])
                xValue.append(value['timepoint'])
        filename = asksaveasfile(defaultextension ='.xlsx', initialfile='data.xlsx')
        if filename != None:
            workbook = xlsxwriter.Workbook(filename.name)
            worksheet = workbook.add_worksheet()
            if self.optionMeasure == 0:
                worksheet.write(0, 0, 'STT')
                worksheet.write(0, 1, 'Voltage')
                worksheet.write(0, 2, 'Ampe')
            elif self.optionMeasure == 1:
                worksheet.write(0, 0, 'STT')
                worksheet.write(0, 1, 'Voltage')
                worksheet.write(0, 2, 'Centimeter')
            else:
                df = pd.DataFrame({'Voltage': yValue, 'Time': xValue})
                worksheet.write(0, 0, 'STT')
                worksheet.write(0, 1, 'Voltage')
                worksheet.write(0, 2, 'TimePoint')

            for row in range (1, len(xValue)+1):
                worksheet.write(row, 0, row)
                worksheet.write(row, 1, yValue[row-1])
                worksheet.write(row, 2, xValue[row-1])

            workbook.close()

    def changeOptionMeasure(self, option):
        if option == "A-V":
            self.optionMeasure = 0
            self.btnMeasure.configure(command=lambda: self.measureOnce())
            self.detect.option = 0
            self.tableLogger.heading(1, text='ID')
            self.tableLogger.heading(2, text='Voltage')
            self.tableLogger.heading(3, text='Ampe')
            self.clearData()
            self.btnIP.grid_forget()

        elif option == "V-cm":
            self.optionMeasure = 1
            self.btnMeasure.configure(command=lambda: self.measureOnce())
            self.detect.option = 1
            self.tableLogger.heading(1, text='ID')
            self.tableLogger.heading(2, text='Centimeter')
            self.tableLogger.heading(3, text='Voltage')
            self.clearData()
            self.btnIP.grid_forget()

        else:
            self.optionMeasure = 2
            self.btnMeasure.configure(command=lambda: self.measureContinuous())
            self.detect.option = 2
            self.tableLogger.heading(1, text='ID')
            self.tableLogger.heading(2, text='Time')
            self.tableLogger.heading(3, text='Voltage')
            self.btnIP.grid(row=0, column=8, sticky='nsw')
            self.clearData()
    
    def clearData(self):
        if self.optionMeasure == 0:
            Constance.historyAV = []
        elif self.optionMeasure == 1:
            Constance.historyCV = []
        else:
            Constance.historyTV = []
        for item in self.tableLogger.get_children():
            self.tableLogger.delete(item)