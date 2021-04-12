import keras
import os
import numpy as np
import pandas as pd
import statistics as st
from keras.utils import to_categorical
from sklearn import metrics
from sklearn.metrics import confusion_matrix

data1 = []
data2 = []
labels = []

def extract_feature(folder='data_test'):
    dirs = os.listdir(folder)
    count = 0
    root = 'Feature_extract'
    for dr in dirs:
        df = pd.read_csv(folder+'/'+dr)
        data1 = list(df.iloc[:,2])
        #data2 = list(df.iloc[:,4])
        
        stdv1 = st.stdev(data1)
        rrt1 = st.mean(data1)
        md1 = st.median(data1)
        data2.append(stdv1)
        data2.append(rrt1)
        data2.append(md1)
        print(stdv1)
        print(rrt1)
        print(md1)
        
        #stdv2 = st.sdev(data2)
        #rrt2 = st.mean(data2)
        #md2 = st.median(data2)

        #d_t = list(zip(stdv1,rrt1,md1))
        finaldirs = os.path.join(root,dr)
        df1 = pd.DataFrame(data2)
        df1.to_csv(finaldirs)
    print('Selesai !')

#extract_feature('Data_filter')
