import pynmea2
import nwfsc_nmea

def main():
    print("NWFSC NMEA Parser Utility")
    print("-------------------------")
    
    sentences = [
        "$PSIMTV80,123456,130326,4736.12,N,12220.45,W,4736.12,N,12220.45,W,10.50,180.00,185.00,150.5,01,a01,b02,50.25,10,123456*12",
        "$PSIMP,D1,201856,130326,D,M,1,10,1,15.5,0.1,2,0,45,15,20,1,0*23",
        "@IIHFB,10.0,M,15.0,M*23",
        "$PFEC,GPatt,0.5,1.2,180.0*23",
        "$SDBB,12.5,M*3F"
    ]
    
    for raw in sentences:
        try:
            msg = pynmea2.parse(raw, check=False)
            print(f"\nRaw: {raw}")
            print(f"Type: {type(msg).__name__}")
            
            if hasattr(msg, 'measurement_description'):
                print(f"Description: {msg.measurement_description}")
            if hasattr(msg, 'value'):
                print(f"Value: {msg.value}")
            if hasattr(msg, 'depth'):
                print(f"Depth: {msg.depth}")
                
        except Exception as e:
            print(f"Error parsing {raw}: {e}")

if __name__ == "__main__":
    main()
