import numpy as np

"""
Before you can run the program, enter the following commands in the terminal:
(This must be done every time, in the directory with the file)

source myenv/bin/activate
python3 -m pip install numpy

Then run with: python3 Decoder3.py

Once done, run the command: deactivate

Only the first time in a new directory, run:
python3 -m venv myenv
"""


# Define your 7-segment decoder values for inputs 0–F
# Input to EEPROM in order: DP, G, F, E, D, C, B, A
seven_seg_values = [ 
    0x3F,  # 0, 0b00111111
    0x06,  # 1, 0b00000110
    0x5B,  # 2, 0b01011011
    0x4F,  # 3, 0b01001111
    0x66,  # 4, 0b01100110
    0x6D,  # 5, 0b01101101
    0x7D,  # 6, 0b01111101
    0x07,  # 7, 0b00000111
    0x7F,  # 8, 0b01111111
    0x6F,  # 9, 0b01101111
    0x77,  # A, 0b01110111
    0x7C,  # B, 0b01111100
    0x39,  # C, 0b00111001
    0x5E,  # D, 0b01011110
    0x79,  # E, 0b01111001
    0x71   # F, 0b01110001
]

def generate_eeprom_hex(filename="output.hex", size=512):
    # Initialize EEPROM data array
    eeprom_data = np.zeros(size, dtype=np.uint8)

    # Populate EEPROM data repeating every 16 addresses - from addr 000 to 0ff
    for addr in range(256):
        eeprom_data[addr] = seven_seg_values[addr % 16]

    # Populate EEPROM data in game mode - from addr 100 to 1ff
    count = 0;
    for addr in range(256, size):
        eeprom_data[addr] = count
        count += 1

    # Write data as standard Intel HEX (16 bytes per line)
    with open(filename, "w") as hex_file:
        for addr in range(0, size, 16):
            chunk = eeprom_data[addr:addr+16]
            byte_count = len(chunk)
            address_high = (addr >> 8) & 0xFF
            address_low = addr & 0xFF
            record_type = 0x00
            checksum = byte_count + address_high + address_low + record_type + sum(int(b) for b in chunk)
            checksum = ((~checksum + 1) & 0xFF)  # Two's complement checksum
            data_str = ''.join(f'{b:02X}' for b in chunk)
            line = f":{byte_count:02X}{addr:04X}{record_type:02X}{data_str}{checksum:02X}\n"
            hex_file.write(line)

        # EOF record
        hex_file.write(":00000001FF\n")

    print(f"HEX file '{filename}' generated successfully.")

# Generate HEX file
generate_eeprom_hex()
