import keras
import tensorflow as tf
import pandas as pd
import os
#['a','b','c','d']
idiot = []
maindirs ='Feature_extract'
dirs = os.listdir(maindirs)
emosi = ['kaget','marah','santai','senang']
for i in emosi:
    df = pd.read_csv(maindirs+'/'+i+'_extracted.csv')
    
    b=list(df.iloc[:,3])
    c=list(df.iloc[:,2])
    d=list(df.iloc[:,1])
    print(i)
    idiot.append(b)
    idiot.append(c)
    idiot.append(d)

a = tf.keras.utils.to_categorical([0, 1, 2, 3, 9], num_classes=15)
a = tf.constant(a, shape=[40, 40])
print(a)
