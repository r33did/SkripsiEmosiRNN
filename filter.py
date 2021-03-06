import pandas as pd
from scipy import signal

def lowpass_filter(sinyal,fcl):
    sampleRate = int(input('Masukkan freq sample rate (Hz) = ')
    wnl = fcl/(sampleRate)