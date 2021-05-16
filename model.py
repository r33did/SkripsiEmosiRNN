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
