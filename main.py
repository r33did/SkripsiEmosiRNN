import serial
import pandas as pd
import datetime
import serial.tools.list_ports
import os
from scipy import signal
import matplotlib.pyplot as plt
import tensorflow as tf
from sklearn.model_selection import train_test_split
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

create_model()
maindirs = 'Feature_extract'
dirs = os.listdir(maindirs)
emosi = ['kaget','marah','santai','senang']
for i in emosi:
    df = pd.read_csv(maindirs+'/'+i+'_extracted.csv')
    b=list(df.iloc[:,3])
    c=list(df.iloc[:,2])
    d=list(df.iloc[:,1])
    X.append(d)
    X.append(c)
    X.append(b)
print(len(X))
y = tf.keras.utils.to_categorical([0,1,2,3], num_classes=4)
y = tf.constant(y, shape=[4, 4])
X_train, X_test, y_train, y_test = train_test_split(X,y,
                                    test_size=0.33,random_state=42)

history = model.fit(
     X_train,
     y_train,
     epochs=25,
     validation_data=(X_test,y_test),
     callbacks=[early_stopping],
     # verbose=0
     )
