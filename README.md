# RP2040_GPS_NMEA
![NMEA](https://www.nmea.org/favicon.ico)
Set of micro-python tools to decode the different types of NMEA sentences provided by a GPS chip.

### **REMINDER**:
 **NMEA sentences are not vendor specific**, which means that these tools will work with any GPS chipset as long as it is properly connected to your MCU.
 
- 1 Generic NMEA decoder (*used as debugger to visualize the different streams sent by the GPS chip*): [Generic decoder](https://github.com/MicroControleurMonde/RP2040_GPS_NMEA/blob/main/TEST_NMEA_%24GP.py)
- 2 RMC Decoder
- 3 GGA Decoder 
- 4 GLL Decoder
- 5 GSA Decoder
- 6 GSV Decoder

These decoders interpret the sentences to extract the values according to the NMEA 0183 standard **without using any external library / module !**

[NMEA 0183](https://en.wikipedia.org/wiki/NMEA_0183)

# Sentences structures

The detailed structure of each NMEA sentences is detailed in this section: [Structures](https://github.com/MicroControleurMonde/RP2040_GPS_NMEA/blob/main/NMEA_sentences_definitions/definitions.md)

## UNDER CONSTUCTION
![Pic](https://github.com/MicroControleurMonde/RP2040_GPS_NMEA/blob/main/1411798446.jpg)
