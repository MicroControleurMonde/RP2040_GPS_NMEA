# TEST_NMEA_GSA.V1.py
# Created on 21 Aug 2024
# MicroPython code for Raspberry Pi Pico to retrieve and display NMEA GSA sentences
# buffer has been added for better processing
'''
GSA GPS receiver operating mode, satellites used in the position solution, and DOP values
Format:
$--GSA,a,x,xx,xx,xx,xx,xx,xx,xx,xx,xx,xx,xx,xx,u.u,v.v,z.z*hh<CR><LF>

1. $--GSA:	Message ID - GSA protocol header. The "--" prefix is replaced by specific identifiers, such as GP for GPS, GL for GLONASS, BD for BeiDou, etc.	
2. a:		Mode - Mode 'M'= Manual, forced to operate in 2D or 3D mode,
                        'A'= Automatic, allowed to automatically switch 2D/3D.
3. x:		Mode - Fix type 1 = Fix not available  (no position calculated) ,
                            2 = 2D Fix (position calculated with less than 4 satellites), 
                            3 = 3D Fix (position calculated with 4 or more satellites)
4. xx’s:	Satellite ID - GPS satellite IDs range from 01 to 32; 
            SBAS (Satellite Boosting System) satellites have PRNs (pseudo-random noise) ranging from 120 to 158. 
            Here, the given range (33-64) corresponds to PRN minus 87.; 
            For GLONASS, IDs range from 65 to 96 (adding 64 to slot numbers); 
            QZSS (Japanese Quasi-Zenith Satellite System) satellites are identified by IDs 193 to 197; 
            BeiDou satellites use the range 01 to 37, but in some configurations they may have BD prefixes to differentiate them; 
            GPS and Beidou satellites are differentiated by the GP and BD prefix; 				
            Maximally 12 satellites are included in each GSA sentence.
5. u.u:		PDOP - Position dilution of precision (00.0 to 99.9).
6. v.v:		HDOP - Horizontal dilution of precision (00.0 to 99.9).
7. z.z:		VDOP - Vertical dilution of precision (00.0 to 99.9).
8. hh: 		checksum.
9. <CR><LF>: 	End of message.
'''
from machine import UART
import utime

# Configure UART communication (using default pins TX=GPIO0, RX=GPIO1)
uart = UART(0, baudrate=9600, bits=8, parity=None, stop=1)

buffer = b""
counter = 1  # Initialize the sentence counter

def get_satellite_type(satellite_id, msg_id):
    """Return the type of satellite based on the ID and message ID."""
    try:
        satellite_id = int(satellite_id)
        if msg_id.startswith('$GPGSA'):
            if 1 <= satellite_id <= 32:
                return "GPS"
            elif 120 <= satellite_id <= 158:
                return "SBAS"
            elif 193 <= satellite_id <= 197:
                return "QZSS"
            else:
                return "Unknown"
        elif msg_id.startswith('$GLGSA'):
            if 65 <= satellite_id <= 96:
                return "GLONASS"
            else:
                return "Unknown"
        elif msg_id.startswith('$BDGSA'):
            if 1 <= satellite_id <= 37:
                return "BeiDou"
            else:
                return "Unknown"
        elif msg_id.startswith('$GNGSA'):
            if 1 <= satellite_id <= 32:
                return "GPS"
            elif 65 <= satellite_id <= 96:
                return "GLONASS"
            elif 1 <= satellite_id <= 37:
                return "BeiDou"
            elif 193 <= satellite_id <= 197:
                return "QZSS"
            else:
                return "Unknown"
        else:
            return "Unknown"
    except ValueError:
        return "Invalid ID"

def get_mode_description(mode):
    """Return a description based on the mode value."""
    if mode == 'M':
        return "Manual"
    elif mode == 'A':
        return "Automatic"
    # "Automatic (allowed to automatically switch 2D/3D)" means that the GPS receiver is in automatic mode
    # and can switch between 2D (two-dimensional) and 3D (three-dimensional) modes depending on the quality of the available data.
    elif mode == '3':
        return "3D Fix"

    else:
        return "Missing data"

