#!/usr/bin/env python3
"""
Fetch business configuration data for specific businesses from Notion database
This script retrieves detailed business configurations for the 5 requested businesses
"""

import os
import json
import pandas as pd
from pathlib import Path
from config import Config
from notion_client import NotionClient
from datetime import datetime

class BusinessConfigFetcher:
    def __init__(self):
        """Initialize the business configuration fetcher"""
        self.notion_client = NotionClient()
        self.target_businesses = [
            "BGK Goalkeeping",
            "360TFT", 
            "Kit-Mart",
            "CD Copland Motors",
            "KF Barbers"
        ]
        
    def fetch_all_businesses(self):
        """Fetch all business configurations from Notion database"""
        
        # First, let's get all records from the database
        query = {
            "page_size": 100
        }
        
        response = self.notion_client._make_request('POST', f'/databases/{self.notion_client.database_id}/query', query)
        
        if not response:
            print("Failed to fetch business data from Notion database")
            return None
            
        return response.get('results', [])
    
    def search_business_by_name(self, business_name):
        """Search for a specific business by name"""
        
        query = {
            "filter": {
                "property": "Title",
                "title": {
                    "contains": business_name
                }
            }
        }
        
        response = self.notion_client._make_request('POST', f'/databases/{self.notion_client.database_id}/query', query)
        
        if response and response.get('results'):
            return response['results'][0]
        return None
    
    def extract_business_properties(self, notion_record):
        """Extract and format business properties from Notion record"""
        
        if not notion_record or 'properties' not in notion_record:
            return None
            
        properties = notion_record['properties']
        business_config = {}
        
        # Extract all relevant properties
        field_mappings = {
            'ID': 'id',
            'Title': 'business_name',
            'Business Category': 'category',
            'Active Status': 'active_status',
            'Target Audience': 'target_audience',
            'GENERATE TEXT - System Message': 'system_message',
            'Content Length Limit': 'content_length_limit',
            'Brand Voice Guidelines': 'brand_voice',
            'Hashtag Strategy': 'hashtag_strategy',
            'Call to Action Template': 'cta_template',
            'GENERATE PROMPT - User Message': 'user_message',
            'GENERATE PROMPT - System Message': 'prompt_system_message',
            'Image Style Preferences': 'image_style',
            'Brand Colors': 'brand_colors',
            'Google Drive Parent Folder': 'drive_folder',
            'Social Platforms': 'social_platforms',
            'SEO Strategy Template': 'seo_strategy',
            'Website URLs': 'website',
            'Business Owner': 'owner',
            'Social Handle': 'social_handle',
            'Created Date': 'created_date',
            'Last Modified': 'last_modified',
            'Notes': 'notes',
            'Global Content Rules': 'content_rules',
            'Email': 'email',
            'Phone': 'phone'
        }
        
        for notion_field, config_field in field_mappings.items():
            if notion_field in properties:
                business_config[config_field] = self._extract_property_value(properties[notion_field])
        
        return business_config
    
    def _extract_property_value(self, property_data):
        """Extract value from Notion property data"""
        
        if not property_data:
            return ""
            
        property_type = list(property_data.keys())[0]
        
        if property_type == 'title':
            if property_data['title']:
                return property_data['title'][0]['text']['content']
        elif property_type == 'rich_text':
            if property_data['rich_text']:
                return property_data['rich_text'][0]['text']['content']
        elif property_type == 'number':
            return property_data['number']
        elif property_type == 'select':
            if property_data['select']:
                return property_data['select']['name']
        elif property_type == 'checkbox':
            return property_data['checkbox']
        elif property_type == 'multi_select':
            if property_data['multi_select']:
                return ', '.join([option['name'] for option in property_data['multi_select']])
        elif property_type == 'email':
            return property_data['email']
        elif property_type == 'phone_number':
            return property_data['phone_number']
        elif property_type == 'url':
            return property_data['url']
        elif property_type == 'date':
            if property_data['date']:
                return property_data['date']['start']
        
        return ""
    
    def fetch_target_businesses(self):
        """Fetch configuration data for the 5 target businesses"""
        
        print("Fetching business configuration data from Notion database...")
        print(f"Target businesses: {', '.join(self.target_businesses)}")
        print("-" * 80)
        
        business_configs = {}
        
        for business_name in self.target_businesses:
            print(f"\nSearching for: {business_name}")
            
            # Search for the business
            notion_record = self.search_business_by_name(business_name)
            
            if notion_record:
                config = self.extract_business_properties(notion_record)
                if config:
                    business_configs[business_name] = config
                    print(f"✓ Found configuration for {business_name}")
                else:
                    print(f"✗ Failed to extract configuration for {business_name}")
            else:
                print(f"✗ Business '{business_name}' not found in database")
        
        return business_configs
    
    def save_configurations(self, business_configs, output_file=None):
        """Save business configurations to JSON file"""
        
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"business_configurations_{timestamp}.json"
        
        output_path = Path(__file__).parent / output_file
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(business_configs, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Business configurations saved to: {output_path}")
        return output_path
    
    def generate_summary_report(self, business_configs):
        """Generate a summary report of the fetched configurations"""
        
        print("\n" + "="*80)
        print("BUSINESS CONFIGURATION SUMMARY REPORT")
        print("="*80)
        
        for business_name, config in business_configs.items():
            print(f"\n📋 {business_name.upper()}")
            print("-" * 60)
            
            # Core business information
            print(f"Category: {config.get('category', 'Not specified')}")
            print(f"Active Status: {'✓ Active' if config.get('active_status') else '✗ Inactive'}")
            print(f"Owner: {config.get('owner', 'Not specified')}")
            print(f"Website: {config.get('website', 'Not specified')}")
            print(f"Email: {config.get('email', 'Not specified')}")
            print(f"Phone: {config.get('phone', 'Not specified')}")
            
            # Target audience (truncated for readability)
            target_audience = config.get('target_audience', '')
            if target_audience:
                preview = target_audience[:200] + "..." if len(target_audience) > 200 else target_audience
                print(f"Target Audience: {preview}")
            
            # Brand voice (truncated for readability)
            brand_voice = config.get('brand_voice', '')
            if brand_voice:
                preview = brand_voice[:200] + "..." if len(brand_voice) > 200 else brand_voice
                print(f"Brand Voice: {preview}")
            
            # CTA template
            cta_template = config.get('cta_template', '')
            if cta_template:
                preview = cta_template[:150] + "..." if len(cta_template) > 150 else cta_template
                print(f"CTA Template: {preview}")
            
            # Social platforms
            social_platforms = config.get('social_platforms', '')
            if social_platforms:
                print(f"Social Platforms: {social_platforms}")
            
            # Social handle
            social_handle = config.get('social_handle', '')
            if social_handle:
                print(f"Social Handle: {social_handle}")
            
            # Brand colors
            brand_colors = config.get('brand_colors', '')
            if brand_colors:
                print(f"Brand Colors: {brand_colors}")
        
        print(f"\n📊 Total businesses retrieved: {len(business_configs)}")
        print(f"Missing businesses: {len(self.target_businesses) - len(business_configs)}")
        
        if len(business_configs) < len(self.target_businesses):
            missing = [b for b in self.target_businesses if b not in business_configs]
            print(f"Missing: {', '.join(missing)}")

def main():
    """Main execution function"""
    
    try:
        # Initialize fetcher
        fetcher = BusinessConfigFetcher()
        
        # Test connection first
        print("Testing Notion database connection...")
        if not fetcher.notion_client.test_connection():
            print("Failed to connect to Notion database. Please check your credentials.")
            return
        
        # Fetch business configurations
        business_configs = fetcher.fetch_target_businesses()
        
        if not business_configs:
            print("\nNo business configurations were retrieved.")
            return
        
        # Save configurations
        output_file = fetcher.save_configurations(business_configs)
        
        # Generate summary report
        fetcher.generate_summary_report(business_configs)
        
        print(f"\n🎉 Successfully fetched configurations for {len(business_configs)} businesses!")
        print(f"💾 Data saved to: {output_file}")
        
    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()