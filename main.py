#import serial
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
#from com_serial import *
#from filter import *
from model import *
rawdata = []
pipi = []
alis = []
wkt = []
count = 0
header_list = ['Waktu','Pipi','Alis']
data = []
X = []
y = []
#akuisisi()
#write()
#filtering()
#extract_feature('Data_filter')

model = create_model()
maindirs = 'Feature_extract'
dirs = os.listdir(maindirs)
emosi = ['kaget','marah','santai','senang']
df = pd.read_csv(maindirs+"/"+"tes_extracted.csv")
maindirs = 'Feature_extract'
dirs = os.listdir(maindirs)
emosi = ['kaget','marah','santai','senang']
df = pd.read_csv(maindirs+"/"+"tes_extracted4.csv")
d_t = df.drop('EMOSI',axis=1)
label = pd.get_dummies(df['EMOSI'])
data_len = int(len(d_t))
for i in range (0,data_len):
    temp = d_t.iloc[[i]]
    temp_list = temp.values.tolist()
    X.append(temp_list)
for j in range(0,data_len):
    temp1 = label.iloc[[j]]
    temp1_list = temp1.values.tolist()
    y.append(temp1_list)
X = np.array(X)
y = np.array(y)
length = 40
num_train = 31
index = np.random.randint(0,length, size=length)
train_X = X[index[0:num_train]]
train_Y = y[index[0:num_train]]
test_X = X[index[num_train:]]
test_Y = y[index[num_train:]]
history = model.fit(
     train_X,
     train_Y,
     epochs=500,
     validation_data=(test_X,test_Y),
     )
history_dict = history.history
loss_values = history_dict['loss']
val_loss_values = history_dict['val_loss']
epochs = range(1, len(loss_values) + 1)
plt.plot(epochs, loss_values, 'bo', label='Training loss')
plt.plot(epochs, val_loss_values, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()
acc_values = history_dict['acc']
val_acc_values = history_dict['val_acc']
plt.plot(epochs, acc_values, 'bo', label='Training acc')
plt.plot(epochs, val_acc_values, 'b', label='Validation acc')
plt.title('Training and validation accuracy')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()
