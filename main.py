import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Eight_Channel_Filter():

    def __init__(self):
        pass
    
    def load_file(self, file_path):
        number_of_channels = 8
        voltage_resolution = 4.12e-7
        num_ADC_bits = 15

        data = np.fromfile(file_path, dtype=np.uint16)
        data = np.reshape(data, (number_of_channels, -1), order='F')
        data = np.multiply(voltage_resolution,
                        (data - np.float_power(2, num_ADC_bits - 1)))