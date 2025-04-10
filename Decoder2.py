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

# Generate a proper Intel HEX file with 16 bytes per line.
def generate_hex_file(data_map, filename="output.hex", size=8192):
    with open(filename, "w") as hex_file:
        # Prepare data array with default values (0xFF for empty cells)
        eeprom_data = [0xFF] * size
        for addr, value in data_map.items():
            if addr < size:
                eeprom_data[addr] = value
        
        # Write data 16 bytes per line
        for addr in range(0, size, 16):
            chunk = eeprom_data[addr:addr+16]
            byte_count = len(chunk)
            address_high = (addr >> 8) & 0xFF
            address_low = addr & 0xFF
            record_type = 0x00
            checksum = byte_count + address_high + address_low + record_type + sum(chunk)
            checksum = ((~checksum + 1) & 0xFF)  # Two's complement
            data_str = ''.join(f'{b:02X}' for b in chunk)
            line = f":{byte_count:02X}{addr:04X}{record_type:02X}{data_str}{checksum:02X}\n"
            hex_file.write(line)

        # EOF Record
        hex_file.write(":00000001FF\n")

    print(f"HEX file '{filename}' generated successfully.")

def main():
    # Load the Excel file
    excel_file = "EEPROM-Video-Card.xlsx"  # Update with the actual file path
    df = pd.read_excel(excel_file)

    # Process data
    data_map = process_data(df)

    # Generate output files
    # generate_bin_file(data_map)
    generate_hex_file(data_map)

if __name__ == "__main__":
    main()