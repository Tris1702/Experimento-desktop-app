import customtkinter as ctk
from detectonline import DetectOnline
from tkinter import messagebox

class FrameOnline:
    def __init__(self, parent, history):
        super().__init__
        self.isSubcribe=False
        self.main_frame = ctk.CTkFrame(master=parent)
        self.detect = DetectOnline(history)
        self.TEXTFONT = "Roboto Medium"
        #==========Create Frames======
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.frame = ctk.CTkFrame(master=self.main_frame, corner_radius=10)
        self.frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

       
        #==========Frame ============
        self.frame.grid_rowconfigure((0,1,2), weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.labelTopic = ctk.CTkLabel(master=self.frame, text="Topic MQTT", text_font=(self.TEXTFONT, -16))
        self.labelTopic.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.entryTopic = ctk.CTkEntry(master=self.frame, placeholder_text="topic/example", text_font=(self.TEXTFONT, -16), corner_radius=10, border_width=1)
        self.entryTopic.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.btnSubcribe = ctk.CTkButton(master=self.frame, text="Subcribe", command=lambda: self.subcribeTopic(self.cbSelectCom.get(),self.entryTopic.get()), text_font=(self.TEXTFONT, -16))
        self.btnSubcribe.grid(row=2, column=0, padx=5, pady=5, sticky="new")

    def subcribeTopic(self, comName, topic):
        if self.isSubcribe == False:
            try:
                # Change button state
                self.btnSubcribe.configure(text="Unsubcribe",fg_color="red")
                self.isSubcribe = True
                self.detect.set_serial_port(comName)
                self.detect.set_topic(topic)
                self.detect.run()
            except NameError:
                messagebox.showerror(title='Alert', message=NameError)
        else:
            try:
                # Change button state
                self.btnSubcribe.configure(text="Subcribe",fg_color="#395E9C")
                self.isSubcribe = False
                self.detect.unsubcribe()
            except NameError:
                print(NameError)