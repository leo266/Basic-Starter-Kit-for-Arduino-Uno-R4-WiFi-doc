#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script to restore commented out image references in RST files
"""

import os
import re

def restore_rst_references():
    """Restore commented out image references in RST files"""
    
    # Base directory for source files
    source_dir = "docs/source"
    
    # Pattern to match commented out image references
    pattern = r'^(\s*)image:: (.*\.png) \(COMMENTED OUT - WEBP format\)$'
    
    # Statistics
    total_files_processed = 0
    total_references_restored = 0
    files_with_changes = []
    
    print("Starting RST reference restoration process...")
    print("=" * 60)
    
    # Walk through all RST files
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.rst'):
                file_path = os.path.join(root, file)
                
                # Read file content
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                    
                    original_content = content
                    lines = content.split('\n')
                    modified_lines = []
                    file_changes = 0
                    
                    for line in lines:
                        match = re.match(pattern, line)
                        if match:
                            # Restore the image reference
                            indent = match.group(1)
                            image_path = match.group(2)
                            restored_line = indent + ".. image:: " + image_path
                            modified_lines.append(restored_line)
                            file_changes += 1
                            print("RESTORED: " + file_path + " -> " + image_path)
                        else:
                            modified_lines.append(line)
                    
                    # Write back if there were changes
                    if file_changes > 0:
                        new_content = '\n'.join(modified_lines)
                        with open(file_path, 'w') as f:
                            f.write(new_content)
                        
                        files_with_changes.append({
                            'file': file_path,
                            'changes': file_changes
                        })
                        total_references_restored += file_changes
                    
                    total_files_processed += 1
                    
                except Exception as e:
                    print("ERROR processing " + file_path + ": " + str(e))
    
    # Print summary
    print("\n" + "=" * 60)
    print("RST REFERENCE RESTORATION SUMMARY:")
    print("=" * 60)
    print("Total RST files processed: " + str(total_files_processed))
    print("Total image references restored: " + str(total_references_restored))
    print("Files with changes: " + str(len(files_with_changes)))
    
    if files_with_changes:
        print("\nFILES MODIFIED:")
        for file_info in files_with_changes:
            print("  " + file_info['file'] + " (" + str(file_info['changes']) + " references)")
    
    print("\nAll image references have been successfully restored!")

if __name__ == "__main__":
    restore_rst_references()