# Video demonstrations

In this folder you can find videos demonstrating the use of:
- **GLL NMEA Decoder**: [GLL video](https://github.com/MicroControleurMonde/RP2040_GPS_NMEA/blob/main/videos/GLL%20NMEA.mp4)
- **GSV NMEA Decoder**: [VSV video](https://github.com/MicroControleurMonde/RP2040_GPS_NMEA/blob/main/videos/GSV%20NMEA.mp4)
- **VTG NMEA Decoder**: [VTG video](https://github.com/MicroControleurMonde/RP2040_GPS_NMEA/blob/main/videos/VTG%20NMEA.mp4)
  
The examples provided show the codes operating in "*normal*" mode (the GPS chip sends continuous NMEA frames after the interpretation of the satellite information) and how the decoding of each sentence is organized.

In some cases, your GPS chip is correctly connected, it emits abundant NMEA streams and yet... when decoding, nothing is displayed! 

This happens when ***`the GPS chip did not have enough time after start-up to accumulate satellite data`***. It also happens when ***`the chip loses reception of satellite signals`***.
The following videos show you what happens at data level and how it translates into each NMEA sentence.

- **NMEA empty streams**: [video](https://github.com/MicroControleurMonde/RP2040_GPS_NMEA/blob/main/videos/NMEA%20Empty%20sentences.mp4)
  
        The NMMEA streams are processed, the data are displayed on your IDE console but if you pay close attention,
        some of the sentences are empty and you can also observe that the value '99.99' is recurrent.
        Which means: Data is incorrect or missing.
  
- **GLL** empty sentences: [video](https://github.com/MicroControleurMonde/RP2040_GPS_NMEA/blob/main/videos/GLL%20NMEA%20sentences%20empty.mp4)
  
        In this video, the code is dismantling the flow field by field and you can clearly observe the missing data
        or the data non-validity.
  
- **VTG** empty sentences: [video](https://github.com/MicroControleurMonde/RP2040_GPS_NMEA/blob/main/videos/VTG%20NMEA%20sentences%20empty.mp4)
  
        Same as the previous video: the sentences are empty.  

All these videos are provided as examples of how the code functions when used with an IDE such as Thonny.

