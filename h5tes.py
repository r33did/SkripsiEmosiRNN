import h5py
import numpy as np
import keras
import pandas as pd
from sklearn.metrics import confusion_matrix

reconstructed_model = keras.models.load_model('my_model')
reconstructed_model.summary()
weights = list(reconstructed_model.get_weights())
df = pd.DataFrame(weights)
df.to_csv('berat.csv')
print("Selesai")
