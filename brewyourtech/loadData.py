import csv
import json
import subprocess

# To run python loadData.py command

def convertCSVtoJSON(input_file, output_file, device):
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
                if device == "phone":
                    # Pre-processed 7127 entries and removed entiries with release dates earlier than 2016 as it is outdated           
                    launch_year = int(float(row['Launch Expected Year'])) if row['Launch Expected Year'] else 0
                    # Skip rows with release years below 2016 as they are typically discontinues
                    if launch_year < 2016:
                        continue

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
                    # +1 increment to entry successfully added to fixture
                    passed_checks += 1 
                elif device == "camera":
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
                elif device == "laptop":
                    # Remove/Pop the 'index' column if it exists
                    row.pop('index', None)
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
                elif device == "tablet":
                    # Remove/Pop the 'index' column if it exists
                    row.pop('index', None)
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
                else: 
                    print("Incorrect device name found! Please try again!")
            except (ValueError, KeyError) as e:
                print(f"Skipping row due to error: {e}")
                continue
            
        # Print counts; For display and tracking purposes 
        print(f"\nTotal rows processed: {total_rows}")
        print(f"Rows that passed the checks: {passed_checks}")
        
    # Save the processed data to a JSON file
    with open(output_file, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False, indent=4)

def loadDataToDB():
    load_data_commands = [
        "python manage.py loaddata json/Tablets.json",
        "python manage.py loaddata json/Phones.json",
        "python manage.py loaddata json/Laptops.json",
        "python manage.py loaddata json/Cameras.json"
    ]
    try:
        for command in load_data_commands:
            print(f"\nRunning command: {command}")
            subprocess.run(command, shell=True, check=True)
    except (ValueError, KeyError) as e:
            print(f"Error running command", command)
    

def main():
    phone_input_file = 'byt/static/byt/csv/Phones.csv' 
    phone_output_file = 'json/Phones.json' 
    camera_input_file = 'byt/static/byt/csv/Cameras.csv' 
    camera_output_file = 'json/Cameras.json' 
    tablet_input_file = 'byt/static/byt/csv/Tablets.csv'
    tablet_output_file = 'json/Tablets.json' 
    laptop_input_file = 'byt/static/byt/csv/Laptops.csv' 
    laptop_output_file = 'json/Laptops.json' 

    convertCSVtoJSON(phone_input_file, phone_output_file, "phone")
    print(f"Fixture file {phone_output_file} created successfully!")

    convertCSVtoJSON(camera_input_file, camera_output_file, "camera")
    print(f"Fixture file {camera_output_file} created successfully!")

    convertCSVtoJSON(tablet_input_file, tablet_output_file, "tablet")
    print(f"Fixture file {tablet_output_file} created successfully!")

    convertCSVtoJSON(laptop_input_file, laptop_output_file, "laptop")
    print(f"Fixture file {laptop_output_file} created successfully!")

    loadDataToDB()
    print("\nAll data suceessfully loaded into db!")

main()