import os
import pandas as pd
dirz = os.listdir('Feature_extract')
emosi=['kaget','marah','santai','senang']
dirs = 'Data_filter'
dirz = os.listdir(dirs)
print(dirz)
print(len(dirz))
for i in emosi:
    for j in range(2,int(len(dirz)/4)+2):
        temp=pd.read_csv(dirs+'/'+i+str(j)+'_filtered'+'.csv')
        print(dirs+'/'+i+str(j)+'_filtered'+'.csv')
        print(temp)
        
