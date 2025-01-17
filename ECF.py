from pathlib import Path
import numpy as np
import pandas as pd
import scipy.signal as sp
import matplotlib.pyplot as plt


class Eight_Channel_Filter:

    # Measurement settings
    sample_freq = 4000
    number_of_channels = 8  
    voltage_resolution = 4.12e-4 # mV
    num_ADC_bits = 15

    def __init__(self):
        return


    def load_file(self, file_name):
        """
        Loads a binary file, representing a 8 channel signals.
        Then converts the the signal measurements into voltage values.
        :param file_name: name of the binary file
        :type file_name: str
        :return: list of voltages over time in 8 channels
        :rtype: list of list
        """

        # Get the file path
        script_dir = Path(__file__).resolve().parent
        file_path = script_dir / file_name

        # Construct an array from the binary file
        data = np.fromfile(file_path, dtype=np.uint16)

        # Divide the data to 8 arrays representing the signal channels
        data = np.reshape(data, (self.number_of_channels, -1), order='F')

        # Represent the signal values as voltage values.
        data = np.multiply(self.voltage_resolution,
                        (data - np.float_power(2, self.num_ADC_bits - 1)))
        
        return data
        

    def convert_dataframe(self, data):
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


    def zp_filter(self, data):
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


    def plot_ch(self,data,sub,time_axis,b_xlim,t_xlim,ch):
        """
        Plot a single channel.
        :param data: data to be filtered
        :param sub: desired subplot to present the channel
        :param time_axis: array of time axis values
        :param b_xlim: plot bottom time limit to show in seconds
        :param t_xlim: plot top time limit to show in seconds
        :param ch: channel to plot
        :type data: list
        :type sub: matplotlib.axes._axes.Axes
        :type time_axis: array
        :type b_xlim: float
        :type t_xlim: float
        :type ch: int
        :return: None
        """
        
        colors = ['b','g','r','y','m','c','orange','purple']
        title_weight = 'demibold'
        label_weight = 'semibold'

        sub.plot(time_axis, data[ch], color=colors[ch])
        sub.set_title("Channel " + str(ch), weight=title_weight)
        sub.set_xlabel("Time [s]", weight=label_weight)
        sub.set_ylabel("Voltage [mV]", weight=label_weight)
        sub.set_xlim(b_xlim,t_xlim)
        sub.grid()


    def show_ch(self, data, channel=-1, b_xlim=0, t_xlim=0.05):
        """
        Presents plot of the channels Voltage[V] vs Time[s].
        :param data: data to be filtered
        :param channel: channel to present (-1 for all channels)
        :param b_xlim: plot bottom time limit to show in seconds
        :param t_xlim: plot top time limit to show in seconds
        :type data: list
        :type channel: int
        :type b_xlim: float
        :type t_xlim: float
        :return: None
        """
        
        # Time lables
        time_axis = [sample / self.sample_freq 
                        for sample in range(len(data[0]))]
        columns = 4    # Number of columns of plots
        rows = 2    # Number of rows of plots

        # String texts
        fig_title = 'Zero Phase Filtered Channel\nVoltage[mV] vs Time[s]'
        sig_time = 'Total measured time: '+str(time_axis[-1])+' seconds'
        
        # Plot all 8 channels 
        if channel == -1:
            fig, axs = plt.subplots(rows, columns)
            for row in range(rows):
                column = columns*row
                for ch in range(column, columns+column):
                    sub = axs[row,ch-column]
                    self.plot_ch(data,sub,time_axis,b_xlim,t_xlim,ch)
        # Plot specific channel
        else:
            fig, axs = plt.subplots(1,1)
            self.plot_ch(data,axs,time_axis,b_xlim,t_xlim,
                         channel)
        
        # Figure settings
        fig.set_size_inches(13,9.5)
        fig.subplots_adjust(left=0.07, right=0.98, bottom=0.05,
                             wspace=0.6, hspace=0.3)
        fig.suptitle(fig_title, size='xx-large', weight='heavy')
        fig.legend([sig_time])

        plt.show()  # Represent whole figure