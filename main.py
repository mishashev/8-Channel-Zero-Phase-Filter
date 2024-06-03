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

        # Construct an array from the binary file
        data = np.fromfile(file_path, dtype=np.uint16)

        # Divide the data to 8 arrays representing the signal channels
        data = np.reshape(data, (number_of_channels, -1), order='F')

        # Represent the signal values as voltage values.
        data = np.multiply(voltage_resolution,
                        (data - np.float_power(2, num_ADC_bits - 1)))
        
        return data
        
    def convert_dataframe(self, data):
        row_labels = ['Channel 1', 'Channel 2', 'Channel 3', 'Channel 4', 
                      'Channel 5', 'Channel 6', 'Channel 7', 'Channel 8']

        # Create a Panda Dataframe from the given data.
        df = pd.DataFrame(data, index=row_labels)

        # Display the DataFrame
        # print(df)

        return df

