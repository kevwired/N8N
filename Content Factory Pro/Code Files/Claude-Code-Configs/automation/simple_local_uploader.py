#!/usr/bin/env python3
"""
Simple content generator - creates files locally for manual upload
No OAuth2 required - generates content with clear upload instructions
"""

import os
import json
import requests
from datetime import datetime
from typing import Dict, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

NOTION_API_KEY = os.getenv('NOTION_API_KEY')
NOTION_DATABASE_ID = os.getenv('NOTION_DATABASE_ID')

class SimpleContentGenerator:
    def __init__(self):
        self.notion_headers = {
            'Authorization': f'Bearer {NOTION_API_KEY}',
            'Content-Type': 'application/json',
            'Notion-Version': '2022-06-28'
        }
        self.base_client_dir = r"Z:\Main Drive\360TFT Resources\Workflows\N8N\Content Factory Pro\Clients"
    
    def get_business_config(self, business_name: str) -> Dict:
        """Fetch business configuration from Notion"""
        url = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query"
        
        payload = {
            "filter": {
                "and": [
                    {
                        "property": "Title",
                        "title": {"equals": business_name}
                    },
                    {
                        "property": "Active Status",  
                        "checkbox": {"equals": True}
                    }
                ]
            }
        }
        
        response = requests.post(url, headers=self.notion_headers, json=payload)
        
        if response.status_code == 200:
            results = response.json().get('results', [])
            if results:
                return self._parse_business_config(results[0])
        return None
    
    def _parse_business_config(self, notion_page: Dict) -> Dict:
        """Parse Notion page data"""
        props = notion_page.get('properties', {})
        
        def get_text(prop):
            if prop.get('rich_text'):
                return prop['rich_text'][0]['plain_text'] if prop['rich_text'] else ''
            elif prop.get('title'):
                return prop['title'][0]['plain_text'] if prop['title'] else ''
            return ''
        
        return {
            'business_name': get_text(props.get('Title', {})),
            'category': props.get('Business Category', {}).get('select', {}).get('name', ''),
            'target_audience': get_text(props.get('Target Audience', {})),
            'brand_voice': get_text(props.get('Brand Voice Guidelines', {})),
            'hashtag_strategy': get_text(props.get('Hashtag Strategy', {})),
            'cta_template': get_text(props.get('Call to Action Template', {})),
            'business_notes': get_text(props.get('Notes', {})),
            'website_urls': get_text(props.get('Website URLs', {})),
            'phone': get_text(props.get('Phone', {})),
            'email': get_text(props.get('Email', {})),
            'google_drive_folder': get_text(props.get('Google Drive Parent Folder', {}))
        }
    
    def generate_marketing_ideas(self, business_config: Dict) -> List[Dict]:
        """Generate 12 marketing content ideas"""
        business_name = business_config['business_name']
        category = business_config['category'].lower()
        
        if 'barber' in business_name.lower() or 'barber' in category:
            return [
                {'type': 'Educational', 'topic': 'How Often Should You Get a Haircut?', 'brief': 'Explain ideal haircut frequency for different hair types and styles.', 'hook': 'Looking sharp requires the right schedule'},
                {'type': 'Educational', 'topic': 'Beard Maintenance Between Visits', 'brief': 'Daily beard care routine and product recommendations.', 'hook': 'Your beard deserves daily attention'},
                {'type': 'Educational', 'topic': 'Choosing the Right Haircut for Your Face Shape', 'brief': 'Guide to selecting flattering cuts based on face shape.', 'hook': 'The perfect cut starts with knowing your face shape'},
                {'type': 'Educational', 'topic': 'Kids Haircut Preparation Tips', 'brief': 'Help parents prepare children for stress-free experiences.', 'hook': 'Make your child\'s haircut a happy experience'},
                {'type': 'Behind-the-Scenes', 'topic': 'Early Morning Prep at the Barbershop', 'brief': 'Show daily routine and dedication to service.', 'hook': 'Ever wonder what happens before we open?'},
                {'type': 'Behind-the-Scenes', 'topic': 'The Art of Traditional Barbering', 'brief': 'Showcase traditional techniques and craftsmanship.', 'hook': 'Where traditional craftsmanship meets modern service'},
                {'type': 'Promotional', 'topic': 'Walk-In Wednesday Special', 'brief': 'Highlight walk-in availability and convenience.', 'hook': 'No appointment? No problem!'},
                {'type': 'Promotional', 'topic': 'Father & Son Appointment Special', 'brief': 'Encourage father-son bonding appointments.', 'hook': 'Create memories that last longer than the haircut'},
                {'type': 'Promotional', 'topic': 'Early Bird Saturday Hours', 'brief': 'Promote early morning appointments.', 'hook': 'Start your weekend looking sharp'},
                {'type': 'Success Story', 'topic': 'Nervous Child Becomes Regular Customer', 'brief': 'Story of transforming haircut fears into excitement.', 'hook': 'How we turned haircut tears into cheers'},
                {'type': 'Success Story', 'topic': 'Three Generations Choose Us', 'brief': 'Families who bring multiple generations.', 'hook': 'When granddad, dad, and son all trust the same barber'},
                {'type': 'Success Story', 'topic': 'Customer Reviews Speak for Themselves', 'brief': 'Share authentic customer feedback.', 'hook': 'Real customers, real results, real satisfaction'}
            ]
        else:
            category = category or 'business'
            return [
                {'type': 'Educational', 'topic': f'Top 5 {category.title()} Tips', 'brief': f'Essential advice for {category} services.', 'hook': 'Start your journey the right way'},
                {'type': 'Educational', 'topic': f'{category.title()} Mistakes to Avoid', 'brief': f'Common pitfalls in {category}.', 'hook': 'Save time and money'},
                {'type': 'Educational', 'topic': f'Seasonal {category.title()} Guide', 'brief': f'How seasons affect {category} needs.', 'hook': 'Prepare for the season ahead'},
                {'type': 'Educational', 'topic': 'Our Service Process', 'brief': 'What customers can expect.', 'hook': 'Know what to expect'},
                {'type': 'Behind-the-Scenes', 'topic': 'Meet Our Expert Team', 'brief': 'Team members and expertise.', 'hook': 'The people who make it happen'},
                {'type': 'Behind-the-Scenes', 'topic': 'Our Quality Standards', 'brief': 'Commitment to excellence.', 'hook': 'Why we go the extra mile'},
                {'type': 'Promotional', 'topic': 'New Customer Welcome', 'brief': 'Special offer for first-time customers.', 'hook': 'Your first experience made special'},
                {'type': 'Promotional', 'topic': 'Refer a Friend Rewards', 'brief': 'Reward customer referrals.', 'hook': 'Share the love, share the rewards'},
                {'type': 'Promotional', 'topic': 'Flexible Scheduling', 'brief': 'Highlight convenience.', 'hook': 'We work around your schedule'},
                {'type': 'Success Story', 'topic': 'Customer Success Story', 'brief': 'Featured satisfied customer.', 'hook': 'Real results from real people'},
                {'type': 'Success Story', 'topic': 'Challenge Overcome', 'brief': 'Difficult problem solved.', 'hook': 'When others said it couldn\'t be done'},
                {'type': 'Success Story', 'topic': 'Long-Term Partnership', 'brief': 'Years of customer loyalty.', 'hook': 'Partnerships that stand the test of time'}
            ]
    
    def generate_content_with_disclaimer(self, idea: Dict, business_config: Dict, content_number: int, month: str) -> str:
        """Generate content with disclaimer"""
        
        shortform_content = f"{idea['hook']}! At {business_config['business_name']}, {idea['brief']}... {business_config['cta_template']}"
        
        longform_content = f"""# {idea['topic']}

{idea['hook']} is the foundation of our approach at {business_config['business_name']}.

## Understanding the Challenge

{idea['brief']} This guide covers everything you need to know about {idea['topic'].lower()}.

## Our Expert Approach

At {business_config['business_name']}, we've developed proven methods that address core challenges. Through experience in {business_config['category']}, we deliver consistent results.

## Key Benefits

- Professional expertise backed by experience
- Personalized solutions for your needs  
- Ongoing support throughout the process
- Transparent communication and fair pricing

## Getting Started

Ready to experience the difference? {business_config['cta_template']}

Contact us today to learn more."""
        
        return f"""❗ DISCLAIMER
═══════════════════════════════════════
Please check all content carefully before you post it. AI can make mistakes. Check and correct important info.

Images can also be incorrect and are only provided as an alternative to your own images.

If you require any changes in how your content and images are produced, contact Kevin via admin@kevinrmiddleton.com or WhatsApp 07926676298
═══════════════════════════════════════

{idea['topic']}

📱 SHORTFORM VERSION
═══════════════════════════════════════

{shortform_content}

📘 LINKEDIN/BLOG/NEWSLETTER VERSION
═══════════════════════════════════════

{longform_content}

🖼️ IMAGE USAGE GUIDE
═══════════════════════════════════════

💡 Quick Platform Guide:
   • Instagram → Use Original or Square (if available)
   • Facebook → Use Universal (if available) or Original
   • LinkedIn → Use Universal (if available) or Original
   • Twitter → Use Universal (if available) or Original
   • YouTube → Use Universal (if available) or Original
═══════════════════════════════════════"""
    
    def create_monthly_folders(self, client_folder: str):
        """Create monthly folders"""
        months = ['Aug_25', 'Sep_25', 'Oct_25', 'Nov_25', 'Dec_25']
        for month in months:
            month_folder = os.path.join(client_folder, month)
            os.makedirs(month_folder, exist_ok=True)
    
    def generate_upload_instructions(self, business_config: Dict, generated_files: List[Dict], monthly_folder: str) -> str:
        """Generate detailed upload instructions"""
        
        current_month = datetime.now().strftime('%b_25')
        drive_folder = business_config.get('google_drive_folder', 'Generated_Content')
        
        return f"""
🚀 GOOGLE DRIVE UPLOAD INSTRUCTIONS
{'='*60}

STEP 1: CREATE FOLDER STRUCTURE IN GOOGLE DRIVE
════════════════════════════════════════════════
1. Go to your Google Drive: https://drive.google.com
2. Navigate to or create: "Social Media Business"
3. Inside that folder, create: "{drive_folder}"
4. Inside "{drive_folder}", create: "{current_month}"

Final structure: My Drive/Social Media Business/{drive_folder}/{current_month}/

STEP 2: UPLOAD FILES
════════════════════
Upload all {len(generated_files)} files from this local folder:
{monthly_folder}

FILES TO UPLOAD:
{'='*20}
"""
    
    def generate_content_package(self, business_name: str, test_mode: bool = False):
        """Generate complete content package locally"""
        
        mode_text = "TEST MODE" if test_mode else "PRODUCTION MODE"
        print(f"[INFO] {mode_text} - Generating content for {business_name}...")
        
        # Get business config
        config = self.get_business_config(business_name)
        if not config:
            print(f"[ERROR] Business '{business_name}' not found in Notion database")
            return
        
        print(f"[SUCCESS] Found configuration for {config['business_name']}")
        print(f"[INFO] Category: {config['category']}")
        print(f"[INFO] Drive folder target: {config.get('google_drive_folder', 'Not specified')}")
        
        # Generate ideas
        ideas = self.generate_marketing_ideas(config)
        print(f"[INFO] Generated {len(ideas)} content ideas")
        
        # Create local folder structure
        test_suffix = "_TEST" if test_mode else ""
        client_folder = os.path.join(self.base_client_dir, f"{business_name}{test_suffix}")
        
        if not os.path.exists(client_folder):
            os.makedirs(client_folder, exist_ok=True)
            print(f"[CREATED] Local folder: {client_folder}")
        
        # Create monthly folders
        self.create_monthly_folders(client_folder)
        
        # Current month folder
        current_month = datetime.now().strftime('%b_25')
        monthly_folder = os.path.join(client_folder, current_month)
        
        print(f"[INFO] Generating content for {current_month}")
        
        # Generate content files
        generated_files = []
        
        for idx, idea in enumerate(ideas, 1):
            clean_topic = idea['topic'].replace('?', '').replace(':', '').replace(' ', '_')[:25]
            filename = f"{current_month}_{idx:02d}_{idea['type']}_{clean_topic}.txt"
            
            content = self.generate_content_with_disclaimer(idea, config, idx, current_month)
            
            # Save locally
            file_path = os.path.join(monthly_folder, filename)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            generated_files.append({
                'filename': filename,
                'path': file_path,
                'type': idea['type'],
                'topic': idea['topic']
            })
            
            print(f"[{idx:02d}/12] Generated: {filename}")
        
        # Create upload instructions file
        instructions = self.generate_upload_instructions(config, generated_files, monthly_folder)
        
        for file_info in generated_files:
            instructions += f"• {file_info['filename']}\n"
        
        instructions += f"""
STEP 3: VERIFY UPLOAD
═══════════════════
After uploading, your Google Drive should look like:

My Drive/
└── Social Media Business/
    └── {config.get('google_drive_folder', 'Generated_Content')}/
        └── {current_month}/
            ├── {current_month}_01_Educational_...
            ├── {current_month}_02_Educational_...
            └── ... (all 12 files)

STEP 4: SHARE ACCESS (if needed)
══════════════════════════════
If you want to share these files:
1. Right-click the "{current_month}" folder in Google Drive
2. Click "Share"
3. Add email addresses and set permissions

CONTENT FEATURES:
═══════════════
✅ Disclaimer headers included
✅ Both short-form and long-form versions
✅ Platform-specific usage guides
✅ Sequential numbering for posting order
✅ Professional formatting

Generated by Content Factory Pro
Contact: admin@kevinrmiddleton.com
Local files: {monthly_folder}
"""
        
        # Save instructions
        instructions_file = os.path.join(monthly_folder, f"{current_month}_UPLOAD_INSTRUCTIONS.txt")
        with open(instructions_file, 'w', encoding='utf-8') as f:
            f.write(instructions)
        
        print(f"\n{'='*60}")
        print(f"✅ CONTENT GENERATION COMPLETE!")
        print(f"{'='*60}")
        print(f"📁 Local folder: {monthly_folder}")
        print(f"📄 Files created: {len(generated_files)} content files")
        print(f"📋 Upload guide: {instructions_file}")
        print(f"🎯 Google Drive target: Social Media Business/{config.get('google_drive_folder', 'Generated_Content')}/{current_month}")
        print(f"{'='*60}")
        print(f"📖 Next step: Open {instructions_file} for upload instructions")

def main():
    """Main function"""
    
    print("="*60)
    print("    Content Factory Pro - Simple Local Generator")
    print("    (No OAuth2 required - Manual upload)")
    print("="*60)
    
    generator = SimpleContentGenerator()
    
    # Choose mode
    print("1. TEST MODE - Create test content")
    print("2. PRODUCTION MODE - Create production content")
    
    mode_choice = input("Choose mode (1 for TEST, 2 for PRODUCTION): ").strip()
    test_mode = mode_choice == "1"
    
    if test_mode:
        print("\n[TEST MODE] Creating test content")
    else:
        print("\n[PRODUCTION MODE] Creating production content")
    
    # Get business name
    business_name = input("Enter business name: ").strip()
    if not business_name:
        print("[ERROR] Business name required")
        return
    
    generator.generate_content_package(business_name, test_mode)

if __name__ == "__main__":
    main()