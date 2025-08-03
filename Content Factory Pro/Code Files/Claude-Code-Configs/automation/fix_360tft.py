#!/usr/bin/env python3
"""
Fix 360TFT content to remove PRIMARY CTA artifacts
"""

import os
from pathlib import Path

def fix_360tft_file(file_path):
    """Fix 360TFT content file"""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Skip if no PRIMARY CTA found
        if 'PRIMARY CTA:' not in content:
            return False
        
        # Replace the problematic text
        fixed_content = content.replace(
            'PRIMARY CTA: "Join 1,200+ coaches transforming football for just $10/month →', 
            'Join 1,200+ coaches at 360TFT.com'
        )
        
        # Clean up any remaining fragments
        fixed_content = fixed_content.replace('PRIMARY CTA:', '')
        
        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        print(f"[FIXED] {os.path.basename(file_path)}")
        return True
        
    except Exception as e:
        print(f"[ERROR] {file_path}: {e}")
        return False

def main():
    """Fix all 360TFT content files"""
    
    print("Fixing 360TFT content files...")
    
    base_dir = Path("Z:/Main Drive/360TFT Resources/Workflows/N8N/Content Factory Pro/Clients/360TFT/Aug_25")
    
    total_fixed = 0
    
    for txt_file in base_dir.glob("Aug_25_*.txt"):
        if fix_360tft_file(txt_file):
            total_fixed += 1
    
    print(f"Fixed {total_fixed} files")

if __name__ == "__main__":
    main()