import customtkinter as ctk
from detect import Detect

class FrameOnline:
    def __init__(self, parent):
        super().__init__
        self.isSubcribe=False
        self.main_frame = ctk.CTkFrame(master=parent)
        self.detect = Detect()
        self.TEXTFONT = "Roboto Medium"
        #==========Create Frames======
        self.main_frame.grid_rowconfigure((0,1), weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.frame1 = ctk.CTkFrame(master=self.main_frame, corner_radius=10)
        self.frame1.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

        self.frame2 = ctk.CTkFrame(master=self.main_frame, corner_radius=10)
        self.frame2.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        #==========Frame 1============
        self.frame1.grid_rowconfigure((0,1), weight=1)
        self.frame1.grid_columnconfigure((0,1), weight=1)
        self.frame1.grid_columnconfigure(2, weight=0)
        
        self.labelSelectCom = ctk.CTkLabel(master=self.frame1, text="COM", text_font=(self.TEXTFONT, -16))
        self.labelSelectCom.grid(row=0, column=0, padx=5, pady = 5, sticky="nsew")
        self.cbSelectCom = ctk.CTkComboBox(master=self.frame1, values=self.detect.get_coms(), width=100, text_font=(self.TEXTFONT, -16), border_width=1, variable='---Select COM---')
        self.cbSelectCom.grid(row=0, column=1, padx=5, pady = 5, sticky="nsew")
        # img = Image.open("./img/refresh.png")
        # img = img.resize((10,10), Image.ANTIALIAS)
        # photoImg =  ImageTk.PhotoImage(img)
        self.btnLoadCom = ctk.CTkButton(master=self.frame1, text='Refresh',command=lambda: self.reloadCom())
        self.btnLoadCom.grid(row=0, column=2, padx=5, pady=5, sticky='nsew')
        #==========Frame 2============
        self.frame2.grid_rowconfigure((0,1), weight=1)
        self.frame2.grid_columnconfigure((0,1), weight=1)
        self.labelTopic = ctk.CTkLabel(master=self.frame2, text="Topic MQTT", text_font=(self.TEXTFONT, -16))
        self.labelTopic.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.entryTopic = ctk.CTkEntry(master=self.frame2, placeholder_text="topic/example", text_font=(self.TEXTFONT, -16), corner_radius=10, border_width=1)
        self.entryTopic.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        self.btnSubcribe = ctk.CTkButton(master=self.frame2, text="Subcribe", command=lambda: self.subcribeTopic(self.cbSelectCom.get(),self.entryTopic.get()), text_font=(self.TEXTFONT, -16))
        self.btnSubcribe.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    def reloadCom(self):
        self.cbSelectCom.configure(values=self.detect.get_coms())
        
    def measure(self):
        self.detect.measure()

    def subcribeTopic(self, comName, topic):
        if self.isSubcribe == False:
            # try:
                # Change button state
                self.btnSubcribe.configure(text="Unsubcribe",fg_color="red")

                self.isSubcribe = True
                self.detect.set_serial_port(comName)
                self.detect.subcribe(topic)
                self.detect.run()
            # except:
            #     messagebox.showerror(title='Alert', message='Oops! Something\'s wrong')
        else:
            try:
                # Change button state
                self.btnSubcribe.configure(text="Subcribe",fg_color="#395E9C")
                self.isSubcribe = False
                self.detect.unsubcribe()
            except:
                messagebox.showerror(title='Alert', message='Oops! Something\'s wrong')