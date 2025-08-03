#!/usr/bin/env python3
"""
Generate content with disclaimer and upload to Google Drive
Uses month + sequential naming convention
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
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

class ContentDriveUploader:
    def __init__(self):
        self.notion_headers = {
            'Authorization': f'Bearer {NOTION_API_KEY}',
            'Content-Type': 'application/json',
            'Notion-Version': '2022-06-28'
        }
        # Base client directory
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
            'google_drive_folder': get_text(props.get('Google Drive Parent Folder', {}))  # This is the key field
        }
    
    def generate_marketing_ideas(self, business_config: Dict) -> List[Dict]:
        """Generate 12 marketing content ideas based on business type"""
        
        business_name = business_config['business_name']
        category = business_config['category'].lower()
        
        # Barber-specific content
        if 'barber' in business_name.lower() or 'barber' in category:
            return [
                {'type': 'Educational', 'topic': 'How Often Should You Get a Haircut?', 'brief': 'Explain ideal haircut frequency for different hair types and styles. Include maintenance tips.', 'hook': 'Looking sharp requires the right schedule'},
                {'type': 'Educational', 'topic': 'Beard Maintenance Between Visits', 'brief': 'Daily beard care routine, product recommendations, and trimming tips between professional visits.', 'hook': 'Your beard deserves daily attention'},
                {'type': 'Educational', 'topic': 'Choosing the Right Haircut for Your Face Shape', 'brief': 'Guide to selecting flattering cuts based on face shape with visual examples.', 'hook': 'The perfect cut starts with knowing your face shape'},
                {'type': 'Educational', 'topic': 'Kids Haircut Preparation Tips', 'brief': 'Help parents prepare children for stress-free haircut experiences.', 'hook': 'Make your child\'s haircut a happy experience'},
                {'type': 'Behind-the-Scenes', 'topic': 'Early Morning Prep at the Barbershop', 'brief': 'Show the daily routine, tool preparation, and dedication to service before opening.', 'hook': 'Ever wonder what happens before we open?'},
                {'type': 'Behind-the-Scenes', 'topic': 'The Art of Traditional Barbering', 'brief': 'Showcase traditional techniques, craftsmanship, and attention to detail.', 'hook': 'Where traditional craftsmanship meets modern service'},
                {'type': 'Promotional', 'topic': 'Walk-In Wednesday Special', 'brief': 'Highlight walk-in availability and convenience for busy schedules.', 'hook': 'No appointment? No problem!'},
                {'type': 'Promotional', 'topic': 'Father & Son Appointment Special', 'brief': 'Encourage booking father-son appointments for bonding experiences.', 'hook': 'Create memories that last longer than the haircut'},
                {'type': 'Promotional', 'topic': 'Early Bird Saturday Hours', 'brief': 'Promote early morning appointments and benefits of beating the rush.', 'hook': 'Start your weekend looking sharp'},
                {'type': 'Success Story', 'topic': 'Nervous Child Becomes Regular Customer', 'brief': 'Share story of transforming haircut fears into excitement for kids.', 'hook': 'How we turned haircut tears into cheers'},
                {'type': 'Success Story', 'topic': 'Three Generations Choose Us', 'brief': 'Highlight families who bring multiple generations for haircuts.', 'hook': 'When granddad, dad, and son all trust the same barber'},
                {'type': 'Success Story', 'topic': 'Customer Reviews Speak for Themselves', 'brief': 'Share authentic customer feedback and satisfaction stories.', 'hook': 'Real customers, real results, real satisfaction'}
            ]
        
        # Automotive-specific content
        elif 'automotive' in category or 'motor' in business_name.lower():
            return [
                {'type': 'Educational', 'topic': 'Essential Car Maintenance Tips', 'brief': 'Basic maintenance every car owner should know to extend vehicle life.', 'hook': 'Simple steps for a longer-lasting vehicle'},
                {'type': 'Educational', 'topic': 'When to Schedule Your MOT', 'brief': 'Understanding MOT requirements and optimal timing for testing.', 'hook': 'Stay legal and safe on the road'},
                {'type': 'Educational', 'topic': 'Electric Vehicle Charging Best Practices', 'brief': 'Guide to proper EV charging habits and battery care.', 'hook': 'Maximize your EV battery life'},
                {'type': 'Educational', 'topic': 'Warning Signs Your Car Needs Attention', 'brief': 'How to identify common car problems before they become expensive.', 'hook': 'Catch problems early, save money later'},
                {'type': 'Behind-the-Scenes', 'topic': 'Meet Our Certified Technicians', 'brief': 'Introduce the skilled team and their qualifications.', 'hook': 'The experts who keep you moving'},
                {'type': 'Behind-the-Scenes', 'topic': 'State-of-the-Art Diagnostic Equipment', 'brief': 'Show modern technology used for accurate vehicle diagnosis.', 'hook': 'Precision diagnostics for precise repairs'},
                {'type': 'Promotional', 'topic': 'New Customer Welcome Offer', 'brief': 'Special pricing or service package for first-time customers.', 'hook': 'Your first visit made special'},
                {'type': 'Promotional', 'topic': 'EV Service Specialist Booking', 'brief': 'Highlight specialized electric vehicle servicing capabilities.', 'hook': 'Expert EV care when you need it'},
                {'type': 'Promotional', 'topic': 'Multi-Vehicle Family Discount', 'brief': 'Special rates for families with multiple vehicles.', 'hook': 'Family fleet? Family savings!'},
                {'type': 'Success Story', 'topic': 'Saved Customer from Costly Repair', 'brief': 'How early diagnosis prevented major expense.', 'hook': 'When prevention saves thousands'},
                {'type': 'Success Story', 'topic': 'Emergency Breakdown Rescue', 'brief': 'Quick response story that got customer back on road.', 'hook': 'When you need us most, we\'re there'},
                {'type': 'Success Story', 'topic': 'Long-Term Customer Loyalty', 'brief': 'Celebrate customers who\'ve trusted us for years.', 'hook': 'Trusted partners for the long haul'}
            ]
        
        # Generic content for other business types
        else:
            return [
                {'type': 'Educational', 'topic': f'Top 5 {category.title()} Tips for Beginners', 'brief': f'Essential advice for those new to {category} services.', 'hook': 'Start your journey the right way'},
                {'type': 'Educational', 'topic': f'Common {category.title()} Mistakes to Avoid', 'brief': f'Help customers avoid typical pitfalls in {category}.', 'hook': 'Save time and money by avoiding these errors'},
                {'type': 'Educational', 'topic': f'Seasonal {category.title()} Considerations', 'brief': f'How seasons affect {category} needs and solutions.', 'hook': 'Prepare for the season ahead'},
                {'type': 'Educational', 'topic': 'Understanding Our Service Process', 'brief': 'Step-by-step explanation of what customers can expect.', 'hook': 'Know what to expect from start to finish'},
                {'type': 'Behind-the-Scenes', 'topic': 'Meet Our Expert Team', 'brief': 'Introduce team members and their expertise.', 'hook': 'The people who make it all happen'},
                {'type': 'Behind-the-Scenes', 'topic': 'Our Quality Standards', 'brief': 'Show commitment to excellence and attention to detail.', 'hook': 'Why we go the extra mile'},
                {'type': 'Promotional', 'topic': 'New Customer Welcome Offer', 'brief': 'Special introductory offer for first-time customers.', 'hook': 'Your first experience made special'},
                {'type': 'Promotional', 'topic': 'Refer a Friend Rewards', 'brief': 'Reward customers for bringing new business.', 'hook': 'Share the love, share the rewards'},
                {'type': 'Promotional', 'topic': 'Flexible Scheduling Options', 'brief': 'Highlight convenience and availability.', 'hook': 'We work around your schedule'},
                {'type': 'Success Story', 'topic': 'Customer Success Spotlight', 'brief': 'Feature a satisfied customer and their experience.', 'hook': 'Real results from real people'},
                {'type': 'Success Story', 'topic': 'Challenge Overcome Success', 'brief': 'How we solved a difficult customer problem.', 'hook': 'When others said it couldn\'t be done'},
                {'type': 'Success Story', 'topic': 'Long-Term Partnership Celebration', 'brief': 'Celebrate customers who have been with us for years.', 'hook': 'Partnerships that stand the test of time'}
            ]
    
    def generate_content_with_disclaimer(self, idea: Dict, business_config: Dict, content_number: int, month: str) -> str:
        """Generate content file with disclaimer header in the exact format requested"""
        
        # Clean topic for filename
        clean_topic = idea['topic'].replace('?', '').replace(':', '').replace(' ', '_')[:30]
        
        # Generate shortform content (placeholder - you can enhance this with actual AI generation)
        shortform_content = f"{idea['hook']}! At {business_config['business_name']}, {idea['brief'][:100]}... {business_config['cta_template']}"
        
        # Generate longform content (placeholder - you can enhance this with actual AI generation)  
        longform_content = f"""# {idea['topic']}

