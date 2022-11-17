from app import App
from detect import Detect
import asyncio

def multiTask():
    app = App() 
    detect = Detect()
    asyncio.create_task(app.mainloop())
    asyncio.create_task(detect.run())

if __name__ == '__main__':
    # app = App()   
    # print('loop') 
    # detect = Detect()
    # app.mainloop()
    
    asyncio.run(multiTask())