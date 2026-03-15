import os
import duckdb
import pathlib
import shutil
import json
import pynmea2
import nwfsc_nmea  # Important to register proprietary sentences

# --- LOCAL CONFIGURATION ---
SOURCE_DIR = r"./data"
OUTPUT_DIR = r"./data/parquet"
TEST_MODE_LIMIT = 0

def parse_nmea_to_json(raw_string):
    """
    DuckDB Python UDF to parse NMEA strings using pynmea2 and nwfsc-nmea.
    """
    if not raw_string:
         return json.dumps({"type": "NONE"})
         
    # Handle known SBE subset
    if raw_string.startswith('=SBE38'):
         # Basic extraction for SBE38
         import re
         match = re.search(r'([-+]?[0-9]*\.?[0-9]+)', raw_string)
         temp = match.group(1) if match else None
         return json.dumps({"type": "SBE38", "temp": temp})
    elif raw_string.startswith('=SBE'):
         return json.dumps({"type": "SBE_OTHER"})
         
    try:
        msg = pynmea2.parse(raw_string, check=False)
        # Convert parsed attributes to dict
        data = {"type": type(msg).__name__}
        
        # We can extract all fields defined in the sentence object
        for field in msg.fields:
            if hasattr(msg, field[1]):
                 data[field[1]] = getattr(msg, field[1])
                 
        return json.dumps(data)
    except Exception as e:
        return json.dumps({"type": "ERROR", "error": str(e), "raw": raw_string})

def run_local_conversion():
    source_path = pathlib.Path(SOURCE_DIR)
    output_path = pathlib.Path(OUTPUT_DIR)
    
    # We will just look at all db files in source_dir, assume one is the wheelhouse
    all_db_files = [f for f in os.listdir(SOURCE_DIR) if f.endswith('.db')]
    
    wheelhouse_file = next((f for f in all_db_files if 'wheelhouse' in f.lower()), None)
    if not wheelhouse_file:
         print(f"ERROR: Wheelhouse database not found in {SOURCE_DIR}")
         return
         
    wh_path = source_path / wheelhouse_file

    # Clean and recreate output directory
    if output_path.exists():
        shutil.rmtree(output_path)
    output_path.mkdir(parents=True, exist_ok=True)

    # Initialize DuckDB (Local file-based for stability with large data)
    db_buffer_file = output_path / "temp_processing.duckdb"
    con = duckdb.connect(database=str(db_buffer_file))

    # Register the UDF
    con.create_function("parse_nmea_to_json", parse_nmea_to_json, [str], str)

    # Attach Wheelhouse
    wh_alias = "wheelhouse"
    print(f"Attaching Wheelhouse: {wheelhouse_file}")
    con.execute(f"ATTACH '{wh_path}' AS {wh_alias} (TYPE SQLITE)")

    # Create the central table
    con.execute(f"""
        CREATE TABLE IF NOT EXISTS nmea_strings (
            survey_year INTEGER,
            vessel_name TEXT,
            vessel_code TEXT,
            vessel_id INTEGER,
            survey_computer_recorded_at TIMESTAMPTZ,
            raw_sentence TEXT,
            nmea_type TEXT,
            parsed_data JSON,
            deployed_equipment_id INTEGER,
            equipment_name TEXT,
            equipment_id INTEGER,
            operation_key TEXT,
            sensor_file_name TEXT
        )
    """)

    # Find all sensor files
    all_sensor_files = [f for f in all_db_files if 'sensors_' in f.lower()]

    if TEST_MODE_LIMIT > 0:
        print(f"TEST MODE: Processing only first {TEST_MODE_LIMIT} files.")
        sensor_files = all_sensor_files[:TEST_MODE_LIMIT]
    else:
        sensor_files = all_sensor_files

    total = len(sensor_files)
    print(f"Found {total} sensor files to process.")

    # Process each file
    for i, filename in enumerate(sensor_files, 1):
        s_path = source_path / filename
        s_alias = f"s_{i}"

        print(f"[{i}/{total}] Processing {filename}...")

        try:
            con.execute(f"ATTACH '{s_path}' AS {s_alias} (TYPE SQLITE)")

            con.execute(f"""
                INSERT INTO nmea_strings
                SELECT
                    EXTRACT(year FROM CAST(env.DATE_TIME AS TIMESTAMPTZ)) as survey_year,
                    (SELECT value FROM {wh_alias}.configuration_settings WHERE parameter = 'Vessel') as vessel_name,
                    CASE CAST((SELECT value FROM {wh_alias}.configuration_settings WHERE parameter = 'Vessel ID') AS INTEGER)
                        WHEN 8 THEN 'EX' WHEN 20 THEN 'LS' WHEN 10 THEN 'MJ' WHEN 17 THEN 'NA' ELSE 'UNKNOWN'
                    END as vessel_code,
                    CAST((SELECT value FROM {wh_alias}.configuration_settings WHERE parameter = 'Vessel ID') AS INTEGER) as vessel_id,
                    CAST(env.date_time AS TIMESTAMPTZ) as survey_computer_recorded_at,
                    env.raw_strings as raw_sentence,
                    CASE 
                        WHEN env.raw_strings LIKE '=SBE%' THEN 'SBE38'
                        ELSE regexp_extract(env.raw_strings, '^[\$@]?([A-Z0-9]{{3,8}})', 1)
                    END as nmea_type,
                    parse_nmea_to_json(env.raw_strings) as parsed_data,
                    env.deployed_equipment_id,
                    e.name as equipment_name,
                    e.equipment_id,
                    COALESCE(td.tow_number, sd.search_number, 'BETWEEN_OPS') as operation_key,
                    '{filename}' as sensor_file_name
                FROM {s_alias}.ENVIRO_NET_RAW_STRINGS env
                LEFT JOIN {wh_alias}.DEPLOYED_EQUIPMENT de ON env.deployed_equipment_id = de.deployed_equipment_id
                LEFT JOIN {wh_alias}.EQUIPMENT e ON de.equipment_id = e.equipment_id
                LEFT JOIN {wh_alias}.TOW_DETAILS td 
                    ON CAST(env.DATE_TIME AS TIMESTAMPTZ) BETWEEN CAST(td.activation_datetime AS TIMESTAMPTZ) AND CAST(td.deactivation_datetime AS TIMESTAMPTZ)
                LEFT JOIN {wh_alias}.SEARCH_DETAILS sd 
                    ON CAST(env.DATE_TIME AS TIMESTAMPTZ) BETWEEN CAST(sd.activation_datetime AS TIMESTAMPTZ) AND CAST(sd.deactivation_datetime AS TIMESTAMPTZ)
                    AND sd.elapsed_search_time IS NOT NULL
            """)
            con.execute(f"DETACH {s_alias}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")

    # Export to Hive-partitioned Parquet
    row_count = con.execute("SELECT count(*) FROM nmea_strings").fetchone()[0]
    print(f"Exporting {row_count} rows to Parquet...")

    con.execute(f"""
        COPY nmea_strings TO '{OUTPUT_DIR}' (
            FORMAT PARQUET, 
            PARTITION_BY (survey_year, vessel_name),
            OVERWRITE_OR_IGNORE 1
        )
    """)

    con.close()

    # Optional: Delete the temporary duckdb file
    if db_buffer_file.exists():
        os.remove(db_buffer_file)

    print(f"Success! Parquet files are ready in: {OUTPUT_DIR}")


if __name__ == "__main__":
    run_local_conversion()
