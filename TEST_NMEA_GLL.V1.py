# TEST_NMEA_GLL.V1.py
# Updated on 23 Aug 2024
# MicroPython code for Raspberry Pi Pico to retrieve and display only GLL NMEA sentences with checksum validation
# GLL—Geographic Position - Latitude/Longitude
'''
The GLL NMEA sentence structure is as follows:

$--GLL,llll.lll,a,yyyyy.yyy,b,hhmmss.sss,A,a*hh<CR><LF>

Here's a breakdown of each field:
1 - Message ID:		$GPGLL (GPS),$GLGLL (GLONASS), $GAGLL (Galileo), $GBGLL (BeiDou) or $GNGLL (multiple) - protocol header
2 - llll.lll: 		Latitude - Latitude in ddmm.mmmm format. Leading zeros are inserted.
3 - a:			    Direction indicator to determine the latitude ('N' for the North, 'S' for the South)
4 - yyyyy.yyy:		Longitude - Longitude in dddmm.mmmm format. Leading zeros are inserted.
5 - b:			    Direction indicator for longitude ('E' for East, 'W' for West)
6 - hhmmss.sssP		UTC Time - UTC of position in hhmmss.sss format, (000000.000 ~ 235959.999)
7 - A:			    Status - 'A'= data valid, 'V'= Data not valid
8 - a:			    Mode - Optional, indicates the positioning source, A=Autonomous, D=DGPS, E=DR (Only present in NMEA v3.00)
9 - *hh:		    Checksum
10 - <CR> <LF>:		End of message termination
'''
from machine import UART
import utime

# Configure UART communication (using default pins TX=GPIO0, RX=GPIO1)
uart = UART(0, baudrate=9600, bits=8, parity=None, stop=1)

buffer = b""
counter = 0  # Initialize a counter for GLL sentences

def format_utc_time(utc_time):
    """ Convert UTC time from HHMMSS.SS to HH:MM:SS format. """
    # Ignore the decimal places after the dot, if present
    utc_time = utc_time.split('.')[0]
    if len(utc_time) == 6 and utc_time.isdigit():
        return f"{utc_time[:2]}:{utc_time[2:4]}:{utc_time[4:6]}"
    return 'Invalid Time'


def get_status_description(status):
    """ Return a description of the status. """
    if status == 'A':
        return 'Valid'
    elif status == 'V':
        return 'Not Valid'
    else:
        return 'Unknown'

def process_gll_sentence(decoded_data):
    """ Decode and display GLL NMEA sentence fields with quotes around each field. """
    fields = decoded_data.split(',')
    
    # Extract fields with default values if missing, and add quotes around them
    message_id = f"'{fields[0]}'" if len(fields) > 0 else "' '"
    latitude = f"'{fields[1]}'" if len(fields) > 1 else "' '"
    lat_dir = f"'{fields[2]}'" if len(fields) > 2 else "' '"
    longitude = f"'{fields[3]}'" if len(fields) > 3 else "' '"
    lon_dir = f"'{fields[4]}'" if len(fields) > 4 else "' '"
    utc_time = f"'{fields[5]}'" if len(fields) > 5 else "' '"
    status = f"'{fields[6]}'" if len(fields) > 6 else "' '"
    mode_and_checksum = fields[7].split('*') if len(fields) > 7 else [' ', ' ']
    mode = f"'{mode_and_checksum[0]}'"
    checksum = f"'{mode_and_checksum[1]}'" if len(mode_and_checksum) > 1 else "' '"
    
    # Display the decoded fields with quotes and checksum
    print(f"DEBUG: Parts [ID:{message_id},{latitude},{lat_dir},{longitude},{lon_dir},{utc_time},{status},{mode},{checksum}]")
    
    # Display Latitude or 'Missing Data' in bold
    if fields[1]:
        print(f"Latitude: {fields[1]}")
    else:
        bold_start = '\033[1m'
        bold_end = '\033[0m'
        print(f"Latitude: {bold_start}Missing Data{bold_end}")
    
    # Display Direction Indicator or 'Missing Data' in bold
    if fields[2]:
        if fields[2] == 'N':
            direction = 'North'
        elif fields[2] == 'S':
            direction = 'South'
        else:
            direction = 'Unknown'
        print(f"Latitude Indicator: {direction}")
    else:
        print(f"Latitude Indicator: {bold_start}Missing Data{bold_end}")
        
    # Display Longitude or 'Missing Data' in bold
    if fields[3]:
        print(f"Longitude: {fields[3]}")
    else:
        print(f"Longitude: {bold_start}Missing Data{bold_end}")
        
        # Display Direction Indicator for Longitude or 'Missing Data' in bold
    if fields[4]:
        if fields[4] == 'E':
            direction = 'East'
        elif fields[4] == 'W':
            direction = 'West'
        else:
            direction = 'Unknown'
        print(f"Longitude Indicator: {direction}")
    else:
        print(f"Longitude Indicator: {bold_start}Missing Data{bold_end}")
    
    # Display UTC Time in HH:MM:SS format or 'Missing Data'
    if fields[5]:
        formatted_time = format_utc_time(fields[5])
        print(f"UTC Time: {formatted_time}")
    else:
        print(f"UTC Time: {bold_start}Missing Data{bold_end}")
    
    # Display Status
    if fields[6]:
        status_description = get_status_description(fields[6])
        print(f"Status: {bold_start}{status_description}{bold_end}")
    else:
        print(f"Status: {bold_start}Missing Data{bold_end}")
    
    # Display Mode with special handling for 'N'
    if fields[7]:
        mode_description = fields[7].split('*')[0]
        if mode_description == 'N':
            mode_description = f"{bold_start}Not Valid{bold_end}"
        print(f"Mode: {mode_description}")
    else:
        print(f"Mode: {bold_start}Missing Data{bold_end}")
    
    # Display Checksum
    if len(mode_and_checksum) > 1:
        print(f"Checksum: {mode_and_checksum[1]}")
    else:
        print(f"Checksum: {bold_start}Missing Data{bold_end}")


def process_nmea(data):
    """ Process and decode GLL NMEA sentences for various constellations. """
    global counter
    if data:
        try:
            decoded_data = data.decode('utf-8', 'ignore').strip()
            # Check for GLL sentences for GPS, GLONASS, Galileo, BeiDou, and multi-constellation
            if any(decoded_data.startswith(prefix) for prefix in ('$GPGLL', '$GLGLL', '$GAGLL', '$GBGLL', '$GNGLL')):
                counter += 1
                print(f"\nDEBUG: raw sentence {counter}: {decoded_data}")
                process_gll_sentence(decoded_data)  # Decode and display fields with quotes and checksum
            else:
                # Optionally log or ignore non-GLL NMEA sentences
                pass
        except UnicodeError as e:
            print("Unicode error:", e)

while True:
    if uart.any():
        buffer += uart.read()  # Append incoming data to buffer
        while b'\n' in buffer:
            line, buffer = buffer.split(b'\n', 1)  # Split lines
            process_nmea(line)
    
    utime.sleep_ms(100)  # Small delay to avoid tight loop
