import pandas as pd
import os
from scipy import signal
import matplotlib.pyplot as plt
data1n = []
data2n = []
root = 'Filtered'
emosi = ['kaget','marah','santai','senang']
    
def lowpass_filter(sinyal,fcl):
    sampleRate = 200
    #sampleRate = int(input('Masukkan freq sample rate (Hz) = ')
    wnl = fcl/(sampleRate)
    b,a = signal.butter(3,wnl,'lowpass')
    fil = signal.filtfilt(b, a, sinyal)
    return fil

def filtering():
    print("Filter dimulai, harap tunggu sebentar")
    maindirs = 'Data_raw'
    dirs = os.listdir(maindirs)
    #print(dirs)
    #print(type(dirs))
    for j in emosi:
        for z in range(2,int(len(dirs)/4)+2):
            df = pd.read_csv(maindirs+'/'+j+str(z)+'.csv')
            print(df)
            print(j+str(z))
            wk = df["Waktu"]
            pp = df['Pipi']
            #al = df['Alis']
            wkt = list(wk)
            data1 = list(pp)
            #data2 = list(al)

            t = [i for i in range(len(data1))]
            w = lowpass_filter(data1,2.0)
            #x = lowpass_filter(data2,2.0)

            mn1 = min(w)
            mx1 = max(w)
            #mn2 = min(x)
            #mx2 = max(x)

            for i in range(len(w)):
                data1n.append((w[i]-mn1)/(mx1-mn1))
            #    data2n.append((x[i]-mn1)/(mx1-mn1))

            #plt.plot(t,data1n)
            #plt.plot(t,data2n)
            #plt.show()

            #d_t = list(zip(wkt,data1n,data2n))
            root = 'Data_filter'
            finaldirs = os.path.join(root,j+str(z)+'_filtered.csv')
            d_t = list(zip(wkt,data1n))
            df1 = pd.DataFrame(d_t,columns=['Waktu','Pipi'])
            df1.to_csv(finaldirs)
            print('Filter Selesai !')
            data1n.clear()
            data2n.clear()
filtering()
