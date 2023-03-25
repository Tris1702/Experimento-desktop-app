from dashboard import Dashboard
from constance import Constance

if __name__ == '__main__':
    app = Dashboard()   
    Constance.root = app
    app.bind('<Return>', app.onEnterPressed)
    app.mainloop()