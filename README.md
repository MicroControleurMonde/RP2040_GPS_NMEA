# RP2040_GPS_NMEA
![Pic](https://github.com/MicroControleurMonde/RP2040_GPS_NMEA/blob/main/NMEA_sentences_definitions/nmea-logo-blue.jpg)

[NMEA 0183](https://en.wikipedia.org/wiki/NMEA_0183) (Wikipedia)

#### Abstract: Set of micro-python tools to decode the different types of NMEA sentences provided by a GPS chip.

## Breakdown of Sections
##### 0. Project Description
##### 1. Requirements
##### 2. NEMA Decoding Tools
##### 3. Decoding Demos (Videos)
##### 4. Sentences structures
##### 5. Disclaimer

# Project Description

This project provides a set of MicroPython tools for decoding various types of NMEA sentences typically received from GPS modules. 

NMEA 0183 is an international standard for communication between GPS receivers and devices. The provided decoders interpret these NMEA sentences without relying on any external libraries, making it easy to use with any compatible GPS chipset. The project is designed to work with the RP2040 (or similar) microcontrollers, such as the Raspberry Pi Pico, and utilizes UART communication for GPS data input.

### **REMINDER**:  **NMEA sentences are not vendor specific !**

# 1.Requirements
#### Hardware:
- Any GPS module compatible NMEA 0183 (e.g., NEO-6M, NEO-7M, u-blox SAM-M8Q, Beitan GPS modules,  etc.).
- A microcontroller with UART capability (RP2040, ESP8266, ESP32 or similar).
- Proper wiring between the GPS module and the microcontroller.

#### Software:
- MicroPython installed on the RP2040 (or other compatible MCU).
- Basic knowledge of UART communication and Python programming.

#### Pins Used:

The default UART settings are:
- `UART 0`
- `TX = GPIO0` / `RX = GPIO1`
  
You should adjust these settings if your setup uses different pins.


# 2.NEMA Decoding Tools

 The project provides several tools to decode the different types of NMEA sentences. These decoders work by reading the serial input from the GPS module, extracting and interpreting the information based on the NMEA 0183 standard.

- 1 Generic NMEA decoder (*used as debugger to visualize the different streams*) - [Generic Decoder Source](https://github.com/MicroControleurMonde/RP2040_GPS_NMEA/blob/main/TEST_NMEA_%24GP.py)
- 2 RMC Decoder - [RMC Decoder Source](https://github.com/MicroControleurMonde/RP2040_GPS_NMEA/blob/main/TEST_NMEA_GNRMC_PARSER.V2.py)
- 3 GGA Decoder - [GCA Decoder Source](https://github.com/MicroControleurMonde/RP2040_GPS_NMEA/blob/main/TEST_NMEA_GGA.v1.py)
- 4 GLL Decoder - [GLL Decoder Source](https://github.com/MicroControleurMonde/RP2040_GPS_NMEA/blob/main/TEST_NMEA_GLL.V1.py)
- 5 GSA Decoder - [GSA Decoder Source](https://github.com/MicroControleurMonde/RP2040_GPS_NMEA/blob/main/TEST_NMEA_GSA.V1.py)
- 6 GSV Decoder - [GSV Decoder Source](https://github.com/MicroControleurMonde/RP2040_GPS_NMEA/blob/main/TEST_NMEA_GSV.V1.py)
- 7 VFG Decoder - [VFG Decoder Source](https://github.com/MicroControleurMonde/RP2040_GPS_NMEA/blob/main/TEST_NMEA_VTG.V1.py)

  ***Note*** The 7 given decoders are the most current sentences emitted by GPS chips. The GPQ, TPS and ZDA NMEA sentences are more rarely observable and are not the ones that are the most useful in terms of geolocation.

These decoders interpret the sentences to extract the values according to the NMEA 0183 standard **without using any external library / module !**

# 3.Decoding Demos (Videos)

In this section, you'll find a few videos on how the tools are working and what they are doing exactly.

[Video Demos](https://github.com/MicroControleurMonde/RP2040_GPS_NMEA/blob/main/videos/demo_video.md)


# 4.Sentences structures

The detailed structure of each NMEA sentences is detailed in this section: [Structures](https://github.com/MicroControleurMonde/RP2040_GPS_NMEA/blob/main/NMEA_sentences_definitions/definitions.md)
(Files are in standard ASCII Text).

Each byte received is interpreted according to the NMEA specifications.

# 5.Disclaimer

The code contained in this repository is provided “as is”, without any warranty of performance, accuracy or result. 
The author shall not be liable for any direct or indirect damages that may result from the use of this code, including, but not limited to, loss of data or interruption of service.

## UNDER CONSTUCTION
I will add other elements soon. 

Stay tuned.


