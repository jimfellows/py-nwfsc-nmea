# py-nwfsc-nmea

An extension for [pynmea2](https://github.com/Knio/pynmea2) to parse proprietary NMEA sentences used by NOAA Fisheries at the Northwest Fisheries Science Center (NWFSC).

## Documentation

- [Simrad/ITI Proprietary Sentences](docs/simrad_proprietary.md)
- [Furuno Proprietary Sentences](docs/furuno_proprietary.md)
- [Standard NMEA 0183 Reference](docs/standard_sentences.md)

## Installation

```bash
uv add pynmea2
uv add --git https://github.com/jim-f/py-nwfsc-nmea.git
```

*Note: Requires `pynmea2`.*

## Usage
This package extends and build on top of pynmea2 by registering
logic for proprietary sentences not included in the base library.

So, you can parse standard sentences
```python
import pynmea2
import nwfsc_nmea

# Example GPRMC sentence (Standard GPS data)
# Structure: Time, Status, Lat, N/S, Lon, E/W, Speed(kn), Course, Date, MagVar, Checksum
raw_data = "$GPRMC,123519,A,4807.038,N,01131.000,E,022.4,084.4,230394,003.1,W*6A"

msg = pynmea2.parse(raw_data)

# Standard GPRMC attributes provided by pynmea2
print(f"Timestamp: {msg.timestamp}")
print(f"Latitude:  {msg.latitude}")
print(f"Longitude: {msg.longitude}")
print(f"Speed (knots): {msg.spd_over_grnd}")
```

Or proprietary ones:
```python
import pynmea2
import nwfsc_nmea

# The proprietary sentences are automatically registered upon importing nwfsc_nmea
msg = pynmea2.parse("$PSIMP,D1,123456,180326,D,M,1,1,1,42.5,0.1,2,0,75,12,25,1,0*08")

print(f"Date: {msg.date}")
print(f"Time: {msg.time}")
print(f"Unit: {msg.unit}")
print(f"Sensor Number: {msg.sensor_num}")
print(f"Measurement Number: {msg.measurement_num}")
print(f"Channel: {msg.channel}")
print(f"Value: {msg.value}")
print(f"Change Rate: {msg.change_rate}")
print(f"Quality: {msg.quality}")
print(f"Interference: {msg.interference}")
print(f"Signal Level: {msg.signal_level}")
print(f"Noise Level: {msg.noise_level}")
print(f"Gain: {msg.gain}")
print(f"Cable Quality: {msg.cable_quality}")
print(f"Error: {msg.error_code}")
```

## Development

This project uses [uv](https://docs.astral.sh/uv/) for dependency management.

```bash
# Install dependencies
uv sync --all-groups

# Run tests
uv run pytest
```

## Distribution

To package the library for distribution (e.g., to PyPI or a private repository):

### 1. Build the Package
This creates a source distribution and a wheel in the `dist/` directory.

```bash
uv build
```

### 2. Publish the Package
To publish to PyPI (requires an API token):

```bash
uv publish
```

To publish to a custom repository:

```bash
uv publish --publish-url https://your.repo.url/legacy/
```

### 3. Install from Local Wheel
During development, you can test installation from the local wheel:

```bash
uv pip install dist/nwfsc_nmea-0.1.0-py3-none-any.whl
```

## NMEA Simulator

The package also includes a robust NMEA Simulator module capable of generating continuous NMEA data streams (Standard and Proprietary) based on realistic vessel kinematics, and broadcasting these streams via diverse network/hardware interfaces.

### Architecture

The simulator is composed of three main decoupled components:
1. **Kinematics Engine (`VesselState`)**: Simulates realistic physical parameters like vessel Lat/Lon, Heading, Speed, Depth, Pitch, Roll, Heave, and Trawl distances.
2. **Generators (`StandardGenerator`, `SimradGenerator`, `FurunoGenerator`)**: Translates the current `VesselState` into valid NMEA strings with checksums.
3. **Data Sinks (`UDPSink`, `TCPSink`, `SerialSink`, `StdoutSink`)**: Publishes the generated sentences to a specific output medium.

### Setup and Usage

You can use the simulator programmatically in your own scripts:

```python
from nwfsc_nmea.simulator import Simulator, VesselState
from nwfsc_nmea.simulator import StandardGenerator, FurunoGenerator, SimradGenerator
from nwfsc_nmea.simulator import StdoutSink, UDPSink, TCPSink, SerialSink

# 1. Initialize engine at 1 Hz update rate (1 sentence per second)
sim = Simulator(hz=1.0)

# Optional: Set starting realistic conditions
sim.state.lat = 47.6
sim.state.lon = -122.3
sim.state.heading = 270.0  # West
sim.state.speed_knots = 10.5

# 2. Add Generators (What to generate)
sim.add_generator(StandardGenerator())     # GGA, RMC, HDT, DPT
sim.add_generator(FurunoGenerator())       # SDDBT, SDBB, GPatt, GPhve
sim.add_generator(SimradGenerator())       # PSIMP, PSIMTV80, etc.

# 3. Add Output Sinks (Where to send the data)
sim.add_sink(StdoutSink())                           # Print to console
sim.add_sink(UDPSink(ip="127.0.0.1", port=10110))    # Broadcast via UDP
# sim.add_sink(TCPSink(ip="0.0.0.0", port=10110))    # Start TCP Server
# sim.add_sink(SerialSink(port="COM3", baudrate=4800)) # Write to Serial COM port

# 4. Start the blocking simulation loop
try:
    sim.start()
except KeyboardInterrupt:
    sim.stop()
```

### Pre-built Demo Script

A runnable demonstration script is included in the package:

```bash
# Starts the simulator broadcasting on UDP 10110 at 2 Hz, printing to stdout
uv run python bin/simulate_vessel.py --stdout --hz 2.0
```

> **Note on Serial Output:** To use the `SerialSink` to stream data over a physical or virtual COM port, you must ensure you have `pyserial` installed (`uv add pyserial`).
