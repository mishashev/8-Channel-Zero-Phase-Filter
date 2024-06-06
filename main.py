from ECF import Eight_Channel_Filter


def main():
    ECF = Eight_Channel_Filter()  # Create Eight Channel Filter Object
    data = ECF.load_file("NEUR0000.DT8")    # Load file and convert to volt
    df = ECF.convert_dataframe(data)    # Convert data to dataframe
    print(df)
    #data = ECF.zp_filter(data)      # Pass through Zero-Phase Filter
    print(max(data[0]),min(data[0]))
    print((max(data[0])-min(data[0]))/2)
    print((max(data[0])+min(data[0]))/2)
    ECF.show_ch(data, b_xlim=-0.005, t_xlim=0.03)  # Plot signals

    
if __name__ == "__main__":
    main()