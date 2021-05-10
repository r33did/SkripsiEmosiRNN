import pandas as pd
import os
emosi = ['kaget','marah','santai','senang']
maindirs = 'Data_raw'
root = 'Data_raw2'
data1n = []
data2n = []
dirs = os.listdir(maindirs)
print(dirs)
for j in emosi:
    for z in range(1,int(len(dirs)/4+1)):
        df = pd.read_csv(maindirs+'/'+j+str(z)+'.csv')
        print(j+str(z))
        pp = list(df['Pipi'])
        al = list(df['Alis'])
        wkt = list(df['Waktu'])
        for i in range(len(pp)):
            data1n.append((pp[i]/1024)*5)
            data2n.append((al[i]/1024)*5)
        print(len(data1n))
        print(len(data2n))
        d_t = list(zip(wkt,data1n,data2n))
        finaldirs = os.path.join(root,j+str(z)+'_2.csv')
        df1 = pd.DataFrame(d_t,columns=['Waktu','Pipi','Alis'])
        df1.to_csv(finaldirs)
        data1n.clear()
        data2n.clear()
