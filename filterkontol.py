import os
import numpy as np
import pandas as pd
import statistics as st
from scipy import signal
import matplotlib.pyplot as plt
data1n = []
data2n = []
root = 'Filtered'
emosi = ['kaget','marah','santai','senang']
maindirs = 'IAPS hari 2'
dirs = os.listdir(maindirs)
def lowpass_filter(sinyal,fcl):
    sampleRate = 50
    wnl = fcl/(sampleRate)
    b,a = signal.butter(3,wnl,'lowpass')
    fil = signal.filtfilt(b, a, sinyal)
    return fil

def filtering(folder):
    print("Filter dimulai, harap tunggu sebentar")
    dirs = os.listdir(folder)
    for j in dirs:
        df = pd.read_csv(folder+'/'+str(j))
        print(j)
        #wk = df["Waktu"]
        pp = df['Pipi']
        al = df['Alis']
        #wkt = list(wk)
        data1 = list(pp)
        data2 = list(al)

        t = [i for i in range(len(data1))]
        w = lowpass_filter(data1,2.0)
        x = lowpass_filter(data2,2.0)

        mn1 = min(w)
        mx1 = max(w)
        mn2 = min(x)
        mx2 = max(x)

        for i in range(len(w)):
            data1n.append((w[i]-mn1)/(mx1-mn1))
            data2n.append((x[i]-mn2)/(mx2-mn2))

        f = plt.figure()
        plt.xlabel('Data ke-')
        plt.ylabel('mV')
        plt.grid(True)
        plt.title(j)
        plt.plot(t,data1n)
        plt.plot(t,data2n)
        plt.savefig('Data_Plot3/'+j+'2.png')
        f.clear()
        plt.close(f)
        d_t = list(zip(data1n,data2n))
        root = 'Data_filter4'
        finaldirs = os.path.join(root,j)
        df1 = pd.DataFrame(d_t,columns=['Pipi','Alis'])
        df1.to_csv(finaldirs)
        data1n.clear()
        data2n.clear()
    print('Filter Selesai !')
filtering('IAPS hari 2')
