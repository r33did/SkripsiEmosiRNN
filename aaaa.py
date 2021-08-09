# com_serial.py is program to log data from arduino serial com
# import clean(data) to clean the raw data
# import write(data) to write data log to .csv format

# Created by Ahmad Akmal, 22-02-2021, for UGM EMG Research
import serial
import pandas as pd
import datetime
import serial.tools.list_ports
import os
rawdata = []
pipi = []
alis = []
wkt = []
count = 0
d = 0
e = 0
header_list = ['Waktu','Pipi','Alis']
def akuisisi():
    p = list(serial.tools.list_ports.comports())
    arduino = serial.Serial(p[0].device,baudrate=115200)
    arduino.flushInput()
    if not arduino.isOpen():
        arduino.open()
    global count
    while True:
        try:
            if count <= 1000:
                data = arduino.readline()
                b = data.decode("ISO-8859-1").strip()
                waktuReal = datetime.datetime.now()
                waktu = waktuReal.strftime('%H:%M:%S.%f')[:-3]
                c = b.split(',')
                d = (int(c[0])/1024)*5
                e = (int(c[1])/1024)*5
                pipi.append(c[0])
                alis.append(c[1])
                wkt.append(waktu)
                count+=1
                print(b)
                if count == 1000:
                    arduino.close()
                    print("Logging Data Selesai")
                    break
        except KeyboardInterrupt:
            print("Keyboard Interrupt")
            arduino.close()
            break

def write():
    root = 'Data_raw'
    d_t = list(zip(wkt,pipi,alis))
    df = pd.DataFrame(d_t, columns=header_list)
    nama_file = input("Masukkan nama file : ")
    finaldirs = os.path.join(root,'%s.csv'%nama_file)
    df.to_csv(finaldirs,header=header_list,mode='w+')
    print("Logging data selesai !")
    return df
akuisisi()
write()
# ---------------------------EOL--------------------------

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
    wnl = fcl/(sampleRate)
    b,a = signal.butter(3,wnl,'lowpass')
    fil = signal.filtfilt(b, a, sinyal)
    return fil

def filtering():
    print("Filter dimulai, harap tunggu sebentar")
    maindirs = 'Data_raw2'
    dirs = os.listdir(maindirs)
    for j in emosi:
        for z in range(1,int(len(dirs)/4)+1):
            df = pd.read_csv(maindirs+'/'+j+str(z)+'_2.csv')
            print(j+str(z))
            wk = df["Waktu"]
            pp = df['Pipi']
            al = df['Alis']
            wkt = list(wk)
            data1 = list(pp)
            data2 = list(al)

            t = [i for i in range(len(data1))]
            w = lowpass_filter(data1,2.0)
            x = lowpass_filter(data2,2.0)

            mn1 = min(w)
            mx1 = max(w)
            mn2 = min(x)
            mx2 = max(x)

            for i in range(len(w)):
                data1n.append((w[i]-mn1)/(mx1-mn1))
                data2n.append((x[i]-mn1)/(mx1-mn1))

            f = plt.figure()
            plt.xlabel('Data ke-')
            plt.ylabel('mV')
            plt.grid(True)
            plt.title(j+str(z))
            plt.plot(t,data1n)
            plt.plot(t,data2n)
            plt.savefig('Data_Plot/'+j+str(z)+'.png')
            f.clear()
            plt.close(f)

            d_t = list(zip(wkt,data1n,data2n))
            root = 'Data_filter2'
            finaldirs = os.path.join(root,j+str(z)+'_filtered.csv')
            df1 = pd.DataFrame(d_t,columns=['Waktu','Pipi','Alis'])
            df1.to_csv(finaldirs)
            data1n.clear()
            data2n.clear()
    print('Filter Selesai !')

import os
import numpy as np
import pandas as pd
import statistics as st
import keras
from keras.utils import to_categorical
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder

data1 = []
data2 = []
labels = []
labels_encoded = []
train_X = []
train_Y = []
val_X = []
val_Y = []
emosi = ['kaget','marah','santai','senang']

