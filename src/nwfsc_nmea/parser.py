import pynmea2
from .proprietary.simrad import (
    PSIMP, PSIMTV80, PSIMDE, PSIMH1, PSIMH2, PSIMS1, PSIMS2, PSIMTM, PSIMMW,
    PSIMTE, DBS, MTW, HFB, HB2, TDS, TS2, TPT, TPC, TFI, DAD, GLL
)
from .proprietary.pfec import (
    GPATT, GPHVE, SDBHR, DRTNM, DRTSM, HDCOM, PIREQ, PIDAT, GPWPL, GPRTC, GPXFR
)
from .proprietary.furuno import SDBB, SDDBT

def register_sentences():
    """
    Register proprietary sentences with pynmea2.
    """
    # 1. $PSIM* Proprietary Sentences (Manufacturer SIM)
    if 'SIM' not in pynmea2.ProprietarySentence.sentence_types:
        pynmea2.ProprietarySentence.sentence_types['SIM'] = {}
        
    simrad_map = pynmea2.ProprietarySentence.sentence_types['SIM']
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
    # These are registered in the main Sentence registry because they use standard Talker IDs
    ii_defs = {
        'DBS': DBS, 'HFB': HFB, 'HB2': HB2, 'TDS': TDS, 'TS2': TS2,
        'TPT': TPT, 'TPC': TPC, 'TFI': TFI, 'DAD': DAD, 'MTW': MTW, 'GLL': GLL
    }
    for stype, scls in ii_defs.items():
        pynmea2.Sentence.sentence_types[stype] = scls

    # 3. Furuno Sonar (SD* talker)
    pynmea2.Sentence.sentence_types['BB']  = SDBB
    pynmea2.Sentence.sentence_types['DBT'] = SDDBT

    # 4. Furuno (Manufacturer FEC)
    if 'FEC' not in pynmea2.ProprietarySentence.sentence_types:
        pynmea2.ProprietarySentence.sentence_types['FEC'] = {}
        
    fec_map = pynmea2.ProprietarySentence.sentence_types['FEC']
    fec_map['GPATT'] = GPATT
    fec_map['GPHVE'] = GPHVE
    fec_map['SDBHR'] = SDBHR
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
