#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import csv
import shutil
from PIL import Image

def replace_images_from_csv():
    csv_file = "bad_png_list.csv"
    converted_dir = "converted_png"
    docs_source_dir = "docs/source"
    
    # Results tracking
    results = {
        'success': [],
        'failed': [],
        'not_found_converted': [],
        'not_found_original': []
    }
    
    print("Starting image replacement process...")
    print("="*60)
    
    # Read CSV file
    try:
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            csv_data = list(reader)
            
        print("CSV file loaded successfully. Found " + str(len(csv_data)) + " entries.")
        
        # Debug: print column names and clean them
        if csv_data:
            original_keys = list(csv_data[0].keys())
            print("Original CSV columns: " + str(original_keys))
            
            # Clean the data by creating new dictionaries with clean keys
            cleaned_data = []
            for row in csv_data:
                cleaned_row = {}
                for key, value in row.items():
                    # Clean the key by removing BOM and quotes
                    clean_key = key.replace('\xef\xbb\xbf', '').replace('"', '').strip()
                    cleaned_row[clean_key] = value.replace('"', '') if isinstance(value, str) else value
                cleaned_data.append(cleaned_row)
            
            csv_data = cleaned_data
            print("Cleaned CSV columns: " + str(list(csv_data[0].keys())))
            
    except Exception as e:
        print("Failed to read CSV file: " + str(e))
        return
    
    print("\nProcessing each image:")
    print("-" * 40)
    
    for row in csv_data:
        # Now we should have clean column names
        if 'Path' not in row:
            print("SKIP: Could not find Path column in row")
            continue
            
        original_path = row['Path']
        
        # Extract filename from full path
        filename = os.path.basename(original_path)
        
        # Paths for replacement
        converted_file = os.path.join(converted_dir, filename)
        
        # Convert absolute path to relative path for docs/source
        if "docs\\source\\" in original_path:
            relative_path = original_path.split("docs\\source\\")[1]
            target_path = os.path.join(docs_source_dir, relative_path)
        else:
            print("SKIP: " + filename + " - Path format not recognized")
            continue
        
        print("Processing: " + filename)
        print("  Target: " + target_path)
        
        # Check if converted file exists
        if not os.path.exists(converted_file):
            print("  FAILED: Converted file not found")
            results['not_found_converted'].append(filename)
            continue
        
        # Check if target directory exists
        target_dir = os.path.dirname(target_path)
        if not os.path.exists(target_dir):
            print("  FAILED: Target directory does not exist: " + target_dir)
            results['failed'].append(filename)
            continue
        
        # Check if original file exists
        if not os.path.exists(target_path):
            print("  FAILED: Original file not found: " + target_path)
            results['not_found_original'].append(filename)
            continue
        
        try:
            # Backup original file
            backup_path = target_path + ".backup"
            if not os.path.exists(backup_path):
                shutil.copy2(target_path, backup_path)
                print("  BACKUP: Created backup")
            
            # Copy converted file to replace original
            shutil.copy2(converted_file, target_path)
            
            # Verify the replacement
            with Image.open(target_path) as img:
                if img.format == 'PNG':
                    print("  SUCCESS: Replaced with PNG format")
                    results['success'].append(filename)
                else:
                    print("  WARNING: File format is " + str(img.format))
                    results['success'].append(filename)  # Still count as success
                    
        except Exception as e:
            print("  FAILED: " + str(e))
            results['failed'].append(filename)
        
        print()
    
    # Print summary
    print("="*60)
    print("REPLACEMENT SUMMARY:")
    print("="*60)
    print("Total files processed: " + str(len(csv_data)))
    print("Successfully replaced: " + str(len(results['success'])))
    print("Failed to replace: " + str(len(results['failed'])))
    print("Converted file not found: " + str(len(results['not_found_converted'])))
    print("Original file not found: " + str(len(results['not_found_original'])))
    
    if results['success']:
        print("\nSUCCESSFUL REPLACEMENTS:")
        for filename in results['success']:
            print("  ✓ " + filename)
    
    if results['failed']:
        print("\nFAILED REPLACEMENTS:")
        for filename in results['failed']:
            print("  ✗ " + filename)
    
    if results['not_found_converted']:
        print("\nCONVERTED FILES NOT FOUND:")
        for filename in results['not_found_converted']:
            print("  ? " + filename)
    
    if results['not_found_original']:
        print("\nORIGINAL FILES NOT FOUND:")
        for filename in results['not_found_original']:
            print("  ? " + filename)
    
    return results

if __name__ == "__main__":
    replace_images_from_csv()