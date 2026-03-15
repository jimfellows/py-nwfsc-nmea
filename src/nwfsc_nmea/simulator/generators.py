import datetime
import math
from .kinematics import VesselState

def calc_nmea_checksum(sentence: str) -> str:
    """Calculates the NMEA checksum for a given sentence (without $ or *)."""
    calc = 0
    for char in sentence:
        calc ^= ord(char)
    return f"{calc:02X}"

def wrap_nmea(sentence: str, prefix: str = "$") -> str:
    return f"{prefix}{sentence}*{calc_nmea_checksum(sentence)}"

class NMEAGenerator:
    def generate(self, state: VesselState) -> list:
        raise NotImplementedError

class StandardGenerator(NMEAGenerator):
    """ Generates Standard NMEA 0183 (GGA, RMC, HDT, DPT) """
    def generate(self, state: VesselState) -> list:
        now = datetime.datetime.utcnow()
        time_str = now.strftime("%H%M%S.%f")[:-4]
        date_str = now.strftime("%d%m%y")
        
        lat_h = abs(state.lat)
        lat_deg = int(lat_h)
        lat_min = (lat_h - lat_deg) * 60
        lat_dir = 'N' if state.lat >= 0 else 'S'
        lat_str = f"{lat_deg:02d}{lat_min:07.4f}"
        
        lon_h = abs(state.lon)
        lon_deg = int(lon_h)
        lon_min = (lon_h - lon_deg) * 60
        lon_dir = 'E' if state.lon >= 0 else 'W'
        lon_str = f"{lon_deg:03d}{lon_min:07.4f}"
        
        sentences = []
        
        # Heading (HDT)
        hdt = f"HEHDT,{state.heading:05.1f},T"
        sentences.append(wrap_nmea(hdt))
        
        # Position (GGA)
        gga = f"GPGGA,{time_str},{lat_str},{lat_dir},{lon_str},{lon_dir},1,08,0.9,0.0,M,0.0,M,,"
        sentences.append(wrap_nmea(gga))
        
        # Recommended Min Specific GPS/TRANSIT Data (RMC)
        rmc = f"GPRMC,{time_str},A,{lat_str},{lat_dir},{lon_str},{lon_dir},{state.speed_knots:05.1f},{state.heading:05.1f},{date_str},,,A"
        sentences.append(wrap_nmea(rmc))
        
        # Depth (DPT)
        dpt = f"SDDPT,{state.depth_meters:.1f},0.0,100.0"
        sentences.append(wrap_nmea(dpt))
        
        return sentences

class SimradGenerator(NMEAGenerator):
    """ Generates Proprietary Simrad / ITI NMEA sentences """
    def generate(self, state: VesselState) -> list:
        now = datetime.datetime.utcnow()
        time_str = now.strftime("%H%M%S")
        date_str = now.strftime("%d%m%y")
        
        sentences = []
        
        # PSIMP,D1 - Depth from ITI
        psimp = f"PSIMP,D1,{time_str},{date_str},D,M,1,10,1,{state.trawl_depth:.1f},0.1,2,0,45,15,20,1,0"
        sentences.append(wrap_nmea(psimp))
        
        # PSIMTV80 - Trawl Velocity 80
        tv80 = f"PSIMTV80,{time_str},{date_str},4736.12,N,12220.45,W,4736.12,N,12220.45,W,{state.speed_knots:.2f},{state.heading:.2f},{state.heading+5:.2f},{state.trawl_distance:.1f},01,a01,b02,{state.trawl_door_spread:.2f},10,{time_str}"
        sentences.append(wrap_nmea(tv80))
        
        # ITI Legacy @II
        # DBS Depth Below Surface
        dbs = f"IIDBS,,,{state.depth_meters:.1f},M,,"
        sentences.append(wrap_nmea(dbs, prefix="@"))
        
        # MTW Water Temp
        mtw = f"IIMTW,{state.water_temp_c:.1f},C"
        sentences.append(wrap_nmea(mtw, prefix="@"))
        
        # HFB Headrope to Footrope
        hfb = f"IIHFB,{state.headrope_height:.1f},M,{(state.headrope_height+2):.1f},M"
        sentences.append(wrap_nmea(hfb, prefix="@"))
        
        return sentences

class FurunoGenerator(NMEAGenerator):
    """ Generates Proprietary Furuno (FEC) sentences """
    def generate(self, state: VesselState) -> list:
        sentences = []
        
        # Pitch and Roll
        gpatt = f"PFEC,GPatt,{state.heading:05.1f},{state.pitch:04.1f},{state.roll:04.1f}"
        sentences.append(wrap_nmea(gpatt))
        
        # Heave
        gphve = f"PFEC,GPhve,{state.heave:.3f},A"
        sentences.append(wrap_nmea(gphve))
        
        # SDBB / SDDBT (Fishfinder depth)
        sdbb = f"SDBB,{state.depth_meters:.1f},M"
        sentences.append(wrap_nmea(sdbb))
        
        feet = state.depth_meters * 3.28084
        fathoms = state.depth_meters * 0.5468066
        sddbt = f"SDDBT,{feet:.1f},f,{state.depth_meters:.1f},M,{fathoms:.1f},F"
        sentences.append(wrap_nmea(sddbt))
        
        return sentences
