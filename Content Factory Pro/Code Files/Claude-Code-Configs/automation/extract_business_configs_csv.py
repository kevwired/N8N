#!/usr/bin/env python3
"""
Extract business configuration data for specific businesses from the CSV database
This script reads the existing CSV database and extracts configurations for the 5 requested businesses
"""

import pandas as pd
import json
from pathlib import Path
from datetime import datetime

class CSVBusinessConfigExtractor:
    def __init__(self):
        """Initialize the CSV business configuration extractor"""
        self.csv_path = Path("Z:/Main Drive/360TFT Resources/Workflows/N8N/Content Factory Pro/Database/Business_Configurations 20ed14ad2042804194a1d732d174e720.csv")
        self.target_businesses = [
            "BGK Goalkeeping",
            "360TFT", 
            "Kit-Mart",
            "CD Copland Motors",
            "KF Barbers"
        ]
        
    def load_csv_data(self):
        """Load the business configurations CSV file"""
        
        if not self.csv_path.exists():
            print(f"Error: CSV file not found at {self.csv_path}")
            return None
            
        try:
            # Try different encodings
            for encoding in ['utf-8-sig', 'utf-8', 'latin-1', 'cp1252']:
                try:
                    df = pd.read_csv(self.csv_path, encoding=encoding)
                    print(f"✓ Loaded {len(df)} business records from CSV database (encoding: {encoding})")
                    return df
                except UnicodeDecodeError:
                    continue
            
            # If all encodings fail, try with error handling
            df = pd.read_csv(self.csv_path, encoding='utf-8', errors='replace')
            print(f"✓ Loaded {len(df)} business records from CSV database (with error handling)")
            return df
            
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            return None
    
    def extract_business_configs(self):
        """Extract configuration data for the 5 target businesses"""
        
        print("Extracting business configuration data from CSV database...")
        print(f"Target businesses: {', '.join(self.target_businesses)}")
        print("-" * 80)
        
        # Load the CSV data
        df = self.load_csv_data()
        if df is None:
            return None
        
        business_configs = {}
        
        for business_name in self.target_businesses:
            print(f"\nSearching for: {business_name}")
            
            # Search for the business (case-insensitive)
            matches = df[df['Title'].str.contains(business_name, case=False, na=False)]
            
            if not matches.empty:
                # Get the first match
                business_row = matches.iloc[0]
                
                # Extract all relevant configuration data
                config = {
                    'id': business_row.get('ID', ''),
                    'business_name': business_row.get('Title', ''),
                    'category': business_row.get('Business Category', ''),
                    'active_status': business_row.get('Active Status', ''),
                    'target_audience': business_row.get('Target Audience', ''),
                    'system_message': business_row.get('GENERATE TEXT - System Message', ''),
                    'content_length_limit': business_row.get('Content Length Limit', ''),
                    'brand_voice': business_row.get('Brand Voice Guidelines', ''),
                    'hashtag_strategy': business_row.get('Hashtag Strategy', ''),
                    'cta_template': business_row.get('Call to Action Template', ''),
                    'user_message': business_row.get('GENERATE PROMPT - User Message', ''),
                    'prompt_system_message': business_row.get('GENERATE PROMPT - System Message', ''),
                    'image_style': business_row.get('Image Style Preferences', ''),
                    'brand_colors': business_row.get('Brand Colors', ''),
                    'drive_folder': business_row.get('Google Drive Parent Folder', ''),
                    'social_platforms': business_row.get('Social Platforms', ''),
                    'seo_strategy': business_row.get('SEO Strategy Template', ''),
                    'website': business_row.get('Website URLs', ''),
                    'owner': business_row.get('Business Owner', ''),
                    'social_handle': business_row.get('Social Handle', ''),
                    'created_date': business_row.get('Created Date', ''),
                    'last_modified': business_row.get('Last Modified', ''),
                    'notes': business_row.get('Notes', ''),
                    'content_rules': business_row.get('Global Content Rules', ''),
                    'email': business_row.get('Email', ''),
                    'phone': business_row.get('Phone', ''),
                }
                
                # Clean up NaN values
                for key, value in config.items():
                    if pd.isna(value):
                        config[key] = ""
                    else:
                        config[key] = str(value)
                
                business_configs[business_name] = config
                print(f"Successfully found and extracted configuration for {business_name}")
                
            else:
                print(f"Business '{business_name}' not found in CSV database")
                
                # Try partial matching
                partial_matches = df[df['Title'].str.contains(business_name.split()[0], case=False, na=False)]
                if not partial_matches.empty:
                    print(f"  Possible partial matches found:")
                    for idx, row in partial_matches.head(3).iterrows():
                        print(f"    - {row['Title']}")
        
        return business_configs
    
    def save_configurations(self, business_configs, output_format='json'):
        """Save business configurations to file"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if output_format == 'json':
            output_file = f"business_configurations_{timestamp}.json"
            output_path = Path(__file__).parent / output_file
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(business_configs, f, indent=2, ensure_ascii=False)
        
        elif output_format == 'csv':
            output_file = f"business_configurations_{timestamp}.csv"
            output_path = Path(__file__).parent / output_file
            
            # Convert to DataFrame for CSV export
            rows = []
            for business_name, config in business_configs.items():
                config['business_name'] = business_name
                rows.append(config)
            
            df = pd.DataFrame(rows)
            df.to_csv(output_path, index=False, encoding='utf-8-sig')
        
        print(f"\nBusiness configurations saved to: {output_path}")
        return output_path
    
    def generate_detailed_report(self, business_configs):
        """Generate a detailed report of the fetched configurations"""
        
        print("\n" + "="*80)
        print("DETAILED BUSINESS CONFIGURATION REPORT")
        print("="*80)
        
        for business_name, config in business_configs.items():
            print(f"\n{'='*20} {business_name.upper()} {'='*20}")
            
            # Core business information
            print(f"\n📊 CORE INFORMATION")
            print(f"ID: {config.get('id', 'Not specified')}")
            print(f"Category: {config.get('category', 'Not specified')}")
            print(f"Active Status: {config.get('active_status', 'Not specified')}")
            print(f"Owner: {config.get('owner', 'Not specified')}")
            print(f"Email: {config.get('email', 'Not specified')}")
            print(f"Phone: {config.get('phone', 'Not specified')}")
            print(f"Website: {config.get('website', 'Not specified')}")
            
            # Target audience
            print(f"\n🎯 TARGET AUDIENCE")
            target_audience = config.get('target_audience', '')
            if target_audience:
                print(f"{target_audience}")
            else:
                print("Not specified")
            
            # Brand voice and messaging
            print(f"\n🗣️ BRAND VOICE GUIDELINES")
            brand_voice = config.get('brand_voice', '')
            if brand_voice:
                print(f"{brand_voice}")
            else:
                print("Not specified")
            
            # System message for content generation
            print(f"\n🤖 CONTENT GENERATION SYSTEM MESSAGE")
            system_message = config.get('system_message', '')
            if system_message:
                print(f"{system_message}")
            else:
                print("Not specified")
            
            # Call to action templates
            print(f"\n📢 CALL TO ACTION TEMPLATES")
            cta_template = config.get('cta_template', '')
            if cta_template:
                print(f"{cta_template}")
            else:
                print("Not specified")
            
            # Social media information
            print(f"\n📱 SOCIAL MEDIA")
            social_platforms = config.get('social_platforms', '')
            social_handle = config.get('social_handle', '')
            hashtag_strategy = config.get('hashtag_strategy', '')
            
            if social_platforms:
                print(f"Platforms: {social_platforms}")
            if social_handle:
                print(f"Handle: {social_handle}")
            if hashtag_strategy:
                print(f"Hashtag Strategy: {hashtag_strategy}")
            
            # Brand colors and visual identity
            print(f"\n🎨 VISUAL IDENTITY")
            brand_colors = config.get('brand_colors', '')
            image_style = config.get('image_style', '')
            
            if brand_colors:
                print(f"Brand Colors: {brand_colors}")
            if image_style:
                print(f"Image Style: {image_style}")
            
            # SEO and content rules
            print(f"\n🔍 SEO & CONTENT STRATEGY")
            seo_strategy = config.get('seo_strategy', '')
            content_rules = config.get('content_rules', '')
            content_length = config.get('content_length_limit', '')
            
            if seo_strategy:
                print(f"SEO Strategy: {seo_strategy}")
            if content_length:
                print(f"Content Length Limit: {content_length}")
            if content_rules:
                print(f"Global Content Rules: {content_rules}")
            
            # Additional notes
            notes = config.get('notes', '')
            if notes:
                print(f"\n📝 ADDITIONAL NOTES")
                print(f"{notes}")
        
        print(f"\n📊 SUMMARY")
        print(f"Total businesses retrieved: {len(business_configs)}")
        print(f"Missing businesses: {len(self.target_businesses) - len(business_configs)}")
        
        if len(business_configs) < len(self.target_businesses):
            missing = [b for b in self.target_businesses if b not in business_configs]
            print(f"Missing: {', '.join(missing)}")

def main():
    """Main execution function"""
    
    try:
        # Initialize extractor
        extractor = CSVBusinessConfigExtractor()
        
        # Extract business configurations
        business_configs = extractor.extract_business_configs()
        
        if not business_configs:
            print("\nNo business configurations were retrieved.")
            return
        
        # Save configurations in both formats
        json_file = extractor.save_configurations(business_configs, 'json')
        csv_file = extractor.save_configurations(business_configs, 'csv')
        
        # Generate detailed report
        extractor.generate_detailed_report(business_configs)
        
        print(f"\n🎉 Successfully extracted configurations for {len(business_configs)} businesses!")
        print(f"💾 JSON data saved to: {json_file}")
        print(f"💾 CSV data saved to: {csv_file}")
        
    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()