from pandas.core.indexes.api import all_indexes_same
import serial # import Serial Library
import serial.tools.list_ports
import numpy  # Import numpy
import matplotlib.pyplot as plt #import matplotlib library
import sys
import os
import pandas as pd
from drawnow import *

plt.ion() #Tell matplotlib you want interactive mode to plot live data
count=0

def makeFig(): #Create a function that makes our desired plot
    plt.ylim(1,4)                                 #Set y min and max values
    plt.title('REAL TIME EMG GOD DAMMIT')           #Plot the title
    plt.grid(True)                                  #Turn the grid on
    plt.ylabel('Volt')                              #Set ylabels
    plt.plot(pipisx, 'ro-', label='EMG Pipi')         #plot the temperature
    plt.legend(loc='upper left')                    #plot the legend
    plt2=plt.twinx()                                #Create a second y axis
    plt.ylim(1,4)                           #Set limits of second y axis- adjust to readings you are getting
    plt2.plot(alisx, 'b^-', label='EMG Alis')        #plot pressure data
    plt2.set_ylabel('Volt')                         #label second y axis
    plt2.ticklabel_format(useOffset=False)          #Force matplotlib to NOT autoscale y axis
    plt2.legend(loc='upper right')                  #plot the legend
    

root = 'IAPS hari 2'
dir = os.listdir(root)
df = pd.read_csv(root+'/'+dir[0])
pipi = df['Pipi'].to_numpy()
alis = df['Alis'].to_numpy()
length = len(pipi)
pipisx, alisx, iterate = [],[],[]
while len(iterate)<=111:
    for j in range(0,length):
        pipisx.append(float(pipi[j]))
        alisx.append(float(alis[j]))
        iterate.append(int(j))
        drawnow(makeFig)
        # plt.pause(0.00001)
        if(len(iterate)>100):                            #If you have 50 or more points, delete the first one from the array
            pipisx.pop(0)                       #This allows us to just see the last 50 data points
            alisx.pop(0)
        if(len(iterate)==110):
            plt.close()