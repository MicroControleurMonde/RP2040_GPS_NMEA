In this folder you can find videos demonstrating the use of:
- **GLL NMEA Decoder**: [GLL video](https://github.com/MicroControleurMonde/RP2040_GPS_NMEA/blob/main/videos/GLL%20NMEA.mp4)
- **GSV NMEA Decoder**: [VSV video](https://github.com/MicroControleurMonde/RP2040_GPS_NMEA/blob/main/videos/GSV%20NMEA.mp4)
- **VTG NMEA Decoder**: [VTG video](https://github.com/MicroControleurMonde/RP2040_GPS_NMEA/blob/main/videos/VTG%20NMEA.mp4)
  
The examples provided show the codes operating in "*normal*" mode (the GPS chip sends continuous NMEA frames after the interpretation of the satellite information) and how the decoding of each sentence is organized.

In some cases, your GPS chip is correctly connected, it emits abundant NMEA streams and yet... when decoding, nothing is displayed! 

This happens when the GPS chip did not have enough time after start-up to accumulate satellite data. It also happens when the chip loses reception of satellite signals.
The following videos show you what happens at data level and how it translates into each NMEA sentence.

- **NMEA empty streams**: [video](https://github.com/MicroControleurMonde/RP2040_GPS_NMEA/blob/main/videos/NMEA%20Empty%20sentences.mp4)
- **GLL** empty sentences: [video](https://github.com/MicroControleurMonde/RP2040_GPS_NMEA/blob/main/videos/GLL%20NMEA%20sentences%20empty.mp4)
- **VTG** empty sentences: [video](https://github.com/MicroControleurMonde/RP2040_GPS_NMEA/blob/main/videos/VTG%20NMEA%20sentences%20empty.mp4)

These videos are provided as examples of how the code functions when used with an IDE such as Thonny.

