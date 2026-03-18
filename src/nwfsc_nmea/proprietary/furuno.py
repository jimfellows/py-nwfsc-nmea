from pynmea2 import TalkerSentence

class SDBB(TalkerSentence):
    """
    Furuno Sounder/Fish Finder Data
    $SDBB,depth,unit
    """
    fields = (
        ("Depth", "depth"),
        ("Unit", "unit"),
    )

class SDDBT(TalkerSentence):
    """
    Furuno Depth Below Transducer
    $SDDBT,feet,f,meters,M,fathoms,F
    """
    fields = (
        ("Depth (feet)", "depth_feet"),
        ("Feet Unit", "feet_unit"),
        ("Depth (meters)", "depth_meters"),
        ("Meters Unit", "meters_unit"),
        ("Depth (fathoms)", "depth_fathoms"),
        ("Fathoms Unit", "fathoms_unit"),
    )
