import keras
import pandas as pd
import os
#import numpy as np

model = keras.models.load_model('model_lstm2')
maindirs = 'Feature_extract'
dirs = os.listdir(maindirs)
df = pd.read_csv(maindirs+"/"+"tes_extracted.csv")
for i in range(1,10):
    temp = df.iloc[i]
    temp_list = temp.values.tolist()
    prediction = model.predict(temp_list)
    print(prediction)
