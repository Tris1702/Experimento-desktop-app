import customtkinter as ctk
from detectoffline import DetectOffline

class FrameOffline:

    def __init__(self, parent):
        super().__init__

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
        self.labelRepeat = ctk.CTkLabel(master=self.frame1, text="Repeat", text_font=(self.TEXTFONT, -16))
        self.labelRepeat.grid(row=4, column=0, sticky='nsw')

        self.entryRepeatTimes = ctk.CTkEntry(master=self.frame1, placeholder_text='2-10 times', text_font=(self.TEXTFONT, -16))
        self.entryRepeatTimes.grid(row=4, column=1, sticky='nsew')

        self.btnMeasureContinuous = ctk.CTkButton(master=self.frame1, corner_radius=10, text="Measure continuous", text_font=(self.TEXTFONT, -14), command=lambda: self.measureContinuous())
        self.btnMeasureContinuous.grid(row=4, column=3, sticky='nsew')


        #========Frame2===========
        self.frame2.grid_rowconfigure(0, weight=0)
        self.frame2.grid_rowconfigure(1, weight=1)
        self.frame2.grid_columnconfigure(0, minsize=10)
        self.frame2.grid_columnconfigure(1, weight=1)
        self.frame2.grid_columnconfigure(2, minsize=10)

        self.frame3 = ctk.CTkFrame(master=self.frame2)
        self.frame3.grid(row=0, column=1, sticky='nsew')
        self.frame3.grid_rowconfigure(0, weight=1)
        self.frame3.grid_columnconfigure(0, weight=0)
        self.frame3.grid_columnconfigure(1, weight=1)

        self.labelLogger = ctk.CTkLabel(master=self.frame3,text='Console Log', text_font=(self.TEXTFONT, -16))
        self.labelLogger.grid(row=0, column=0, sticky='nsw')

        self.btnDrawChart = ctk.CTkButton(master=self.frame3, text='Draw', text_font=(self.TEXTFONT, -16), command=lambda: self.drawChart())
        self.btnDrawChart.grid(row=0, column = 1, sticky='nse')

        self.tbLogger = ctk.CTkTextbox(master=self.frame2, corner_radius=10, state='disabled', text_font=(self.TEXTFONT, -14), height=100)
        self.tbLogger.grid(row=1, column=1, pady=10, sticky='nsew')
        
    def reloadCom(self):
        self.cbCom.configure(values=self.detect.get_coms())

    def measureContinuous(self):
        print('yes, i measure')

    def measureOnce(self):
        if self.detect.SERIAL_PORT == None:
            print('set port')
            self.detect.set_serial_port(self.cbCom.get())
        self.detect.measure(self.entryDistance.get())