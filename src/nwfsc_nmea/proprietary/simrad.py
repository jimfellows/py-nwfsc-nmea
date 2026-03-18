from pynmea2 import ProprietarySentence, NMEASentence, TalkerSentence

class SimradSentence(ProprietarySentence):
    """
    Base class for Simrad proprietary sentences ($PSIM*)
    """
    def __init__(self, manufacturer, data):
        super(SimradSentence, self).__init__(manufacturer, data)

class PSIMP(ProprietarySentence):
    """
    Simrad Sensor Data (PS/PI/PX)
    $PSIMP,D1,tt,dd,M,U,SNo,MNo,C,V,Cr,Q,In,SL,NL,G,Cb,error
    """
    fields = (
        ("Sentence Specifier", "specifier"),
        ("Time", "time"),
        ("Date", "date"),
        ("Measurement Type", "measurement_type"),
        ("Unit", "unit"),
        ("Sensor Number", "sensor_num"),
        ("Measurement Number", "measurement_num"),
        ("Channel", "channel"),
        ("Value", "value"),
        ("Change Rate", "change_rate"),
        ("Quality", "quality"),
        ("Interference", "interference"),
        ("Signal Level", "signal_level"),
        ("Noise Level", "noise_level"),
        ("Gain", "gain"),
        ("Cable Quality", "cable_quality"),
        ("Error", "error_code"),
    )

    MEASUREMENT_TYPES = {
        "D": "Depth",
        "T": "Temperature",
        "C": "Catch",
        "B": "Bottom",
        "N": "No sensor",
        "M": "Marker",
    }

    QUALITY_STATES = {
        "0": "No connection",
        "1": "Lost pulses (predicted)",
        "2": "Reliable",
    }

    CABLE_QUALITY_STATES = {
        "0": "Not connected",
        "1": "Good",
        "2": "Short-circuited / High current",
    }

    @property
    def measurement_description(self):
        return self.MEASUREMENT_TYPES.get(self.measurement_type, f"Unknown ({self.measurement_type})")

    @property
    def quality_description(self):
        return self.QUALITY_STATES.get(self.quality, f"Unknown ({self.quality})")

    @property
    def interference_detected(self):
        return self.interference == "1"

    @property
    def cable_quality_description(self):
        return self.CABLE_QUALITY_STATES.get(self.cable_quality, f"Unknown ({self.cable_quality})")

    @property
    def has_error(self):
        return self.error_code != "0"

class PSIMTV80(ProprietarySentence):
    """
    Simrad TV80 Sensor Data
    $PSIMTV80,hhmmss,yymmdd,ddmm.hh,N,dddmm.hh,W,ddmm.hh,N,dddmm.hh,W,kk.kk,ccc.cc,hhh.hh,mmmm.m,tt,fff,ooo,vvvv.vv,qq,xxxxxx*cc
    """
    fields = (
        ("UTC Time", "timestamp"),
        ("Date", "date"),
        ("Vessel Latitude", "lat"),
        ("Vessel Latitude Direction", "lat_dir"),
        ("Vessel Longitude", "lon"),
        ("Vessel Longitude Direction", "lon_dir"),
        ("Sensor Latitude", "sensor_lat"),
        ("Sensor Latitude Direction", "sensor_lat_dir"),
        ("Sensor Longitude", "sensor_lon"),
        ("Sensor Longitude Direction", "sensor_lon_dir"),
        ("Vessel Speed (knots)", "vessel_speed"),
        ("COG (degrees)", "cog"),
        ("Heading (degrees)", "heading"),
        ("Sounder Depth (meters)", "sounder_depth"),
        ("Measurement Type", "measurement_type"),
        ("Source Location", "source_location"),
        ("Target Location", "target_location"),
        ("Value", "value"),
        ("Quality", "quality"),
        ("Sensor ID", "sensor_id"),
    )

    MEASUREMENT_TYPES = {
        "01": "Spread",
        "02": "Height",
        "03": "Depth",
        "04": "Roll",
        "05": "Pitch",
        "19": "Temperature",
        "20": "Catch",
        "21": "Bottom contact",
    }

    LOCATION_PARTS = {
        "1": "Port door",
        "2": "Starboard door / Clump",
        "7": "Headrope",
        "8": "Footrope",
        "11": "Codend 1",
        "12": "Codend 2",
        "13": "Codend 3",
        "14": "Codend 4",
        "15": "Codend 5",
        "16": "Codend 6",
        "17": "Codend 7",
        "18": "Codend 8",
    }

    @property
    def measurement_description(self):
        return self.MEASUREMENT_TYPES.get(self.measurement_type, f"Unknown ({self.measurement_type})")

    def _parse_location(self, loc_code):
        if not loc_code or len(loc_code) < 2:
            return f"Unknown ({loc_code})"
        
        trawl_id = loc_code[0]
        part_code = loc_code[1:].lstrip('0')  # Remove leading zeros for lookup
        part_desc = self.LOCATION_PARTS.get(part_code, f"Unknown part ({part_code})")
        
        return f"Trawl {trawl_id}: {part_desc}"

    @property
    def source_description(self):
        return self._parse_location(self.source_location)

    @property
    def target_description(self):
        return self._parse_location(self.target_location)

class PSIT(ProprietarySentence):
    """
    Simrad ITI Proprietary Sentences
    """
    fields = (
        ("Sentence Type", "type"),
        ("Data", "data"),
    )

