from pynmea2 import ProprietarySentence, NMEASentence

class FECSentence(ProprietarySentence):
    """
    Base class for Furuno proprietary sentences ($PFEC)
    """
    def __init__(self, manufacturer, data):
        super(FECSentence, self).__init__(manufacturer, data)

class GPATT(FECSentence):
    """
    Furuno Attitude Data
    $PFEC,GPatt,hhh.h,pp.p,rr.r
    """
    fields = (
        ("Sentence ID", "id"),
        ("Heading", "heading"),
        ("Pitch", "pitch"),
        ("Roll", "roll"),
    )

class GPHVE(FECSentence):
    """
    Furuno Heave Data
    $PFEC,GPhve,xx.xxx,Status
    """
    fields = (
        ("Sentence ID", "id"),
        ("Heave", "heave"),
        ("Status", "status"),
    )

class SDBHR(FECSentence):
    """
    Furuno Bottom Hardness
    $PFEC,SDbhr,val,stat
    """
    fields = (
        ("Sentence ID", "id"),
        ("Value", "value"),
        ("Status", "status"),
    )

class DRTNM(FECSentence):
    """ Radar Target Number """
    fields = (("Sentence ID", "id"), ("Target Number", "target_num"))

class DRTSM(FECSentence):
    """ Radar Target Status """
    fields = (("Sentence ID", "id"), ("Target Status", "target_status"))

class HDCOM(FECSentence):
    """ Heading Command """
    fields = (("Sentence ID", "id"), ("Command", "command"))

class PIREQ(FECSentence):
    """ Data Request """
    fields = (("Sentence ID", "id"), ("Request", "request"))

class PIDAT(FECSentence):
    """ Data Response """
    fields = (("Sentence ID", "id"), ("Data", "data"))

class GPWPL(FECSentence):
    """ Waypoint Location """
    fields = (("Sentence ID", "id"), ("Data", "data"))

class GPRTC(FECSentence):
    """ Real-Time Clock """
    fields = (("Sentence ID", "id"), ("Data", "data"))

class GPXFR(FECSentence):
    """ Almanac Transfer """
    fields = (("Sentence ID", "id"), ("Data", "data"))
