# TEST_NMEA_GGA.v1.py
# Created on 26 Aug 2024
# MicroPython code for Raspberry Pi Pico to retrieve and display NMEA GGA sentences
"""
Reads NMEA GGA sentences from a UART serial interface, processes them to extract relevant information
and displays the parsed data in a readable format. 
##Features:
- Configures UART communication with default pins TX=GPIO0 and RX=GPIO1.
- Reads and buffers incoming NMEA sentences.
- Validates and calculates checksums to ensure data integrity.
- Extracts and formats key components from GGA sentences including UTC time, fix quality, number of satellites, and HDOP.
- Converts UTC time to local time (GMT+3).
- Prints the extracted information with a unique identifier for each sentence.
##Functions:
- format_nil(value): Formats empty values as 'Nil'.
- calculate_checksum(sentence): Computes the checksum for an NMEA sentence.
- get_fix_quality_description(quality_code): Provides a description for the GPS fix quality based on the quality code.
- format_utc_time(utc_time): Converts UTC time from hhmmss.ss format to hh:mm:ss format.
- convert_utc_to_local(utc_time, offset_hours): Converts UTC time to local time using a specified offset.
- process_nmea(data): Processes NMEA sentences, validates checksums, and displays relevant data.
##Main Loop:
- Continuously reads data from the UART interface.
- Processes and prints each GGA sentence as it is received, ensuring only valid and complete sentences are handled.
"""
from machine import UART
import utime

# Configure UART communication (using default pins TX=GPIO0, RX=GPIO1)
uart = UART(0, baudrate=9600, bits=8, parity=None, stop=1)

buffer = b""
sentence_count = 1  # Initialize the sentence count

def format_nil(value):
    """ Format 'Nil' for empty values. """
    return value if value else 'Nil'

def calculate_checksum(sentence):
    """ Calculate checksum for an NMEA sentence. """
    checksum = 0
    for char in sentence:
        checksum ^= ord(char)
    return f"{checksum:02X}"

def get_fix_quality_description(quality_code):
    """ Return description for GPS fix quality based on the quality code. """
    fix_quality = {
        '0': "No fix",
        '1': "GPS fix autonomous (no correction data used)",
        '2': "Differential GPS fix (Using local DGPS base station or correction services WAAS or EGNOS)",
    }
    return fix_quality.get(quality_code, "Unknown quality code")

def format_utc_time(utc_time):
    """ Format UTC time from hhmmss.ss to hh:mm:ss format. """
    return f"{utc_time[0:2]}:{utc_time[2:4]}:{utc_time[4:6]}" if len(utc_time) >= 6 else 'Unknown'

def convert_utc_to_local(utc_time, offset_hours):
    """ Convert UTC time to local time based on the provided offset. """
    if len(utc_time) >= 6:
        utc_hours, utc_minutes, utc_seconds = int(utc_time[0:2]), int(utc_time[2:4]), int(utc_time[4:6])
        local_hours = (utc_hours + offset_hours) % 24
        return f"{local_hours:02}:{utc_minutes:02}:{utc_seconds:02}"
    return 'Unknown'

def process_nmea(data):
    """ Process and display specific NMEA sentences with replaced prefixes and a count. """
    global sentence_count
    if data:
        try:
            decoded_data = data.decode('utf-8', 'ignore').strip()

            # Check if the sentence is of the type $--GGA
            if decoded_data.startswith('$') and len(decoded_data) >= 6:
                try:
                    if '*' in decoded_data:
                        sentence, provided_checksum = decoded_data.split('*', 1)
                        provided_checksum = provided_checksum.upper()
                    else:
                        sentence = decoded_data
                        provided_checksum = ''
                    
                    calculated_checksum = calculate_checksum(sentence[1:])  # Exclude the initial $
                    checksum_status = "Valid" if provided_checksum == calculated_checksum else f"Invalid (Expected {calculated_checksum})"
                except ValueError:
                    print("Error splitting checksum.")
                    return

                prefix = decoded_data[1:3]  # Extract prefix (GP, GL, BD, etc.)
                if decoded_data[3:6] == 'GGA':
                    prefix_map = {
                        'GP': 'GPS',
                        'GL': 'GLONASS',
                        'BD': 'BeiDou',
                        'GN': 'GNSS'
                    }
                    identifier = prefix_map.get(prefix, 'Unknown')

                    # Split the GGA sentence into parts
                    parts = sentence[6:].split(',')

                    # Ensure there are enough parts
                    parts.extend([''] * (15 - len(parts)))

                    # Replace empty strings with 'Nil'
                    parts = [format_nil(part) for part in parts]
                    
                    # Extract Quality, Satellites in use, HDOP, and UTC Time
                    quality = parts[6]
                    satellites_in_use = parts[7]
                    hdop = parts[8]
                    utc_time = parts[1]  # UTC time is the second field in GGA sentence

                    # Get description for the quality of fix
                    fix_description = get_fix_quality_description(quality)

                    # Format UTC Time and convert to GMT+3
                    formatted_utc_time = format_utc_time(utc_time)
                    formatted_local_time = convert_utc_to_local(utc_time, 3)  # GMT+3

                    # Print only the necessary information with message ID
                    print(f"\nID: {identifier} #{sentence_count}")
                    print(f"UTC: {formatted_utc_time} | GMT+3: {formatted_local_time}")
                    print(f"Quality = {quality} : {fix_description}")
                    print(f"Satellites in use: {satellites_in_use}")
                    print(f"HDOP: {hdop}")
                    sentence_count += 1
        except UnicodeError as e:
            print(f"Unicode error: {e}")

# Main loop
while True:
    if uart.any():
        buffer += uart.read()  # Append incoming data to buffer
        # Process only lines that contain NMEA sentences
        while b'\n' in buffer:
            line, buffer = buffer.split(b'\n', 1)  # Split lines
            # Only process lines that are GGA sentences
            process_nmea(line)   
    utime.sleep_ms(100)  # Small delay to avoid tight loop


