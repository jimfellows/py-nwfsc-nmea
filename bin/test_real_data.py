import sqlite3
import pynmea2
import nwfsc_nmea
from collections import Counter
import os
import sys

# Default path to the database
DEFAULT_DB = r"c:\Users\jim-f\dev\py-nwfsc-nmea\data\sensors_20250520.db"

def run_report(db_path=DEFAULT_DB, limit=None):
    if not os.path.exists(db_path):
        print(f"Error: Database not found at {db_path}")
        return

    print(f"Connecting to {db_path}...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    query = "SELECT RAW_STRINGS FROM ENVIRO_NET_RAW_STRINGS"
    if limit:
        query += f" LIMIT {limit}"
    else:
        # We'll default to a large enough chunk if not specified, 
        # or process all if they want the full report
        pass
        
    cursor.execute(query)

    stats = Counter()
    unrecognized = Counter()
    errors = Counter()
    
    print("Processing rows (this may take a minute for millions of rows)...")
    
    count = 0
    while True:
        rows = cursor.fetchmany(20000)
        if not rows:
            break
            
        for (raw,) in rows:
            count += 1
            if count % 200000 == 0:
                print(f"  Processed {count} rows...")
                
            if not raw or not raw.strip():
                continue
            
            # Cleanup
            raw_clean = raw.strip()
            
            # Find start of sentence
            start_idx = -1
            for char in ['$', '!', '@']:
                idx = raw_clean.find(char)
                if idx != -1:
                    if start_idx == -1 or idx < start_idx:
                        start_idx = idx
            
            if start_idx == -1:
                stats["No NMEA Start"] += 1
                continue
                
            raw_clean = raw_clean[start_idx:]
            
            try:
                msg = pynmea2.parse(raw_clean, check=False)
                sentence_type = type(msg).__name__
                stats[sentence_type] += 1
                
                # Check for "generic" parses that indicate missing subclass
                if sentence_type in ['Sentence', 'ProprietarySentence']:
                   # Get the identifier (e.g., $GPMSG or $PSIMTV80)
                   identifier = raw_clean.split(',')[0].split('*')[0]
                   unrecognized[identifier] += 1
                   
            except Exception as e:
                errors[f"{type(e).__name__}"] += 1

    conn.close()

    # Print Report
    print("\n" + "="*60)
    print("NWFSC NMEA PACKAGE - REAL WORLD DATA REPORT")
    print("="*60)
    print(f"Total entries analyzed: {count}")
    
    print("\n[Parsed Sentence Types (Top 20)]")
    # Sort by count desc
    for stype, scount in sorted(stats.items(), key=lambda x: x[1], reverse=True)[:20]:
        print(f"  {stype:25}: {scount}")
        
    if unrecognized:
        print("\n[Potential Unrecognized Sentences/Identifiers]")
        print("These were parsed as generic types; consider adding specific support.")
        for ident, ucount in sorted(unrecognized.items(), key=lambda x: x[1], reverse=True)[:20]:
            print(f"  {ident:25}: {ucount}")
            
    if errors:
        print("\n[Parsing Exceptions]")
        for err, ecount in sorted(errors.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {err:50}: {ecount}")
            
    print("\n" + "="*60)

if __name__ == "__main__":
    limit = None
    if len(sys.argv) > 1:
        try:
            limit = int(sys.argv[1])
        except ValueError:
            print("Usage: python test_real_data.py [row_limit]")
            sys.exit(1)
    run_report(limit=limit)
