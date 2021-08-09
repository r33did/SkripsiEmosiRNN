import keras
import pandas as pd
#import datetime
#import serial.tools.list_ports
import os
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
X = []
y = []
maindirs = 'Feature_extract'
dirs = os.listdir(maindirs)
emosi = ['kaget','marah','santai','senang']
df = pd.read_csv(maindirs+"/"+"tes_extracted.csv")
d_t = df.drop('EMOSI',axis=1)
label = pd.get_dummies(df['EMOSI'])
print(label)
data_len = int(len(d_t))
for i in range (0,data_len):
    temp = d_t.loc[i]
    temp_list = temp.values.tolist()
    print(temp_list)
    X.append(temp_list)
for j in range(0,data_len):
    temp1 = label.iloc[j]
    # print(temp1)
    temp1_list = temp1.values.tolist()
    y.append(temp1_list)
print(X)
print(y)
