from tkinter import *
import pandas as pd
import datetime
import serial.tools.list_ports
import os
import functools
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


pipi = []
alis = []
wkt = []
count = 0
d = 0
e = 0
header_list = ['Waktu','Pipi','Alis']
data_list = np.array([])
cond = False

ports = serial.tools.list_ports.comports()
serialObj = serial.Serial()


root = Tk()
root.config(bg='grey')

def initComPort(index):
    currentPort = str(ports[index])
    currentPort2 = str(currentPort.split(' ')[0])
    print(currentPort2)
    serialObj.port = currentPort2
    serialObj.baudrate = 9600
    serialObj.open()
    

for onePort in ports:
    comButton = Button(
        root, text=onePort, font=('Calibri','13'),
        height=1,width=45,
        command=functools.partial(initComPort,index=ports.index(onePort))
        )
    comButton.grid(row=ports.index(onePort),column=0)

# dataCanvas = Canvas(root,width=930,height=600,bg='black')
# dataCanvas.grid(row=0, column=1,rowspan=100)

# vsb = Scrollbar(root, orient='horizontal',command=dataCanvas.xview)
# vsb.grid(row=0,column=0,rowspan=100,sticky='ns')

# dataCanvas.config(xscrollcommand=vsb.set)

# dataFrame = Frame(dataCanvas,bg='white')
# dataCanvas.create_window((10,0),window=dataFrame,anchor='nw')

fig = Figure();
ax = fig.add_subplot(111)
ax.set_title('Serial Data');
ax.set_xlabel('Sample')
ax.set_ylabel('Voltage (V)')
ax.set_xlim(0,1000)
ax.set_ylim(-0.5,6)
lines = ax.plot([],[])[0]
canvas = FigureCanvasTkAgg(fig, master = root)
canvas.get_tk_widget().place(x=415,y=0,width=950,height=700)
canvas.draw()


def checkSerialPort():
    if serialObj.isOpen() and serialObj.in_waiting:
        # Mulai record serial (sampe count kelar)
        global count
        data = serialObj.readline()
        b = data.decode("ISO-8859-1").strip()
        waktuReal = datetime.datetime.now()
        waktu = waktuReal.strftime('%H:%M:%S.%f')[:-3]
        c = b.split(',')
        # Label(dataFrame,text=c[0], font=('Calibri','13'),bg='green').pack()
        # Label(dataFrame,text=c[1], font=('Calibri','13'),bg='yellow').pack()
        # print(type(c[0]))
        count+=1
        if (len(pipi) <= 100):
            pipi.append(float(c[0]))
            alis.append(float(c[1]))
            wkt.append(waktu)
        else:
            pipi[0:99] = pipi[1:100]
            alis[0:99] = alis[1:100]
            wkt[0:99] = wkt[1:100]
        lines.set_xdata(np.arange(0,len(pipi)))
        lines.set_ydata(pipi)

        canvas.draw()


    #             if count == 100:
    #                 serialObj.close()
    #                 print("Logging Data Selesai")
    #                 break
    #     except KeyboardInterrupt:
    #         print("Keyboard Interrupt")
    #         serialObj.close()
    #         break

while True:
    root.update()
    # create_plot()
    checkSerialPort()
    
    # dataCanvas.config(scrollregion=dataCanvas.bbox('all'))
