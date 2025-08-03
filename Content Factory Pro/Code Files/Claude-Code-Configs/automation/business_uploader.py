#!/usr/bin/env python3
"""
Generic Business Uploader for Content Factory Pro
Handles any business upload to Notion database
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Add the automation directory to Python path
sys.path.append(str(Path(__file__).parent))

from notion_client import NotionClient

class BusinessUploader:
    def __init__(self):
        """Initialize the business uploader"""
        from config import Config
        
        try:
            config = Config.get_notion_config()
            self.api_key = config['api_key']
            self.database_id = config['database_id']
            self.client = NotionClient(api_key=self.api_key, database_id=self.database_id)
        except ValueError as e:
            print(f"Configuration Error: {e}")
            print("Please create a .env file with your API credentials.")
            print("See .env.example for the required format.")
            raise
        
    def get_business_data_interactive(self):
        """Get business data through interactive prompts - ALL 29 COLUMNS"""
        print("\n=== Content Factory Pro - Business Upload (Complete Schema) ===")
        print("Enter business information (press Enter to skip optional fields):\n")
        
        # Required fields
        name = input("Business Name (required): ").strip()
        if not name:
            print("Error: Business name is required!")
            return None
            
        # Basic info
        phone = input("Phone Number: ").strip()
        email = input("Email Address: ").strip()
        website = input("Website URL: ").strip()
        contact_name = input("Business Owner/Contact Name: ").strip()
        social_handle = input("Primary Social Media Handle (e.g., @businessname): ").strip()
        
        # Business details
        print("\nBusiness Category Options:")
        categories = [
            "Real Estate & Mortgage Services", "Automotive", "Plumbing", 
            "Health & Fitness", "Sports Coaching & Training", "Travel & Cruise",
            "Food Service", "Professional Services", "Retail", "Home Services",
            "Technology", "Education", "Other"
        ]
        for i, cat in enumerate(categories, 1):
            print(f"{i}. {cat}")
        
        cat_choice = input("\nSelect category number (or type custom): ").strip()
        if cat_choice.isdigit() and 1 <= int(cat_choice) <= len(categories):
            business_category = categories[int(cat_choice) - 1]
        else:
            business_category = cat_choice if cat_choice else "Other"
        
        # Location and description
        location = input("Business Address/Location: ").strip()
        description = input("Business Description (what they do): ").strip()
        
        # Marketing info
        print("\nTarget Audience (describe their ideal customers, demographics, pain points):")
        target_audience = input("> ").strip()
        
        print("\nBrand Voice Guidelines (how they communicate - tone, style, personality):")
        brand_voice = input("> ").strip()
        
        print("\nSocial Media Platforms (comma-separated, e.g., Facebook, Instagram, LinkedIn):")
        social_platforms = input("> ").strip()
        
        # Content strategy fields
        print("\nHashtag Strategy (main hashtags for the business):")
        hashtag_strategy = input("> ").strip()
        
        print("\nCall to Action Template (how should posts end? e.g., 'Call us at...'):")
        cta_template = input("> ").strip()
        
        print("\nSEO Strategy/Keywords (what do customers search for?):")
        seo_strategy = input("> ").strip()
        
        print("\nBrand Colors (main colors used in branding):")
        brand_colors = input("> ").strip()
        
        print("\nImage Style Preferences (describe ideal photo/image style):")
        image_style = input("> ").strip()
        
        # Advanced fields with defaults
        content_length = input("Content Length Limit (default 150): ").strip()
        content_length_limit = int(content_length) if content_length.isdigit() else 150
        
        # Get next ID automatically
        next_id = self.client.get_next_business_id()
        
        # Generate system message automatically
        system_message = f"You are writing content for {name}, {description}. TARGET AUDIENCE: {target_audience}. BRAND VOICE: {brand_voice}. Focus on professional quality content that reflects the business expertise and connects with the target audience."
        
        # Generate image prompt system message
        prompt_system_message = f"Create professional imagery for {name} that showcases {description}. Style should reflect {brand_voice} and appeal to {target_audience}. Use {brand_colors} color scheme when specified."
        
        return {
            # Basic fields
            'id': next_id,
            'name': name,
            'contact_name': contact_name,
            'phone': phone,
            'email': email,
            'website': website,
            'business_category': business_category,
            'location': location,
            'description': description,
            
            # Content strategy fields
            'target_audience': target_audience,
            'system_message': system_message,
            'content_length_limit': content_length_limit,
            'brand_voice': brand_voice,
            'hashtag_strategy': hashtag_strategy,
            'cta_template': cta_template,
            'user_message': f"Create engaging social media content for {name}",
            'prompt_system_message': prompt_system_message,
            'image_style': image_style,
            'brand_colors': brand_colors,
            'drive_folder': name.replace(' ', '_'),
            'social_platforms': social_platforms,
            'seo_strategy': seo_strategy,
            'social_handle': social_handle,
            
            # Additional fields
            'notes': f"Business uploaded on {datetime.now().strftime('%Y-%m-%d')}",
            'content_rules': f"1. Always mention {name} brand name, 2. Focus on {description}, 3. Target {target_audience}, 4. Use {brand_voice} tone, 5. Include location {location} when relevant",
            'submission_date': datetime.now().strftime('%Y-%m-%d'),
            
            # ID fields
            'id_1': '',
            'id_2': '',
            'id_3': next_id
        }
    
    def load_business_from_json(self, json_file):
        """Load business data from JSON file"""
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Get next ID if not provided
            if 'id' not in data:
                data['id'] = self.client.get_next_business_id()
                
            # Add submission date if not provided
            if 'submission_date' not in data:
                data['submission_date'] = datetime.now().strftime('%Y-%m-%d')
                
            return data
        except Exception as e:
            print(f"Error loading JSON file: {e}")
            return None
    
    def upload_business(self, business_data):
        """Upload business to Notion database"""
        try:
            print(f"\nUploading {business_data['name']} to Notion...")
            
            # Test connection
            if not self.client.test_connection():
                print("Failed to connect to Notion database")
                return False
            
            # Check if business already exists
            existing = self.client.find_business_by_name(business_data['name'])
            
            if existing:
                print(f"Business '{business_data['name']}' already exists.")
                update = input("Update existing record? (y/n): ").lower().startswith('y')
                
                if update:
                    result = self.client.update_business_record(existing['id'], business_data)
                    print(f"Successfully updated {business_data['name']}")
                else:
                    print("Upload cancelled")
                    return False
            else:
                result = self.client.add_business_to_database(business_data)
                print(f"Successfully added {business_data['name']} to database")
            
            # Print summary
            self.print_upload_summary(business_data)
            return True
            
        except Exception as e:
            print(f"Error uploading business: {e}")
            return False
    
    def print_upload_summary(self, business_data):
        """Print upload summary"""
        print(f"\n{'='*50}")
        print("UPLOAD SUMMARY")
        print(f"{'='*50}")
        print(f"Business Name: {business_data['name']}")
        print(f"Category: {business_data.get('business_category', 'N/A')}")
        print(f"Phone: {business_data.get('phone', 'N/A')}")
        print(f"Email: {business_data.get('email', 'N/A')}")
        print(f"Website: {business_data.get('website', 'N/A')}")
        if business_data.get('location'):
            print(f"Location: {business_data['location']}")
        print(f"Database ID: {business_data.get('id', 'Auto-generated')}")
        print(f"{'='*50}")
    
    def create_template_json(self, filename="business_template.json"):
        """Create a template JSON file for business data"""
        template = {
            "name": "Example Business Name",
            "contact_name": "John Smith",
            "phone": "555-123-4567",
            "email": "contact@business.com",
            "website": "https://www.business.com",
            "description": "Brief description of what the business does",
            "target_audience": "Describe their ideal customers, demographics, pain points",
            "brand_voice": "Describe their communication style (professional, friendly, etc.)",
            "social_platforms": "Facebook, Instagram, LinkedIn",
            "business_category": "Professional Services",
            "location": "123 Main St, City, State",
            "notes": "Any additional notes about the business"
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(template, f, indent=2)
            print(f"Template created: {filename}")
            print("Edit this file with your business data, then run: python business_uploader.py --json business_template.json")
        except Exception as e:
            print(f"Error creating template: {e}")

def main():
    """Main function with command line options"""
    uploader = BusinessUploader()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--json" and len(sys.argv) > 2:
            # Load from JSON file
            json_file = sys.argv[2]
            if not os.path.exists(json_file):
                print(f"Error: File '{json_file}' not found")
                return
                
            business_data = uploader.load_business_from_json(json_file)
            if business_data:
                success = uploader.upload_business(business_data)
                if success:
                    print(f"\nBusiness successfully uploaded from {json_file}!")
                
        elif sys.argv[1] == "--template":
            # Create template file
            filename = sys.argv[2] if len(sys.argv) > 2 else "business_template.json"
            uploader.create_template_json(filename)
            
        elif sys.argv[1] == "--help":
            print("\nContent Factory Pro - Business Uploader")
            print("Usage:")
            print("  python business_uploader.py                    # Interactive mode")
            print("  python business_uploader.py --json file.json   # Upload from JSON")
            print("  python business_uploader.py --template         # Create template")
            print("  python business_uploader.py --template file.json # Create named template")
            
    else:
        # Interactive mode
        business_data = uploader.get_business_data_interactive()
        if business_data:
            success = uploader.upload_business(business_data)
            if success:
                print(f"\n{business_data['name']} successfully uploaded to Notion database!")
                print("The business is now ready for content creation in your workflow.")

if __name__ == "__main__":
    main()