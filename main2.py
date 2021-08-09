import os
import numpy as np
import pandas as pd
from scipy import signal
import matplotlib.pyplot as plt
import statistics as st
import keras
from keras.utils import to_categorical
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix,classification_report
#from sklearn.model_selection import cross_val_score
#from sklearn.preprocessing import StandardScaler
#from sklearn.pipeline import Pipeline
#from keras.wrappers.scikit_learn import KerasClassifier

data1n = []
data2n = []
root_filter = 'Filtered'
emosi = ['NH','NL','PH','PL']
# pasien = ['adit','agus','amin','eka','hasna','riznop']
pasien = ['adit','agus','amin','bagus','basith','eka','hanif','rizki']
stdvn1 = []
rrtn1 = []
mdn1 = []
stdvn2 = []
rrtn2 = []
mdn2 = []
emosi_list = []
count = 0
root_extract = 'IAPS hari 1'
rawdata = []
pipi = []
alis = []
wkt = []
count = 0
header_list = ['Waktu','Pipi','Alis']
data = []
X = []
y = []

def create_model():
    model = keras.models.Sequential([
            keras.layers.LSTM(8, return_sequences=True, input_shape=[None,6]),
            keras.layers.LSTM(8),
            keras.layers.Dense(4, activation='softmax')
            ])
    model.compile(
        loss="categorical_crossentropy",
        optimizer=keras.optimizers.Adam(lr=0.01),
        metrics=["acc"]
    )
    model.summary()
    return model

model = create_model()
# model = keras.models.load_model('model_lstm2')

maindirs = 'IAPS1_extract'
dirs = os.listdir(maindirs)
emosi = ['NH','NL','PH','PL']
df = pd.read_csv(maindirs+"/"+"iaps2_extracted.csv")
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
length = 599
num_train = 395
index = np.random.randint(0,length, size=length)
train_X = X[index[0:num_train]]
train_Y = y[index[0:num_train]]
test_X = X[index[num_train:]]
test_Y = y[index[num_train:]]
# train_X = X[0:num_train]
# train_Y = y[0:num_train]
# test_X = X[num_train:]
# test_Y = y[num_train:]
train_X = np.reshape(train_X, (train_X.shape[0],1,train_X.shape[1]))
test_X = np.reshape(test_X, (test_X.shape[0],1,test_X.shape[1]))
print(train_X.shape)
print(train_Y.shape)
print(test_X.shape)
print(test_Y.shape)
callback = keras.callbacks.EarlyStopping(monitor='loss', patience=3)
history = model.fit(
     train_X,
     train_Y,
     batch_size = 10,
     epochs=1000,
#      callbacks=[callback],
     validation_data=(test_X,test_Y),
     )
inpoot = int(input("Apakah mau simpan model ? "))
if inpoot == 1:
    nama_model = str(input('Nama model = '))
    model.save(nama_model)
    model.save_weights(nama_model+'.h5')
    print("Model berhasil disimpan !")
    keras.backend.clear_session()
else:
    print("ga disimpen")
    keras.backend.clear_session()
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

length = 599
num_train = 395
index = np.random.randint(0,length, size=length)
train_X = X[index[0:num_train]]
train_Y = y[index[0:num_train]]
test_X = X[index[num_train:]]
test_Y = y[index[num_train:]]
train_X = np.reshape(train_X, (train_X.shape[0],1,train_X.shape[1]))
test_X = np.reshape(test_X, (test_X.shape[0],1,test_X.shape[1]))
y_pred = model.predict(test_X)
matrix = confusion_matrix(test_Y.argmax(axis=1), y_pred.argmax(axis=1))
print('NH,NL,PH,PL')
print(matrix)
print(classification_report(test_Y.argmax(axis=1), y_pred.argmax(axis=1), digits=3,target_names=emosi))
