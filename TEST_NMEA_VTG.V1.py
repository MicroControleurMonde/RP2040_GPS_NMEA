# TEST_NMEA_VTG.V1.py
# Updated on 23 Aug 2024
# MicroPython code for Raspberry Pi Pico to retrieve and display only $GNVTG NMEA sentences with checksum validation
# VTG—Course Over Ground and Ground Speed
'''
The VTG NMEA sentence structure is as follows:

$--VTG,x.x,T,x.x,M,x.x,N,x.x,A,K*hh

Here's a breakdown of each field:
1) $ GPVTG or GNVTG: 	The message ID
2) x.x:		Track Made Good (True): The track made good in degrees (0–359.9), relative to true north.
3) T:		Fixed text "T" - This indicates that the track made good is relative to true north.
4) x.x:		Magnetic Track - This field represents the track made good in degrees relative to magnetic north.
5) M:		Reference - This indicates that the previous value is relative to magnetic north.
6) x.x: 	This field indicates the speed over ground in knots, which can have 0 to 3 decimal places.
7) N:		Units - Fixed text "N" indicates that speed over ground is in knots
8) x.x:		Speed over ground in kilometers/hour (0–3 decimal places)
9) K:		Units - Fixed text "K" indicates that the speed over ground is in kilometers per hour.
10) Mode:	Fixed text "A"=Autonomous, "D"=DGPS (Differential), "E"=Estimated (dead reckoning), "N"= not valid
11) *hh:	Checksum data, always begins with *

Field marked as '10)' apply only to NMEA version 2.3 (and later) in this NMEA message description.
'''
from machine import UART
import utime

# Configure UART communication (using default pins TX=GPIO0, RX=GPIO1)
uart = UART(0, baudrate=9600, bits=8, parity=None, stop=1)

buffer = b""
vtg_counter = 0  # Initialize VTG sentence counter

# ANSI escape sequences for text formatting
BOLD_ON = "\033[1m"
BOLD_OFF = "\033[0m"

def calculate_checksum(sentence):
    """Calculate the checksum for an NMEA sentence."""
    checksum = 0
    for char in sentence:
        checksum ^= ord(char)
    return '{:02X}'.format(checksum)

def process_vtg(data):
    """Process and display VTG NMEA sentences."""
    global vtg_counter
    if data:
        try:
            decoded_data = data.decode('utf-8', 'ignore').strip()
            # Check if it's a VTG sentence
            if decoded_data.startswith('$GPVTG') or decoded_data.startswith('$GNVTG'):
                vtg_counter += 1  # Increment counter for each VTG sentence
                
                # Remove the checksum part if it exists
                if '*' in decoded_data:
                    sentence, checksum = decoded_data.split('*', 1)
                else:
                    sentence = decoded_data
                    checksum = 'None'

                # Check checksum if provided
                if checksum != 'None':
                    expected_checksum = calculate_checksum(sentence[1:])
                    if checksum == expected_checksum:
                        checksum_status = f"Valid"
                    else:
                        checksum_status = f"{BOLD_ON}Invalid{BOLD_OFF}"
                else:
                    checksum_status = f"{BOLD_ON}No Checksum{BOLD_OFF}"
                
                fields = sentence.split(',')
                
                # Add checksum to fields if it's present
                if checksum != 'None':
                    fields.append(checksum)
                
                # Display the full VTG sentence
                print(f"\nVTG Sentence #{vtg_counter}:")
                print(f"DEBUG: Raw sentence: {decoded_data}")  # Full sentence
                print(f"DEBUG: Parts: {fields}")  # Display parts of the sentence with checksum
                
                # Ensure the message has at least 10 fields (according to the specification)
                if len(fields) >= 10:
                    track_true = fields[1].strip() if fields[1] else f'{BOLD_ON}Missing Data{BOLD_OFF}'
                    track_magnetic = fields[3].strip() if fields[3] else f'{BOLD_ON}Missing Data{BOLD_OFF}'
                    speed_knots = fields[5].strip() if fields[5] else f'{BOLD_ON}Missing Data{BOLD_OFF}'
                    speed_kph = fields[7].strip() if fields[7] else f'{BOLD_ON}Missing Data{BOLD_OFF}'
                    mode = fields[9].strip() if len(fields) > 9 else f'{BOLD_ON}Missing Data{BOLD_OFF}'

                    print(f"Track Made Good (True)(°): {track_true}")
                    print(f"Magnetic Track(°): {track_magnetic}")
                    print(f"Speed Over Ground (Knots): {speed_knots}")
                    print(f"Speed Over Ground (km/h): {speed_kph}")
                    
                    # Display Mode with proper interpretation
                    if mode == 'A':
                        mode_status = "Autonomous"
                    elif mode == 'D':
                        mode_status = "DGPS"
                    elif mode == 'E':
                        mode_status = "Estimated (Dead Reckoning)"
                    elif mode == 'N':
                        mode_status = f"{BOLD_ON}Not Valid{BOLD_OFF}"
                    else:
                        mode_status = f"{BOLD_ON}Unknown Mode{BOLD_OFF}"
                    
                    print(f"Acquisition mode: {mode_status}")
                    print(f"Checksum Status: {checksum_status}")
                else:
                    print("Incomplete VTG data")
            else:
                # Optionally log or ignore non-VTG sentences
                pass
        except UnicodeError as e:
            print("Unicode error:", e)

while True:
    if uart.any():
        buffer += uart.read()  # Append incoming data to buffer
        while b'\n' in buffer:
            line, buffer = buffer.split(b'\n', 1)  # Split lines
            process_vtg(line)
    
    utime.sleep_ms(100)  # Small delay to avoid tight loop

