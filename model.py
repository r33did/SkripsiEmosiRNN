import keras
import os
import numpy as np
import pandas as pd
from keras.utils import to_categorical
from sklearn import metrics
from sklearn.metrics import confusion_matrix

data = []
labels = []

def extract_data_test(folder='data_test'):
    dirs = os.listdir(folder)
    counter = 0
    # for dr in dirs:
    #     for file in os.listdir(folder+'/'+dr):
    #         counter+=1


def extract_feature(folder='data_test'):
    dirs = os.listdir(folder)
    count = 0
    df = pd.read_csv()