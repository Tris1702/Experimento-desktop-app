import customtkinter as ctk
from detectoffline import DetectOffline
import matplotlib.pyplot as plt
import numpy as np
from tkinter import ttk
from tkinter.filedialog import asksaveasfile
import pandas as pd
import threading
from constance import Constance
from tkinter import messagebox
import xlsxwriter
import numpy as np
from scipy.interpolate import make_interp_spline
import time

class FrameOffline:
    def __init__(self, parent):
        super().__init__
        self.isMeasuring = False
        self.TEXTFONT = "Roboto Medium"
        self.optionMeasure = 1
        self.whichPort = 0
        self.whichLesson = 1
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
        self.btnRefreshCom.grid(row=0, column=2, sticky='nsew')

            #===Second line===
        self.comboType = ctk.CTkComboBox(master=self.frame1, values=["V-cm", "V-t", "V1-I2"], text_font=(self.TEXTFONT, -16), command=self.changeOptionMeasure)
        self.comboType.grid(row=2, column=0, sticky='nsw')

        self.entryValue = ctk.CTkEntry(master=self.frame1, placeholder_text="Giá trị khoảng cách (cm)", text_font=(self.TEXTFONT, -16))
        self.entryValue.grid(row=2, column=1, sticky='nsew')

        self.cbWhichPort = ctk.CTkComboBox(master=self.frame1, values=["Cổng 1", "Cổng 2"], text_font=(self.TEXTFONT, -16), command=self.changePortMeasure)
        self.cbWhichPort.grid(row=2, column=2, sticky='nsew')

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

        self.btnDrawChart = ctk.CTkButton(master=self.frame3, text='Vẽ', text_font=(self.TEXTFONT, -16), command=lambda: self.drawChart(self.optionMeasure))
        self.btnDrawChart.grid(row=0, column = 1, sticky='nsw')

        self.btnExport = ctk.CTkButton(master=self.frame3, text='Xuất file', text_font=(self.TEXTFONT, -16), command=self.exportData)
        self.btnExport.grid(row=0, column = 3, sticky='nsw')

        self.cbWhichLesson = ctk.CTkComboBox(master=self.frame3, values=['Phóng tụ', 'Nạp tụ'], text_font=(self.TEXTFONT, -16), command=self.changeLesson)

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
        self.tableLogger = ttk.Treeview(master=self.frame2, show='headings', height='10')
        self.tableLogger.grid(row=2, column = 1, sticky='nsew')
        
        self.tableLogger.tag_configure('odd', background='#292929', foreground='white')
        self.tableLogger.tag_configure('even', background='#3D3D3D', foreground='white')

        self.tableLogger["columns"] = [1,2,3,4]
        self.tableLogger["displaycolumns"] =[1,2,3]

        self.tableLogger.column(1, stretch=0, anchor='c')
        self.tableLogger.column(2, stretch=True, anchor='c')
        self.tableLogger.column(3, stretch=True, anchor='c')
        self.tableLogger.column(4, stretch=True, anchor='c')

        self.tableLogger.heading(1, text='ID')
        self.tableLogger.heading(2, text='Khoảng cách (cm)')
        self.tableLogger.heading(3, text='Hiệu điện thế (V)')
        self.tableLogger.heading(4, text='Hiệu điện thế Ur (V)')

        self.fig = plt.figure() 
        self.ax = self.fig.add_subplot(111)
        self.fig.canvas.mpl_connect('pick_event', self.onpick)   
        
    def reloadCom(self):
        listComs = self.detect.get_coms()
        self.cbCom.configure(values=listComs)
        self.cbCom.set(listComs[0])

    def measureContinuous(self):
        if self.detect.SERIAL_PORT == None:
            print('set port')
            self.detect.set_serial_port(self.cbCom.get())
        try:
            self.detect.measure(-1, port=self.whichPort)
        except:
            print('loi')
        time.sleep(1)
        if self.isMeasuring == False:
            self.isMeasuring = True
            self.measureWithInterval(timer = 0)
        else:
            self.isMeasuring = False
            self.timer_measure.cancel()

    def measureWithInterval(self, timer):
        self.timer_measure = threading.Timer(Constance.intervalTime, lambda: self.measureWithInterval(round(timer+Constance.intervalTime, 1)))
        self.timer_measure.start()
        
        if self.detect.SERIAL_PORT == None:
            print('set port')
            self.detect.set_serial_port(self.cbCom.get())
        try:
            if self.whichLesson == 1:
                self.detect.measure(0, timer)
            else:
                self.detect.measure(0, timer, port=self.whichPort)
            if self.whichLesson == 1:
                self.tableLogger.insert("", 0, iid=len(Constance.historyTVV), values=(len(Constance.historyTVV),Constance.historyTVV[-1]['timepoint'],Constance.historyTVV[-1]['voltage1'],Constance.historyTVV[-1]['voltage2']), tags='odd' if len(Constance.historyTVV)%2 else 'even')
            else:
                self.tableLogger.insert("", 0, iid=len(Constance.historyTV), values=(len(Constance.historyTV),Constance.historyTV[-1]['timepoint'],Constance.historyTV[-1]['voltage']), tags='odd' if len(Constance.historyTV)%2 else 'even')
        except NameError:
            print(NameError)
            self.timer_measure.cancel()
            messagebox.showerror(title='Alert', message="Yêu cầu điền thông tin đầy đủ")

    def measureOnce(self):
        if self.detect.SERIAL_PORT == None:
            print('set port')
            self.detect.set_serial_port(self.cbCom.get())
        try:
            self.detect.measure(float(self.entryValue.get()), port=self.whichPort)

            if self.optionMeasure == 0:
                self.tableLogger.insert("", 0, iid=len(Constance.historyAV), values=(len(Constance.historyAV),Constance.historyAV[-1]['ampe'],Constance.historyAV[-1]['voltage']), tags='odd' if len(Constance.historyAV)%2 else 'even')
            elif self.optionMeasure == 1:
                self.tableLogger.insert("", 0, iid=len(Constance.historyCV), values=(len(Constance.historyCV),Constance.historyCV[-1]['centimeter'],Constance.historyCV[-1]['voltage']), tags='odd' if len(Constance.historyCV)%2 else 'even')
        except:
            messagebox.showerror(title='Alert', message="Yêu cầu điền thông tin đầy đủ")

    def measureV1A2(self):
        if self.detect.SERIAL_PORT == None:
            print('set port')
            self.detect.set_serial_port(self.cbCom.get())
        try:
            self.detect.measure(float(self.entryValue.get()), Rvalue=float(self.entryValue.get()))
            self.tableLogger.insert("", 0, iid=len(Constance.historyA2V1), values=(len(Constance.historyA2V1),Constance.historyA2V1[-1]['voltage1'],Constance.historyA2V1[-1]['ampe2']), tags='odd' if len(Constance.historyA2V1)%2 else 'even')
        except:
            messagebox.showerror(title='Alert', message="Yêu cầu điền thông tin đầy đủ")

    def measureI1I2(self):
        if self.detect.SERIAL_PORT == None:
            print('set port')
            self.detect.set_serial_port(self.cbCom.get())
        self.detect.measure()
        try:
            self.tableLogger.insert("", 0, iid=len(Constance.historyI1I2), values=(len(Constance.historyI1I2),Constance.historyI1I2[-1]['ampe1'],Constance.historyI1I2[-1]['ampe2']), tags='odd' if len(Constance.historyI1I2)%2 else 'even')
        except:
            messagebox.showerror(title='Alert', message="Kiểm tra thông tin cài đặt các đầu đo")
    def drawChart(self, option):
        self.fig = plt.figure() 
        self.ax = self.fig.add_subplot(111)
        self.fig.canvas.mpl_connect('pick_event', self.onpick) 
        if self.optionMeasure in [3,4]:
            try:
                xValue, yValue = self.getSmoothXValueAndYValue()
            except:
                messagebox.showwarning(title="Cảnh báo", message="Yêu cầu nhiều điểm dữ liệu hơn!")
                return
        else:
            xValue, yValue = self.getXValueAndYValue()
        if self.optionMeasure == 0:
            self.ax.set_xlabel('Voltage')
            self.ax.set_ylabel('Ampe')
        elif self.optionMeasure == 1:
            self.ax.set_xlabel('Khoảng cách (cm)')
            self.ax.set_ylabel('Hiệu điện thế (V)')
        elif self.optionMeasure == 2:
            self.ax.set_xlabel('Time (s)')
            self.ax.set_ylabel('Hiệu điện thế (V)')
        elif self.optionMeasure == 3:
            self.ax.set_ylabel('Voltage 1')
            self.ax.set_xlabel('Ampe 2')
        else:
            self.ax.set_ylabel(Constance.symbolIP1 + "("+Constance.unitIP1+")")
            self.ax.set_xlabel(Constance.symbolIP2 + "("+Constance.unitIP2+")")
        
        if self.optionMeasure == 2:
            if self.whichLesson == 1:
                self.line1, = self.ax.plot(xValue, yValue[0], 'r-', picker=True, pickradius=10, label='Uc')
                self.line2, = self.ax.plot(xValue, yValue[1], 'b-', picker=True, pickradius=10, label='Ur')
                self.fig.legend()
            else:
                self.line, = self.ax.plot(xValue, yValue, picker=True, pickradius=10)
        else:
            self.line, = self.ax.plot(xValue, yValue, picker=True, pickradius=10)
        self.fig.show()
    
    def onpick(self, event):
        if self.optionMeasure == 4:
            if event.artist!=self.line: 
                return True     
            if not len(event.ind):  
                return True
            ind = event.ind[0]
            Constance.ind.append(ind)
            if len(Constance.ind) == 2:
                self.drawBestStraightLine()
                Constance.ind = []
            return True
        if self.optionMeasure == 2:
            if self.whichLesson == 1 and event.artist!=self.line1 and event.artist != self.line2: 
                return True   
            if self.whichLesson == 0 and event.artist!=self.line:
                return True  
            if not len(event.ind):  
                return True
            ind = event.ind[0]
            Constance.ind.append(ind)
            print(Constance.ind)
            if len(Constance.ind) >= 2:
                xValue, yValue = self.getXValueAndYValue()
                if self.whichLesson == 1:
                    if event.artist==self.line1: 
                        self.drawBestStraightLine(xValue=xValue, yValue=yValue[0], decimalPlace = Constance.decimalPlacesIP1)
                    elif event.artist==self.line2:
                        self.drawBestStraightLine(xValue=xValue, yValue=yValue[1], decimalPlace = Constance.decimalPlacesIP2)
                else:
                    if self.whichPort == 0:
                        self.drawBestStraightLine(xValue=xValue, yValue=yValue, decimalPlace = Constance.decimalPlacesIP1)
                    else:
                        self.drawBestStraightLine(xValue=xValue, yValue=yValue, decimalPlace = Constance.decimalPlacesIP2)
                
                Constance.ind = []
            return True
            
    
    def drawBestStraightLine(self, xValue = None, yValue = None, decimalPlace = 3):
        Constance.ind.sort()
        if self.optionMeasure == 4:
            try:
                xValue, yValue = self.getSmoothXValueAndYValue()    
                fig, ax = plt.subplots()
                ax.set_ylabel(Constance.symbolIP1 + "("+Constance.unitIP1+")")
                ax.set_xlabel(Constance.symbolIP2 + "("+Constance.unitIP2+")")
                ax.plot(xValue, yValue, picker=False)
                m, b = np.polyfit(xValue[Constance.ind[0]:Constance.ind[1]], yValue[Constance.ind[0]:Constance.ind[1]], 1)
                x = xValue[Constance.ind[0]:(Constance.ind[1]+1)]
                y = m*x + b

                if decimalPlace == None: decimalPlace = 3
                m = round(m, decimalPlace)
                b = round(b, decimalPlace)

                if b > 0:
                    labelLine = "y=%fx + %f" % (m, b)
                else:
                    labelLine = "y=%fx - %f" % (m, abs(b))
                ax.axline((x[0], y[0]),(x[-1], y[-1]), linewidth=2, color='r', label=labelLine)
                fig.legend()
                fig.show()
            except:
                messagebox.showwarning(title="Cảnh báo", message="Khoảng cách điểm chọn quá gần!")
        if self.optionMeasure == 2:
            try:
                fig2, ax2= plt.subplots()
                xValue =np.array(xValue)
                yValue = np.array(yValue)
                ax2.set_ylabel('Voltage')
                ax2.set_xlabel('Timepoint')
                ax2.plot(xValue, yValue, picker=False)
                m, b = np.polyfit(xValue[Constance.ind[0]:Constance.ind[1]], yValue[Constance.ind[0]:Constance.ind[1]], 1)
                x = xValue[Constance.ind[0]:(Constance.ind[1]+1)]
                y = m*x + b

                if decimalPlace == None: decimalPlace = 3
                m = round(m, decimalPlace)
                b = round(b, decimalPlace)

                if b > 0:
                    labelLine = "y=%fx + %f" % (m, b)
                else:
                    labelLine = "y=%fx - %f" % (m, abs(b))
                ax2.axline((x[0], y[0]),(x[-1], y[-1]), linewidth=2, color='r', label=labelLine)
                fig2.legend()
                fig2.show()
            except:
                messagebox.showwarning(title="Cảnh báo", message="Khoảng cách điểm chọn quá gần!")

    def getSmoothXValueAndYValue(self):
        xValue, yValue = self.getXValueAndYValue()
        xValue = np.array(xValue)
        yValue = np.array(yValue)
        df = pd.DataFrame()
        df['xsort'] = xValue
        df['ysort'] = yValue
        mean = df.groupby('xsort').mean()
        df_x = mean.index
        df_y = mean['ysort']
        xValue = df_x
        yValue = df_y
        X_Y_Spline = make_interp_spline(xValue, yValue)
        xValue = np.linspace(xValue.min(), xValue.max(), 150)
        yValue = X_Y_Spline(xValue)
        return xValue, yValue

    def getXValueAndYValue(self):
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
        elif self.optionMeasure == 2:
            if self.whichLesson == 1:
                yValue0 = []
                yValue1 = []
                for value in Constance.historyTVV:
                    yValue0.append(value['voltage1'])
                    yValue1.append(value['voltage2'])
                    xValue.append(value['timepoint'])
                yValue.append(yValue0)
                yValue.append(yValue1)
            else:
                for value in Constance.historyTV:
                    yValue.append(value['voltage'])
                    xValue.append(value['timepoint'])
        elif self.optionMeasure == 3:
            for value in Constance.historyA2V1:
                yValue.append(value['voltage1'])
                xValue.append(value['ampe2'])
        else:
            for value in Constance.historyI1I2:
                yValue.append(value['ampe1'])
                xValue.append(value['ampe2'])
        return xValue, yValue
    def exportData(self):
        
        xValue, yValue = self.getXValueAndYValue()

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
                worksheet.write(0, 1, 'Hiệu điện thế (V)')
                worksheet.write(0, 2, 'Khoảng cách (cm)')
            elif self.optionMeasure == 2:
                if self.whichLesson == 1:
                    worksheet.write(0, 0, 'STT')
                    worksheet.write(0, 1, 'Hiệu điện thế Uc (V)')
                    worksheet.write(0, 2, 'Hiệu điện thế Ur (V)')
                    worksheet.write(0, 3, 'Thời gian (s)')
                else:
                    worksheet.write(0, 0, 'STT')
                    worksheet.write(0, 1, 'Hiệu điện thế Uc (V)')
                    worksheet.write(0, 2, 'Thời gian (s)')
            elif self.optionMeasure == 3:
                worksheet.write(0, 0, 'STT')
                worksheet.write(0, 1, 'Voltage 1')
                worksheet.write(0, 2, 'Ampe 2')
            else:
                worksheet.write(0, 0, 'STT')
                worksheet.write(0, 1, Constance.symbolIP1+"("+Constance.unitIP1+")")
                worksheet.write(0, 2, Constance.symbolIP1+"("+Constance.unitIP1+")")
            if self.optionMeasure == 2 and self.whichLesson == 1:
                for row in range (1, len(xValue)+1):
                    worksheet.write(row, 0, row)
                    worksheet.write(row, 1, yValue[0][row-1])
                    worksheet.write(row, 2, yValue[1][row-1])
                    worksheet.write(row, 3, xValue[row-1])

            else:    
                for row in range (1, len(xValue)+1):
                    worksheet.write(row, 0, row)
                    worksheet.write(row, 1, yValue[row-1])
                    worksheet.write(row, 2, xValue[row-1])

            workbook.close()

    def changeOptionMeasure(self, option):
        if option == "A-V":
            self.optionMeasure = 0
            self.detect.option = 0
            self.tableLogger.heading(1, text='ID')
            self.tableLogger.heading(2, text='Voltage')
            self.tableLogger.heading(3, text='Ampe')
            self.loadData()
            self.entryValue.configure(placeholder_text="Giá trị  cường độ dòng điện (A)")
            self.entryValue.grid(row=2, column=1, sticky='nsew')
            self.cbWhichPort.grid(row=2, column=2, sticky='nsew')
            self.cbWhichLesson.grid_forget()
            self.tableLogger["displaycolumns"] =[1,2,3]

        elif option == "V-cm":
            self.optionMeasure = 1
            self.detect.option = 1
            self.tableLogger.heading(1, text='ID')
            self.tableLogger.heading(2, text='Khoảng cách (cm)')
            self.tableLogger.heading(3, text='Hiệu điện thế (V)')
            self.entryValue.configure(placeholder_text="Giá trị khoảng cách (cm)")
            self.loadData()
            self.entryValue.grid(row=2, column=1, sticky='nsew')
            self.cbWhichPort.grid(row=2, column=2, sticky='nsew')
            self.cbWhichLesson.grid_forget()
            self.tableLogger["displaycolumns"] =[1,2,3]

        elif option == "V-t":
            self.optionMeasure = 2
            self.detect.option = 2
            self.entryValue.configure(placeholder_text="Giá trị thời gian lặp")
            self.entryValue.grid_forget()
            if self.whichLesson == 1:
                self.tableLogger.heading(1, text='ID')
                self.tableLogger.heading(2, text='Time (s)')
                self.tableLogger.heading(3, text='Hiệu điện thế Uc (V)')
                self.tableLogger["displaycolumns"] =[1,2,3,4]
            else:
                self.tableLogger.heading(1, text='ID')
                self.tableLogger.heading(2, text='Time (s)')
                self.tableLogger.heading(3, text='Hiệu điện thế (V)')
                self.tableLogger["displaycolumns"] =[1,2,3]

            self.loadData()
            self.cbWhichPort.grid_forget()
            self.cbWhichLesson.grid(row=0, column=8, sticky='nsw')

        elif option == 'I1-I2':
            self.optionMeasure = 3
            self.detect.option = 3
            self.tableLogger.heading(1, text='ID')
            self.tableLogger.heading(2, text='Voltage 1')
            self.tableLogger.heading(3, text='Ampe 2')
            self.loadData()
            self.entryValue.grid(row=2, column=1, sticky='nsew')
            self.entryValue.configure(placeholder_text="Giá trị R")
            self.cbWhichPort.grid_forget()
            self.tableLogger["displaycolumns"] =[1,2,3]
        elif option == 'V1-I2':
            self.optionMeasure = 4
            self.detect.option = 4
            self.tableLogger.heading(1, text='ID')
            self.tableLogger.heading(2, text=Constance.symbolIP1)
            self.tableLogger.heading(3, text=Constance.symbolIP2)
            self.loadData()
            self.entryValue.grid_forget()
            self.cbWhichPort.grid_forget()
            self.tableLogger["displaycolumns"] =[1,2,3]
            self.cbWhichLesson.grid_forget()
    
    def loadData(self):
        self.clearTableData()
        if self.optionMeasure == 0:
            for i in range(0, len(Constance.historyAV)):
                item = Constance.historyAV[i]
                self.tableLogger.insert("", 0, iid=i+1, values=(i+1,item['ampe'],item['voltage']), tags='odd' if (i+1)%2 else 'even')
        elif self.optionMeasure == 1:
            for i in range(0, len(Constance.historyCV)):
                item = Constance.historyCV[i]
                self.tableLogger.insert("", 0, iid=i+1, values=(i+1,item['centimeter'],item['voltage']), tags='odd' if (i+1)%2 else 'even')
        elif self.optionMeasure == 2:
            if self.whichLesson == 1:
                for i in range(0, len(Constance.historyTVV)):
                    item = Constance.historyTVV[i]
                    self.tableLogger.insert("", 0, iid=i+1, values=(i+1,item['timepoint'],item['voltage1'],item['voltage2']), tags='odd' if (i+1)%2 else 'even')
            else:
                for i in range(0, len(Constance.historyTV)):
                    item = Constance.historyTV[i]
                    self.tableLogger.insert("", 0, iid=i+1, values=(i+1,item['timepoint'],item['voltage']), tags='odd' if (i+1)%2 else 'even')
        elif self.optionMeasure == 3:
            for i in range(0, len(Constance.historyI1I2)):
                item = Constance.historyI1I2[i]
                self.tableLogger.insert("", 0, iid=i+1, values=(i+1,item['ampe1'],item['ampe2']), tags='odd' if (i+1)%2 else 'even')
        elif self.optionMeasure == 4:
            print(Constance.historyI1I2)
            for i in range(0, len(Constance.historyI1I2)):
                item = Constance.historyI1I2[i]
                self.tableLogger.insert("", 0, iid=i+1, values=(i+1,item['ampe1'],item['ampe2']), tags='odd' if (i+1)%2 else 'even')
    
    def clearTableData(self):
        for item in self.tableLogger.get_children():
            self.tableLogger.delete(item)

    def clearData(self):
        if self.optionMeasure == 0:
            Constance.historyAV = []
        elif self.optionMeasure == 1:
            Constance.historyCV = []
        elif self.optionMeasure == 2:
            Constance.historyTV = []
            Constance.historyTVV = []
        elif self.optionMeasure == 3:
            Constance.historyA2V1 = []
        else:
            Constance.historyI1I2 = []
        self.clearTableData()

    def changePortMeasure(self, option):
        if option == "Cổng 1":
            self.whichPort = 0
        elif option == "Cổng 2":
            self.whichPort = 1

    def measure(self):
        if self.optionMeasure == 0:
            self.measureOnce()
        elif self.optionMeasure == 1:
            self.measureOnce()
        elif  self.optionMeasure == 2:
            self.measureContinuous()
        elif self.optionMeasure == 3:
            self.measureV1A2()
        else:
            self.measureI1I2()
    
    @property
    def onEnterPressed(self):
        self.measure()

    def changeLesson(self, option):
        if option == 'Phóng tụ':
            self.whichLesson = 1
            for item in self.tableLogger.get_children():
                self.tableLogger.delete(item)
            self.tableLogger.heading(3, text="Hiệu điện thế Uc (V)")
            for i in range(0, len(Constance.historyTVV)):
                item = Constance.historyTVV[i]
                self.tableLogger.insert("", 0, iid=i+1, values=(i+1,item['timepoint'],item['voltage1'],item['voltage2']), tags='odd' if (i+1)%2 else 'even')

            self.tableLogger["displaycolumns"] =[1,2,3,4]
            self.cbWhichPort.grid_forget()
        else:
            self.whichLesson = 2
            for item in self.tableLogger.get_children():
                self.tableLogger.delete(item)
            for i in range(0, len(Constance.historyTV)):
                item = Constance.historyTV[i]
                self.tableLogger.insert("", 0, iid=i+1, values=(i+1,item['timepoint'],item['voltage']), tags='odd' if (i+1)%2 else 'even')

            self.tableLogger.heading(3, text="Hiệu điện thế (V)")
            self.tableLogger["displaycolumns"] =[1,2,3]
            self.cbWhichPort.grid(row=2, column=2, sticky='nsew')