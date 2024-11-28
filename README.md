# RP2040_GPS_NMEA
![Pic](https://github.com/MicroControleurMonde/RP2040_GPS_NMEA/blob/main/NMEA_sentences_definitions/nmea-logo-blue.jpg)

### Set of micro-python tools to decode the different types of NMEA sentences provided by a GPS chip.

### **REMINDER**:
 **NMEA sentences are not vendor specific**, which means that these tools will work with any GPS chipset as long as it is properly connected to your MCU.
 
# NEMA Decoding Tools
 
- 1 Generic NMEA decoder (*used as debugger to visualize the different streams*) - [Generic Decoder Source](https://github.com/MicroControleurMonde/RP2040_GPS_NMEA/blob/main/TEST_NMEA_%24GP.py)
- 2 RMC Decoder - [RMC Decoder Source](https://github.com/MicroControleurMonde/RP2040_GPS_NMEA/blob/main/TEST_NMEA_GNRMC_PARSER.V2.py)
- 3 GGA Decoder - [GCA Decoder Source](https://github.com/MicroControleurMonde/RP2040_GPS_NMEA/blob/main/TEST_NMEA_GGA.v1.py)
- 4 GLL Decoder - [GLL Decoder Source](https://github.com/MicroControleurMonde/RP2040_GPS_NMEA/blob/main/TEST_NMEA_GLL.V1.py)
- 5 GSA Decoder - [GSA Decoder Source](https://github.com/MicroControleurMonde/RP2040_GPS_NMEA/blob/main/TEST_NMEA_GSA.V1.py)
- 6 GSV Decoder - [GSV Decoder Source](https://github.com/MicroControleurMonde/RP2040_GPS_NMEA/blob/main/TEST_NMEA_GSV.V1.py)

These decoders interpret the sentences to extract the values according to the NMEA 0183 standard **without using any external library / module !**

All of them are using **UART0**, **TX=GPIO0**, **RX=GPIO1** as default. So remember to change the settings according to your setup !

[NMEA 0183](https://en.wikipedia.org/wiki/NMEA_0183)

# Sentences structures

The detailed structure of each NMEA sentences is detailed in this section: [Structures](https://github.com/MicroControleurMonde/RP2040_GPS_NMEA/blob/main/NMEA_sentences_definitions/definitions.md)

Each byte received is interpreted according to the NMEA specifications.

## UNDER CONSTUCTION
![Pic](https://github.com/MicroControleurMonde/RP2040_GPS_NMEA/blob/main/1411798446.jpg)
