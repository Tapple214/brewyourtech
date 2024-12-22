### START ###

import csv
import json

# A CSV to fixture (JSON) converter for the Tablets.csv

# Input and output file paths; Output will appear in the same directory as input
input_file = '/Users/tapple/Desktop/UOL Y3/Sem 1/Advanced Web Development/Midterm/BYT/brewyourtech/byt/static/byt/csv/Tablets.csv'
output_file = 'Tablets.json' 


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
        
        # Remove/Pop the 'index' column if it exists
        row.pop('index', None)

        try:
            # Append a JSON object for each row
            data.append({
                "model": "byt.Tablet", 
                "pk": None, 
                "fields": {
                    "name": row['name'],
                    "brand": row['brand'],
                    "rating": float(row['rating']) if row['rating'] else 0.0,
                    "price": row['price'],  
                    "processor_brand": row['processor_brand'],
                    "num_processor": int(float(row['num_processor'])) if row['num_processor'] else 0,
                    "processor_speed": float(row['processor_speed']) if row['processor_speed'] else 0.0,
                    "ram": row['ram'], 
                    "memory_inbuilt": row['memory_inbuilt'],  
                    "battery_capacity": row['battery_capacity'],  
                    "charger": row['charger'],
                    "charging": row['charging'],
                    "display_size_inches": float(row['display_size_inches']) if row['display_size_inches'] else 0.0,
                    "pixel": row['pixel'],
                    "resolution_width": int(float(row['resolution_width'])) if row['resolution_width'] else 0,
                    "resolution_height": int(float(row['resolution_height'])) if row['resolution_height'] else 0,
                    "ppi": float(row['ppi']) if row['ppi'] else 0.0,
                    "frequency_display_hz": float(row['frequency_display_hz']) if row['frequency_display_hz'] else None,
                    "primary_front_camera": float(row['primary_front_camera']) if row['primary_front_camera'] else None,
                    "secondary_front_camera": float(row['secondry_front_camera']) if row['secondry_front_camera'] else None,
                    "primary_rear_camera": float(row['primary_rear_camera']) if row['primary_rear_camera'] else None,
                    "secondary_rear_camera": float(row['secondry_rear_camera']) if row['secondry_rear_camera'] else None,
                    "os_brand": row['os_brand'],
                    "version": row['version'],
                    "memory_card_upto": row['memory_card_upto'],  
                    "sim": row['sim'],
                    "is_5G": row['is_5G'].lower() == 'true',
                    "is_wifi": row['is_wifi'].lower() == 'true',
                }
            })
            # +1 increment to entry successfully added to fixture
            passed_checks += 1  
        except (ValueError, KeyError) as e:
            print(f"Skipping row due to error: {e}")
            continue

# Save the processed data to a JSON file
with open(output_file, 'w', encoding='utf-8') as jsonfile:
    json.dump(data, jsonfile, ensure_ascii=False, indent=4)

# Step 1: RUN python byt/tabletCsvToJson.py
# Step 2: Move the output file into fixtures
# Step 3: RUN python manage.py loaddata Tablets.json

# Print counts; For display and tracking purposes 
print(f"Total rows processed: {total_rows}") # Total rows processed: 390
print(f"Rows that passed the checks: {passed_checks}") # Rows that passed the checks: 390
print(f"Fixture file {output_file} created successfully!") # Fixture file Tablets.json created successfully!

# All data from the csv was loaded into the db

### END ###