def extract_feature(folder):
    stdvn1 = []
    rrtn1 = []
    mdn1 = []
    stdvn2 = []
    rrtn2 = []
    mdn2 = []
    emosi = ['kaget','marah','santai','senang']
    emosi_list = []
    dirs = os.listdir(folder)
    count = 0
    root = 'Feature_extract'
    for i in emosi:
        for j in range(1,int(len(dirs)/4)+1):
            df = pd.read_csv(folder+'/'+i+str(j)+'_filtered.csv')
            print(folder+'/'+i+str(j)+'_filtered.csv')
            data1 = list(df.iloc[:,2])
            data2 = list(df.iloc[:,3])
            stdv1 = st.stdev(data1)
            rrt1 = st.mean(data1)
            md1 = st.median(data1)
            stdvn1.append(stdv1)
            rrtn1.append(rrt1)
            mdn1.append(md1)
            stdv2 = st.stdev(data2)
            rrt2 = st.mean(data2)
            md2 = st.median(data2)
            stdvn2.append(stdv2)
            rrtn2.append(rrt2)
            mdn2.append(md2)
            if(i == 'kaget'):
                mk = 1
                emosi_list.append(mk)
            elif(i == 'marah'):
                mk = 2
                emosi_list.append(mk)
            elif(i == 'santai'):
                mk = 3
                emosi_list.append(mk)
            elif(i == 'senang'):
                mk = 4
                emosi_list.append(mk)
            print('Selesai !')
    namafile = 'tes_extracted2.csv'
    finaldirs = os.path.join(root,namafile)
    df1 = pd.DataFrame({'STDEV1' : stdvn1,'AVG1' : rrtn1,'MDN1' : mdn1,
                        'STDEV2':stdvn2,'AVG2' : rrtn2,'MDN2' : mdn2,'EMOSI' : emosi_list})
    df1.to_csv(finaldirs,mode='w+')
    print(finaldirs)
    print('Ekstraksi Fitur Selesai !')
        #namafile = i+'_extracted.csv'
        #finaldirs = os.path.join(root,namafile)
        #if(i == 'kaget'):
        #    i = 1
        #elif(i == 'marah'):
        #    i = 2
        #elif(i == 'santai'):
        #    i = 3
        #elif(i == 'senang'):
        #    i = 4
        #df1 = pd.DataFrame({'STDEV1' : stdvn1,'AVG1' : rrtn1,'MDN1' : mdn1,
        #                    'STDEV2':stdvn2,'AVG2' : rrtn2,'MDN2' : mdn2,'EMOSI' : i})
        #df1.to_csv(finaldirs,mode='w+')
        #print(finaldirs)
        #stdvn1.clear()
        #rrtn1.clear()
        #mdn1.clear()
        #stdvn2.clear()
        #rrtn2.clear()
        #mdn2.clear()

def create_model():
    model = keras.models.Sequential([
            keras.layers.LSTM(8, return_sequences=True, input_shape=(1,6)),
            keras.layers.LSTM(8, return_sequences=True),
            keras.layers.Dense(4, activation='softmax')
            ])
    model.compile(
        loss="categorical_crossentropy",
        optimizer=keras.optimizers.Adam(lr=0.01),
        metrics=["acc"]
    )
    model.summary()
    return model

def prepare_inputs(X_train, X_test):
	ohe = OneHotEncoder()
	ohe.fit(X_train)
	X_train_enc = ohe.transform(X_train)
	X_test_enc = ohe.transform(X_test)
	return X_train_enc, X_test_enc

def prepare_targets(y_train, y_test):
	le = LabelEncoder()
	le.fit(y_train)
	y_train_enc = le.transform(y_train)
	y_test_enc = le.transform(y_test)
	return y_train_enc, y_test_enc

# history = model.fit(
#     train_X,
#     train_Y,
#     epochs=25,
#     validation_data=(val_X,val_Y),
#     callbacks=[early_stopping],
#     # verbose=0
#     )

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
#df = pd.read_csv(maindirs+"/"+"tes_extracted4.csv")
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
print(X[0:5])
print(y[0:5])
length = 159
num_train = 90
index = np.random.randint(0,length, size=length)
train_X = X[index[0:num_train]]
train_Y = y[index[0:num_train]]
test_X = X[index[num_train:]]
test_Y = y[index[num_train:]]
#checkpoint_path = 'Model/cp.ckpt'
#checkpoint_dir = os.path.dirname(checkpoint_path)
#cp_callback = keras.callbacks.ModelCheckpoint(checkpoint_path,
#                                              save_weight_only=True,
#                                              verbose=1)
history = model.fit(
     train_X,
     train_Y,
     batch_size = 10,
     epochs=300,
     validation_data=(test_X,test_Y),
     #callbacks = (cp_callback)
     )
model.save('lstm.h5')
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
