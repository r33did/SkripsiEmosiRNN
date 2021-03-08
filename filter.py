import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy import signal
data1n = []
data2n = []
    
def lowpass_filter(sinyal,fcl):
    sampleRate = 200
    #sampleRate = int(input('Masukkan freq sample rate (Hz) = ')
    wnl = fcl/(sampleRate)
    b,a = signal.butter(3,wnl,'lowpass')
    fil = signal.filtfilt(b, a, sinyal)
    return fil

if __name__ == "__main__":
    import matplotlib.pyplot as plt

baca = input('Masukkan nama file yang akan difilter : ')
#dirs = os.listdir(\Kuliah\Tugas Akhir\Source Code\test_git\SkripsiEmosiRNN="Data_training")
df = pd.read_csv('%s.csv'%baca)
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
    #data2n.append((x[i]-mn1)/(mx1-mn1))

plt.plot(t,data1n)
#plt.plot(t,data2n)
plt.show()

#d_t = list(zip(wkt,data1n,data2n))
d_t = list(zip(wkt,data1n))
df1 = pd.DataFrame(d_t,columns=['Waktu','Pipi'])
df1.to_csv('%s_filtered.csv'%baca)
