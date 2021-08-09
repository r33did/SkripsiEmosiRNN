import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from itertools import count
from matplotlib.animation import FuncAnimation
import random
import serial
import datetime
import serial.tools.list_ports
import os
import sys
root = 'IAPS2_filter'
nama = input('nama klien = ')
emosi = input('emosi klien = ')
df = pd.read_csv(root+'/'+nama+emosi+'.csv')
print(root+'/'+nama+emosi+'.csv')
pipi = []
alis = []
index = count()
data1 = df['Pipi']
data2 = df['Alis']
x_vals = []
y_vals = []
index = count()
f = plt.figure()
f.set_figwidth(10)
f.set_figheight(3)
for j in range(0,len(data1)-1):
    x_vals.append(next(index))
    pipi.append(round(float(data1[j]),4))
    alis.append(round(float(data2[j]),4))
    plt.cla()
    plt.plot(x_vals,pipi, label='EMG Pipi')
    plt.plot(x_vals,alis, label='EMG Alis')
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.show()
