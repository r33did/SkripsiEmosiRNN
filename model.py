import keras
import os
import numpy as np
import pandas as pd
import statistics as st
from keras.utils import to_categorical
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import train_test_split

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
    stdv = []
    rrt = []
    md = []
    emosi = ['kaget','marah','santai','senang']
    dirs = os.listdir(folder)
    count = 0
    root = 'Feature_extract'
    for i in emosi:
        for j in range(2,int(len(dirs)/4)+2):
            df = pd.read_csv(folder+'/'+i+str(j)+'_filtered.csv')
            data1 = list(df.iloc[:,2])
            print(len(data1))
            #data2 = list(df.iloc[:,4])
            stdv1 = st.stdev(data1)
            rrt1 = st.mean(data1)
            md1 = st.median(data1)
            stdv.append(stdv1)
            rrt.append(rrt1)
            md.append(md1)
            # stdv2 = st.sdev(data2)
            # rrt2 = st.mean(data2)
            # md2 = st.median(data2)

        namafile = i+'_extracted.csv'
        #d_t = list(zip(stdv1,rrt1,md1))
        finaldirs = os.path.join(root,namafile)
        df1 = pd.DataFrame({'STDEV' : stdv,'AVG' : rrt,'MDN' : md})
        df1.to_csv(finaldirs,mode='w+')
        print(finaldirs)
        stdv.clear()
        rrt.clear()
        md.clear()
    print('Selesai !')

#extract_feature('Data_filter')
def create_model():
    model = keras.Sequential([
        keras.layers.SimpleRNN(3,input_shape=(1000,3)),
        keras.layers.BatchNormalization(),
        keras.layers.Dense(4,activation='softmax')
    ])
    optimizer = keras.optimizers.Adam(lr=0.01)
    model.compile(
        loss='categorical_crossentropy',
        optimizer=optimizer,
        metrics=['binary_accuracy']
    )
    model.summary()
    early_stopping = keras.callbacks.EarlyStopping(
        patience=10,
        min_delta=0.001,
        restore_best_weights=True,
    )
    return model



# history = model.fit(
#     train_X,
#     train_Y,
#     epochs=25,
#     validation_data=(val_X,val_Y),
#     callbacks=[early_stopping],
#     # verbose=0
#     )
