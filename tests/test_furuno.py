import pynmea2
import nwfsc_nmea
import pytest

def test_sdbb_parsing():
    # Example SDBB sentence (Depth)
    raw = "$SDBB,12.5,M*3F"
    msg = pynmea2.parse(raw)
    assert isinstance(msg, nwfsc_nmea.proprietary.furuno.SDBB)
    assert msg.depth == '12.5'
    assert msg.unit == 'M'

def test_sddbt_parsing():
    # Example SDDBT sentence (Depth Below Transducer)
    # $SDDBT,feet,f,meters,M,fathoms,F
    raw = "$SDDBT,41.0,f,12.5,M,6.8,F*34"
    msg = pynmea2.parse(raw)
    assert isinstance(msg, nwfsc_nmea.proprietary.furuno.SDDBT)
    assert msg.depth_meters == '12.5'
    assert msg.depth_feet == '41.0'
