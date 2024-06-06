# 8-Channel-Zero-Phase-Filter

This project represents an 8 Channel Zero Phase Filtered Signal.

## Details:
A binary file contains:
	- 8 parallel channels.
	- Each signal is sampled at a 4000[Hz] rate.
	- The samples are arranged in ascending order.

The conversion of the binary file to voltage values:
	data = np.fromfile(file_path, dtype=np.uint16)
	data = np.reshape(data, (number_of_channels, -1), order='F')
	data = np.multiply(voltage_resolution,
	                   (data - np.float_power(2, num_ADC_bits - 1)))

Number of ADC bits: 15, Resolution: 4.12e-7 [V]

Build a python Class, that includes the following methods:
	- Loading the binary files and converting to voltage values.
	- Converting the data to Pandas Dataframe.
	- Filter the signals (data) with a Zero Phase Bandpass Filter for each channel.
	- Plot the data using matplotlib.


## REQUIREMENTS:
1) Packages:
	-numpy
	-pandas
	-scipy
	-matplotlib
