#!/usr/bin/env python3
"""
Simple business configuration extractor from CSV database
"""

import pandas as pd
import json
from pathlib import Path
from datetime import datetime

def main():
    """Extract business configurations for the 5 target businesses"""
    
    # Define target businesses
    target_businesses = [
        "BGK Goalkeeping",
        "360TFT", 
        "Kit-Mart",
        "CD Copland Motors",
        "KF Barbers"
    ]
    
    # Load CSV data
    csv_path = Path("Z:/Main Drive/360TFT Resources/Workflows/N8N/Content Factory Pro/Database/Business_Configurations 20ed14ad2042804194a1d732d174e720.csv")
    
    print("Loading business configuration data...")
    
    try:
        df = pd.read_csv(csv_path, encoding='utf-8-sig')
        print(f"Loaded {len(df)} business records from CSV database")
    except:
        try:
            df = pd.read_csv(csv_path, encoding='latin-1')
            print(f"Loaded {len(df)} business records from CSV database")
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            return
    
    # Extract configurations
    business_configs = {}
    
    for business_name in target_businesses:
        print(f"\nSearching for: {business_name}")
        
        # Search for the business
        matches = df[df['Title'].str.contains(business_name, case=False, na=False)]
        
        if not matches.empty:
            business_row = matches.iloc[0]
            
            # Extract configuration data
            config = {}
            for col in df.columns:
                value = business_row.get(col, '')
                if pd.isna(value):
                    config[col] = ""
                else:
                    config[col] = str(value)
            
            business_configs[business_name] = config
            print(f"Found configuration for {business_name}")
        else:
            print(f"Business '{business_name}' not found")
    
    # Save configurations
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"business_configurations_{timestamp}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(business_configs, f, indent=2, ensure_ascii=False)
    
    print(f"\nSaved {len(business_configs)} business configurations to {output_file}")
    
    # Generate summary report
    print("\n" + "="*60)
    print("BUSINESS CONFIGURATION SUMMARY")
    print("="*60)
    
    for business_name, config in business_configs.items():
        print(f"\n{business_name.upper()}")
        print("-" * 40)
        
        print(f"Category: {config.get('Business Category', 'Not specified')}")
        print(f"Active: {config.get('Active Status', 'Not specified')}")
        print(f"Owner: {config.get('Business Owner', 'Not specified')}")
        print(f"Email: {config.get('Email', 'Not specified')}")
        print(f"Phone: {config.get('Phone', 'Not specified')}")
        print(f"Website: {config.get('Website URLs', 'Not specified')}")
        
        # Target audience (first 200 chars)
        target_audience = config.get('Target Audience', '')
        if target_audience and len(target_audience) > 200:
            target_audience = target_audience[:200] + "..."
        print(f"Target Audience: {target_audience}")
        
        # Brand voice (first 200 chars)
        brand_voice = config.get('Brand Voice Guidelines', '')
        if brand_voice and len(brand_voice) > 200:
            brand_voice = brand_voice[:200] + "..."
        print(f"Brand Voice: {brand_voice}")
        
        # CTA template (first 150 chars)
        cta_template = config.get('Call to Action Template', '')
        if cta_template and len(cta_template) > 150:
            cta_template = cta_template[:150] + "..."
        print(f"CTA Template: {cta_template}")
        
        print(f"Social Platforms: {config.get('Social Platforms', 'Not specified')}")
        print(f"Social Handle: {config.get('Social Handle', 'Not specified')}")
        print(f"Brand Colors: {config.get('Brand Colors', 'Not specified')}")
    
    print(f"\nTotal businesses retrieved: {len(business_configs)}")
    print(f"Missing businesses: {len(target_businesses) - len(business_configs)}")

if __name__ == "__main__":
    main()