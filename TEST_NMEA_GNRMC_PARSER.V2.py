# TEST_NMEA_GNRMC.V2.py
# Updated on 22 Aug 2024
# MicroPython code for Raspberry Pi Pico to retrieve and display only $GNRMC NMEA sentences with checksum validation
# UTC Time / UTC Date/ Status / Mode / Latitude/Longitude / Ground Speed (Km/h)

from machine import UART
import utime

# Configure UART communication
uart = UART(0, baudrate=9600, bits=8, parity=None, stop=1)

buffer = b""

def validate_checksum(sentence):
    """ Validate NMEA sentence checksum. """
    try:
        data, checksum = sentence.rsplit(b'*', 1)
        checksum = int(checksum, 16)
        computed_checksum = 0
        for byte in data[1:]:  # Skip initial '$'
            computed_checksum ^= byte
        return computed_checksum == checksum
    except ValueError:
        return False

def convert_knots_to_kmh(knots):
    """ Convert knots to kilometers per hour. """
    try:
        knots = float(knots)
        return knots * 1.852
    except ValueError:
        return None

def convert_to_decimal_degrees(coord, direction, is_longitude=False):
    """ Convert NMEA DMS coordinates to decimal degrees. """
    try:
        if is_longitude:
            degrees = int(coord[:3])  # Longitude has 3 digits for degrees
            minutes = float(coord[3:])
        else:
            degrees = int(coord[:2])  # Latitude has 2 digits for degrees
            minutes = float(coord[2:])
        decimal_degrees = degrees + minutes / 60.0

        if direction in ['S', 'W']:
            decimal_degrees = -decimal_degrees

        return decimal_degrees
    except ValueError:
        return None

def format_time_utc(heure_utc):
    """ Format the UTC time from HHMMSS.SS to HH:MM:SS.SS. """
    if len(heure_utc) >= 6:
        hours = heure_utc[:2]
        minutes = heure_utc[2:4]
        seconds = heure_utc[4:]
        return f"{hours}:{minutes}:{seconds}"
    return "Non fourni"

def decode_gnrmc_sentence(sentence):
    """ Decode and display $GNRMC sentence information with debug output. """
    parts = sentence.split(',')

    # Print the raw sentence and parts for debugging
    print(f"DEBUG: Raw sentence: {sentence}")
    print(f"DEBUG: Parts: {parts}")

    if len(parts) >= 13:  # Make sure there are at least 13 elements to include the mode
        heure_utc = format_time_utc(parts[1])
        statut = parts[2]
        latitude = parts[3]
        latitude_dir = parts[4]
        longitude = parts[5]
        longitude_dir = parts[6]
        vitesse_knots = parts[7]
        date_utc = parts[9]

        # Extract mode and strip checksum
        mode_field = parts[12].strip()
        mode = mode_field.split('*')[0] if '*' in mode_field else mode_field
        print(f"DEBUG: Extracted Mode: '{mode}' (should be a single character)")

        # Convert coordinates to decimal degrees
        latitude_decimal = convert_to_decimal_degrees(latitude, latitude_dir)
        longitude_decimal = convert_to_decimal_degrees(longitude, longitude_dir, is_longitude=True)

        # Convert speed to km/h
        vitesse_kmh = convert_knots_to_kmh(vitesse_knots)

        # Convert mode to readable text
        mode_conversion = {
            'A': 'Autonomous',
            'D': 'Differential',
            'E': 'Estimated',
            'M': 'Manual input',
            'N': 'Data not valid'
        }
        mode_text = mode_conversion.get(mode, 'Unknown')
        print(f"DEBUG: Mode text after conversion: '{mode_text}'")

        # Convert status to readable text
        statut_text = 'Valid data' if statut == 'A' else 'Void'

        # Format date
        if len(date_utc) == 6:
            date_formatee = f"{date_utc[0:2]}/{date_utc[2:4]}/{date_utc[4:6]}"
        else:
            date_formatee = 'Not provided'

        # Print results
        print(f"Time UTC: {heure_utc}")
        print(f"Date UTC: {date_formatee}")
        print(f"Status: {statut_text}")
        print(f"Mode: {mode_text}")
        if latitude_decimal is not None and longitude_decimal is not None:
            print(f"Latitude: {latitude_decimal:.6f}°")
            print(f"Longitude: {longitude_decimal:.6f}°")
        else:
            print("Latitude/Longitude: Not provided")
        if vitesse_kmh is not None:
            print(f"Ground speed: {vitesse_kmh:.2f} km/h")
        else:
            print("Ground speed: Not provided")
        print("")
    else:
        print("The $GNRMC frame is incomplete.")


def process_nmea(data):
    """ Process and display only $GNRMC NMEA sentences. """
    if data:
        try:
            decoded_data = data.decode('utf-8', 'ignore').strip()
            if decoded_data.startswith('$GNRMC'):
                if validate_checksum(data):
                    decode_gnrmc_sentence(decoded_data)
                else:
                    print("Invalid checksum for sentence:", decoded_data)
            else:
                # Optionally log or ignore non-$GNRMC sentences
                pass
        except UnicodeError as e:
            print("Unicode error:", e)

while True:
    if uart.any():
        buffer += uart.read()  # Append incoming data to buffer
        while b'\n' in buffer:
            line, buffer = buffer.split(b'\n', 1)  # Split lines
            if line:
                process_nmea(line)
    
    utime.sleep_ms(200)  # Small delay to avoid tight loop
