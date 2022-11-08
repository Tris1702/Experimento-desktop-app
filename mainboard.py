import customtkinter as ctk
from detect import Detect
from frameoffline import FrameOffline
from frameonline import FrameOnline

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue") 

class MainBoard(ctk.CTk):
    def __init__(self):
        super().__init__();
        WIDTH = 800
        HEIGHT = 600
        self.TEXTFONT = "Roboto Medium"
        self.isSubcribe = False
        # Calculate center
        screen_width = self.winfo_screenwidth()  # Width of the screen
        screen_height = self.winfo_screenheight() # Height of the screen
        x = (screen_width/2) - (WIDTH/2)
        y = (screen_height/2) - (HEIGHT/2)

        self.geometry('%dx%d+%d+%d' % (WIDTH, HEIGHT, x, y))
        self.title("Experimento")
        self.minsize(WIDTH, HEIGHT)
    
        #============== Create Frame ==========
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.frame_right = ctk.CTkFrame(master=self, corner_radius=10)
        self.frame_right.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
        self.frame_left = ctk.CTkFrame(master=self, corner_radius=10)
        self.frame_left.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        #============== Frame left ===============
        self.frame_left.grid_columnconfigure(0, minsize=5)
        self.frame_left.grid_columnconfigure(1, weight=0)
        self.frame_left.grid_rowconfigure(0, minsize=5)
        self.frame_left.grid_rowconfigure(1, weight=0)
        self.frame_left.grid_rowconfigure(2, minsize=10)
        self.frame_left.grid_rowconfigure(3, weight=0)
        self.frame_left.grid_rowconfigure(4, weight=1)
        self.frame_left.grid_columnconfigure(2, minsize=5)
        
        self.created_by = ctk.CTkLabel(master=self.frame_left, text="Created by @ProPTIT")
        self.created_by.grid(row=4, column=1, sticky='sw')

        self.btn_option_offline = ctk.CTkButton(master=self.frame_left, text='Offline', text_font=(self.TEXTFONT, -16), fg_color='#4D4D4D',command=lambda: self.changeFrame('offline'))
        self.btn_option_offline.grid(row=1,column=1, sticky='w')
        self.btn_option_online = ctk.CTkButton(master=self.frame_left, text='Online', text_font=(self.TEXTFONT, -16),fg_color='#4D4D4D' ,command=lambda: self.changeFrame('online'))
        self.btn_option_online.grid(row=3, column=1, sticky='w')
        

    def changeFrame(self, option):
        if option == 'offline':
            self.frame_right = FrameOffline(parent=self).main_frame
            self.frame_right.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
            self.btn_option_offline.configure(fg_color = '#395E9C')
            self.btn_option_online.configure(fg_color ='#4D4D4D')
        else: 
            self.frame_right = FrameOnline(parent=self).main_frame
            self.frame_right.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
            self.btn_option_offline.configure(fg_color = '#4D4D4D')
            self.btn_option_online.configure(fg_color = '#395E9C')
