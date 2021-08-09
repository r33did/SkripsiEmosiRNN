from re import I
import pandas as pd
import os
import sys
import tkinter as tk
import numpy as np
import serial
import time
import matplotlib.pyplot as plt
import datetime
import serial.tools.list_ports
from itertools import count
from matplotlib.animation import FuncAnimation

x_data = []
y_data = []
data = np.array([])
fig,ax = plt.subplots()
ax.set_xlabel("Sample")
ax.set_xlim(0,1000)
ax.set_ylabel("Voltage")
ax.set_ylim(0,5)
line, = ax.plot(0,0)
index = count()
k=0
def animate(angka):
    x_data.append(next(index))
    y_data.append(angka)

    line.set_xdata(x_data)
    line.set_ydata(y_data)
    return line,

port = list(serial.tools.list_ports.comports())
arduino = serial.Serial(port[0].device,baudrate=9600)
while k<=1000:
    a = arduino.readline()
    b = a.decode("ISO-8859-1").strip();
    c = b.split(',');
    if (sys.getsizeof(c[0])==56):
        d = float(c[0])
        data = np.append(data,d);
        animation = FuncAnimation(fig, func=animate(angka=c[0]))
        plt.show()
        k += 1


