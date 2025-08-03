#!/usr/bin/env python3
"""
Complete business configuration report for all 5 requested businesses
"""

import pandas as pd
import json
from pathlib import Path
from datetime import datetime

def extract_kf_barbers_config():
    """Extract KF Barbers configuration from their CSV file"""
    
    kf_csv_path = Path("Z:/Main Drive/360TFT Resources/Workflows/N8N/Content Factory Pro/Clients/KF Barbers/Aug_25/2. Business_Config CSV")
    
    try:
        df = pd.read_csv(kf_csv_path)
        if not df.empty:
            business_row = df.iloc[0]
            
            # Extract configuration data
            config = {}
            for col in df.columns:
                value = business_row.get(col, '')
                if pd.isna(value):
                    config[col] = ""
                else:
                    config[col] = str(value)
            
            return config
    except Exception as e:
        print(f"Error reading KF Barbers CSV: {e}")
        return None

def main():
    """Generate complete business configuration report"""
    
    print("COMPLETE BUSINESS CONFIGURATION REPORT")
    print("="*80)
    print("Content Factory Pro - Business Configuration Data")
    print("Retrieved on:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("="*80)
    
    # Load the main JSON configuration file with 4 businesses
    json_file = "business_configurations_20250803_052959.json"
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            business_configs = json.load(f)
    except Exception as e:
        print(f"Error loading main configuration file: {e}")
        return
    
    # Add KF Barbers configuration
    kf_config = extract_kf_barbers_config()
    if kf_config:
        business_configs["KF Barbers"] = kf_config
        print("✓ Successfully added KF Barbers configuration")
    else:
        print("✗ Failed to load KF Barbers configuration")
    
    print(f"\nTotal businesses configured: {len(business_configs)}")
    print("\nBusinesses included:")
    for i, business_name in enumerate(business_configs.keys(), 1):
        print(f"{i}. {business_name}")
    
    # Generate detailed report for each business
    for business_name, config in business_configs.items():
        print(f"\n{'='*60}")
        print(f"BUSINESS: {business_name.upper()}")
        print(f"{'='*60}")
        
        # Core Information
        print(f"\n📊 CORE INFORMATION")
        print(f"Business ID: {config.get('ID', 'Not specified')}")
        print(f"Category: {config.get('Business Category', 'Not specified')}")
        print(f"Active Status: {config.get('Active Status', 'Not specified')}")
        print(f"Owner: {config.get('Business Owner', 'Not specified')}")
        print(f"Email: {config.get('Email', 'Not specified')}")
        print(f"Phone: {config.get('Phone', 'Not specified')}")
        print(f"Website: {config.get('Website URLs', 'Not specified')}")
        print(f"Social Handle: {config.get('Social Handle', 'Not specified')}")
        print(f"Social Platforms: {config.get('Social Platforms', 'Not specified')}")
        
        # Target Audience
        print(f"\n🎯 TARGET AUDIENCE")
        target_audience = config.get('Target Audience', 'Not specified')
        if len(target_audience) > 500:
            print(f"{target_audience[:500]}...")
        else:
            print(target_audience)
        
        # Brand Voice Guidelines
        print(f"\n🗣️ BRAND VOICE GUIDELINES")
        brand_voice = config.get('Brand Voice Guidelines', 'Not specified')
        if len(brand_voice) > 500:
            print(f"{brand_voice[:500]}...")
        else:
            print(brand_voice)
        
        # Content Generation System Message
        print(f"\n🤖 CONTENT GENERATION SYSTEM MESSAGE")
        system_message = config.get('GENERATE TEXT - System Message', 'Not specified')
        if len(system_message) > 500:
            print(f"{system_message[:500]}...")
        else:
            print(system_message)
        
        # Call to Action Templates
        print(f"\n📢 CALL TO ACTION TEMPLATES")
        cta_template = config.get('Call to Action Template', 'Not specified')
        if len(cta_template) > 300:
            print(f"{cta_template[:300]}...")
        else:
            print(cta_template)
        
        # Visual Identity
        print(f"\n🎨 VISUAL IDENTITY")
        brand_colors = config.get('Brand Colors', 'Not specified')
        image_style = config.get('Image Style Preferences', 'Not specified')
        hashtag_strategy = config.get('Hashtag Strategy', 'Not specified')
        
        print(f"Brand Colors: {brand_colors}")
        if len(image_style) > 200:
            print(f"Image Style: {image_style[:200]}...")
        else:
            print(f"Image Style: {image_style}")
        
        if len(hashtag_strategy) > 200:
            print(f"Hashtag Strategy: {hashtag_strategy[:200]}...")
        else:
            print(f"Hashtag Strategy: {hashtag_strategy}")
        
        # Content Strategy
        print(f"\n📝 CONTENT STRATEGY")
        content_length = config.get('Content Length Limit', 'Not specified')
        seo_strategy = config.get('SEO Strategy Template', 'Not specified')
        content_rules = config.get('Global Content Rules', 'Not specified')
        
        print(f"Content Length Limit: {content_length}")
        
        if len(seo_strategy) > 300:
            print(f"SEO Strategy: {seo_strategy[:300]}...")
        else:
            print(f"SEO Strategy: {seo_strategy}")
        
        if len(content_rules) > 300:
            print(f"Global Content Rules: {content_rules[:300]}...")
        else:
            print(f"Global Content Rules: {content_rules}")
        
        # Additional Information
        notes = config.get('Notes', '')
        if notes and notes != 'Not specified':
            print(f"\n📋 ADDITIONAL NOTES")
            if len(notes) > 400:
                print(f"{notes[:400]}...")
            else:
                print(notes)
    
    # Save complete configuration
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    complete_file = f"complete_business_configurations_{timestamp}.json"
    
    with open(complete_file, 'w', encoding='utf-8') as f:
        json.dump(business_configs, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}")
    print(f"✓ Successfully retrieved configurations for {len(business_configs)} businesses")
    print(f"✓ Complete data saved to: {complete_file}")
    print(f"✓ All requested businesses configured:")
    
    target_businesses = ["BGK Goalkeeping", "360TFT", "Kit-Mart", "CD Copland Motors", "KF Barbers"]
    for business in target_businesses:
        status = "✓ Found" if business in business_configs else "✗ Missing"
        print(f"   {status}: {business}")
    
    print(f"\n🎉 Configuration data retrieval complete!")

if __name__ == "__main__":
    main()