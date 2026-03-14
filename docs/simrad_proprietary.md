# Simrad Proprietary NMEA Sentences

This document provides technical reference for the Simrad proprietary NMEA sentences supported by this library, based on the Simrad TV80 Reference Manual.

---

## 1. PSIMTV80 (Sensor Data)

Used by Simrad TV80 software to provide real-time measurements and location data for sensors attached to fishing gear.

### Format
`$PSIMTV80,hhmmss,yymmdd,ddmm.hh,N,dddmm.hh,W,ddmm.hh,N,dddmm.hh,W,kk.kk,ccc.cc,hhh.hh,mmmm.m,tt,fff,ooo,vvvv.vv,qq,xxxxxx*cc`

### Field Definitions
| Position | Label | Format | Description |
| :-- | :-- | :-- | :-- |
| 1 | UTC Time | `hhmmss` | Coordinated Universal Time |
| 2 | Date | `yymmdd` | Date (Year, month, day) |
| 3, 4 | Vessel Latitude | `ddmm.hh,N/S` | Vessel latitude |
| 5, 6 | Vessel Longitude | `dddmm.hh,W/E` | Vessel longitude |
| 7, 8 | Sensor Latitude | `ddmm.hh,N/S` | Calculated sensor latitude |
| 9, 10 | Sensor Longitude | `dddmm.hh,W/E` | Calculated sensor longitude |
| 11 | Vessel Speed | `kk.kk` | Speed in knots |
| 12 | COG | `ccc.cc` | Course over ground in degrees |
| 13 | Heading | `hhh.hh` | Vessel heading in degrees |
| 14 | Sounder Depth | `mmmm.m` | Echo sounder depth in meters |
| 15 | Measurement Type | `tt` | See lookup table below |
| 16 | Source Location | `fff` | Trawl location code |
| 17 | Target Location | `ooo` | Paired sensor location code |
| 18 | Value | `vvvv.vv` | Measured value (SI units) |
| 19 | Quality | `qq` | 0 (Error) to 10 (High) |
| 20 | Sensor ID | `xxxxxx` | Unique sensor identifier (Serial No.) |

### Measurement Type (tt)
- `01`: Spread
- `02`: Height
- `03`: Depth
- `04`: Roll
- `05`: Pitch
- `19`: Temperature
- `20`: Catch
- `21`: Bottom contact

---

## 2. PSIMP,D1 (Sensor Data / Hardware Status)

A modern replacement for the PSIMP,D datagram. Provides detailed measurements and hardware status for PS, PI, and PX sensors.

### Format
`$PSIMP,D1,tt,dd,M,U,SNo,MNo,C,V,Cr,Q,In,SL,NL,G,Cb,error*chksum`

### Field Definitions
| Position | Label | Format | Description |
| :-- | :-- | :-- | :-- |
| 1 & 2 | Talker & ID | `PSIMP` | Datagram identifier |
| 3 | Specifier | `D1` | Sentence specifier |
| 4 | Time | `tt` | Time of measurement |
| 5 | Date | `dd` | Date of measurement |
| 6 | Measure Type | `M` | `D`=Depth, `T`=Temp, `C`=Catch, `B`=Bottom, `N`=No sensor, `M`=Marker |
| 7 | Unit | `U` | `M`=meters, `C`=Celsius (SI units) |
| 8 | Sensor No. | `SNo` | Assigned sensor number |
| 9 | Measure No. | `MNo` | Specific measurement number |
| 10 | Channel | `C` | Communication channel number |
| 11 | Value | `V` | Actual value of measurement |
| 12 | Change Rate | `Cr` | Rate of change |
| 13 | Quality | `Q` | `0`=No connection, `1`=Lost pulses (predicted), `2`=Reliable |
| 14 | Interference | `In` | `0`=None, `1`=Interference detected |
| 15 | Signal Level | `SL` | Signal level in dB // 1 µPa |
| 16 | Noise Level | `NL` | Noise level in dB // 1 µPa |
| 17 | Gain | `G` | Hardware gain: 0, 20, or 40 dB |
| 18 | Cable Quality | `Cb` | `0`=Disconnected, `1`=Good, `2`=Short-circuited |
| 19 | Error | `error` | `0`=No error, others indicate error condition |
---

## 3. Gear Geometry & Monitoring (@II* Sentences)

Used for high-resolution gear geometry. Note the `@` start delimiter.

### DBS (Depth Below Surface)
`@IIDBS,,,x.x,M,,*chksum`
- Field 4: Depth in meters (0–2000m).

### HFB (Headrope to Footrope)
`@IIHFB,x.x,M,y.y,M*chksum`
- Field 1: Vertical opening (headrope to footrope) in meters.
- Field 3: Height (headrope to bottom) in meters.

### TDS (Door Spread)
`@IITDS,x.x,M*chksum`
- Field 1: Distance between doors in meters.

---

## 4. Combined Position & Measurement ($PSIM*)

Combines measurements with acoustic positioning (Range/Bearing).

### Common Structure
- **Slant Range**: Meters.
- **Horizontal Range**: Meters.
- **True Bearing**: Degrees.
- **Measurement**: Varies by type.
- **Timestamp**: `hhmmss`.

### Datagrams
| ID | Measurement | Description |
| :--- | :--- | :--- |
| `DE` | Sensor Depth | Position + Depth |
| `H1` | Opening & Height | Position + Opening/Height |
| `S1` | Spread | Position + Door Spread |
| `TM` | Water Temp | Position + Temperature |
| `MW` | Middle Weight | Twin Rig Geometry |

---

## 5. Simrad ITI Specific Datagrams

### Trawl Position True (@IITPT)
`@IITPT,xxxx,M,yyy,P,zzzz.z,M`
- Field 1: Horizontal range (0-4000m).
- Field 3: True bearing to target (relative to North).
- Field 5: Depth below surface (0-2000m).

### Trawl Position Cartesian (@IITPC)
`@IITPC,x.M,y,M,z,M`
- Field 1: Starboard/Port distance from centerline.
- Field 3: Distance behind vessel.
- Field 5: Depth.

### Trawl Filling (@IITFI)
`@IITFI,x,y,z`
- Fields: Catch sensor status (0=Off, 1=On, 2=No Answer).

### Ascend/Descend (@IIDAD)
`@IIDAD,x.x,M,x.x,M`
- Field 1: Depth.
- Field 3: Rate in m/min.

### Trawl Latitude/Longitude ($IIGLL)
`$IIGLL,ddmm.hhh,N,dddmm.hhh,W,hhmmss.ss,A`
- High-precision geographical position of the trawl.

### Trawl Eye Echo ($PSIMTE)
`$PSIMTE,xx%y...a,x.x, ,Gx,gx, Vx.x`
- Field 1: Percentage of samples above threshold and average level for 10 echo cells.
- Field 2: Total range of fish detection (2.5 to 50 m).
- Hardware and software gain settings.
- Fish velocity data.
