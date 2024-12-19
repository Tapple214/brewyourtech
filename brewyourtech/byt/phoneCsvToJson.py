import csv
import json

# Input and output file paths
input_file = '/Users/tapple/Desktop/UOL Y3/Sem 1/Advanced Web Development/Midterm/BYT/brewyourtech/byt/static/byt/csv/Phones.csv' 
output_file = 'Phones.json'  # The fixture file to be created

# Initialize counters
total_rows = 0
passed_checks = 0

# Open the CSV file and read its contents
with open(input_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)  # Automatically uses the header row for keys
    data = []

    # Process each row
    for row in reader:
        total_rows += 1  # Increment total row count
        try:
            # Extract the release year
            launch_year = int(float(row['Launch Expected Year'])) if row['Launch Expected Year'] else 0
            
            # Skip rows with release years below 2015
            if launch_year < 2015:
                continue

            passed_checks += 1  # Increment passed checks count

            # Append a JSON object for each row
            data.append({
                "model": "byt.Phone",  # Replace `your_app_name` with the name of your app
                "pk": None,  # Optionally set this to a unique value if needed
                "fields": {
                    "url": row['URL'],
                    "brand": row['Brand'],
                    "model": row['Model'],
                    "hits": int(row['Hits']) if row['Hits'] else 0,  # Default to 0 if empty
                    "became_fan": int(row['Became Fan']) if row['Became Fan'] else 0,  # Default to 0
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

# Print comparison results
print(f"Total rows processed: {total_rows}")
print(f"Rows that passed the checks: {passed_checks}")
print(f"Fixture file {output_file} created successfully!")

# RUN python byt/phoneCsvToJson.py
# then RUN python manage.py loaddata Phones.json (make sure it is in fixtures)

# Phones where I removed phones released earlier than 2015
# Total rows processed: 7127
# Rows that passed the checks: 3550
# Fixture file PhonesJson.json created successfully!