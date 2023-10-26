import customtkinter as ctk
from detectoffline import DetectOffline
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from tkinter import ttk
from tkinter import Menu
from tkinter.filedialog import asksaveasfile
import threading
from constance import Constance
from tkinter import messagebox
import xlsxwriter
import numpy as np
from scipy.interpolate import PchipInterpolator
import pyautogui
from scipy.optimize import curve_fit
import time
from numpy import ones,vstack
from numpy.linalg import lstsq
from chosingPoint import ChosingPoint

class FrameOffline:
    def __init__(self, parent):
        super().__init__
        self.isMeasuring = False
        self.TEXTFONT = "Roboto Medium"
        self.optionMeasure = 2
        self.subOptionMeasure = 1
        self.whichPort = 0
        self.whichLesson = 2
        Constance.whichLesson = 2
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
        self.labelCom = ctk.CTkLabel(master=self.frame1, text="Cổng kết nối", font=(self.TEXTFONT, -16))
        self.labelCom.grid(row=0, column=0, sticky='nsw')

        self.cbCom = ctk.CTkComboBox(master=self.frame1, values =self.detect.get_coms(), font=(self.TEXTFONT, -16))
        self.cbCom.grid(row=0, column=1, sticky='nsew')

        self.btnRefreshCom = ctk.CTkButton(master=self.frame1, corner_radius=10, text="Cập nhật", font=(self.TEXTFONT, -14), command=lambda: self.reloadCom())
        self.btnRefreshCom.grid(row=0, column=2, sticky='nsew')

        #     #===Second line===
        self.comboType = ctk.CTkComboBox(master=self.frame1, values=["Nạp tụ", "Phóng tụ"], font=(self.TEXTFONT, -16), command=self.changeOptionMeasure)
        self.comboType.grid(row=2, column=0, sticky='nsw')

        self.entryValue = ctk.CTkEntry(master=self.frame1, placeholder_text="Giá trị khoảng cách (cm)", font=(self.TEXTFONT, -16))
        # self.entryValue.grid(row=2, column=1, sticky='nsew')

        self.cbWhichPort = ctk.CTkComboBox(master=self.frame1, values=["Cổng 1", "Cổng 2"], font=(self.TEXTFONT, -16), command=self.changePortMeasure)
        self.cbWhichPort.grid(row=2, column=2, sticky='nsew')

        # #========Frame2===========
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
        self.frame3.grid_columnconfigure(7, weight=0)

        self.labelLogger = ctk.CTkLabel(master=self.frame3,text='Kết quả', font=(self.TEXTFONT, -16))
        self.labelLogger.grid(row=0, column=0, sticky='nsw')

        self.btnDrawChart = ctk.CTkButton(master=self.frame3, text='Vẽ', font=(self.TEXTFONT, -16), command=lambda: self.drawChart(self.optionMeasure))
        self.btnDrawChart.grid(row=0, column = 1, sticky='nsw')

        self.btnDrawChart2 = ctk.CTkButton(master=self.frame3, text='Vẽ I1 theo t', font=(self.TEXTFONT, -16), command=lambda: self.drawChart2())

        self.btnExport = ctk.CTkButton(master=self.frame3, text='Xuất file', font=(self.TEXTFONT, -16), command=self.exportData)
        self.btnExport.grid(row=0, column = 5, sticky='nsw')

        self.cbWhichLesson = ctk.CTkComboBox(master=self.frame3, values=['Phóng tụ', 'Nạp tụ'], font=(self.TEXTFONT, -16), command=self.changeLesson)

        self.btnExport = ctk.CTkButton(master=self.frame3, text='Xóa dữ liệu', font=(self.TEXTFONT, -16), command=self.clearData)
        self.btnExport.grid(row=0, column = 7, sticky='nsw')

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
        self.changeOptionMeasure("Nạp tụ")
        
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
        # else:
        #     self.isMeasuring = False
        #     self.timer_measure.cancel()

    def measureWithInterval(self, timer):
        if round(timer+Constance.intervalTime, 2) > Constance.timeMeasure+0.1:
            self.isMeasuring = False
            self.timer_measure.cancel()
            return
        self.timer_measure = threading.Timer(Constance.intervalTime, lambda: self.measureWithInterval(round(timer+Constance.intervalTime, 2)))
        self.timer_measure.start()
        
        if self.detect.SERIAL_PORT == None:
            print('set port')
            self.detect.set_serial_port(self.cbCom.get())
        try:
            self.detect.measure(0, timer)
            if self.whichLesson == 1:
                self.tableLogger.insert("", 0, iid=len(Constance.historyTV), values=(len(Constance.historyTV),Constance.historyTV[-1]['timepoint'],Constance.historyTV[-1]['voltage']), tags='odd' if len(Constance.historyTV)%2 else 'even')
            else:
                self.tableLogger.insert("", 0, iid=len(Constance.historyTV), values=(len(Constance.historyTV),Constance.historyTV[-1]['timepoint'],Constance.historyTV[-1]['voltage1'],Constance.historyTV[-1]['voltage2']), tags='odd' if len(Constance.historyTV)%2 else 'even')
        except NameError:
            print(NameError)
            self.isMeasuring = False
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
        except NameError:
            messagebox.showerror(title='Alert', message="Kiểm tra thông tin cài đặt các đầu đo")

    def remove0(self, y):
        y = np.copy(y)
        index = 0
        for i in range(0, len(y)):
            if y[i] == 0:
                index = i
        return [index+1, y[index+1:]]

    def removeMax(self, y):
        return y
        # index = 0
        # for i in range(0, len(y)):
        #     if abs(y[i] - max(y)) <= 1:
        #         index = i
        # return y[index:]

    def drawChart(self, option):
        self.drawTk = ctk.CTkToplevel()
        self.drawTk.title("VL01 LAB")
        self.fig = plt.figure() 
        self.ax = self.fig.add_subplot(111)
        self.fig.canvas = FigureCanvasTkAgg(self.fig, master = self.drawTk)
        self.fig.canvas.get_tk_widget().pack()
        self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        self.fig.canvas.mpl_connect('pick_event', self.onpick)
        if self.optionMeasure in [3,4]:
            try:
                xValue, yValue = self.getSmoothXValueAndYValue()
            except:
                # messagebox.showwarning(title="Cảnh báo", message="Yêu cầu nhiều điểm dữ liệu hơn!")
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
            self.ax.set_ylim(-15, 15)
        elif self.optionMeasure == 3:
            self.ax.set_ylabel('Voltage 1')
            self.ax.set_xlabel('Ampe 2')
        else:
            self.ax.set_ylim(0)
            self.ax.set_ylabel(Constance.symbolIP2 + "("+Constance.unitIP2+")")
            self.ax.set_xlabel(Constance.symbolIP1 + "("+Constance.unitIP1+")")
        self.ax.set_xlim(0)

        if self.optionMeasure == 2:
            self.ax.set_xticks(np.arange(0, Constance.timeMeasure+1, 1))
            
            # if Constance.whichLesson == 1:
            #     # values, counts = np.unique([value for value in yValue if value > 0.5 and value >= yValue[len(yValue)//3]], return_counts=True)
            #     # maxValue = values[counts.argmax()]
            #     # Constance.vs = maxValue
            #     # R1value = float(Constance.formulaIP1[4:])
            #     # operator1 = Constance.formulaIP1[3:4]
                
            #     # if operator1 == '/':
            #     #     Constance.vs = round(float(maxValue)/R1value, int(Constance.decimalPlacesIP1))
            #     # elif operator1 == '*':
            #     #     Constance.vs = round(float(maxValue)*R1value, int(Constance.decimalPlacesIP1))
            #     # elif operator1 == '+':
            #     #     Constance.vs = round(float(maxValue)+R1value, int(Constance.decimalPlacesIP1))
            #     # elif operator1 == '-':
            #     #     Constance.vs = round(float(maxValue)-R1value, int(Constance.decimalPlacesIP1))

            #     minValue = Constance.tl2Un*float(Constance.vs)
            # else:
            #     minValue = 0
            #     # maxValue = Constance.tl1Un*float(Constance.vs)

            # firstGreaterThan0 = -1
            # firstMax = -1
            if Constance.whichLesson == 2:
                y = self.replaceMax(yValue[1])
                popt, _ = curve_fit(self.functionX, np.arange(1, len(y)+1, 1), np.array(y))
                a, b, c = popt
                tau = (1/b) * 0.03
                Constance.A = a
                Constance.B = b
                Constance.C = c
                Constance.tau = tau
                print(tau)
            else:
                y = self.removeMax(yValue)
                popt, _ = curve_fit(self.functionX, np.arange(1, len(y)+1, 1), np.array(y))
                a, b, c = popt
                tau = (1/b) * 0.03
                Constance.A = a
                Constance.B = b
                Constance.C = c
                Constance.tau = tau
                print(tau)
            # if Constance.whichLesson == 1:
            #     minValue = a
            #     maxValue = Constance.tl1Un*float(Constance.vs)
            # else:
            #     minValue = 0
            #     maxValue = 
            # firstGreaterThan0 = -1
            # firstMax = -1
            # if Constance.whichLesson == 2:
            #     for index in range(0, len(yValue[0])):
            #         if yValue[0][index] == 0:
            #             firstGreaterThan0 = -1
            #         if yValue[0][index] >= 0 and firstGreaterThan0 == -1:
            #             firstGreaterThan0 = index

            # else:
            #     for index in range(len(yValue)-1, -1, -1):
            #         if firstMax == -1 or abs(yValue[index] - a) < abs(yValue[firstMax] - a):
            #             firstMax = index

            # print("Vs:" + str(Constance.vs))
            # print("minValue" + str(minValue))
            # print("maxvalue" + str(maxValue))
            # print("index0: " + str(firstGreaterThan0) +' '+ str(xValue[firstGreaterThan0]))
            # print("indexMax: " + str(firstMax) +' '+ str(xValue[firstMax]))    

            # result = str(round(abs(xValue[firstMax] - xValue[firstGreaterThan0]), 2))
                
            # self.ax.text(0.05, 0.95, '\u03C4: ' + result +' s\n' + 'Uo: ' + str(Constance.vs) + ' V', transform=self.ax.transAxes, fontsize=14, verticalalignment='top') 
            
            if self.whichLesson == 2:
                self.line2, = self.ax.plot(xValue, yValue[1], 'r-', picker=False, pickradius=10, label='Ur')
                self.line, = self.ax.plot(xValue, yValue[0], 'b-', picker=True, pickradius=10, label='Uc')
            else:
                self.line, = self.ax.plot(xValue, yValue, 'b-', picker=True, pickradius=10, label='Uc')
            self.fig.legend()
        else:
            if self.optionMeasure == 4:
                # self.ax.set_xticks(np.arange(min(yValue), max(yValue)+0.5, 0.1))
                # self.ax.set_yticks(np.arange(min(xValue), max(xValue)+0.5, 0.1))
                self.ax.set_xticks(np.arange(min(yValue), max(yValue)+0.5, abs(max(yValue)-min(yValue)) / 5))
                self.ax.set_yticks(np.arange(min(xValue), max(xValue)+0.5, abs(max(xValue)-min(xValue)) / 5))

                self.line, = self.ax.plot(yValue, xValue, picker=True, pickradius=10)
            else:
                self.line, = self.ax.plot(yValue, xValue, picker=True, pickradius=10)
        self.ax.grid()
    def replaceMax(self, y):
        x = np.copy(y)
        for i in range(0, len(x)):
            if x[i] == 0:
                x[i] = Constance.vs
        return x
    def drawChart2(self):
        tmp, yOldValue = self.getXValueAndYValue()
        yOldValue = [y for y in yOldValue]
        xOldValue = np.array([yOldValue[0] + 0.1*x for x in range(0, len(yOldValue))])
        yOldValue = np.array(yOldValue)

        m, b = np.polyfit(yOldValue[0:len(yOldValue)-1], xOldValue[0:len(yOldValue)-1], 1)
        
        yy = m*yOldValue + b
        
        fig, ax = plt.subplots()
        ax.plot(yy, yOldValue, 'r-')
        ax.set_xlabel('Thời gian (t)')
        ax.set_ylabel('I1 (A)')
        fig.show()
    def onpick(self, event):
        if self.optionMeasure == 2:
            xValue, yValue = self.getXValueAndYValue()
            if (Constance.whichLesson == 2 and event.artist!=self.line2) or (Constance.whichLesson == 1 and event.artist!=self.line): 
                return True  
            Constance.ind.append(event.ind[0])
            if len(Constance.ind) == 1:
                self.chosingPoint = ChosingPoint()
                if Constance.whichLesson == 1: 
                    self.chosingPoint.setPoint1(yValue[Constance.ind[0]], xValue[Constance.ind[0]])
                else: 
                    self.chosingPoint.setPoint1(yValue[1][Constance.ind[0]], xValue[Constance.ind[0]])
            elif len(Constance.ind) == 2:
                if Constance.whichLesson == 1: 
                    self.chosingPoint.setPoint2(yValue[Constance.ind[1]], xValue[Constance.ind[1]])
                else: 
                    self.chosingPoint.setPoint2(yValue[1][Constance.ind[1]], xValue[Constance.ind[1]])
            else:
                return True
            
    def onclick(self, event):
        if self.optionMeasure == 2:
            if event.button == 3 and len(Constance.ind) >= 2:
                position = pyautogui.position()
                contextMenu = Menu(master=self.drawTk, tearoff=0)
                contextMenu.add_command(label="Fit function", command=self.showFitFunction)
                contextMenu.tk_popup(position.x, position.y)
                # print(pyautogui.position().)

    def showFitFunction(self):
        self.chosingPoint.destroy()

        xValue, yValue = self.getXValueAndYValue()

        newTopUp = ctk.CTkToplevel(fg_color='white')
        newTopUp.title("VL01 LAB - Fit function")
        if Constance.vs == None and Constance.whichLesson == 1:
            Constance.vs = max(yValue)
        label = ctk.CTkLabel(master=newTopUp, text=f'   A = {Constance.vs}V, B = {Constance.tau}s (A*exp(-x/B))   ',text_color='black', font=('Roboto Bold', 14))
        label.pack()
        newTopUp.focus()

        drawTk = ctk.CTkToplevel()
        drawTk.title("VL01 LAB - Visual")
        fig1, ax1 = plt.subplots()
        fig1.canvas = FigureCanvasTkAgg(fig1, master = drawTk)
        fig1.canvas.get_tk_widget().pack()

        if Constance.whichLesson == 2:
            index, yy = self.remove0(yValue[1])
            ax1.plot(xValue[index:], yy, 'b-', label='Ur', linewidth=3)
            popt, _ = curve_fit(self.functionX, xValue[index:], yy)
            a, b, c = popt
            x_line = np.arange(min(xValue[index:]), max(xValue[index:]), 1)
            y_line = self.functionX(x_line, a, b, c)
        else:
            index = min(Constance.ind)
            xValue = xValue[index:]
            yValue = yValue[index:]
            ax1.plot(xValue, yValue, 'b-', label='Ur', linewidth=3)
            popt, _ = curve_fit(self.functionX, xValue, yValue)
            a, b, c = popt
            x_line = np.arange(min(xValue), max(xValue), 1)
            y_line = self.functionX(x_line, a, b, c)
        ax1.set_ylim(-15, 15)
        ax1.grid() 
        ax1.plot(x_line, y_line, '--', color='red')
        Constance.ind = []

    def functionX(self, x, a, b, c):
        return a * np.exp(-b * x) + c
    
    def drawBestStraightLine(self, xValue = None, yValue = None, decimalPlace = 3):
        Constance.ind.sort()
        if self.optionMeasure == 4:
            # try:
                xValue, yValue = self.getSmoothXValueAndYValue()    
                fig, ax = plt.subplots()
                ax.set_xlim(0)
                ax.set_ylim(0)
                ax.set_xticks(np.arange(min(yValue), max(yValue)+0.5, abs(max(yValue)-min(yValue)) / 5))
                ax.set_yticks(np.arange(min(xValue), max(xValue)+0.5, abs(max(xValue)-min(xValue)) / 5))
                ax.set_ylabel(Constance.symbolIP2 + "("+Constance.unitIP2+")")
                ax.set_xlabel(Constance.symbolIP1 + "("+Constance.unitIP1+")")
                ax.grid()
                ax.plot(yValue, xValue, picker=False)

                points = [(yValue[Constance.ind[0]], xValue[Constance.ind[0]]),(yValue[Constance.ind[1]],xValue[Constance.ind[1]])]

                x_coords, y_coords = zip(*points)
                A = vstack([x_coords,ones(len(x_coords))]).T
                m, b = lstsq(A, y_coords)[0]
                # print("Line Solution is y = {m}x + {c}".format(m=m,c=c))

                # m, b = np.polyfit(yValue[Constance.ind[0]:Constance.ind[1]], xValue[Constance.ind[0]:Constance.ind[1]], 1)
                x = yValue[Constance.ind[0]:(Constance.ind[1]+1)]
                y = m*x + b

                if decimalPlace == None: 
                    decimalPlace = 3
                m = round(m, decimalPlace)
                b = round(b, decimalPlace)

                labelPointX= "X0 = (%3f, 0)" % round(-b/m,3)
                labelPointY= "Y0 = (0, %3f)" % round(b, 3)
                ax.plot([-b/m], [0], 'go', label=labelPointX)
                ax.plot([0], [b], 'yo', label=labelPointY)

                # if b > 0:
                #     labelLine = "y=%3fx + %3f" % (m, b)
                # else:
                #     labelLine = "y=%3fx - %3f" % (m, abs(b))
                ax.axline((x[0], y[0]),(x[-1], y[-1]), linewidth=2, color='r')
                fig.legend()
                fig.show()
            # except:
            #     print(NameError)
                # messagebox.showwarning(title="Cảnh báo", message="Khoảng cách điểm chọn quá gần!")
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
        X_Y_Spline = PchipInterpolator(yValue, xValue)
        yValue = np.linspace(yValue.min(), yValue.max(), 150)
        xValue = X_Y_Spline(yValue)
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
            if Constance.whichLesson == 1:
                for index in range(1, len(Constance.historyTV)):
                    value = Constance.historyTV[index]
                    yValue.append(value['voltage'])
                    xValue.append(value['timepoint'])
            else:
                yValue1 = []
                yValue2 = []
                for index in range(1, len(Constance.historyTV)):
                    value = Constance.historyTV[index]
                    yValue1.append(value['voltage1'])
                    yValue2.append(value['voltage2'])
                    xValue.append(value['timepoint'])
                yValue.append(yValue1)
                yValue.append(yValue2)
        elif self.optionMeasure == 3:
            for value in Constance.historyA2V1:
                yValue.append(value['voltage1'])
                xValue.append(value['ampe2'])
        else:
            for index in range (0, len(Constance.historyI1I2)):
                value = Constance.historyI1I2[index]
                if len(xValue) > 1:
                    value1 = xValue[len(xValue)-1]
                    value2 = xValue[len(xValue)-2]
                    if not (value2 >= value1 and value1 >= value['ampe2']):
                        yValue.pop()
                        xValue.pop()
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
                if self.whichLesson == 2:
                    worksheet.write(0, 0, 'STT')
                    worksheet.write(0, 1, 'Time (s)')
                    worksheet.write(0, 2, 'Uc (V)')
                    worksheet.write(0, 3, 'Ur (V)')
                else:
                    worksheet.write(0, 0, 'STT')
                    worksheet.write(0, 1, 'Time (s)')
                    worksheet.write(0, 2, 'Uc (V)')
            elif self.optionMeasure == 3:
                worksheet.write(0, 0, 'STT')
                worksheet.write(0, 1, 'Voltage 1')
                worksheet.write(0, 2, 'Ampe 2')
            else:
                worksheet.write(0, 0, 'STT')
                worksheet.write(0, 1, Constance.symbolIP1+"("+Constance.unitIP1+")")
                worksheet.write(0, 2, Constance.symbolIP2+"("+Constance.unitIP2+")")
            if self.optionMeasure == 2:
                if self.whichLesson == 2:
                    for row in range (1, len(xValue)+1):
                        worksheet.write(row, 0, row)
                        worksheet.write(row, 1, xValue[row-1])
                        worksheet.write(row, 2, yValue[0][row-1])
                        worksheet.write(row, 3, yValue[1][row-1])
                else:
                    for row in range (1, len(xValue)+1):
                        worksheet.write(row, 0, row)
                        worksheet.write(row, 1, xValue[row-1])
                        worksheet.write(row, 2, yValue[row-1])

            else:    
                for row in range (1, len(xValue)+1):
                    worksheet.write(row, 0, row)
                    worksheet.write(row, 1, xValue[row-1])
                    worksheet.write(row, 2, yValue[row-1])

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
            self.btnDrawChart2.grid_forget()
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
            self.btnDrawChart2.grid_forget()
            self.tableLogger["displaycolumns"] =[1,2,3]

        elif option == "Nạp tụ":
            self.optionMeasure = 2
            self.detect.option = 2
            Constance.currentLession = 2
            Constance.whichLesson = 2
            self.whichLesson = 2
            self.entryValue.configure(placeholder_text="Giá trị thời gian lặp")
            self.btnDrawChart.configure(text='Vẽ')
            self.entryValue.grid_forget()
            self.tableLogger.heading(1, text='ID')
            self.tableLogger.heading(2, text='Time (s)')
            self.tableLogger.heading(3, text='Uc (V)')
            self.tableLogger.heading(4, text='Ur (V)')
            self.tableLogger["displaycolumns"] =[1,2,3,4]

            self.loadData()
            self.cbWhichPort.grid_forget()
            self.btnDrawChart2.grid_forget()
            # self.cbWhichLesson.grid(row=0, column=8, sticky='nsw')
        elif option == "Phóng tụ":
            self.optionMeasure = 2
            self.detect.option = 2
            Constance.currentLession = 2
            Constance.whichLesson = 1
            self.whichLesson = 1
            self.entryValue.configure(placeholder_text="Giá trị thời gian lặp")
            self.btnDrawChart.configure(text='Vẽ')
            self.entryValue.grid_forget()
            
            self.tableLogger.heading(1, text='ID')
            self.tableLogger.heading(2, text='Time (s)')
            self.tableLogger.heading(3, text='Uc (V)')
            self.tableLogger["displaycolumns"] =[1,2,3]

            self.loadData()
            self.cbWhichPort.grid_forget()
            self.btnDrawChart2.grid_forget()
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
            self.btnDrawChart2.grid_forget()
            self.tableLogger["displaycolumns"] =[1,2,3]
        elif option == 'I2-I1':
            self.optionMeasure = 4
            self.detect.option = 4
            Constance.currentLession = 4
            self.btnDrawChart.configure(text='Vẽ I2 theo I1')
            self.btnDrawChart2.grid(row=0, column=3, sticky='nsw')
            self.tableLogger.heading(1, text='ID')
            self.tableLogger.heading(2, text=Constance.symbolIP1)
            self.tableLogger.heading(3, text=Constance.symbolIP2)
            self.loadData()
            self.entryValue.grid_forget()
            self.cbWhichPort.grid_forget()
            self.tableLogger["displaycolumns"] =[1,2,3]
            self.cbWhichLesson.grid_forget()
    
    def loadData(self):
        self.clearData()
        self.clearTableData()
        # if self.optionMeasure == 0:
        #     for i in range(0, len(Constance.historyAV)):
        #         item = Constance.historyAV[i]
        #         self.tableLogger.insert("", 0, iid=i+1, values=(i+1,item['ampe'],item['voltage']), tags='odd' if (i+1)%2 else 'even')
        # elif self.optionMeasure == 1:
        #     for i in range(0, len(Constance.historyCV)):
        #         item = Constance.historyCV[i]
        #         self.tableLogger.insert("", 0, iid=i+1, values=(i+1,item['centimeter'],item['voltage']), tags='odd' if (i+1)%2 else 'even')
        # elif self.optionMeasure == 2:
        #     if self.whichLesson == 1:
        #         for i in range(0, len(Constance.historyTV)):
        #             item = Constance.historyTV[i]
        #             self.tableLogger.insert("", 0, iid=i+1, values=(i+1,item['timepoint'],item['voltage']), tags='odd' if (i+1)%2 else 'even')
        #     else:
        #         for i in range(0, len(Constance.historyTV)):
        #             item = Constance.historyTV[i]
        #             self.tableLogger.insert("", 0, iid=i+1, values=(i+1,item['timepoint'],item['voltage'],Constance.vs-float(item['voltage'])), tags='odd' if (i+1)%2 else 'even')
        # elif self.optionMeasure == 3:
        #     for i in range(0, len(Constance.historyI1I2)):
        #         item = Constance.historyI1I2[i]
        #         self.tableLogger.insert("", 0, iid=i+1, values=(i+1,item['ampe1'],item['ampe2']), tags='odd' if (i+1)%2 else 'even')
        # elif self.optionMeasure == 4:
        #     print(Constance.historyI1I2)
        #     for i in range(0, len(Constance.historyI1I2)):
        #         item = Constance.historyI1I2[i]
        #         self.tableLogger.insert("", 0, iid=i+1, values=(i+1,item['ampe1'],item['ampe2']), tags='odd' if (i+1)%2 else 'even')
    
    def clearTableData(self):
        for item in self.tableLogger.get_children():
            self.tableLogger.delete(item)

    def clearData(self):
        Constance.historyTV = []
        Constance.vs = None
        if self.optionMeasure == 0:
            Constance.historyAV = []
        elif self.optionMeasure == 1:
            Constance.historyCV = []
        elif self.optionMeasure == 2:
            Constance.historyTV = []
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
        print("change")
        # if option == 'Phóng tụ':
        #     self.whichLesson = 1
        #     for item in self.tableLogger.get_children():
        #         self.tableLogger.delete(item)
        #     self.tableLogger.heading(3, text="Hiệu điện thế Uc (V)")
        #     for i in range(0, len(Constance.historyTVV)):
        #         item = Constance.historyTVV[i]
        #         self.tableLogger.insert("", 0, iid=i+1, values=(i+1,item['timepoint'],item['voltage1'],item['voltage2']), tags='odd' if (i+1)%2 else 'even')

        #     self.tableLogger["displaycolumns"] =[1,2,3,4]
        #     self.cbWhichPort.grid_forget()
        # else:
        #     self.whichLesson = 2
        #     for item in self.tableLogger.get_children():
        #         self.tableLogger.delete(item)
        #     for i in range(0, len(Constance.historyTV)):
        #         item = Constance.historyTV[i]
        #         self.tableLogger.insert("", 0, iid=i+1, values=(i+1,item['timepoint'],item['voltage'],Constance.vs-float(item['voltage'])), tags='odd' if (i+1)%2 else 'even')

        #     self.tableLogger.heading(3, text="Hiệu điện thế (V)")
        #     self.tableLogger["displaycolumns"] =[1,2,3]
        #     self.cbWhichPort.grid(row=2, column=2, sticky='nsew')