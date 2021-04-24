import os
import pandas as pd
dirz = os.listdir('Feature_extract')
emosi=['kaget','marah','santai','senang']
dirs = 'Feature_extract'
dirz = os.listdir(dirs)
print(dirz)
print(len(dirz))
for i in emosi:
    temp=pd.read_csv(dirs+'/'+i+'_extracted.csv')
    print(temp.iloc[:,4])
