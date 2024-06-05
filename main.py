from pathlib import Path
import numpy as np
import pandas as pd
import scipy.signal as sp
import matplotlib.pyplot as plt


class Eight_Channel_Filter():    

    def load_file(file_name):
        """
        Loads a binary file, representing a 8 channel signals.
        Then converts the the signal measurements into voltage values.
        :param file_name: name of the binary file
        :type file_name: str
        :return: list of voltages over time in 8 channels
        :rtype: list of list
        """

        number_of_channels = 8
        voltage_resolution = 4.12e-7
        num_ADC_bits = 15

        # Get the file path
        script_dir = Path(__file__).resolve().parent
        file_path = script_dir / file_name

        # Construct an array from the binary file
        data = np.fromfile(file_path, dtype=np.uint16)

        # Divide the data to 8 arrays representing the signal channels
        data = np.reshape(data, (number_of_channels, -1), order='F')

        # Represent the signal values as voltage values.
        data = np.multiply(voltage_resolution,
                        (data - np.float_power(2, num_ADC_bits - 1)))
        
        return data
        

    def convert_dataframe(data):
        """
        Converts data to Pandas DataFrame. Each index represents a channel.
        :param data: data to be converted
        :type data: list
        :return: pandas dataframe
        :rtype: pandas dataframe
        """

        row_labels = ['Channel 1', 'Channel 2', 'Channel 3', 'Channel 4', 
                      'Channel 5', 'Channel 6', 'Channel 7', 'Channel 8']

        # Create a Panda Dataframe from the given data.
        df = pd.DataFrame(data, index=row_labels)

        return df


    def zp_filter(data):
        """
        Pass data channels through a Zero Phase Bandpass Filter.
        :param data: data to be filtered
        :type data: list
        :return: filtered data
        :rtype: list of lists
        """

        b = [1,0]
        a = [1,0]
        
        for i in range(8):
            data[i] = sp.filtfilt(b,a,data[i])
        
        return data
            


    def sig_plot(data, b_xlim=0, t_xlim=0.2):
        """
        Plots the channels Voltage[V] vs Time[s].
        :param data: data to be filtered
        :param b_xlim: plot bottom time limit to show in seconds
        :param t_xlim: plot top time limit to show in seconds
        :type data: list
        :type b_xlim: float
        :type t_xlim: float
        :type data: list
        """
        
        sample_freq = 4000   # Sampling frequency
        columns = 4    # Number of columns of plots
        rows = 2    # Number of rows of plots

        # Time lables
        time_axis = [sample / sample_freq 
                             for sample in range(len(data[0]))]
        # Plot all 8 channels
        fig, axs = plt.subplots(2,4)

        for row in range(rows):
            column = columns*row
            for list in range(column, columns+column):
                #plt.subplot(row,columns,(row,list+1))
                i_plot = axs[row,list-column]
                sig_length = str(time_axis[-1])+' seconds'
                i_plot.plot(time_axis, data[list], label=sig_length)
                i_plot.set_title("Channel" + str(list))
                i_plot.set_xlabel("Time [s]")
                i_plot.set_ylabel("Voltage [V]")
                i_plot.set_xlim(b_xlim,t_xlim)
                i_plot.grid()
                i_plot.legend(loc="upper left")
        plt.show()

def main():
    ECF = Eight_Channel_Filter  # Create Eight Channel Filter Object
    data = ECF.load_file("NEUR0000.DT8")    # Load file and convert to volt
    df = ECF.convert_dataframe(data)    # Convert data to dataframe
    data = ECF.zp_filter(data)      # Pass through Zero-Phase Filter

    # ECF.sig_plot(data)  # Plot signals

    

if __name__ == "__main__":
    main()