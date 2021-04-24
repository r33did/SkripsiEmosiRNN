#import serial
import keras
import pandas as pd
#import datetime
#import serial.tools.list_ports
import os
import numpy as np
#from scipy import signal
#import matplotlib.pyplot as plt
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
#from com_serial import *
#from filter import *
from model import create_model
rawdata = []
pipi = []
alis = []
wkt = []
count = 0
header_list = ['Waktu','Pipi','Alis']
X = []
Y = []
#akuisisi()
#write()
#filtering()
#extract_feature('Data_filter')

model = create_model()
early_stopping = keras.callbacks.EarlyStopping(
        patience=10,
        min_delta=0.001,
        restore_best_weights=True,
)
maindirs = 'Feature_extract'
dirs = os.listdir(maindirs)
emosi = ['kaget','marah','santai','senang']
le = LabelEncoder()
#y = le.fit_transform(emosi)
#for i in emosi:
#    df = pd.read_csv(maindirs+'/'+i+'_extracted.csv')
#    df.loc['Unnamed'] = 0
#    b=list(df.iloc[0])
    #c=list(df.iloc[:,2])
    #d=list(df.iloc[:,1])
    #X.append(d)
    #X.append(c)
 #   X.append(b) 
#X = np.array(X)
df = pd.read_csv(maindirs+"/"+"tes_only.csv")
X = np.array(df.drop('EMOSI',axis=1))
y = np.array(df['EMOSI'])
print(X.shape)
print("GOTEM")
print(y.shape)
X_train, X_test, y_train, y_test = train_test_split(X,y,
                                    test_size=0.33,random_state=42)
print(X_train)
print(X_test)
print(y_train)
print(y_test)
history = model.fit(
     X_train,
     y_train,
     epochs=25,
     validation_data=(X_test,y_test),
     callbacks=[early_stopping],
     # verbose=0
     )
