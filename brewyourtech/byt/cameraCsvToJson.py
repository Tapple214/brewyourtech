### START ###

import csv
import json

# A CSV to fixture (JSON) converter for the Cameras.csv

# Input and output file paths; Output will appear in the same directory as input
input_file = '/Users/tapple/Desktop/UOL Y3/Sem 1/Advanced Web Development/Midterm/BYT/brewyourtech/byt/static/byt/csv/Cameras.csv' 
output_file = 'Cameras.json' 

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
            # Append a JSON object for each row
            data.append({
                "model": "byt.Camera", 
                "pk": None,  
                "fields": {
                    "model": row['Model'],
                    "release_date": int(row['Release date']) if row['Release date'] else None,
                    "max_resolution": int(row['Max resolution']) if row['Max resolution'] else 0,
                    "low_resolution": int(row['Low resolution']) if row['Low resolution'] else 0,
                    "effective_pixels": float(row['Effective pixels']) if row['Effective pixels'] else 0.0,
                    "zoom_wide": int(row['Zoom wide (W)']) if row['Zoom wide (W)'] else 0,
                    "zoom_tele": int(row['Zoom tele (T)']) if row['Zoom tele (T)'] else 0,
                    "normal_focus_range": int(row['Normal focus range']) if row['Normal focus range'] else None,
                    "macro_focus_range": int(row['Macro focus range']) if row['Macro focus range'] else None,
                    "storage_included": int(row['Storage included']) if row['Storage included'] else 0,
                    "weight": int(row['Weight (inc. batteries)']) if row['Weight (inc. batteries)'] else 0,
                    "dimensions": row['Dimensions'] if row['Dimensions'] else "Unknown",
                    "price": float(row['Price']) if row['Price'] else 0.0,
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

# Step 1: RUN python byt/cameraCsvToJson.py
# Step 2: Move the output file into fixtures
# Step 3: RUN python manage.py loaddata Cameras.json

# Print counts; For display and tracking purposes 
print(f"Total rows processed: {total_rows}") # Total rows processed: 1038
print(f"Rows that passed the checks: {passed_checks}") # Rows that passed the checks: 1038
print(f"Fixture file {output_file} created successfully!") # Fixture file Cameras.json created successfully!

### END ###