{idea['hook']} is more than just a catchphrase - it's the foundation of our approach at {business_config['business_name']}.

## Understanding the Challenge

{idea['brief']} This comprehensive guide will walk you through everything you need to know about {idea['topic'].lower()}.

## Our Expert Approach

At {business_config['business_name']}, we've developed a proven methodology that addresses the core challenges our customers face. Through years of experience in {business_config['category']}, we've refined our approach to deliver consistent results.

## Key Benefits

When you work with {business_config['business_name']}, you can expect:

- Professional expertise backed by industry experience
- Personalized solutions tailored to your specific needs
- Ongoing support and guidance throughout the process
- Transparent communication and fair pricing

## Getting Started

Ready to experience the difference? {business_config['cta_template']}

## Why Choose {business_config['business_name']}

{business_config['business_notes'][:200] if business_config['business_notes'] else 'We are committed to providing exceptional service and building lasting relationships with our customers.'}

Contact us today to learn more about how we can help you achieve your goals."""
        
        # Create the content with exact disclaimer format
        content = f"""❗ DISCLAIMER
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
        
        return content
    
    def create_monthly_folders(self, client_folder: str):
        """Create monthly folders for content organization"""
        
        months = ['Aug_25', 'Sep_25', 'Oct_25', 'Nov_25', 'Dec_25']
        
        for month in months:
            month_folder = os.path.join(client_folder, month)
            os.makedirs(month_folder, exist_ok=True)
    
    def save_content_with_drive_info(self, business_name: str, ideas: List[Dict], business_config: Dict):
        """Save content with Google Drive information and naming convention"""
        
        # Determine client folder path
        client_folder = os.path.join(self.base_client_dir, business_name)
        
        if not os.path.exists(client_folder):
            print(f"[ERROR] Client folder not found: {client_folder}")
            return
        
        # Create monthly folders
        self.create_monthly_folders(client_folder)
        
        # Determine current month folder
        current_month = datetime.now().strftime('%b_25')  # Aug_25, Sep_25, etc.
        monthly_folder = os.path.join(client_folder, current_month)
        
        # Get Google Drive folder name from business config
        drive_folder = business_config.get('google_drive_folder', 'Generated_Content')
        
        print(f"[INFO] Google Drive target folder: {drive_folder}")
        print(f"[INFO] Generating content for {current_month}")
        
        # Generate and save individual content files
        generated_files = []
        
        for idx, idea in enumerate(ideas, 1):
            # Create filename with month + sequential numbering
            clean_topic = idea['topic'].replace('?', '').replace(':', '').replace(' ', '_')[:25]
            filename = f"{current_month}_{idx:02d}_{idea['type']}_{clean_topic}.txt"
            
            # Generate content with disclaimer
            content = self.generate_content_with_disclaimer(idea, business_config, idx, current_month)
            
            # Save to monthly folder
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
        
        # Create summary with Google Drive instructions
        summary_file = os.path.join(monthly_folder, f"{current_month}_Content_Summary.txt")
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(f"""CONTENT PACKAGE SUMMARY - {business_name}
{'='*60}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Month: {current_month}
Total Files: {len(generated_files)}

GOOGLE DRIVE UPLOAD INFORMATION:
===============================
Target Google Drive Folder: {drive_folder}
Upload Location: Google Drive > {drive_folder} > {current_month}

GENERATED FILES:
===============
""")
            
            for file_info in generated_files:
                f.write(f"{file_info['filename']}\n")
                f.write(f"  Type: {file_info['type']}\n")
                f.write(f"  Topic: {file_info['topic']}\n")
                f.write(f"  Local Path: {file_info['path']}\n\n")
        
        f.write(f"""
NAMING CONVENTION:
=================
Format: {current_month}_##_Type_Topic.txt
- {current_month}: Current month folder
- ##: Sequential number (01-12)
- Type: Content type (Educational, Promotional, etc.)
- Topic: Shortened topic name

UPLOAD INSTRUCTIONS:
===================
1. Open Google Drive
2. Navigate to folder: {drive_folder}
3. Create subfolder: {current_month} (if not exists)
4. Upload all 12 content files to that subfolder
5. Files are ready for use with disclaimer included

DISCLAIMER INCLUDED:
===================
Each file includes:
- Safety disclaimer about checking AI content
- Contact information for changes
- Both shortform and longform versions
- Platform usage guide

Generated by Content Factory Pro
Contact: admin@kevinrmiddleton.com
""")
        
        print(f"\n[SUCCESS] Content package generated for {business_name}")
        print(f"[LOCATION] Local folder: {monthly_folder}")
        print(f"[DRIVE TARGET] Google Drive folder: {drive_folder}")
        print(f"[FILES] 12 content files created with {current_month}_##_ naming")
        print(f"[SUMMARY] Upload instructions saved in summary file")
    
    def generate_client_content_with_drive(self, business_name: str):
        """Generate complete content package with Google Drive information"""
        
        print(f"[INFO] Generating content with Drive info for {business_name}...")
        
        # Get business config
        config = self.get_business_config(business_name)
        if not config:
            print(f"[ERROR] Business '{business_name}' not found or inactive in Notion database")
            return
        
        print(f"[SUCCESS] Found configuration for {config['business_name']}")
        print(f"[INFO] Category: {config['category']}")
        print(f"[INFO] Drive folder: {config.get('google_drive_folder', 'Not specified')}")
        
        # Generate marketing ideas
        ideas = self.generate_marketing_ideas(config)
        print(f"[INFO] Generated {len(ideas)} content ideas")
        
        # Save content with Drive information
        self.save_content_with_drive_info(business_name, ideas, config)

def main():
    """Main function"""
    
    uploader = ContentDriveUploader()
    
    # Get business name
    business_name = input("Enter business name: ").strip()
    if not business_name:
        print("[ERROR] Business name is required")
        return
    
    uploader.generate_client_content_with_drive(business_name)

if __name__ == "__main__":
    main()