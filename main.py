from ECF import Eight_Channel_Filter


def main():
    # Example code for testing
    ECF = Eight_Channel_Filter()  # Create Eight Channel Filter Object
    data = ECF.load_file("NEUR0000.DT8")    # Load file and convert to volt
    df = ECF.convert_dataframe(data)    # Convert data to dataframe
    print(df)
    data = ECF.zp_filter(data)      # Pass through Zero-Phase Filter
    ECF.show_ch(data)  # Plot channels


if __name__ == "__main__":
    main()