import numpy as np

"""
Before you can run the program, enter the following commands in the terminal:
(This must be done every time, in the directory with the file, was done because unable to install numpy on mac with brew)

source myenv/bin/activate

Then run with: python3 Decoder_BIN.py

Once done, run the command: deactivate

Only the first time in a new directory, run:
python3 -m venv myenv
python3 -m pip install numpy
"""


# Define your 7-segment common-cathode decoder values for inputs 0–F
# Input to EEPROM in order: DP, G, F, E, D, C, B, A
# Comments formatted: # DisplayOutput, BinaryEncoding, BitwiseInverse (for common-anode)
seven_seg_codes = [ 
    0x3F,  # 0, 0b00111111, 0xC0
    0x06,  # 1, 0b00000110, 0xF9
    0x5B,  # 2, 0b01011011, 0xA4
    0x4F,  # 3, 0b01001111, 0xB0
    0x66,  # 4, 0b01100110, 0x99
    0x6D,  # 5, 0b01101101, 0x92
    0x7D,  # 6, 0b01111101, 0x82
    0x07,  # 7, 0b00000111, 0xF8
    0x7F,  # 8, 0b01111111, 0x80
    0x6F,  # 9, 0b01101111, 0x90
    0x77,  # A, 0b01110111, 0x88
    0x7C,  # B, 0b01111100, 0x83
    0x39,  # C, 0b00111001, 0xC6
    0x5E,  # D, 0b01011110, 0xA1
    0x79,  # E, 0b01111001, 0x86
    0x71   # F, 0b01110001, 0x8E
] 

"""
This program will populate an array with the above 7-segment encodings 
as well as a second array with the bitwise inverse to be used for common-anode dispays.
For the lab, students only need to generate the common-cathode output 
BUT should also be able to explain how they would enode the common-anode decoder.
This is one way, and the easier option. Students can also define the encoding for common-anode
as done above.
"""
def generate_eeprom(size=512):
    # Initialize EEPROM data array
    eeprom_anode = np.zeros(size, dtype=np.uint8)
    eeprom_cathode = np.zeros(size, dtype=np.uint8)

    # Populate EEPROM data repeating every 16 addresses - from addr 000 to 0ff
    for addr in range(256):
        eeprom_anode[addr] = 0xFF ^ seven_seg_codes[addr % 16]
        eeprom_cathode[addr] = seven_seg_codes[addr % 16]

    # Populate EEPROM data in game mode - from addr 100 to 1ff
    count = 255
    for addr in range(256, size):
        eeprom_anode[addr] = count
        eeprom_cathode[addr] = 255 - count #cathode ends at 511 i.e. size - 1
        count -= 1

    write_bin_file("output_anode.bin", eeprom_anode)
    write_bin_file("output_cathode.bin", eeprom_cathode)

# Generates the BINARY output file
def write_bin_file(filename, eeprom_data):
    with open(filename, "wb") as f:
        f.write(bytes(eeprom_data))
    print(f"Binary file '{filename}' generated successfully.")

# Generate .bin files
generate_eeprom()

