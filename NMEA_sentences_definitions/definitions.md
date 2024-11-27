
Here are all the definitions for the different NMEA0183 sentences, explained in details by data fields

- **GBS** NMEA sentence structure: [link](https://github.com/MicroControleurMonde/RP2040_GPS_NMEA/blob/main/NMEA_sentences_definitions/GBS%20NMEA%20sentence%20structure.txt)

        The GBS sentence is primarily used to ensure the integrity of GNSS signals
  
- **GGA** NMEA sentence structure: [link](https://github.com/MicroControleurMonde/RP2040_GPS_NMEA/blob/main/NMEA_sentences_definitions/GGA%20NMEA%20sentence%20structure.txt)

        The GGA sentence provides fundamental positioning data from a GNSS receiver

- **GLL** – Geographic Position (Lat_Long): [link](https://github.com/MicroControleurMonde/RP2040_GPS_NMEA/blob/main/NMEA_sentences_definitions/GLL%20%E2%80%93%20Geographic%20Position%20(Lat_Long).txt)
  
        The GLL NMEA sentence is used to transmit basic positioning information (latitude, longitude, UTC time)
        and the status of the GNSS fix.
        It's a simple and lightweight.
  
- **GPQ**  NMEA sentence structure: [link](https://github.com/MicroControleurMonde/RP2040_GPS_NMEA/blob/main/NMEA_sentences_definitions/GPQ%20%20NMEA%20sentence%20structure.txt)

        The GPQ NMEA sentence is used for reporting the quality and status of the GNSS receiver, including satellite
        visibility, signal quality, fix status, and receiver health.
  
- **GSA** NMEA sentence structure: [link](https://github.com/MicroControleurMonde/RP2040_GPS_NMEA/blob/main/NMEA_sentences_definitions/GSA%20NMEA%20sentence%20structure.txt)

        The GSA NMEA sentence is used to report the fix status, the satellites used for the position calculation,
        and the DOP values (Position Dilution of Precision, Horizontal Dilution of Precision, and Vertical Dilution
        of Precision).

- **GST** NMEA sentence structure: [link](https://github.com/MicroControleurMonde/RP2040_GPS_NMEA/blob/main/NMEA_sentences_definitions/GST%20NMEA%20sentence%20structure.txt)
  
        The GST NMEA sentence is used to report the standard deviation (uncertainty) of the GNSS position,
        along with the DOP values (PDOP, HDOP, and VDOP), which provide insight into the quality of the GNSS fix. 

- **RMC** NMEA sentence structure: [link](https://github.com/MicroControleurMonde/RP2040_GPS_NMEA/blob/main/NMEA_sentences_definitions/RMC%20NMEA%20sentence%20structure.txt)

        The RMC (Recommended Minimum Specific GPS/Transit Data) NMEA sentence is widely used to provide basic
        but critical positioning, speed, and heading information from a GPS receiver.
 
- **VTG** NMEA sentence structure: [link](https://github.com/MicroControleurMonde/RP2040_GPS_NMEA/blob/main/NMEA_sentences_definitions/VTG%20NMEA%20sentence%20structure.txt)

        The VTG (Course and Speed Over Ground) NMEA sentence provides vital navigation information including
        the course over ground and speed over ground.
  
- **ZDA** NMEA sentence structure: [link](https://github.com/MicroControleurMonde/RP2040_GPS_NMEA/blob/main/NMEA_sentences_definitions/ZDA%20NMEA%20sentence%20structure.txt)

        The ZDA (Time and Date) NMEA sentence is used to provide accurate date and time information,
        including UTC time, the day, month, year, and the local time offset from UTC.
