# Standard NMEA 0183 Sentences

This library leverages `pynmea2` for parsing standard NMEA 0183 sentences. Below is a reference of the standard sentences supported and used in this project, based on the Actisense NMEA 0183 Information Sheet.

---

## 1. Navigation & Waypoint Data

### AAM (Waypoint Arrival Alarm)
Status of arrival at a waypoint.
- **Fields**: Status (Arrival circle entered), Perpendicular passed, Arrival circle radius, Waypoint ID.

### BWC (Bearing and Distance to Waypoint)
Bearing and distance to a waypoint along a Great Circle.
- **Fields**: UTC Time, Waypoint Position (Lat/Lon), Bearing (True/Magnetic), Distance, Waypoint ID, Mode Indicator.

### RMB (Recommended Minimum Navigation Information)
Sent when a destination waypoint is active.
- **Fields**: Status, Cross Track Error, Origin/Destination Waypoint IDs, Destination Position, Range/Bearing to Destination, Closing Velocity, Arrival Status.

---

## 2. GNSS Position & Status

### GGA (Global Positioning System Fix Data)
- **Fields**: Quality Indicator, Satellites in use, HDOP, Antenna Altitude, Geoidal Separation.

### GSA (GNSS DOP and Active Satellites)
- **Fields**: Selection Mode, Fix Mode, Satellite IDs, PDOP, HDOP, VDOP.

### RMC (Recommended Minimum Specific GNSS Data)
- **Fields**: Status, SOG, COG, Date, Magnetic Variation, Mode Indicator.

---

## 3. Vessel Motion & Environment

### HDG / HDT (Heading)
- **HDG**: Magnetic heading, Deviation, and Variation.
- **HDT**: True heading.

### VHW (Water Speed and Heading)
- **Fields**: Heading (True/Magnetic), Speed (Knots/KMH).

### DPT / DBT (Depth)
- **DPT**: Depth below transducer and offset.
- **DBT**: Depth below transducer in Feet, Meters, and Fathoms.

### MWV (Wind Speed and Angle)
- **Fields**: Wind Angle, Reference (Relative/True), Wind Speed, Status.

---

## 4. Data Management

### TXT (Text Transmission)
Used for status messages or alerts.
- **Fields**: Total messages, message number, text identifier, Text Message.
