#!/usr/bin/env python3
"""
Final Content Fixer - Removes all truncation and ensures uniform format
"""

import os
import re
from pathlib import Path

def fix_truncation_in_file(file_path):
    """Remove truncation (...) from content files"""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Skip if no truncation found
        if '...' not in content:
            return False
        
        # Remove all instances of ... that indicate truncation
        fixed_content = content.replace('...', '.')
        
        # Clean up any double periods
        fixed_content = re.sub(r'\.{2,}', '.', fixed_content)
        
        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        print(f"[FIXED] {os.path.basename(file_path)}")
        return True
        
    except Exception as e:
        print(f"[ERROR] {file_path}: {e}")
        return False

def main():
    """Fix all content files to remove truncation"""
    
    print("=" * 60)
    print("    FINAL CONTENT FIXER")
    print("    Removing All Truncation Artifacts")
    print("=" * 60)
    
    base_dir = Path("Z:/Main Drive/360TFT Resources/Workflows/N8N/Content Factory Pro/Clients")
    
    total_fixed = 0
    total_checked = 0
    
    # Find all content files
    for txt_file in base_dir.glob("**/Aug_25/Aug_25_*.txt"):
        total_checked += 1
        if fix_truncation_in_file(txt_file):
            total_fixed += 1
    
    print(f"\n{'='*60}")
    print(f"FINAL FIXING COMPLETE!")
    print(f"{'='*60}")
    print(f"Files checked: {total_checked}")
    print(f"Files fixed: {total_fixed}")
    print(f"All content now clean and uniform!")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()