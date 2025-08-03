#!/usr/bin/env python3
"""
Batch Business Uploader for Content Factory Pro
Upload multiple businesses from JSON or CSV files
"""

import json
import csv
import os
import sys
from pathlib import Path

# Add the automation directory to Python path
sys.path.append(str(Path(__file__).parent))

from business_uploader import BusinessUploader

class BatchUploader:
    def __init__(self):
        self.uploader = BusinessUploader()
        
    def upload_from_csv(self, csv_file):
        """Upload multiple businesses from CSV file"""
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                businesses = list(reader)
                
            print(f"Found {len(businesses)} businesses in {csv_file}")
            
            successful = 0
            failed = 0
            
            for i, business in enumerate(businesses, 1):
                print(f"\nProcessing {i}/{len(businesses)}: {business.get('name', 'Unknown')}")
                
                # Clean up the data
                cleaned_business = self.clean_business_data(business)
                
                if cleaned_business:
                    success = self.uploader.upload_business(cleaned_business)
                    if success:
                        successful += 1
                    else:
                        failed += 1
                else:
                    print(f"Skipped {business.get('name', 'Unknown')} - missing required data")
                    failed += 1
                    
            print(f"\n{'='*50}")
            print("BATCH UPLOAD COMPLETE")
            print(f"{'='*50}")
            print(f"Successful uploads: {successful}")
            print(f"Failed uploads: {failed}")
            print(f"Total processed: {len(businesses)}")
            
        except Exception as e:
            print(f"Error processing CSV file: {e}")
            
    def upload_from_json_array(self, json_file):
        """Upload multiple businesses from JSON array file"""
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                businesses = json.load(f)
                
            if not isinstance(businesses, list):
                print("Error: JSON file must contain an array of business objects")
                return
                
            print(f"Found {len(businesses)} businesses in {json_file}")
            
            successful = 0
            failed = 0
            
            for i, business in enumerate(businesses, 1):
                print(f"\nProcessing {i}/{len(businesses)}: {business.get('name', 'Unknown')}")
                
                success = self.uploader.upload_business(business)
                if success:
                    successful += 1
                else:
                    failed += 1
                    
            print(f"\n{'='*50}")
            print("BATCH UPLOAD COMPLETE")
            print(f"{'='*50}")
            print(f"Successful uploads: {successful}")
            print(f"Failed uploads: {failed}")
            print(f"Total processed: {len(businesses)}")
            
        except Exception as e:
            print(f"Error processing JSON file: {e}")
    
    def clean_business_data(self, raw_data):
        """Clean and validate business data from CSV"""
        required_fields = ['name']
        
        # Check for required fields
        for field in required_fields:
            if not raw_data.get(field, '').strip():
                return None
                
        # Map CSV columns to expected format
        cleaned = {
            'name': raw_data.get('name', '').strip(),
            'contact_name': raw_data.get('contact_name', raw_data.get('owner', '')).strip(),
            'phone': raw_data.get('phone', raw_data.get('telephone', '')).strip(),
            'email': raw_data.get('email', raw_data.get('email_address', '')).strip(),
            'website': raw_data.get('website', raw_data.get('url', '')).strip(),
            'description': raw_data.get('description', raw_data.get('business_description', '')).strip(),
            'target_audience': raw_data.get('target_audience', '').strip(),
            'brand_voice': raw_data.get('brand_voice', raw_data.get('voice_guidelines', '')).strip(),
            'social_platforms': raw_data.get('social_platforms', raw_data.get('social_media', '')).strip(),
            'business_category': raw_data.get('business_category', raw_data.get('category', 'Other')).strip(),
            'location': raw_data.get('location', raw_data.get('address', '')).strip(),
        }
        
        return cleaned
    
    def create_csv_template(self, filename="batch_upload_template.csv"):
        """Create a CSV template for batch uploads"""
        headers = [
            'name', 'contact_name', 'phone', 'email', 'website',
            'description', 'target_audience', 'brand_voice', 
            'social_platforms', 'business_category', 'location'
        ]
        
        sample_data = [
            [
                'Example Business 1', 'John Smith', '555-123-4567', 
                'john@business1.com', 'https://business1.com',
                'Professional consulting services', 
                'Small business owners seeking growth',
                'Professional yet approachable',
                'LinkedIn, Facebook', 'Professional Services',
                '123 Main St, City, State'
            ],
            [
                'Example Business 2', 'Jane Doe', '555-987-6543',
                'jane@business2.com', 'https://business2.com',
                'Local fitness and wellness center',
                'Health-conscious individuals 25-45',
                'Motivational and energetic',
                'Instagram, Facebook, TikTok', 'Health & Fitness',
                '456 Gym Ave, City, State'
            ]
        ]
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                writer.writerows(sample_data)
                
            print(f"CSV template created: {filename}")
            print("Edit this file with your business data, then run:")
            print(f"python batch_uploader.py --csv {filename}")
            
        except Exception as e:
            print(f"Error creating CSV template: {e}")
    
    def create_json_template(self, filename="batch_upload_template.json"):
        """Create a JSON template for batch uploads"""
        template = [
            {
                "name": "Example Business 1",
                "contact_name": "John Smith",
                "phone": "555-123-4567",
                "email": "john@business1.com",
                "website": "https://business1.com",
                "description": "Professional consulting services",
                "target_audience": "Small business owners seeking growth strategies",
                "brand_voice": "Professional yet approachable, industry expert",
                "social_platforms": "LinkedIn, Facebook",
                "business_category": "Professional Services",
                "location": "123 Main St, City, State"
            },
            {
                "name": "Example Business 2", 
                "contact_name": "Jane Doe",
                "phone": "555-987-6543",
                "email": "jane@business2.com",
                "website": "https://business2.com",
                "description": "Local fitness and wellness center",
                "target_audience": "Health-conscious individuals aged 25-45",
                "brand_voice": "Motivational, energetic, supportive community",
                "social_platforms": "Instagram, Facebook, TikTok",
                "business_category": "Health & Fitness",
                "location": "456 Gym Ave, City, State"
            }
        ]
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(template, f, indent=2)
                
            print(f"JSON template created: {filename}")
            print("Edit this file with your business data, then run:")
            print(f"python batch_uploader.py --json {filename}")
            
        except Exception as e:
            print(f"Error creating JSON template: {e}")

