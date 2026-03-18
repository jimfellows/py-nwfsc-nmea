import pynmea2
import nwfsc_nmea
import pytest

def test_gpatt_parsing():
    # $PFEC,GPatt,hhh.h,pp.p,rr.r
    raw = "$PFEC,GPatt,180.0,1.2,0.5*47"
    msg = pynmea2.parse(raw, check=False)
    
    assert isinstance(msg, nwfsc_nmea.proprietary.pfec.GPATT)
    assert msg.heading == '180.0'
    assert msg.pitch == '1.2'
    assert msg.roll == '0.5'

def test_gphve_parsing():
    # $PFEC,GPhve,xx.xxx,A
    raw = "$PFEC,GPhve,0.125,A*39"
    msg = pynmea2.parse(raw, check=False)
    
    assert isinstance(msg, nwfsc_nmea.proprietary.pfec.GPHVE)
    assert msg.heave == '0.125'
    assert msg.status == 'A'

def test_sdbhr_parsing():
    # $PFEC,SDbhr,val,stat
    raw = "$PFEC,SDbhr,15,A*16"
    msg = pynmea2.parse(raw, check=False)
    assert isinstance(msg, nwfsc_nmea.proprietary.pfec.SDBHR)
    assert msg.value == '15'
    assert msg.status == 'A'
