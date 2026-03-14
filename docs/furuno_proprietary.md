# Furuno Proprietary NMEA Sentences ($PFEC)

This document provides technical reference for Furuno proprietary NMEA sentences supported by this library, based on Furuno technical documentation including the FR-10/12 series.

Furuno proprietary sentences use the talker identifier **PFEC** (Proprietary Furuno Electronic Corporation).

---

## 1. Common Attitude & Sensor Datagrams

### GPatt (Attitude Data)
Provides the vessel's physical orientation (Heading, Pitch, Roll).
**Format**: `$PFEC,GPatt,hhh.h,pp.p,rr.r*cc`

| Position | Label | Description |
| :--- | :--- | :--- |
| 1 | Heading | True heading in degrees (0.0 to 359.9) |
| 2 | Pitch | Pitch angle in degrees (positive for bow up) |
| 3 | Roll | Roll angle in degrees (positive for starboard roll) |

### GPhve (Heave Data)
Used for vertical motion correction.
**Format**: `$PFEC,GPhve,xx.xxx,A*cc`

| Position | Label | Description |
| :--- | :--- | :--- |
| 1 | Heave Value | Vertical displacement in meters (e.g., 0.125) |
| 2 | Status | A = Valid, V = Invalid |

### SDbhr (Bottom Hardness)
Identifies the composition of the seabed.
**Format**: `$PFEC,SDbhr,val,stat*cc`

| Position | Label | Description |
| :--- | :--- | :--- |
| 1 | Hardness Value | Numeric representation of bottom density |
| 2 | Status | Data reliability indicator |

---

## 2. Radar & System Integration (FR-10/12 Series)

| ID | Name | Description |
| :--- | :--- | :--- |
| **DRtnm** | Target Number | Specific ID number assigned to a radar target |
| **DRtsm** | Target Status | Tracking state (acquiring, lost, dangerous) |
| **hdcom** | Heading Command | Synchronized heading alignment between networked displays |
| **pireq** | Data Request | Polling for specific internal parameters |
| **pidat** | Data Response | Output sentence containing requested data |

---

## 3. Navigation & Configuration

| ID | Name | Description |
| :--- | :--- | :--- |
| **GPwpl** | Waypoint Location | Proprietary version including icons/colors |
| **GPrtc** | Real-Time Clock | Synchronize multiple devices via internal RTC data |
| **GPxfr** | Almanac Transfer | Transferring Almanac/Ephemeris data during "cold start" |

---

## 4. Furuno Sonar & Depth (SD/BB)

These sentences use the **SD** (Depth Sounder) or **BB** talker identifiers.

### SDBB (Sonar/Fish Finder Depth)
`$SDBB,x.x,M`
- Field 1: Depth value.
- Field 2: Unit (M=Meters).

### SDDBT (Depth Below Transducer)
`$SDDBT,feet,f,meters,M,fathoms,F`
- Provides depth in three different units simultaneously.
