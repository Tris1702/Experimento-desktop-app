import customtkinter as ctk
from constance import Constance


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue") 

class InputsSetting(ctk.CTkToplevel):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TEXTFONT = "Roboto Medium"
        WIDTH = 500
        HEIGHT = 400
        
        screen_width = self.winfo_screenwidth()  # Width of the screen
        screen_height = self.winfo_screenheight() # Height of the screen
        
        x = (screen_width/2) - (WIDTH/2)
        y = (screen_height/2) - (HEIGHT/2)
        self.title('Cài đặt đầu đo')
        self.geometry('%dx%d+%d+%d' % (WIDTH, HEIGHT, x, y))

        self.grid_rowconfigure((0,1,2), weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.selectInputFrame = ctk.CTkFrame(master=self)
        self.selectInputFrame.grid(row=0, column=0, padx=5, pady=5, sticky="news")
        self.propertiesFrame = ctk.CTkFrame(master=self)
        self.propertiesFrame.grid(row=1, column=0, padx=5, pady=5, sticky="news")
        self.btnSave = ctk.CTkButton(master=self, text='Lưu', command=self.onSave)
        self.btnSave.grid(row=2, column=0)

        #===================SelectInputFrame========================
        self.selectInputFrame.grid_rowconfigure(0, weight=0)
        self.selectInputFrame.grid_columnconfigure(0, weight=0)
        self.selectInputFrame.grid_columnconfigure(1, weight=1)
        self.selectInputLabel = ctk.CTkLabel(master=self.selectInputFrame, text="Chọn đầu đo",font=(self.TEXTFONT, -16))
        self.selectInputLabel.grid(row=0, column=0, padx=5, pady=5, sticky='new')
        self.cbSelectInput = ctk.CTkComboBox(master=self.selectInputFrame, values=["Input 1", "Input 2"], command=self.loadData,font=(self.TEXTFONT, -16))
        self.cbSelectInput.grid(row=0, column=1, padx=5, pady=5, sticky='news')

        #====================PropertiesFrame========================
        self.propertiesFrame.grid_rowconfigure((0,1,2,3,4,5), weight=0)
        self.propertiesFrame.grid_columnconfigure((0,1), weight=1)
        self.formulaLabel = ctk.CTkLabel(master=self.propertiesFrame, text="Công thức (IP1, IP2)",font=(self.TEXTFONT, -16))
        self.formulaLabel.grid(row=0, column=0, padx=5, pady=5, sticky='nw')

        self.formulaStringVar = ctk.StringVar()
        self.formulaEntry = ctk.CTkEntry(master=self.propertiesFrame, textvariable=self.formulaStringVar,font=(self.TEXTFONT, -16))
        self.formulaEntry.grid(row=0, column=1, padx=5, pady=5, sticky='news')
        
        self.symbolStringVar = ctk.StringVar()
        self.symbolLabel = ctk.CTkLabel(master=self.propertiesFrame, text='Ký hiệu',font=(self.TEXTFONT, -16))
        self.symbolEntry = ctk.CTkEntry(master=self.propertiesFrame, textvariable=self.symbolStringVar,font=(self.TEXTFONT, -16))
        self.symbolLabel.grid(row=1, column=0, padx=5, pady=5, sticky='nw')
        self.symbolEntry.grid(row=1, column=1, padx=5, pady=5, sticky='news')
        
        self.unitStringVar = ctk.StringVar()
        self.unitLabel = ctk.CTkLabel(master=self.propertiesFrame, text='Đơn vị',font=(self.TEXTFONT, -16))
        self.unitEntry = ctk.CTkEntry(master=self.propertiesFrame, textvariable=self.unitStringVar,font=(self.TEXTFONT, -16))
        self.unitLabel.grid(row=2, column=0, padx=5, pady=5, sticky='nw')
        self.unitEntry.grid(row=2, column=1, padx=5, pady=5, sticky='news')

        # self.fromStringVar = ctk.StringVar()
        # self.fromLabel = ctk.CTkLabel(master=self.propertiesFrame, text='Từ')
        # self.fromEntry = ctk.CTkEntry(master=self.propertiesFrame, textvariable=self.fromStringVar,font=(self.TEXTFONT, -16))
        # self.fromLabel.grid(row=3, column=0, padx=5, pady=5, sticky='nw')
        # self.fromEntry.grid(row=3, column=1, padx=5, pady=5, sticky='news')

        # self.toStringVar = ctk.StringVar()
        # self.toLabel = ctk.CTkLabel(master=self.propertiesFrame, text='Đến')
        # self.toEntry = ctk.CTkEntry(master=self.propertiesFrame, textvariable=self.toStringVar,font=(self.TEXTFONT, -16))
        # self.toLabel.grid(row=4, column=0, padx=5, pady=5, sticky='nw')
        # self.toEntry.grid(row=4, column=1, padx=5, pady=5, sticky='news')

        self.decimalPlacesStringVar = ctk.StringVar()
        self.decimalPlacesLabel = ctk.CTkLabel(master=self.propertiesFrame, text='Làm tròn (x chữ số)',font=(self.TEXTFONT, -16))
        self.decimalPlacesEntry = ctk.CTkEntry(master=self.propertiesFrame, textvariable=self.decimalPlacesStringVar,font=(self.TEXTFONT, -16))
        self.decimalPlacesLabel.grid(row=3, column=0, padx=5, pady=5, sticky='nw')
        self.decimalPlacesEntry.grid(row=3, column=1, padx=5, pady=5, sticky='news')

        self.loadData()

    def loadData(self, value=None):
        if self.cbSelectInput.get() == 'Input 1':
            if Constance.formulaIP1 != None:
                self.formulaStringVar.set(str(Constance.formulaIP1))
            else:
                self.formulaStringVar.set('')
            if Constance.symbolIP1 != None:
                self.symbolStringVar.set(str(Constance.symbolIP1))
            else:
                self.symbolStringVar.set('')
            # if Constance.fromValueIP1 != None:
                # self.fromStringVar.set(str(Constance.fromValueIP1))
            if Constance.unitIP1 != None:
                self.unitStringVar.set(str(Constance.unitIP1))
            # if Constance.toValueIP1 != None:
            #     self.toStringVar.set(str(Constance.toValueIP1))
            if Constance.decimalPlacesIP1 != None:
                self.decimalPlacesStringVar.set(str(Constance.decimalPlacesIP1))
        else:
            if Constance.formulaIP2 != None:
                self.formulaStringVar.set(str(Constance.formulaIP2))
            else:
                self.formulaStringVar.set('')
            if Constance.symbolIP2 != None:
                self.symbolStringVar.set(str(Constance.symbolIP2))
            else:
                self.symbolStringVar.set('')
            if Constance.unitIP2 != None:
                self.unitStringVar.set(str(Constance.unitIP2))
            # if Constance.fromValueIP2 != None:
            #     self.fromStringVar.set(str(Constance.fromValueIP2))
            # if Constance.toValueIP2 != None:
            #     self.toStringVar.set(str(Constance.toValueIP2))
            if Constance.decimalPlacesIP2 != None:
                self.decimalPlacesStringVar.set(str(Constance.decimalPlacesIP2))


    def onSave(self):
        self.updateData()
        if Constance.currentLession == 2 or self.cbSelectInput.get() == 'Input 2':
            self.destroy()
    
    def updateData(self):
        if self.cbSelectInput.get() == 'Input 1':
            Constance.formulaIP1 = self.formulaEntry.get()
            Constance.symbolIP1 = self.symbolEntry.get()
            # Constance.fromValueIP1 = self.fromEntry.get()
            Constance.unitIP1 = self.unitEntry.get()
            # Constance.toValueIP1 = self.toEntry.get()
            Constance.decimalPlacesIP1 = self.decimalPlacesEntry.get()
        else:
            Constance.formulaIP2 = self.formulaEntry.get()
            Constance.symbolIP2 = self.symbolEntry.get()
            # Constance.fromValueIP2 = self.fromEntry.get()
            Constance.unitIP2 = self.unitEntry.get()
            # Constance.toValueIP2 = self.toEntry.get()
            Constance.decimalPlacesIP2 = self.decimalPlacesEntry.get()