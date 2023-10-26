import customtkinter as ctk
from constance import Constance

class ChosingPoint(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Điểm chọn")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.configure(fg_color="white")

    def on_closing(self):
        Constance.ind = []
        self.destroy()

    def setPoint1(self, y, x):
        self.label1 = ctk.CTkLabel(master=self, text=f"         Điểm 1: ({x}, {y})        ",text_color='black', font=('Roboto Bold', 14))
        self.label1.pack()
        self.focus()

    def setPoint2(self, y, x):
        self.label2 = ctk.CTkLabel(master=self, text=f"         Điểm 2: ({x}, {y})        ",text_color='black', font=('Roboto Bold', 14))
        self.label2.pack()
        self.focus()
    

