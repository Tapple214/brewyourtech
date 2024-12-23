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
                    "company": row['Company'],
                    "product": row['Product'],
                    "type_name": row['TypeName'],
                    "inches": float(row['Inches']) if row['Inches'] else 0.0,
                    "ram": int(row['Ram']) if row['Ram'].isdigit() else 0,
                    "operating_system": row['OS'],
                    "weight": float(row['Weight']) if row['Weight'] else 0.0,
                    "price_euros": float(row['Price_euros']) if row['Price_euros'] else 0.0,
                    "screen_type": row['Screen'],
                    "screen_width": int(row['ScreenW']) if row['ScreenW'].isdigit() else 0,
                    "screen_height": int(row['ScreenH']) if row['ScreenH'].isdigit() else 0,
                    "touchscreen": row['Touchscreen'] == 'Yes',
                    "ips_panel": row['IPSpanel'] == 'Yes',
                    "retina_display": row['RetinaDisplay'] == 'Yes',
                    "cpu_company": row['CPU_company'],
                    "cpu_frequency": float(row['CPU_freq']) if row['CPU_freq'] else 0.0,
                    "cpu_model": row['CPU_model'],
                    "primary_storage_capacity": row['PrimaryStorage'],  # Treat as string
                    "secondary_storage_capacity": int(row['SecondaryStorage']) if row['SecondaryStorage'].isdigit() else None,
                    "primary_storage_type": row['PrimaryStorageType'],
                    "secondary_storage_type": row['SecondaryStorageType'] if row['SecondaryStorageType'] else None,
                    "gpu_company": row['GPU_company'],
                    "gpu_model": row['GPU_model'],
                    "gpu_full_model": row['GPU Model'],
                    "year": int(row['Year']) if row['Year'].isdigit() else 0,
                    "quarter": row['Quarter'],
                    "architecture": row['Architecture'],
                    "process_nm": int(row['Process (nm)']) if row['Process (nm)'].isdigit() else 0,
                    "cores_shaders": row['Cores (Shaders)'],
                    "base_clock_mhz": row['Base Clock (MHz)'] if row['Base Clock (MHz)'].isdigit() else row['Base Clock (MHz)'],  # Treat as string for mixed formats
                    "memory_size_gb": row['Memory Size (GB)'],
                    "memory_type": row['Memory Type'] if row['Memory Type'] else None,
                    "memory_bus_width_bits": int(row['Memory Bus Width (bits)']) if row['Memory Bus Width (bits)'].isdigit() else None,
                    "tdp_w": row['TDP (W)'] if row['TDP (W)'].isdigit() else row['TDP (W)'],  # Treat as string for mixed formats
                    "integrated_gpu": row['Integrated GPU'] == 'Yes',
                    "mobile_gpu": row['Mobile GPU'] == 'Yes',
                    "quantity": int(row['QTY']) if row['QTY'].isdigit() else 0
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
print(f"Total rows processed: {total_rows}") # Total rows processed: 1275
print(f"Rows that passed the checks: {passed_checks}") # Rows that passed the checks: 1275
print(f"Fixture file {output_file} created successfully!") # Fixture file Laptops.json created successfully!

### END ###