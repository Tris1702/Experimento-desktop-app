from dashboard import Dashboard
from constance import Constance
from tkinter import messagebox
import pandas as pd

app = Dashboard()
# def motion(event):
#     x, y = event.x, event.y
#     Constance.currentX = x
#     Constance.currentY = y
#     print('{}, {}'.format(x, y))

def saveToTrace():
    trace = {
        'formulaIP1': [Constance.formulaIP1],
        'symbolIP1': [Constance.symbolIP1],
        'unitIP1': [Constance.unitIP1],
        'decimalPlacesIP1': [Constance.decimalPlacesIP1],
        'formulaIP2': [Constance.formulaIP2],
        'symbolIP2': [Constance.symbolIP2],
        'unitIP2': [Constance.unitIP2],
        'decimalPlacesIP2': [Constance.decimalPlacesIP2],
        'timeMeasure': [Constance.timeMeasure]
    }
    data = pd.DataFrame(trace)
    data.to_csv("trace.csv", sep=',', encoding='utf-8', index=False)
    print()

def getFromTrace():
    try:
        data = pd.read_csv('trace.csv', delimiter=',')
        trace = data.values.tolist()[0]
        print(trace)
        Constance.formulaIP1 = str(trace[0])
        Constance.symbolIP1 = str(trace[1])
        Constance.unitIP1 = str(trace[2])
        Constance.decimalPlacesIP1 = str(trace[3]) 
        Constance.formulaIP2 = str(trace[4])
        Constance.symbolIP2= str(trace[5])
        Constance.unitIP2 = str(trace[6])
        Constance.decimalPlacesIP2 = str(trace[7])
        try:
            Constance.timeMeasure = float(trace[9])
        except:
            Constance.timeMeasure = 8
    except:
        print('No trace')

def on_closing():
    # saveToTrace()
    app.quit()

if __name__ == '__main__':
    # getFromTrace()
    Constance.root = app
    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.bind('<Return>', app.onEnterPressed)
    # app.bind('<Motion>', motion)
    app.mainloop()
    
    