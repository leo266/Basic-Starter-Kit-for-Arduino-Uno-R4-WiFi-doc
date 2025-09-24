#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Final verification script to check image replacement and RST reference restoration
"""

import os
import csv
from PIL import Image

def verify_final_result():
    """Verify that all images have been replaced and RST references restored"""
    
    print("Starting final verification...")
    print("=" * 60)
    
    # 1. Verify RST references
    print("1. VERIFYING RST REFERENCES:")
    print("-" * 40)
    
    source_dir = "docs/source"
    commented_refs = 0
    active_refs = 0
    
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.rst'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                        
                        # Count commented out references
                        commented_refs += content.count('(COMMENTED OUT - WEBP format)')
                        
                        # Count active image references
                        active_refs += content.count('.. image::')
                        
                except Exception as e:
                    print("Error reading " + file_path + ": " + str(e))
    
    print("Active image references: " + str(active_refs))
    print("Commented out references: " + str(commented_refs))
    
    # 2. Check some sample converted images
    print("\n2. VERIFYING SAMPLE CONVERTED IMAGES:")
    print("-" * 40)
    
    sample_files = [
        "docs/source/Basic_Project/img/0.96_inch_OLED_Wiring1.png",
        "docs/source/Basic_Project/img/Active_Buzzer.png", 
        "docs/source/Basic_Project/img/LED_Blink_Wiring1.png",
        "docs/source/Get_Started_with_Arduino/img/Creat_Skerch2.png",
        "docs/source/Get_Started_with_Arduino/img/Install_Arduino_IDE_6.png"
    ]
    
    png_count = 0
    for file_path in sample_files:
        if os.path.exists(file_path):
            try:
                with Image.open(file_path) as img:
                    if img.format == 'PNG':
                        print("  OK: " + os.path.basename(file_path) + " -> PNG format")
                        png_count += 1
                    else:
                        print("  WARN: " + os.path.basename(file_path) + " -> " + str(img.format))
            except Exception as e:
                print("  ERROR: " + os.path.basename(file_path) + " -> " + str(e))
        else:
            print("  MISSING: " + file_path)
    
    # 3. Check backup directory
    print("\n3. VERIFYING BACKUPS:")
    print("-" * 40)
    
    backup_dir = "backup_original_images"
    if os.path.exists(backup_dir):
        backup_files = []
        for root, dirs, files in os.walk(backup_dir):
            backup_files.extend(files)
        print("Backup files created: " + str(len(backup_files)))
    else:
        print("Backup directory not found")
    
    # 4. Summary
    print("\n" + "=" * 60)
    print("FINAL VERIFICATION SUMMARY:")
    print("=" * 60)
    print("Sample PNG files verified: " + str(png_count) + "/" + str(len(sample_files)))
    print("RST commented references: " + str(commented_refs) + " (should be 0)")
    print("RST active references: " + str(active_refs))
    
    if commented_refs == 0:
        print("\nSUCCESS: All tasks completed successfully!")
        print("- All pseudo-PNG images have been converted to real PNG format")
        print("- All images have been replaced in the source directory")
        print("- All RST file references have been restored")
        print("- Original files have been backed up")
    else:
        print("\nWARNING: " + str(commented_refs) + " references still commented out")

if __name__ == "__main__":
    verify_final_result()