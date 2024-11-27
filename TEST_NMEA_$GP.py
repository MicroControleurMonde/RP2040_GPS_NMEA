# TEST_NMEA_$GP.py
# Created on January 30, 2024
# MicroPython code for Raspberry Pi Pico which receives and displays the NMEA sentences on the console.
# Used to do a real-time debugging of NMEA sentences.
# This script uses the UART to communicate with a GPS receiver.
#
# The code configures the UART0 serial port at a rate of 9600 baud, retrieves the NMEA data from the GPS receiver
# and displays them on the console in real time.

from machine import UART
import utime

# Configures the UART communication with the serial port (UART0).
# GPIO0 pins for TX and GPIO1 for RX.
# Baud rate set at 9600, commonly used for GPS receivers.
uart = UART(0, baudrate=9600, tx=0, rx=1)

while True:
    # Checks if data is available on the RX port
    if uart.any():
        # Reads the incoming data to the end of the line (end of one of the NMEA sentences)
        data = uart.readline()

        # NMEA sentence processing (by convention, GPS sentences start with '$GP')
        if data.startswith(b'$GP'):
            # Displays the NMEA sentence by decoding the bytes in UTF-8 and removing unnecessary spaces
            print("Phrase NMEA:", data.decode('utf-8', 'ignore').strip())

        # Adds a delay of 100ms to avoid a too tight loop and allow other tasks to run
        utime.sleep_ms(100)
