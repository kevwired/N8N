#!/usr/bin/env python3
"""
Fix content format across all businesses to ensure uniform, clean output
"""

import os
import re
from pathlib import Path

def fix_content_file(file_path):
    """Fix a single content file to remove development artifacts and ensure clean format"""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file needs fixing (has development artifacts)
        if 'PRIMARY CTA OPTIONS:' not in content and 'FOR TRAINING INQUIRIES:' not in content:
            print(f"[SKIP] Already clean: {os.path.basename(file_path)}")
            return False
        
        # Extract the clean shortform content (remove truncation and multiple CTAs)
        shortform_match = re.search(r'📱 SHORTFORM VERSION\n.*?\n\n(.*?)\n\n📘', content, re.DOTALL)
        if shortform_match:
            shortform_content = shortform_match.group(1)
            
            # Remove truncation artifacts
            if '...' in shortform_content:
                # Split at the first '...' and clean up
                before_dots = shortform_content.split('...')[0].strip()
                
                # Find the first clean CTA option
                cta_match = re.search(r'"([^"]+)"', content)
                if cta_match:
                    clean_cta = cta_match.group(1)
                    # Reconstruct clean shortform content
                    clean_shortform = f"{before_dots}. {clean_cta}"
                    
                    # Replace in content
                    content = re.sub(
                        r'(📱 SHORTFORM VERSION\n.*?\n\n).*?(\n\n📘)',
                        f'\\1{clean_shortform}\\2',
                        content,
                        flags=re.DOTALL
                    )
        
        # Fix longform CTA section
        longform_cta_pattern = r'## Ready to Experience the Difference\?\n\n.*?(?=\n\n---|$)'
        cta_match = re.search(r'"([^"]+)"', content)
        if cta_match:
            clean_cta = cta_match.group(1)
            clean_longform_cta = f"## Ready to Experience the Difference?\n\n{clean_cta}"
            
            content = re.sub(longform_cta_pattern, clean_longform_cta, content, flags=re.DOTALL)
        
        # Write fixed content back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"[FIXED] {os.path.basename(file_path)}")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to fix {file_path}: {e}")
        return False

def main():
    """Fix all content files across all businesses"""
    
    print("=" * 60)
    print("    CONTENT FORMAT FIXER")
    print("    Ensuring Uniform, Clean Content Across All Businesses")
    print("=" * 60)
    
    base_dir = Path("Z:/Main Drive/360TFT Resources/Workflows/N8N/Content Factory Pro/Clients")
    businesses = ['BGK Goalkeeping', '360TFT', 'Kit-mart', 'CD Copland Motors', 'KF Barbers', 'Athlete Recovery Zone']
    
    total_fixed = 0
    total_checked = 0
    
    for business in businesses:
        business_dir = base_dir / business / "Aug_25"
        
        if not business_dir.exists():
            print(f"[SKIP] Directory not found: {business}")
            continue
        
        print(f"\n{'='*50}")
        print(f"FIXING CONTENT FOR: {business}")
        print(f"{'='*50}")
        
        # Find all content files
        content_files = list(business_dir.glob("Aug_25_*_*.txt"))
        
        for file_path in content_files:
            total_checked += 1
            if fix_content_file(file_path):
                total_fixed += 1
    
    print(f"\n{'='*60}")
    print(f"CONTENT FORMAT FIXING COMPLETE!")
    print(f"{'='*60}")
    print(f"Files checked: {total_checked}")
    print(f"Files fixed: {total_fixed}")
    print(f"All content now uniform and professional!")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()