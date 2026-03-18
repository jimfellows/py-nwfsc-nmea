import pynmea2
import nwfsc_nmea
import pytest

def test_psimp_parsing():
    # Example PSIMP D1 sentence based on documentation
    # $PSIMP,D1,201856,130326,D,M,1,10,1,15.5,0.1,2,0,45,15,20,1,0*23
    raw = "$PSIMP,D1,201856,130326,D,M,1,10,1,15.5,0.1,2,0,45,15,20,1,0*3F"
    msg = pynmea2.parse(raw, check=False)
    
    assert isinstance(msg, nwfsc_nmea.proprietary.simrad.PSIMP)
    assert msg.specifier == 'D1'
    assert msg.time == '201856'
    assert msg.date == '130326'
    assert msg.measurement_type == 'D'
    assert msg.measurement_description == 'Depth'
    assert msg.unit == 'M'
    assert msg.value == '15.5'
    assert msg.quality == '2'
    assert msg.quality_description == 'Reliable'
    assert msg.interference_detected is False
    assert msg.cable_quality == '1'
    assert msg.cable_quality_description == 'Good'
    assert msg.has_error is False

def test_psimtv80_parsing():
    # Example PSIMTV80 sentence based on Simrad TV80 documentation
    # $PSIMTV80,123456,130326,4736.12,N,12220.45,W,4736.12,N,12220.45,W,10.50,180.00,185.00,150.5,01,a01,b02,50.25,10,123456*12
    # Note: Checksum *12 is a placeholder, pynmea2 might complain if it's incorrect.
    # We can use check=False or provide a valid one.
    raw = "$PSIMTV80,123456,130326,4736.12,N,12220.45,W,4736.12,N,12220.45,W,10.50,180.00,185.00,150.5,01,a01,b02,50.25,10,123456*24"
    msg = pynmea2.parse(raw, check=False)
    
    assert isinstance(msg, nwfsc_nmea.proprietary.simrad.PSIMTV80)
    assert msg.timestamp == '123456'
    assert msg.date == '130326'
    assert msg.lat == '4736.12'
    assert msg.lat_dir == 'N'
    assert msg.lon == '12220.45'
    assert msg.lon_dir == 'W'
    assert msg.vessel_speed == '10.50'
    assert msg.measurement_type == '01'
    assert msg.measurement_description == 'Spread'
    assert msg.source_location == 'a01'
    assert msg.source_description == 'Trawl a: Port door'
    assert msg.target_location == 'b02'
    assert msg.target_description == 'Trawl b: Starboard door / Clump'
    assert msg.value == '50.25'
    assert msg.quality == '10'
    assert msg.sensor_id == '123456'

def test_legacy_ii_parsing():
    # DBS: Depth Below Surface
    raw = "@IIDBS,,,12.5,M,,*00"
    msg = pynmea2.parse(raw, check=False)
    assert isinstance(msg, nwfsc_nmea.proprietary.simrad.DBS)
    assert msg.depth == '12.5'

    # HFB: Headrope to Footrope
    raw = "@IIHFB,10.0,M,15.0,M*49"
    msg = pynmea2.parse(raw, check=False)
    assert isinstance(msg, nwfsc_nmea.proprietary.simrad.HFB)
    assert msg.opening == '10.0'
    assert msg.height == '15.0'

def test_psim_combined_parsing():
    # PSIMDE: Slant, Horizontal, Bearing, Depth, Time
    # $PSIMDE,100,M,80,M,180.0,T,12.5,M,202349*23
    raw = "$PSIMDE,100,M,80,M,180.0,T,12.5,M,202349*3B"
    msg = pynmea2.parse(raw, check=False)
    assert isinstance(msg, nwfsc_nmea.proprietary.simrad.PSIMDE)
    assert msg.slant_range == '100'
    assert msg.horizontal_range == '80'
    assert msg.true_bearing == '180.0'
    assert msg.measurement_value == '12.5'
    assert msg.timestamp == '202349'