def main():
    """Main function for batch operations"""
    batch = BatchUploader()
    
    if len(sys.argv) < 2:
        print("\nContent Factory Pro - Batch Business Uploader")
        print("Usage:")
        print("  python batch_uploader.py --csv file.csv         # Upload from CSV")
        print("  python batch_uploader.py --json file.json       # Upload from JSON array")
        print("  python batch_uploader.py --csv-template         # Create CSV template")
        print("  python batch_uploader.py --json-template        # Create JSON template")
        return
    
    command = sys.argv[1]
    
    if command == "--csv" and len(sys.argv) > 2:
        csv_file = sys.argv[2]
        if os.path.exists(csv_file):
            batch.upload_from_csv(csv_file)
        else:
            print(f"Error: File '{csv_file}' not found")
            
    elif command == "--json" and len(sys.argv) > 2:
        json_file = sys.argv[2] 
        if os.path.exists(json_file):
            batch.upload_from_json_array(json_file)
        else:
            print(f"Error: File '{json_file}' not found")
            
    elif command == "--csv-template":
        filename = sys.argv[2] if len(sys.argv) > 2 else "batch_upload_template.csv"
        batch.create_csv_template(filename)
        
    elif command == "--json-template":
        filename = sys.argv[2] if len(sys.argv) > 2 else "batch_upload_template.json"
        batch.create_json_template(filename)
        
    else:
        print("Invalid command. Use --help for usage information")

if __name__ == "__main__":
    main()