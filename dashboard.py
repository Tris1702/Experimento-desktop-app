import customtkinter as ctk
from frameoffline import FrameOffline
from frameonline import FrameOnline
from framesetting import FrameSetting

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue") 
class Dashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        WIDTH = 1200
        HEIGHT = 600
        self.TEXTFONT = "Roboto Medium"
        self.isSubcribe = False
        # Calculate center
        screen_width = self.winfo_screenwidth()  # Width of the screen
        screen_height = self.winfo_screenheight() # Height of the screen
        x = (screen_width/2) - (WIDTH/2)
        y = (screen_height/2) - (HEIGHT/2)

        self.geometry('%dx%d+%d+%d' % (WIDTH, HEIGHT, x, y))
        self.title("Thí nghiệm Vật lý - VL01")
        self.minsize(WIDTH, HEIGHT)

        #============== Create Frame ==========
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=1)

        #==============FRAME LEFT================

        self.frame_left = FrameOffline(parent=self)
        self.frame_left.main_frame.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')

        #==============FRAME RIGHT===============

        # self.frame_right = FrameOnline(parent=self).main_frame
        # self.frame_right.grid(row=0, column=2, padx=5, pady=5, sticky='nsew')

        #==============FRAME SETTING=============

        self.frame_setting = FrameSetting(parent=self)
        self.frame_setting.main_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

    def onEnterPressed(self, event):
        self.frame_left.onEnterPressed