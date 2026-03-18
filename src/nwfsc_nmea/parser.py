import pynmea2
from .proprietary.simrad import (
    PSIMP, PSIMTV80, PSIMDE, PSIMH1, PSIMH2, PSIMS1, PSIMS2, PSIMTM, PSIMMW,
    PSIMTE, DBS, MTW, HFB, HB2, TDS, TS2, TPT, TPC, TFI, DAD, GLL
)
from .proprietary.pfec import (
    GPATT, GPHVE, SDBHR, DRTNM, DRTSM, HDCOM, PIREQ, PIDAT, GPWPL, GPRTC, GPXFR
)
from .proprietary.furuno import SDBB, SDDBT

import re

def patch_pynmea2():
    """
    pynmea2's regex strictly expects 5 character standard sentence headers (2 talker + 3 type).
    Some Furuno sentences like $SDBB have 4 characters (2 talker + 2 type).
    We monkey-patch the NMEASentence patterns to support 2 AND 3 character types.
    """
    pattern = pynmea2.NMEASentence.sentence_re.pattern
    pattern = pattern.replace(r'(\w{2}\w{3},)', r'(\w{2}\w{2,3},)')
    pattern = pattern.replace(r'^\s*\$?', r'^\s*[$@!]?')
    pynmea2.NMEASentence.sentence_re = re.compile(pattern, re.X | re.IGNORECASE)
    pynmea2.NMEASentence.talker_re = re.compile(r'^(?P<talker>\w{2})(?P<sentence>\w{2,3}),$')

patch_pynmea2()

class SIMRouter:
    """
    Router to dynamically instantiate the correct proprietary subtype for SIM.
    pynmea2 expects a class here, not a dict. We inspect data[0] to find the subtype.
    """
    subtype_map = {}
    
    def __new__(cls, manufacturer, data):
        subtype = data[0] if data else ''
        subcls = cls.subtype_map.get(subtype, pynmea2.ProprietarySentence)
        return subcls(manufacturer, data)

class FECRouter:
    """
    Router to dynamically instantiate the correct proprietary subtype for FEC.
    """
    subtype_map = {}
    
    def __new__(cls, manufacturer, data):
        subtype = data[0] if data else ''
        subcls = cls.subtype_map.get(subtype, pynmea2.ProprietarySentence)
        return subcls(manufacturer, data)

def register_sentences():
    """
    Register proprietary sentences with pynmea2.
    """
    # 1. $PSIM* Proprietary Sentences (Manufacturer SIM)
    pynmea2.ProprietarySentence.sentence_types['SIM'] = SIMRouter
    simrad_map = SIMRouter.subtype_map
    simrad_map['P']    = PSIMP
    simrad_map['TV80'] = PSIMTV80
    simrad_map['DE']   = PSIMDE
    simrad_map['H1']   = PSIMH1
    simrad_map['H2']   = PSIMH2
    simrad_map['S1']   = PSIMS1
    simrad_map['S2']   = PSIMS2
    simrad_map['TM']   = PSIMTM
    simrad_map['MW']   = PSIMMW
    simrad_map['TE']   = PSIMTE

    # 2. @II* and $II* Sentences
    ii_defs = {
        'DBS': DBS, 'HFB': HFB, 'HB2': HB2, 'TDS': TDS, 'TS2': TS2,
        'TPT': TPT, 'TPC': TPC, 'TFI': TFI, 'DAD': DAD, 'MTW': MTW, 'GLL': GLL
    }
    for stype, scls in ii_defs.items():
        pynmea2.TalkerSentence.sentence_types[stype] = scls

    # 3. Furuno Sonar (SD* talker)
    pynmea2.TalkerSentence.sentence_types['BB']  = SDBB
    pynmea2.TalkerSentence.sentence_types['DBT'] = SDDBT

    # 4. Furuno (Manufacturer FEC)
    pynmea2.ProprietarySentence.sentence_types['FEC'] = FECRouter
    fec_map = FECRouter.subtype_map
    fec_map['GPatt'] = GPATT
    fec_map['GPhve'] = GPHVE
    fec_map['SDbhr'] = SDBHR
    fec_map['DRTNM'] = DRTNM
    fec_map['DRTSM'] = DRTSM
    fec_map['HDCOM'] = HDCOM
    fec_map['PIREQ'] = PIREQ
    fec_map['PIDAT'] = PIDAT
    fec_map['GPWPL'] = GPWPL
    fec_map['GPRTC'] = GPRTC
    fec_map['GPXFR'] = GPXFR

# Call registration on import
register_sentences()
