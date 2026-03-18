
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