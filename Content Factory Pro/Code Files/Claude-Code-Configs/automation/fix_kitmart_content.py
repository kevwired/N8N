#!/usr/bin/env python3
"""
Fix Kit-mart content specifically with proper business-focused content
"""

import os
import re
from pathlib import Path

KITMART_CONTENT_MAP = {
    'Educational': {
        'base': "From local clubs to schools and authorities, we've learned what makes kit ordering simple and stress-free. Our streamlined process has helped outfit over 600 teams with quality custom sportswear they're proud to wear.",
        'specific': {
            'Bespoke_Kit_Ordering': "Professional kits for grassroots clubs! How local clubs can access professional-quality custom kit without the complexity. From initial design to final delivery, we make the entire process straightforward for teams of any size.",
            'School_Sports_Kit': "Equipping tomorrow's athletes today! Complete guide to ordering custom sports kit for schools and educational institutions. Our educational partnerships ensure students get quality kit that performs while staying within school budgets.",
            'Savi_Sportswear': "Quality sportswear for every team! Everything you need to know about our comprehensive Savi sportswear collection. From training gear to match-day kits, our range covers every team's needs with consistent quality.",
            'Training_Kit': "From training ground to match day! The complete range of training products and accessories every team needs. Our training essentials complement match kits perfectly for a complete team solution."
        }
    },
    'Behind-the-Scenes': {
        'base': "Watch how we process hundreds of kit orders weekly while maintaining the quality control standards that teams depend on. Every piece is checked before shipping to ensure your team looks and feels professional.",
        'specific': {
            'Processing_600': "The busiest kit supplier in grassroots football! A look inside our facility as we process hundreds of kit orders for clubs across the UK. Our efficient systems ensure every order is handled with care and delivered on time.",
            'Quality_Control': "Quality is never an accident! How we ensure every piece of custom kit meets our high standards before shipping. See the attention to detail that makes clubs trust us with their team identity."
        }
    },
    'Promotional': {
        'base': "We specialize in bespoke kit solutions for clubs, schools, and local authorities across the UK. With our Savi sportswear range and bulk ordering options, we make professional-quality kit accessible to every team.",
        'specific': {
            'Local_Authority': "Trusted by local authorities nationwide! Reliable kit supply partnerships with local councils and government organizations. Our proven track record with educational institutions makes us the go-to choice for official suppliers.",
            'Club_Bulk': "Better rates for team orders! Special rates and streamlined processes for clubs ordering complete team kits. Bulk ordering means better prices and coordinated delivery for your entire squad.",
            'Custom_Hoodies': "Look professional, feel professional! Complete your team's look with custom hoodies, tracksuits, and training wear. Our design team helps create cohesive team identity across all your kit needs."
        }
    },
    'Success Story': {
        'base': "See how clubs and schools have transformed their team identity with our custom kit solutions. From grassroots teams to educational institutions, these partnerships show the difference quality kit makes.",
        'specific': {
            'School_Success': "Transforming school sports, one kit at a time! How we helped a local school transform their sports program with quality kit. See the difference professional appearance makes to team confidence and performance.",
            'Club_Kit': "When clubs look professional, they play professional! From basic kit to professional appearance - a grassroots club's transformation story. Quality kit builds pride and team unity that shows on the pitch.",
            'High_Volume': "Reliability at scale! How our efficient systems help us consistently deliver hundreds of orders on time. Teams trust us because we deliver what we promise, when we promise it."
        }
    }
}

def get_kitmart_content(content_type, filename):
    """Get specific Kit-mart content based on type and filename"""
    
    # Determine specific content based on filename keywords
    if content_type in KITMART_CONTENT_MAP:
        specific_content = KITMART_CONTENT_MAP[content_type]['specific']
        
        for key, content in specific_content.items():
            if key.lower().replace('_', '') in filename.lower().replace('_', '').replace('-', ''):
                return content
        
        # Fallback to base content for this type
        return KITMART_CONTENT_MAP[content_type]['base']
    
    return None

def fix_kitmart_file(file_path):
    """Fix a single Kit-mart file"""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Skip summary files
        if 'SUMMARY' in file_path.name:
            return False
        
        # Determine content type from filename
        content_type = "Educational"
        if "Promotional" in file_path.name:
            content_type = "Promotional"
        elif "Behind-the-Scenes" in file_path.name:
            content_type = "Behind-the-Scenes"
        elif "Success Story" in file_path.name:
            content_type = "Success Story"
        
        # Get specific Kit-mart content
        kitmart_content = get_kitmart_content(content_type, file_path.name)
        if not kitmart_content:
            return False
        
        # Extract current CTA
        shortform_match = re.search(r'📱 SHORTFORM VERSION\n═+\n\n(.*?)\n\n📘', content, re.DOTALL)
        if not shortform_match:
            return False
        
        current_shortform = shortform_match.group(1).strip()
        
        # Extract CTA (last part with action words)
        parts = current_shortform.split('. ')
        cta = ""
        for part in reversed(parts):
            if any(keyword in part.lower() for keyword in ['more', 'get', 'order', 'special', 'tag', 'join', 'book', 'outfit']):
                cta = part.strip()
                break
        
        if not cta:
            cta = "Get your kit sorted at Kit-Mart"
        
        # Create new content
        new_shortform = f"{kitmart_content} {cta}"
        
        # Replace in content
        new_content = re.sub(
            r'(📱 SHORTFORM VERSION\n═+\n\n).*?(\n\n📘)',
            f'\\1{new_shortform}\\2',
            content,
            flags=re.DOTALL
        )
        
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"[FIXED] {file_path.name}")
            return True
        
        return False
        
    except Exception as e:
        print(f"[ERROR] {file_path}: {e}")
        return False

def main():
    """Fix all Kit-mart content"""
    
    print("=" * 60)
    print("    KIT-MART CONTENT FIXER")
    print("    Adding Proper Business-Specific Content")
    print("=" * 60)
    
    kitmart_dir = Path("Z:/Main Drive/360TFT Resources/Workflows/N8N/Content Factory Pro/Clients/Kit-mart/Aug_25")
    
    if not kitmart_dir.exists():
        print("Kit-mart directory not found!")
        return
    
    total_fixed = 0
    
    for txt_file in kitmart_dir.glob("Aug_25_*.txt"):
        if fix_kitmart_file(txt_file):
            total_fixed += 1
    
    print(f"\n{'='*60}")
    print(f"COMPLETE! Fixed {total_fixed} Kit-mart files")
    print(f"All content now includes proper business details")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()