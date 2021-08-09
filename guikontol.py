import pandas as pd
import os
import sys
import tkinter as tk
import numpy as np
import serial
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import datetime
import serial.tools.list_ports

# ==============global variable
pipi = []
alis = []
wkt = []
count = 0
d = 0
e = 0
cond = False
# ===============func
def plot_data():
    global cond,pipi,alis
    while cond == True:
        data = arduino.readline()
        b = data.decode("ISO-8859-1").strip()
        c = b.split(',')
        if (sys.getsizeof(c[0])==56):
            if (len(data)<1000):
                pipi.append(float(c[0]))
                alis.append(float(c[1]))
                canvas.draw()
                # wkt.append(waktu)
                # count+=1
            else:
                pipi[0:999] = pipi[1:1000]
                pipi[99] = float(c[0])
                alis[0:999] = alis[1:1000]
                alis[99] = float(c[0])
            lines.set_xdata(np.arange(0,len(data)))
            lines.set_ydata(pipi)
            # lines.set_ydata(alis)
        else:
            pass
    root.after(1,plot_data)
def plot_start():
    global cond
    cond=True
    print("condition True !")

def plot_stop():
    global cond
    cond = False
    print("condition False !")
# ==================================================
header_list = ['Waktu','Pipi','Alis']
root = 'IAPS2_filter'
nama = input('nama klien = ')
emosi = input('emosi klien = ')
df = pd.read_csv(root+'/'+nama+emosi+'.csv')
print(root+'/'+nama+emosi+'.csv')
df = df.drop("Unnamed: 0",axis=1)
pp = df['Pipi']
als = df['Alis']
root=tk.Tk()
root.title('Real Time Plot')
root.configure(background = 'light blue')
root.geometry('800x640')
fig = Figure();
ax = fig.add_subplot(111)
ax.set_title('EMG')
ax.set_xlabel('Sample')
ax.set_ylabel('Volt')
ax.set_xlim(0,1000)
ax.set_ylim(0,5)
lines = ax.plot([],[])[0]
canvas = FigureCanvasTkAgg(fig,master=root)
canvas.get_tk_widget().place(x=10,y=10,width=700,height=500)
canvas.draw()
root.update()
start = tk.Button(root,text='Start',font=('calibri',12),
                 command=lambda: plot_start())
start.place(x=100,y=500)
root.update()
stop = tk.Button(root,text='Stop',font=('calibri',12),
                command=lambda: plot_stop())
stop.place(x=start.winfo_x()+start.winfo_reqwidth()+20,y=500)

p = list(serial.tools.list_ports.comports())
arduino = serial.Serial(p[0].device,baudrate=9600)

root.after(1,plot_data)
root.mainloop()