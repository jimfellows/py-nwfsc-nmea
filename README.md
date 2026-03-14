# py-nwfsc-nmea

An extension for [pynmea2](https://github.com/Knio/pynmea2) to parse proprietary NMEA sentences used by NOAA Fisheries at the Northwest Fisheries Science Center (NWFSC).

## Documentation

- [Simrad/ITI Proprietary Sentences](docs/simrad_proprietary.md)
- [Furuno Proprietary Sentences](docs/furuno_proprietary.md)
- [Standard NMEA 0183 Reference](docs/standard_sentences.md)

## Installation

```bash
pip install nwfsc-nmea
```

*Note: Requires `pynmea2`.*

## Usage

```python
import pynmea2
import nwfsc_nmea

# The proprietary sentences are automatically registered upon importing nwfsc_nmea
msg = pynmea2.parse("$PSIMP,D1,1,L,12.5,M,0.0,M,0.0,M*45")
print(msg.depth)
```

## Development

This project uses [Poetry](https://python-poetry.org/) for dependency management.

```bash
# Install dependencies
poetry install

# Run tests
poetry run pytest
```

## Python Support

Supports Python 3.6 to 3.13.