class SimradIIData(TalkerSentence):
    """
    Base for Simrad @II sentences
    Note: These use @ as start delimiter
    """
    def __init__(self, talker, type, data):
        super(SimradIIData, self).__init__(talker, type, data)

class DBS(SimradIIData):
    """ @IIDBS, , , x.x, M, , """
    fields = (
        ("Empty 1", "_"),
        ("Empty 2", "_"),
        ("Depth", "depth"),
        ("Unit", "unit"),
        ("Empty 3", "_")
    )

class MTW(TalkerSentence):
    """ $IIMTW, xx.x, C """
    fields = (
        ("Temperature", "temperature"),
        ("Unit", "unit")
    )

class HFB(SimradIIData):
    """ @IIHFB, x.x, M, y.y, M """
    fields = (
        ("Opening", "opening"),
        ("Opening Unit", "opening_unit"),
        ("Height", "height"),
        ("Height Unit", "height_unit")
    )

class HB2(HFB):
    """ @IIHB2 - Same as HFB for Trawl 2 """
    pass

class TDS(SimradIIData):
    """ @IITDS, x.x, M """
    fields = (
        ("Spread", "spread"),
        ("Unit", "unit")
    )

class TS2(TDS):
    """ @IITS2 - Same as TDS for Trawl 2 """
    pass

class PSIMCombined(ProprietarySentence):
    """ Base for $PSIMDE, H1, H2, S1, S2, TM """
    fields = (
        ("Slant Range", "slant_range"),
        ("Slant Range Unit", "slant_range_unit"),
        ("Horizontal Range", "horizontal_range"),
        ("Horizontal Range Unit", "horizontal_range_unit"),
        ("True Bearing", "true_bearing"),
        ("True Bearing Unit", "true_bearing_unit"),
        ("Measurement Value", "measurement_value"),
        ("Value Unit", "value_unit"),
        ("Timestamp", "timestamp")
    )

class PSIMDE(PSIMCombined): pass
class PSIMH1(PSIMCombined): pass
class PSIMH2(PSIMCombined): pass
class PSIMS1(PSIMCombined): pass
class PSIMS2(PSIMCombined): pass
class PSIMTM(PSIMCombined): pass
class PSIMH2(PSIMCombined): pass

class PSIMMW(ProprietarySentence):
    """
    Simrad ITI Middle Weight / Clump (Twin Rig)
    $PSIMMW,xxxx.x,M,xxxx.x,M,yyy.y,T,z.z,M,y.y,D,c,hhmmss
    """
    fields = (
        ("Slant Range", "slant_range"),
        ("Slant Range Unit", "slant_range_unit"),
        ("Horizontal Range", "horizontal_range"),
        ("Horizontal Range Unit", "horizontal_range_unit"),
        ("True Bearing", "true_bearing"),
        ("True Bearing Unit", "true_bearing_unit"),
        ("Deviation", "deviation"),
        ("Deviation Unit", "deviation_unit"),
        ("Starboard Angle", "starboard_angle"),
        ("Angle Unit", "angle_unit"),
        ("Status", "status"),
        ("Timestamp", "timestamp"),
    )

class TPT(SimradIIData):
    """ @IITPT, xxxx, M, yyy, P, zzzz.z, M """
    fields = (
        ("Horizontal Range", "horizontal_range"),
        ("Horizontal Range Unit", "horizontal_range_unit"),
        ("True Bearing", "true_bearing"),
        ("Bearing Type", "bearing_type"),
        ("Depth", "depth"),
        ("Depth Unit", "depth_unit"),
    )

class TPC(SimradIIData):
    """ @IITPC, x.M, y, M, z, M """
    fields = (
        ("Distance Centerline", "x_dist"),
        ("X Unit", "x_unit"),
        ("Distance Transducer", "y_dist"),
        ("Y Unit", "y_unit"),
        ("Depth", "z_depth"),
        ("Z Unit", "z_unit"),
    )

class TFI(SimradIIData):
    """ @IITFI, x, y, z (Catch Sensors) """
    fields = (
        ("Catch 1", "catch_1"),
        ("Catch 2", "catch_2"),
        ("Catch 3", "catch_3"),
    )

class DAD(SimradIIData):
    """ @IIDAD, x.x, M, x.x, M (Ascend/Descend) """
    fields = (
        ("Depth", "depth"),
        ("Depth Unit", "depth_unit"),
        ("Rate", "rate"),
        ("Rate Unit", "rate_unit"),
    )

class GLL(NMEASentence):
    """ $IIGLL - Trawl Lat/Lon """
    fields = (
        ("Latitude", "lat"),
        ("Latitude Direction", "lat_dir"),
        ("Longitude", "lon"),
        ("Longitude Direction", "lon_dir"),
        ("Timestamp", "timestamp"),
        ("Status", "status"),
    )

class PSIMTE(ProprietarySentence):
    """
    Simrad ITI Trawl Eye Echo
    $PSIMTE,xx%y...a,x.x, ,Gx,gx, Vx.x
    """
    fields = (
        ("Echo Data", "echo_data"),
        ("Range", "detection_range"),
        ("Range Unit", "range_unit"),
        ("Hardware Gain", "hardware_gain"),
        ("Software Gain", "software_gain"),
        ("Velocity", "velocity"),
    )
