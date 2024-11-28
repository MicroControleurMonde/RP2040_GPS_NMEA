# TEST_NMEA_GSV.V1.py
# Created on 21 Aug 2024
# MicroPython code for Raspberry Pi Pico to retrieve and display NMEA sentences with enhanced GSV parsing

"""
Strucutre: $GPGSV,x,y,z,a,b,c,d,e,f,g,h,...*hh

$GPGSV: GSV message identifier (for GPS, ‘GPGSV’, for other GNSS systems, the prefixes change, e.g. GLGSV for GLONASS).
x: Total number of GSV messages required to transmit all the information (range from 1 to 3).
y: Current message number (range from 1 to 3).
z: Total number of satellites in view.
a: Satellite 1 ID (range from 1 to 32).
b: Satellite 1 elevation (range from 0 to 90 degrees).
c: Azimuth of satellite 1 (range 0 to 359 degrees).
d: Satellite 1 signal-to-noise ratio (SNR) (range 0 to 99 dBHz, or null if not tracked).
e: Satellite 2 ID (range 1 to 32).
f: Satellite 2 elevation (range 0 to 90 degrees).
g: Satellite 2 azimuth (range 0 to 359 degrees).
h: Satellite 2 signal-to-noise ratio (SNR) (range 0 to 99 dBHz, or null if not tracked).
    (And so on for the following satellites, up to a maximum of 4 satellites per GSV message).
*hh: Checksum for message integrity verification.
<CR><LF>: Frame termination (carriage return and line feed).

With satellite ID:
01 ~ 32 for GPS;
33 ~ 64 for SBAS (PRN minus 87);
65 ~ 96 for GLONASS (64 location numbers plus);
193 ~ 197 for QZSS;
01 ~ 37 for Beidou (BD PRN).
GPS and Beidou satellites are differentiated by the prefixes GP and BD.
Each GSV sentence comprises a maximum of 4 satellites. 
"""

from machine import UART
import utime

# Configure UART communication (using default pins TX=GPIO0, RX=GPIO1)
uart = UART(0, baudrate=9600, bits=8, parity=None, stop=1)

buffer = b""

def parse_gsv_sentence(sentence):
    """ Parse a GSV sentence and extract relevant information. """
    parts = sentence.split(b',')
    if len(parts) < 4:
        return  # Not enough data to parse
    
    try:
        # Extracting data from the GSV sentence
        total_msgs = int(parts[1])
        msg_num = int(parts[2])
        total_satellites = int(parts[3])
        
        print(f"Total satellites in view: {total_satellites}")
        
        # Process each satellite block (4 satellites per message)
        index = 4
        for _ in range(4):
            if index >= len(parts) - 1:
                break
            prn = int(parts[index])
            elevation = int(parts[index+1])
            azimuth = int(parts[index+2])
            snr = int(parts[index+3]) if parts[index+3] else "N/A"
            
            # Determine satellite type based on PRN range
            if 1 <= prn <= 32:
                sat_type = "GPS"
            elif 33 <= prn <= 64:
                sat_type = "SBAS"
            elif 65 <= prn <= 96:
                sat_type = "GLONASS"
            elif 193 <= prn <= 197:
                sat_type = "QZSS"
            elif 1 <= prn <= 37:
                sat_type = "Beidou"
            else:
                sat_type = "Unknown"
            
            print(f"Satellite PRN: {prn}, Type: {sat_type}, Elevation: {elevation}°, Azimuth: {azimuth}°, SNR: {snr} dBHz")
            
            # Move to the next satellite
            index += 4

    except ValueError as e:
        print("Value error while parsing GSV sentence:", e)

def process_nmea(data):
    """ Process and display NMEA sentences. """
    if data:
        try:
            decoded_data = data.decode('utf-8', 'ignore').strip()
            if decoded_data.startswith('$G') and not decoded_data.startswith('$GNTXT'):
                if decoded_data.startswith('$GPGSV') or decoded_data.startswith('$GLGSV'):
                    parse_gsv_sentence(data)
                else:
                    print("NMEA sentence:", decoded_data)
            else:
                # Optionally log or ignore non-NMEA or error messages
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
