#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import csv
from PIL import Image
import shutil

def convert_fake_png_to_real_png():
    # File paths
    csv_file = "bad_png_list.csv"
    fake_png_dir = u"伪png"
    converted_dir = "converted_png"
    
    # Create converted directory
    if not os.path.exists(converted_dir):
        os.makedirs(converted_dir)
        print("Created directory: " + converted_dir)
    
    # Statistics
    total_files = 0
    converted_count = 0
    failed_count = 0
    skipped_count = 0
    
    # Read CSV file to get format info
    format_info = {}
    try:
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                filename = os.path.basename(row['Path'])
                format_info[filename] = row['Detect']
    except Exception as e:
        print("Failed to read CSV file: " + str(e))
        # Continue without format info
        pass
    
    # Process all files in fake png directory
    for filename in os.listdir(fake_png_dir):
        if filename.lower().endswith('.png'):
            total_files += 1
            source_path = os.path.join(fake_png_dir, filename)
            target_path = os.path.join(converted_dir, filename)
            
            # Get real format of file
            file_format = format_info.get(filename, 'Unknown')
            
            try:
                # Open image with PIL (auto-detect format)
                with Image.open(source_path) as img:
                    # Keep transparency if exists, otherwise convert to RGB
                    if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                        # Keep transparency
                        if img.mode != 'RGBA':
                            img = img.convert('RGBA')
                    else:
                        # Convert to RGB
                        img = img.convert('RGB')
                    
                    # Save as PNG format
                    img.save(target_path, 'PNG', optimize=True)
                    converted_count += 1
                    print("SUCCESS: " + filename + " (" + file_format + " -> PNG)")
                    
            except Exception as e:
                failed_count += 1
                print("FAILED: " + filename + " - " + str(e))
                
                # If PIL cannot handle, try direct copy
                try:
                    shutil.copy2(source_path, target_path)
                    print("COPIED: " + filename)
                    skipped_count += 1
                except Exception as copy_error:
                    print("COPY FAILED: " + filename + " - " + str(copy_error))
    
    # Output statistics
    print("\n" + "="*50)
    print("Conversion Statistics:")
    print("Total files: " + str(total_files))
    print("Successfully converted: " + str(converted_count))
    print("Failed conversions: " + str(failed_count))
    print("Direct copies: " + str(skipped_count))
    print("="*50)
    
    return converted_count, failed_count, skipped_count

if __name__ == "__main__":
    print("Starting batch conversion of fake PNG images...")
    convert_fake_png_to_real_png()
    print("Conversion process completed!")