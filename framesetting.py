import customtkinter as ctk
from recordsetting import RecordSetting
from inputssetting import InputsSetting

class FrameSetting():
    def __init__(self, parent):
        super().__init__
        self.main_frame = ctk.CTkFrame(master=parent)
        self.TEXTFONT = "Roboto Medium"
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.recordSetting = None
        self.inputsSetting = None

        #=========================================
        self.insideFrame = ctk.CTkFrame(master=self.main_frame, corner_radius=10)
        self.insideFrame.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")
        self.insideFrame.grid_rowconfigure(0, weight=1)
        self.insideFrame.grid_rowconfigure((1,2), weight=0)
        self.insideFrame.grid_rowconfigure(3, weight=1)
        
        self.insideFrame.columnconfigure(0, weight=1)

        self.txtSetting = ctk.CTkLabel(master=self.insideFrame, text="Cài đặt", text_font=(self.TEXTFONT, -16))
        self.txtSetting.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.btnSettingRecord = ctk.CTkButton(master=self.insideFrame, text="Kiểu đo", command=self.openSettingRecordType)
        self.btnSettingRecord.grid(row=1, column=0, padx=5, pady=5, sticky="new")
        self.btnSettingInputs = ctk.CTkButton(master=self.insideFrame, text="Cài đặt đầu đo", command=self.openSettingInputs)
        self.btnSettingInputs.grid(row=2, column=0, padx=5, pady=5, sticky="new")

    def openSettingRecordType(self):
        if self.recordSetting is None or not self.recordSetting.winfo_exists():
            self.recordSetting = RecordSetting(self.main_frame)  # create window if its None or destroyed
        else:
            self.recordSetting.lift(aboveThis=self.main_frame)  # if window exists focus it

    def openSettingInputs(self):
        if self.inputsSetting is None or not self.inputsSetting.winfo_exists():
            self.inputsSetting = InputsSetting(self.main_frame)  # create window if its None or destroyed
        else:
            self.inputsSetting.lift(aboveThis=self.main_frame)  # if window exists focus it


