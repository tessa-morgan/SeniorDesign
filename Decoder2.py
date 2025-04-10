import pandas as pd
import numpy as np

def process_data(df):
    """
    Process the Excel dataframe to extract EEPROM address and data values.
    """
    data_map = {}

    for _, row in df.iterrows():
        try:
            # Extract the address (assuming it's in decimal format)
            address = int(row["Address"])
            
            # Extract EEPROM data (which is in hex format in the spreadsheet)
            eeprom_value = int(str(row["EEPROM"]), 16)  # Convert from hex string to integer
            
            # Store in dictionary
            data_map[address] = eeprom_value
        
        except ValueError as e:
            print(f"Skipping row due to error: {e}")

    return data_map

def generate_bin_file(data_map, filename="output.bin", size=256):
    """
    Generate a .BIN file for EEPROM programming.
    """
    bin_data = np.zeros(size, dtype=np.uint8)  # Initialize with zeroes
    for addr, value in data_map.items():
        if addr < size:  # Ensure we don't exceed EEPROM size
            bin_data[addr] = value

    bin_data.tofile(filename)
    print(f"Binary file '{filename}' generated successfully.")

def generate_hex_file(data_map, filename="output.hex", size=256):
    """
    Generate an Intel HEX file for EEPROM programming.
    """
    with open(filename, "w") as hex_file:
        for addr, value in data_map.items():
            if addr < size:
                record = f":01{addr:04X}00{value:02X}{(0x100 - (1 + (addr >> 8) + (addr & 0xFF) + value)) & 0xFF:02X}\n"
                hex_file.write(record)
        
        hex_file.write(":00000001FF\n")  # End of file record
    
    print(f"HEX file '{filename}' generated successfully.")

def main():
    # Load the Excel file
    excel_file = "EEPROM-Video-Card.xlsx"  # Update with the actual file path
    df = pd.read_excel(excel_file)

    # Process data
    data_map = process_data(df)

    # Generate output files
    generate_bin_file(data_map)
    generate_hex_file(data_map)

if __name__ == "__main__":
    main()