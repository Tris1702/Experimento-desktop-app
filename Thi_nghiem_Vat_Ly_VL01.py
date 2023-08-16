from dashboard import Dashboard
from constance import Constance
from tkinter import messagebox

def on_closing():
    if messagebox.askokcancel("Thoát", "Bạn chắc chắn muốn thoát?"):
        app.destroy()
app = Dashboard()
if __name__ == '__main__':
    Constance.root = app

    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.bind('<Return>', app.onEnterPressed)
    app.mainloop()