def calculate_checksum(sentence):
    """Calculate the NMEA checksum."""
    checksum = 0
    for char in sentence:
        checksum ^= ord(char)
    return '{:02X}'.format(checksum)

def process_nmea(data):
    """Process and display specific NMEA sentences."""
    global counter
    if data:
        try:
            decoded_data = data.decode('utf-8', 'ignore').strip()
            if decoded_data.startswith('$GPGSA') or decoded_data.startswith('$GLGSA') or decoded_data.startswith('$BDGSA') or decoded_data.startswith('$GNGSA'):
                print("\nDEBUG Raw sentence # {}: {}".format(counter, decoded_data))
                parts = decoded_data.split(',')
                if len(parts) >= 8:  # Ensure there are enough parts for processing
                    msg_id = parts[0]
                    mode = parts[1]
                    fix_type = parts[2]
                    satellite_ids = [part if part else 'nil' for part in parts[3:15]]
                    pdop = parts[15] if len(parts) > 15 and parts[15] else 'Missing data'
                    hdop = parts[16] if len(parts) > 16 and parts[16] else 'Missing data'
                    vdop_checksum = parts[17].split('*')
                    vdop = vdop_checksum[0] if len(vdop_checksum) > 0 and vdop_checksum[0] else 'Missing data'
                    checksum_provided = vdop_checksum[1] if len(vdop_checksum) > 1 else 'nil'
                    
                    # Calculate the checksum
                    checksum_calculated = calculate_checksum(decoded_data[1:decoded_data.find('*')])
                    
                    # Determine satellite type for each ID
                    satellite_types = [get_satellite_type(sid, msg_id) if sid != 'nil' else 'nil' for sid in satellite_ids]
                    
                    # Determine mode description
                    mode_description = get_mode_description(mode)
                    
                    # Determine fix type description
                    fix_type_description = {
                        '1': 'Fix not available (no calcul)',
                        # No calculation of position. Not enough satellite data
                        '2': '2D Fix',
                        # 2D Fix: The GPS receiver calculates position using latitude and longitude, but not altitude.
                        # This mode is generally used when the receiver has a limited view of the satellites,
                        # and usually requires at least 3 satellites to obtain a position.
                        '3': '3D Fix'
                        # The GPS receiver calculates position using latitude, longitude and altitude.
                        #This mode is more precise and is used when the receiver has a clearer view of the satellites,
                        #requiring at least 4 satellites to obtain an accurate 3-dimensional position.
                        
                    }.get(fix_type, 'Missing data')
                    
                    # Print sentence details
                    print("DEBUG Parts [ID: '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}']".format(
                        msg_id, mode, fix_type, ', '.join(satellite_ids), pdop, hdop, vdop, checksum_provided))
                    print("Mode: {} - {}".format(mode, mode_description))
                    print("Fix Type: {}".format(fix_type_description))

                    if any(sid != 'nil' for sid in satellite_ids):
                        print("Satellite Types: {}".format(
                            ', '.join('{}={}'.format(sid, satellite_types[i]) for i, sid in enumerate(satellite_ids) if sid != 'nil')))
                    else:
                        print("Satellite Types: No Satellite Data")
                    
                    print("PDOP: {}".format(pdop))
                    print("HDOP: {}".format(hdop))
                    print("VDOP: {}".format(vdop))
                    
                    # Check the checksum validity
                    if checksum_provided.upper() == checksum_calculated:
                        print("Checksum: {} - Valid".format(checksum_provided))
                    else:
                        print("Checksum: {} - Invalid".format(checksum_provided))
                    
                    # Increment the counter after processing each GSA sentence
                    counter += 1
                else:
                    print("Parts: Insufficient data fields.")
            else:
                # Ignore all other sentences
                pass
        except Exception as e:
            print("Error processing NMEA data: {}".format(e))

while True:
    if uart.any():
        buffer += uart.read()  # Append incoming data to buffer
        while b'\n' in buffer:
            line, buffer = buffer.split(b'\n', 1)  # Split lines
            process_nmea(line)
    
    utime.sleep_ms(100)  # Small delay to avoid tight loop

