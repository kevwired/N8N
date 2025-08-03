#!/usr/bin/env python3
"""
Final comprehensive business configuration report for all 5 requested businesses
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
            
            # Extract configuration data and convert to standard format
            config = {
                'ID': str(business_row.get('ID', '')),
                'Title': str(business_row.get('Title', '')),
                'Business Category': str(business_row.get('Business Category', '')),
                'Active Status': str(business_row.get('Active Status', '')),
                'Target Audience': str(business_row.get('Target Audience', '')),
                'GENERATE TEXT - System Message': str(business_row.get('GENERATE TEXT - System Message', '')),
                'Content Length Limit': str(business_row.get('Content Length Limit', '')),
                'Brand Voice Guidelines': str(business_row.get('Brand Voice Guidelines', '')),
                'Hashtag Strategy': str(business_row.get('Hashtag Strategy', '')),
                'Call to Action Template': str(business_row.get('Call to Action Template', '')),
                'GENERATE PROMPT - User Message': str(business_row.get('GENERATE PROMPT - User Message', '')),
                'GENERATE PROMPT - System Message': str(business_row.get('GENERATE PROMPT - System Message', '')),
                'Image Style Preferences': str(business_row.get('Image Style Preferences', '')),
                'Brand Colors': str(business_row.get('Brand Colors', '')),
                'Google Drive Parent Folder': str(business_row.get('Google Drive Parent Folder', '')),
                'Social Platforms': str(business_row.get('Social Platforms', '')),
                'SEO Strategy Template': str(business_row.get('SEO Strategy Template', '')),
                'Website URLs': str(business_row.get('Website URLs', '')),
                'Business Owner': str(business_row.get('Business Owner', '')),
                'Social Handle': str(business_row.get('Social Handle', '')),
                'Created Date': str(business_row.get('Created Date', '')),
                'Last Modified': str(business_row.get('Last Modified', '')),
                'Notes': str(business_row.get('Notes', '')),
                'Global Content Rules': str(business_row.get('Global Content Rules', '')),
                'Email': str(business_row.get('Email', '')),
                'Phone': str(business_row.get('Phone', '')),
                'ID 1': str(business_row.get('ID 1', '')),
                'ID 2': str(business_row.get('ID 2', '')),
                'ID 3': str(business_row.get('ID 3', ''))
            }
            
            # Clean up NaN values
            for key, value in config.items():
                if value == 'nan' or pd.isna(value):
                    config[key] = ""
            
            return config
    except Exception as e:
        print(f"Error reading KF Barbers CSV: {e}")
        return None

def main():
    """Generate complete business configuration report"""
    
    print("CONTENT FACTORY PRO - BUSINESS CONFIGURATION REPORT")
    print("=" * 80)
    print("Retrieved on:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("Requested businesses: BGK Goalkeeping, 360TFT, Kit-Mart, CD Copland Motors, KF Barbers")
    print("=" * 80)
    
    # Load the main JSON configuration file with 4 businesses
    json_file = "business_configurations_20250803_052959.json"
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            business_configs = json.load(f)
        print(f"Loaded {len(business_configs)} businesses from main database")
    except Exception as e:
        print(f"Error loading main configuration file: {e}")
        return
    
    # Add KF Barbers configuration
    kf_config = extract_kf_barbers_config()
    if kf_config:
        business_configs["KF Barbers"] = kf_config
        print("Successfully added KF Barbers configuration from client folder")
    else:
        print("Failed to load KF Barbers configuration")
    
    print(f"\nFINAL RESULT: {len(business_configs)} out of 5 businesses configured")
    
    # Save complete configuration
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    complete_file = f"all_5_business_configurations_{timestamp}.json"
    
    with open(complete_file, 'w', encoding='utf-8') as f:
        json.dump(business_configs, f, indent=2, ensure_ascii=False)
    
    print(f"Complete configuration data saved to: {complete_file}")
    
    # Generate summary for each business
    print("\n" + "=" * 80)
    print("BUSINESS CONFIGURATION SUMMARY")
    print("=" * 80)
    
    for business_name, config in business_configs.items():
        print(f"\n{business_name.upper()}")
        print("-" * 60)
        
        # Core information
        print(f"ID: {config.get('ID', 'Not specified')}")
        print(f"Category: {config.get('Business Category', 'Not specified')}")
        print(f"Active: {config.get('Active Status', 'Not specified')}")
        print(f"Owner: {config.get('Business Owner', 'Not specified')}")
        print(f"Email: {config.get('Email', 'Not specified')}")
        print(f"Phone: {config.get('Phone', 'Not specified')}")
        print(f"Website: {config.get('Website URLs', 'Not specified')}")
        print(f"Social Handle: {config.get('Social Handle', 'Not specified')}")
        print(f"Social Platforms: {config.get('Social Platforms', 'Not specified')}")
        
        # Target audience summary
        target_audience = config.get('Target Audience', '')
        if target_audience:
            if len(target_audience) > 200:
                print(f"Target Audience: {target_audience[:200]}...")
            else:
                print(f"Target Audience: {target_audience}")
        
        # Brand voice summary
        brand_voice = config.get('Brand Voice Guidelines', '')
        if brand_voice:
            if len(brand_voice) > 200:
                print(f"Brand Voice: {brand_voice[:200]}...")
            else:
                print(f"Brand Voice: {brand_voice}")
        
        # CTA template summary
        cta_template = config.get('Call to Action Template', '')
        if cta_template:
            if len(cta_template) > 150:
                print(f"CTA Template: {cta_template[:150]}...")
            else:
                print(f"CTA Template: {cta_template}")
        
        # Brand colors
        brand_colors = config.get('Brand Colors', '')
        if brand_colors:
            print(f"Brand Colors: {brand_colors}")
        
        # Content length limit
        content_length = config.get('Content Length Limit', '')
        if content_length:
            print(f"Content Length Limit: {content_length}")
    
    print("\n" + "=" * 80)
    print("CONFIGURATION RETRIEVAL COMPLETE")
    print("=" * 80)
    print(f"Total businesses retrieved: {len(business_configs)}")
    print("Status:")
    
    target_businesses = ["BGK Goalkeeping", "360TFT", "Kit-Mart", "CD Copland Motors", "KF Barbers"]
    for business in target_businesses:
        status = "FOUND" if business in business_configs else "MISSING"
        print(f"  {status}: {business}")
    
    print(f"\nAll business configuration data has been successfully retrieved and saved!")
    print(f"Complete data file: {complete_file}")

if __name__ == "__main__":
    main()