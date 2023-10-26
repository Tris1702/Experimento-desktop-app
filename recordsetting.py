import customtkinter as ctk
from constance import Constance

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue") 

class RecordSetting(ctk.CTkToplevel):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TEXTFONT = "Roboto Medium"
        self.isManual = None
        WIDTH = 400
        HEIGHT = 200
        
        screen_width = self.winfo_screenwidth()  # Width of the screen
        screen_height = self.winfo_screenheight() # Height of the screen
        
        x = (screen_width/2) - (WIDTH/2)
        y = (screen_height/2) - (HEIGHT/2)
        self.title('Chọn kiểu đo')
        self.geometry('%dx%d+%d+%d' % (WIDTH, HEIGHT, x, y))

        self.grid_rowconfigure((0,1,2), weight=0)
        self.grid_columnconfigure(0, weight=1)

        self.detailSettingFrame = ctk.CTkFrame(master=self)
        self.detailSettingFrame.grid(row=1, column=0, padx=5, pady=5, sticky="news")
        self.detailSettingFrame.grid_rowconfigure(0, weight=1)
        self.detailSettingFrame.grid_rowconfigure(1, minsize=5)
        self.detailSettingFrame.grid_rowconfigure(2, weight=1)
        self.detailSettingFrame.grid_rowconfigure(3, minsize=5)
        self.detailSettingFrame.grid_rowconfigure(4, weight=1)
        self.detailSettingFrame.grid_rowconfigure(5, minsize=5)
        self.detailSettingFrame.grid_rowconfigure(6, weight=1)
        self.detailSettingFrame.grid_rowconfigure(7, minsize=5)
        self.detailSettingFrame.grid_rowconfigure(8, weight=1)
        self.detailSettingFrame.grid_rowconfigure(9, minsize=5)
        self.detailSettingFrame.grid_rowconfigure(10, weight=1)

        self.detailSettingFrame.grid_columnconfigure(0, weight=0)
        self.detailSettingFrame.grid_columnconfigure(1, weight=1)

        self.radioGroupFrame = ctk.CTkFrame(master=self)
        self.radioGroupFrame.grid(row=0, column=0, padx=5, pady=5, sticky="news")
        self.radioGroupFrame.grid_rowconfigure(0, weight=1)
        self.radioGroupFrame.grid_columnconfigure((0,1), weight=1)

        self.btnSave = ctk.CTkButton(master=self, text="Lưu", command=self.saveChange,font=(self.TEXTFONT, -16))
        self.btnSave.grid(row=2, column=0)
        #======================Radio Frame==========================
        self.radioManual = ctk.CTkRadioButton(master=self.radioGroupFrame, text="Thủ công", command=lambda: self.setRecordType(isManual=True), hover=True,font=(self.TEXTFONT, -16))
        self.radioManual.grid(row=0, column=0, padx=5, pady=5, sticky='news')
        self.radioAuto = ctk.CTkRadioButton(master=self.radioGroupFrame, text="Tự động", command=lambda: self.setRecordType(isManual=False), hover=True,font=(self.TEXTFONT, -16))
        self.radioAuto.grid(row=0, column=1, padx=5, pady=5, sticky='news')

        #====================Detail Setting Frame===================
        # self.labelIntervalTime = ctk.CTkLabel(master=self.detailSettingFrame, text="Khoảng thời gian đo (s)",font=(self.TEXTFONT, -16))
        # self.labelIntervalTime.grid(row=0, column=0, padx=5, pady=5, sticky='nes')
        # self.intervalTimeStringVar = ctk.StringVar()
        # self.intervalTime = ctk.CTkEntry(master=self.detailSettingFrame, textvariable=self.intervalTimeStringVar,font=(self.TEXTFONT, -16))
        # self.intervalTime.grid(row=0, column=1, padx=5, pady=5, sticky='news')
        self.labelTimeMeasure = ctk.CTkLabel(master=self.detailSettingFrame, text='Thời gian đo (s)',font=(self.TEXTFONT, -16))
        self.labelTimeMeasure.grid(row=2, column=0, padx=5, pady=5, sticky='nes')
        self.timeMeasureStringVar = ctk.StringVar()
        self.timeMeasure = ctk.CTkEntry(master=self.detailSettingFrame, textvariable=self.timeMeasureStringVar,font=(self.TEXTFONT, -16))
        self.timeMeasure.grid(row=2, column=1, padx=5, pady=5, sticky='news')
        # self.labelVS = ctk.CTkLabel(master=self.detailSettingFrame, text='U nguồn', font=(self.TEXTFONT, -16))
        # self.labelVS.grid(row=4, column=0, padx=5, pady=5, sticky='nes')
        # self.vsStringVar = ctk.StringVar()
        # self.vs = ctk.CTkEntry(master=self.detailSettingFrame, textvariable=self.vsStringVar, font=(self.TEXTFONT, -16))
        # self.vs.grid(row=4, column=1, padx=5, pady=5, sticky='nes')
        # self.labelDelta = ctk.CTkLabel(master=self.detailSettingFrame, text='\u0394 U', font=(self.TEXTFONT, -16))
        # self.labelDelta.grid(row=6, column=0, padx=5, pady=5, sticky='nes')
        # self.deltaStringVar = ctk.StringVar()
        # self.delta = ctk.CTkEntry(master=self.detailSettingFrame, textvariable=self.deltaStringVar, font=(self.TEXTFONT, -16))
        # self.delta.grid(row=6, column=1, padx=5, pady=5, sticky='nes')
        
        # self.labelTl1Un = ctk.CTkLabel(master=self.detailSettingFrame, text='Tỉ lệ U nạp', font=(self.TEXTFONT, -16))
        # self.labelTl1Un.grid(row=6, column=0, padx=5, pady=5, sticky='nes')
        # self.tl1UnStringVar = ctk.StringVar()
        # self.tl1Un = ctk.CTkEntry(master=self.detailSettingFrame, textvariable=self.tl1UnStringVar, font=(self.TEXTFONT, -16))
        # self.tl1Un.grid(row=6, column=1, padx=5, pady=5, sticky='nes')

        # self.labelTl2Un = ctk.CTkLabel(master=self.detailSettingFrame, text='Tỉ lệ U phóng', font=(self.TEXTFONT, -16))
        # self.labelTl2Un.grid(row=8, column=0, padx=5, pady=5, sticky='nes')
        # self.tl2UnStringVar = ctk.StringVar()
        # self.tl2Un = ctk.CTkEntry(master=self.detailSettingFrame, textvariable=self.tl2UnStringVar, font=(self.TEXTFONT, -16))
        # self.tl2Un.grid(row=8, column=1, padx=5, pady=5, sticky='nes')
        self.loadData()

    def loadData(self):
        self.setRecordType(Constance.isManualRecord)
        # self.intervalTimeStringVar.set(str(Constance.intervalTime))
        self.timeMeasureStringVar.set(str(Constance.timeMeasure))
        # self.vsStringVar.set(str(Constance.vs))
        # self.deltaStringVar.set(str(Constance.deltaV))
        # self.tl1UnStringVar.set(str(Constance.tl1Un))
        # self.tl2UnStringVar.set(str(Constance.tl2Un))

    def saveChange(self):
        Constance.isManualRecord=self.isManual
        try:
            # Constance.intervalTime = float(self.intervalTime.get())
            Constance.timeMeasure = float(self.timeMeasure.get())
            # Constance.vs = float(self.vsStringVar.get())
            # Constance.deltaV = float(self.deltaStringVar.get())
            # Constance.tl1Un = float(self.tl1UnStringVar.get())
            # Constance.tl2Un = float(self.tl2UnStringVar.get())
        except ValueError:
            # Constance.intervalTime = 0.1
            print("Wrong numer")
        self.destroy()
        self.update()
        
    def setRecordType(self, isManual):
        self.isManual = isManual
        if isManual:
            self.radioManual.select()
            self.radioAuto.deselect()
            self.detailSettingFrame.grid_forget()
        else:
            self.radioAuto.select()
            self.radioManual.deselect()
            self.detailSettingFrame.grid(row=1, column=0, padx=5, pady=5, sticky="news")