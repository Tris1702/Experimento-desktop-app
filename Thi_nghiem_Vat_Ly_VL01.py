from dashboard import Dashboard
from constance import Constance
from tkinter import messagebox

app = Dashboard()
if __name__ == '__main__':
    Constance.root = app
    app.protocol("WM_DELETE_WINDOW", app.quit)
    app.bind('<Return>', app.onEnterPressed)
    app.mainloop()
    