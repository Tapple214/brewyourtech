### START ###

import csv
import json

# A CSV to fixture (JSON) converter for the Laptops.csv

# Input and output file paths; Output will appear in the same directory as input
input_file = '/Users/tapple/Desktop/UOL Y3/Sem 1/Advanced Web Development/Midterm/BYT/brewyourtech/byt/static/byt/csv/Laptops.csv' 
output_file = 'Laptops.json' 

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
        
        # Remove/Pop the 'index' column if it exists
        row.pop('index', None)

        try:
            # Append a JSON object for each row
            data.append({
                "model": "byt.Laptop",  
                "pk": None,  
                "fields": {
                    "brand": row['brand'],
                    "model": row['Model'],
                    "price": float(row['Price']) if row['Price'] else 0.0,
                    "rating": float(row['Rating']) if row['Rating'] else 0.0,
                    "processor_brand": row['processor_brand'],
                    "processor_tier": row['processor_tier'],
                    "num_cores": int(row['num_cores']) if row['num_cores'] else 0,
                    "num_threads": int(row['num_threads']) if row['num_threads'] else 0,
                    "ram_memory": float(row['ram_memory']) if row['ram_memory'] else 0.0,
                    "primary_storage_type": row['primary_storage_type'],
                    "primary_storage_capacity": int(row['primary_storage_capacity']) if row['primary_storage_capacity'] else 0,
                    "secondary_storage_type": row['secondary_storage_type'] if row['secondary_storage_type'] else None,
                    "secondary_storage_capacity": int(row['secondary_storage_capacity']) if row['secondary_storage_capacity'] else None,
                    "gpu_brand": row['gpu_brand'],
                    "gpu_type": row['gpu_type'],
                    "is_touch_screen": row['is_touch_screen'] == 'True',
                    "display_size": float(row['display_size']) if row['display_size'] else 0.0,
                    "resolution_width": int(row['resolution_width']) if row['resolution_width'] else 0,
                    "resolution_height": int(row['resolution_height']) if row['resolution_height'] else 0,
                    "operating_system": row['OS'],
                    "year_of_warranty": int(row['year_of_warranty']) if row['year_of_warranty'] else None,  
                }
            })
            # +1 increment to entry successfully added to fixture
            passed_checks += 1  
        except (ValueError, KeyError) as e:
            print(f"Skipping row due to error: {e}")
            continue

# Save the processed data to a JSON file
with open(output_file, 'w', encoding='utf-8') as jsonfile:# Uses the header row for keys
    json.dump(data, jsonfile, ensure_ascii=False, indent=4)

# Step 1: RUN python byt/laptopCsvToJson.py
# Step 2: Move the output file into fixtures
# Step 3: RUN python manage.py loaddata Laptops.json

# Print counts; For display and tracking purposes 
print(f"Total rows processed: {total_rows}") # Total rows processed: 991
print(f"Rows that passed the checks: {passed_checks}") # Rows that passed the checks: 973
print(f"Fixture file {output_file} created successfully!") # Fixture file Laptops.json created successfully!

# 21 entries were skipped due to error: invalid literal for int() with base 10: 'No information'

### END ###


