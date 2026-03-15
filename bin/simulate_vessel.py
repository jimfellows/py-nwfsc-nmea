#!/usr/bin/env python
"""
Example script to run the nwfsc-nmea vessel simulator.
Broadcasts realistic NMEA 0183 standard and proprietary sentences.
"""

import time
import argparse
from nwfsc_nmea.simulator import Simulator, StandardGenerator, SimradGenerator, FurunoGenerator, UDPSink, StdoutSink

def main():
    parser = argparse.ArgumentParser(description="Simulate an NWFSC Vessel NMEA stream.")
    parser.add_argument("--udp-port", type=int, default=10110, help="UDP port to broadcast on")
    parser.add_argument("--stdout", action="store_true", help="Print NMEA strings to stdout as well")
    parser.add_argument("--hz", type=float, default=1.0, help="Frequency of NMEA string generation")
    args = parser.parse_args()

    print(f"Starting NWFSC Vessel Simulator...")
    print(f"UDP Broadcast: 127.0.0.1:{args.udp_port}")
    print(f"Frequency: {args.hz} Hz")
    if args.stdout:
        print("Stdout mirror ENABLED")
    print("Press Ctrl+C to stop.\n")

    # 1. Initialize the Simulator engine (controls time and physics)
    simulator = Simulator(hz=args.hz)
    
    # Optional: Configure starting state
    simulator.state.lat = 47.6
    simulator.state.lon = -122.3
    simulator.state.heading = 270.0  # Heading West
    simulator.state.speed_knots = 12.5
    
    # 2. Add Generators (What NMEA sentences to build based on physics)
    simulator.add_generator(StandardGenerator())
    simulator.add_generator(SimradGenerator())
    simulator.add_generator(FurunoGenerator())
    
    # 3. Add Sinks (Where to send the NMEA strings)
    simulator.add_sink(UDPSink(port=args.udp_port))
    if args.stdout:
        simulator.add_sink(StdoutSink())

    # 4. Run the Engine
    simulator.start()

if __name__ == "__main__":
    main()
