import csv
import json

# Input and output file paths
input_file = '/Users/tapple/Desktop/UOL Y3/Sem 1/Advanced Web Development/Midterm/BYT/brewyourtech/byt/static/byt/csv/Laptops.csv' 
output_file = 'Laptops.json'  # The fixture file to be created

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
        
        # Safeguard: Remove the 'index' column if it exists
        row.pop('index', None)

        try:
            # Append a JSON object for each row
            data.append({
                "model": "byt.Laptop",  # Replace `your_app_name` with the name of your app
                "pk": None,  # Optionally set this to a unique value if needed
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
                    "year_of_warranty": int(row['year_of_warranty']) if row['year_of_warranty'] else None,  # Include year_of_warranty
                }
            })
            passed_checks += 1  # Increment passed checks count
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

# Skipping row due to error: invalid literal for int() with base 10: 'No information'
# Skipping row due to error: invalid literal for int() with base 10: 'No information'
# Total rows processed: 991
# Rows that passed the checks: 973
# Fixture file Laptops.json created successfully!