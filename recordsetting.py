import customtkinter as ctk
from constance import Constance

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue") 

class RecordSetting(ctk.CTkToplevel):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
        self.detailSettingFrame.grid_columnconfigure(0, weight=0)
        self.detailSettingFrame.grid_columnconfigure(1, weight=1)

        self.radioGroupFrame = ctk.CTkFrame(master=self)
        self.radioGroupFrame.grid(row=0, column=0, padx=5, pady=5, sticky="news")
        self.radioGroupFrame.grid_rowconfigure(0, weight=1)
        self.radioGroupFrame.grid_columnconfigure((0,1), weight=1)

        self.btnSave = ctk.CTkButton(master=self, text="Lưu", command=self.saveChange)
        self.btnSave.grid(row=2, column=0)
        #======================Radio Frame==========================
        self.radioManual = ctk.CTkRadioButton(master=self.radioGroupFrame, text="Thủ công", command=lambda: self.setRecordType(isManual=True), hover=True)
        self.radioManual.grid(row=0, column=0, padx=5, pady=5, sticky='news')
        self.radioAuto = ctk.CTkRadioButton(master=self.radioGroupFrame, text="Tự động", command=lambda: self.setRecordType(isManual=False), hover=True)
        self.radioAuto.grid(row=0, column=1, padx=5, pady=5, sticky='news')

        #====================Detail Setting Frame===================
        self.labelIntervalTime = ctk.CTkLabel(master=self.detailSettingFrame, text="Khoảng thời gian đo (s)")
        self.labelIntervalTime.grid(row=0, column=0, padx=5, pady=5, sticky='nes')
        self.intervalTimeStringVar = ctk.StringVar()
        self.intervalTime = ctk.CTkEntry(master=self.detailSettingFrame, textvariable=self.intervalTimeStringVar)
        self.intervalTime.grid(row=0, column=1, padx=5, pady=5, sticky='news')
        self.loadData()

    def loadData(self):
        self.setRecordType(Constance.isManualRecord)
        self.intervalTimeStringVar.set(str(Constance.intervalTime))

    def saveChange(self):
        Constance.isManualRecord=self.isManual
        try:
            Constance.intervalTime = float(self.intervalTime.get())
        except ValueError:
            Constance.intervalTime = 0.1
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