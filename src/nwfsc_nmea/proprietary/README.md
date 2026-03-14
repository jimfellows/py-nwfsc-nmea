# Simrad Proprietary Sentences Reference

This folder contains the implementation for Simrad proprietary NMEA sentences.

## Supported Sentences

### 1. Standard Datagrams ($IIMTW, etc.)
- **MTW**: Water Temperature (e.g., `$IIMTW,xx.x,C`).

### 2. Gear Monitoring (@II* Sentences)
These sentences use the `@` start delimiter and provided high-resolution gear geometry.
- **DBS**: Depth Below Surface (Trawl depth).
- **HFB**: Trawl Headrope to Footrope (Opening and Height).
- **HB2**: Trawl Headrope to Footrope (Trawl 2).
- **TDS**: Door Spread.
- **TS2**: Door Spread (Trawl 2).

### 3. Proprietary Combined Sentences ($PSIM*)
These sentences combine measurements with acoustic positioning data (Range/Bearing).
- **PSIMTV80**: Comprehensive Sensor Data (Modern TV80 format).
- **PSIMP**: Sensor Data with Hardware Status (D1 Specifier).
- **PSIMDE**: Sensor Depth + Position.
- **PSIMH1/H2**: Opening & Height + Position.
- **PSIMS1/S2**: Spread + Position.
- **PSIMTM**: Water Temperature + Position.
- **PSIT**: ITI Proprietary data.

## Furuno Proprietary Sentences ($PFEC)
- **GPatt**: Attitude Data (Heading, Pitch, Roll).
- **GPhve**: Heave Data.
- **SDbhr**: Bottom Hardness.
- **Radar Target Management**: `DRtnm`, `DRtsm`.
- **System Integration**: `hdcom`, `pireq`, `pidat`.
- **Navigation**: `GPwpl`, `GPrtc`, `GPxfr`.

## Implementation Details
All classes inherit from `pynmea2.Sentence` or `pynmea2.ProprietarySentence`. 
Special handling is included for the `@II` delimiter style used by legacy Simrad gear.
