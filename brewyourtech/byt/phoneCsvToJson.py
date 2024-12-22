### START ###

import csv
import json

# A CSV to fixture (JSON) converter for the Phones.csv

# Input and output file paths; Output will appear in the same directory as input
input_file = '/Users/tapple/Desktop/UOL Y3/Sem 1/Advanced Web Development/Midterm/BYT/brewyourtech/byt/static/byt/csv/Phones.csv' 
output_file = 'Phones.json' 

# Counters; For display and tracking purposes 
total_rows = 0
passed_checks = 0

# Open the CSV file
# Read its contents
with open(input_file, newline='', encoding='utf-8') as csvfile:
    # Uses the header row for keys
    reader = csv.DictReader(csvfile) 
    data = []

    for row in reader:
        # Start row count in increments of 1
        total_rows += 1 
        try:
            # Pre-processed 7127 entries and removed entiries with release dates earlier than 2016 as it is outdated           
            launch_year = int(float(row['Launch Expected Year'])) if row['Launch Expected Year'] else 0
            
            # Skip rows with release years below 2016 as they are typically discontinues
            if launch_year < 2016:
                continue

            # +1 increment to entry successfully added to fixture
            passed_checks += 1  

            # Append a JSON object for each row
            data.append({
                "model": "byt.Phone", 
                "pk": None,  
                "fields": {
                    "url": row['URL'],
                    "brand": row['Brand'],
                    "model": row['Model'],
                    "hits": int(row['Hits']) if row['Hits'] else 0,  
                    "became_fan": int(row['Became Fan']) if row['Became Fan'] else 0,  
                    "launch_expected_year": launch_year,
                    "height_mm": float(row['Height (mm)']) if row['Height (mm)'] else 0.0,
                    "width_mm": float(row['Width (mm)']) if row['Width (mm)'] else 0.0,
                    "thickness_mm": float(row['Thickness (mm)']) if row['Thickness (mm)'] else 0.0,
                    "body_weight_g": float(row['Body_Weight (g)']) if row['Body_Weight (g)'] else 0.0,
                    "display_type": row['Display_Type'] if row['Display_Type'] else "Unknown",
                    "pixels_x": int(float(row['Pixels_X'])) if row['Pixels_X'] else 0,
                    "pixels_y": int(float(row['Pixels_Y'])) if row['Pixels_Y'] else 0,
                    "display_size_inches": float(row['Display Size (inches)']) if row['Display Size (inches)'] else 0.0,
                    "screen_to_body_ratio": float(row['Screen_to_Body_Ratio (%)']) if row['Screen_to_Body_Ratio (%)'] else 0.0,
                    "ram_gb": float(row['RAM (GB)']) if row['RAM (GB)'] else 0.0,
                    "main_camera_single_mp": float(row['Main Camera_Single (MP)']) if row['Main Camera_Single (MP)'] else None,
                    "selfie_camera_single_mp": float(row['Selfie camera_Single (MP)']) if row['Selfie camera_Single (MP)'] else None,
                    "sound_3_5mm_jack": row['Sound_3.5mm jack'] == '1.0',
                    "comms_bluetooth": row['Comms_Bluetooth'] if row['Comms_Bluetooth'] else "Unknown",
                    "comms_nfc": row['Comms_NFC'] == '1.0',
                    "battery_capacity_mah": int(float(row['Battery_Capacity (mAh)'])) if row['Battery_Capacity (mAh)'] else 0,
                    "price_usd": float(row['Price in USD']) if row['Price in USD'] else 0.0,
                }
            })
        except (ValueError, KeyError) as e:
            print(f"Skipping row due to error: {e}")
            continue

# Save the processed data to a JSON file
with open(output_file, 'w', encoding='utf-8') as jsonfile:
    json.dump(data, jsonfile, ensure_ascii=False, indent=4)

# Step 1: RUN python byt/phoneCsvToJson.py
# Step 2: Move the output file into fixtures
# Step 3: RUN python manage.py loaddata Phones.json

# Print counts; For display and tracking purposes 
print(f"Total rows processed: {total_rows}") # Total rows processed: 7127
print(f"Rows that passed the checks: {passed_checks}") # Rows that passed the checks: 3072
print(f"Fixture file {output_file} created successfully!") # Fixture file PhonesJson.json created successfully!

# 4055 entries were skipped their launch year being < 2016

### END ###


