#import serial
import keras
import pandas as pd
#import serial.tools.list_ports
import os
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
#from com_serial import *
#from filter import *
from model import *
from sklearn.metrics import confusion_matrix,classification_report
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

#model = create_model()
model = keras.models.load_model('model_lstm2')
maindirs = 'Feature_extract'
dirs = os.listdir(maindirs)
emosi = ['kaget','marah','santai','senang']
df = pd.read_csv(maindirs+"/"+"tes_extracted.csv")
#df = pd.read_csv(maindirs+"/"+"tes_extracted4.csv")
d_t = df.drop('EMOSI',axis=1)
label = pd.get_dummies(df['EMOSI'])
data_len = int(len(d_t))
for i in range (0,data_len):
    temp = d_t.iloc[i]
    temp_list = temp.values.tolist()
    X.append(temp_list)
for j in range(0,data_len):
    temp1 = label.iloc[j]
    temp1_list = temp1.values.tolist()
    y.append(temp1_list)
X = np.array(X)
y = np.array(y)
length = 159
num_train = 90
index = np.random.randint(0,length, size=length)
train_X = X[index[0:num_train]]
train_Y = y[index[0:num_train]]
test_X = X[index[num_train:]]
test_Y = y[index[num_train:]]
train_X = np.reshape(train_X, (train_X.shape[0],1,train_X.shape[1]))
test_X = np.reshape(test_X, (test_X.shape[0],1,test_X.shape[1]))
print(train_X.shape)
print(train_Y.shape)
print(test_X.shape)
print(test_Y.shape)
# history = model.fit(
#      train_X,
#      train_Y,
#      batch_size = 10,
#      epochs=300,
#      validation_data=(test_X,test_Y),
#      )
# inpoot = int(input("Apakah mau simpan model ? "))
# if inpoot == 1:
#     model.save('model_lstm2')
#     model.save_weights('lstm2.h5')
#     print("Model berhasil disimpan !")
# else:
#     print("ga disimpen")
# history_dict = history.history
# loss_values = history_dict['loss']
# val_loss_values = history_dict['val_loss']
# epochs = range(1, len(loss_values) + 1)
# plt.plot(epochs, loss_values, 'bo', label='Training loss')
# plt.plot(epochs, val_loss_values, 'b', label='Validation loss')
# plt.title('Training and validation loss')
# plt.xlabel('Epochs')
# plt.ylabel('Loss')
# plt.legend()
# plt.show()
# acc_values = history_dict['acc']
# val_acc_values = history_dict['val_acc']
# plt.plot(epochs, acc_values, 'bo', label='Training acc')
# plt.plot(epochs, val_acc_values, 'b', label='Validation acc')
# plt.title('Training and validation accuracy')
# plt.xlabel('Epochs')
# plt.ylabel('Loss')
# plt.legend()
# plt.show()

y_pred = model.predict(test_X)
matrix = confusion_matrix(test_Y.argmax(axis=1), y_pred.argmax(axis=1))
print('kaget,marah,santai,senang')
print(matrix)
print(classification_report(test_Y.argmax(axis=1), y_pred.argmax(axis=1), digits=3,target_names=emosi))
