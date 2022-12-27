import customtkinter as ctk
from frameoffline import FrameOffline
from frameonline import FrameOnline

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue") 
global HISTORY
class Dashboard(ctk.CTk):
    def __init__(self):
        super().__init__();
        WIDTH = 1000
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
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.frame_right = ctk.CTkFrame(master=self, corner_radius=10)
        self.frame_right.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
        self.frame_left = ctk.CTkFrame(master=self, corner_radius=10)
        self.frame_left.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        #==============FRAME LEFT================

        self.frame_left = FrameOffline(parent=self).main_frame
        self.frame_left.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        #==============FRAME RIGHT===============

        self.frame_right = FrameOnline(parent=self).main_frame
        self.frame_right.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')