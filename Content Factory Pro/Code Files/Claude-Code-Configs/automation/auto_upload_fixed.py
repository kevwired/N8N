#!/usr/bin/env python3
"""
Generate content with disclaimer and automatically upload to Google Drive using OAuth2
Fixed version with proper authentication handling
"""

import os
import json
import requests
import pickle
from datetime import datetime
from typing import Dict, List
from dotenv import load_dotenv

# Google Drive imports
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Allow insecure transport for localhost OAuth2 callback
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Load environment variables
load_dotenv()

NOTION_API_KEY = os.getenv('NOTION_API_KEY')
NOTION_DATABASE_ID = os.getenv('NOTION_DATABASE_ID')

# OAuth2 configuration
SCOPES = ['https://www.googleapis.com/auth/drive.file']
CREDENTIALS_FILE = 'oauth_credentials.json'
TOKEN_FILE = 'token.pickle'

class ContentDriveOAuthUploader:
    def __init__(self):
        self.notion_headers = {
            'Authorization': f'Bearer {NOTION_API_KEY}',
            'Content-Type': 'application/json',
            'Notion-Version': '2022-06-28'
        }
        # Base client directory
        self.base_client_dir = r"Z:\Main Drive\360TFT Resources\Workflows\N8N\Content Factory Pro\Clients"
        
        # Initialize Google Drive service with OAuth2
        self.drive_service = None
        self._initialize_oauth_drive_service()
    
    def _initialize_oauth_drive_service(self):
        """Initialize Google Drive API service using OAuth2 authentication"""
        
        creds = None
        
        # Check if we have stored credentials
        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, 'rb') as token:
                creds = pickle.load(token)
        
        # If there are no (valid) credentials available, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                    print("[SUCCESS] Refreshed existing OAuth2 credentials")
                except Exception as e:
                    print(f"[WARNING] Failed to refresh credentials: {e}")
                    creds = None
            
            if not creds:
                if not os.path.exists(CREDENTIALS_FILE):
                    print(f"[ERROR] OAuth2 credentials file not found: {CREDENTIALS_FILE}")
                    print("[INFO] Please create OAuth2 credentials and save as oauth_credentials.json")
                    print("[GUIDE] Visit: https://console.cloud.google.com/apis/credentials")
                    return
                
                try:
                    print("[INFO] Starting OAuth2 authentication...")
                    print("[INFO] This will open a browser window automatically")
                    print("[INFO] Please authorize the application in the browser")
                    
                    # Use InstalledAppFlow for proper handling
                    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
                    
                    # Try to run local server for automatic callback handling
                    try:
                        creds = flow.run_local_server(port=8080, open_browser=False)
                        print("[SUCCESS] OAuth2 authentication completed automatically")
                    except Exception as server_error:
                        print(f"[INFO] Automatic server failed: {server_error}")
                        print("[INFO] Falling back to manual authorization...")
                        
                        # Manual authorization flow
                        auth_url, _ = flow.authorization_url(prompt='consent')
                        
                        print("\n" + "="*60)
                        print("MANUAL AUTHORIZATION REQUIRED")
                        print("="*60)
                        print("Please visit this URL to authorize the application:")
                        print(auth_url)
                        print("\nAfter authorization, you'll get a code.")
                        print("Copy the code and paste it below:")
                        print("="*60)
                        
                        auth_code = input("Enter authorization code: ").strip()
                        
                        if auth_code:
                            flow.fetch_token(code=auth_code)
                            creds = flow.credentials
                            print("[SUCCESS] Manual OAuth2 authorization completed")
                        else:
                            print("[ERROR] No authorization code provided")
                            return
                    
                except Exception as e:
                    print(f"[ERROR] OAuth2 authentication failed: {e}")
                    return
            
            # Save the credentials for the next run
            with open(TOKEN_FILE, 'wb') as token:
                pickle.dump(creds, token)
                print(f"[SAVED] OAuth2 credentials saved to {TOKEN_FILE}")
        
        try:
            # Build the Drive service
            self.drive_service = build('drive', 'v3', credentials=creds)
            print("[SUCCESS] Google Drive API initialized with OAuth2")
            
            # Test the connection
            about = self.drive_service.about().get(fields='user').execute()
            user_email = about.get('user', {}).get('emailAddress', 'Unknown')
            print(f"[AUTHENTICATED] Connected as: {user_email}")
            
        except Exception as e:
            print(f"[ERROR] Failed to initialize Google Drive: {e}")
    
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
    
    def find_or_create_drive_folder(self, folder_name: str, parent_id: str = None) -> str:
        """Find existing folder or create new one in Google Drive"""
        
        if not self.drive_service:
            return None
        
        try:
            # Search for existing folder
            query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'"
            if parent_id:
                query += f" and '{parent_id}' in parents"
            
            results = self.drive_service.files().list(q=query).execute()
            items = results.get('files', [])
            
            if items:
                print(f"[FOUND] Google Drive folder: {folder_name}")
                return items[0]['id']
            
            # Create new folder
            folder_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            
            if parent_id:
                folder_metadata['parents'] = [parent_id]
            
            folder = self.drive_service.files().create(body=folder_metadata).execute()
            print(f"[CREATED] Google Drive folder: {folder_name}")
            return folder.get('id')
            
        except Exception as e:
            print(f"[ERROR] Failed to create/find folder '{folder_name}': {e}")
            return None
    
    def find_social_media_business_folder(self, test_mode: bool = False) -> str:
        """Find the 'Social Media Business' folder or test folder"""
        
        if not self.drive_service:
            return None
        
        try:
            # Use test folder if in test mode
            folder_name = 'Social Media Business - TEST' if test_mode else 'Social Media Business'
            
            # Search for folder
            query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'"
            
            results = self.drive_service.files().list(q=query).execute()
            items = results.get('files', [])
            
            if items:
                folder_id = items[0]['id']
                print(f"[FOUND] {folder_name} folder")
                return folder_id
            else:
                # Create the folder if it doesn't exist
                folder_metadata = {
                    'name': folder_name,
                    'mimeType': 'application/vnd.google-apps.folder'
                }
                
                folder = self.drive_service.files().create(body=folder_metadata).execute()
                folder_id = folder.get('id')
                print(f"[CREATED] {folder_name} folder")
                return folder_id
                
        except Exception as e:
            print(f"[ERROR] Failed to find/create '{folder_name}' folder: {e}")
            return None
    
    def upload_file_to_drive(self, file_path: str, file_name: str, folder_id: str = None) -> str:
        """Upload file to Google Drive"""
        
        if not self.drive_service:
            return None
        
        try:
            file_metadata = {'name': file_name}
            if folder_id:
                file_metadata['parents'] = [folder_id]
            
            media = MediaFileUpload(file_path, resumable=True)
            
            file = self.drive_service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id,name,webViewLink'
            ).execute()
            
            print(f"[UPLOADED] {file_name}")
            return file.get('webViewLink')
            
        except Exception as e:
            print(f"[ERROR] Failed to upload '{file_name}': {e}")
            return None
    
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
        
        # Generate shortform content (placeholder - can be enhanced with AI)
        shortform_content = f"{idea['hook']}! At {business_config['business_name']}, {idea['brief'][:100]}... {business_config['cta_template']}"
        
        # Generate longform content (placeholder - can be enhanced with AI)  
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
    
    def generate_and_upload_content(self, business_name: str, ideas: List[Dict], business_config: Dict, test_mode: bool = False):
        """Generate content and upload to Google Drive automatically using OAuth2"""
        
        # Determine client folder path
        test_suffix = "_TEST" if test_mode else ""
        client_folder = os.path.join(self.base_client_dir, f"{business_name}{test_suffix}")
        
        if not os.path.exists(client_folder):
            os.makedirs(client_folder, exist_ok=True)
            print(f"[CREATED] Local test folder: {client_folder}")
        
        # Create monthly folders
        self.create_monthly_folders(client_folder)
        
        # Determine current month folder
        current_month = datetime.now().strftime('%b_25')  # Aug_25, Sep_25, etc.
        monthly_folder = os.path.join(client_folder, current_month)
        
        # Get Google Drive folder name from business config
        drive_folder = business_config.get('google_drive_folder', 'Generated_Content')
        if test_mode:
            drive_folder = f"{drive_folder}_TEST"
        
        folder_type = "TEST" if test_mode else "PRODUCTION"
        print(f"[INFO] Mode: {folder_type}")
        print(f"[INFO] Google Drive target folder: {drive_folder}")
        print(f"[INFO] Generating content for {current_month}")
        
        # Set up Google Drive folder structure: My Drive/Social Media Business/[Client Folder]/[Month]
        social_media_business_id = None
        client_drive_folder_id = None
        monthly_drive_folder_id = None
        
        if self.drive_service:
            # Find or create Social Media Business folder (or test folder)
            social_media_business_id = self.find_social_media_business_folder(test_mode)
            
            if social_media_business_id:
                # Find or create client folder inside Social Media Business
                client_drive_folder_id = self.find_or_create_drive_folder(drive_folder, social_media_business_id)
                
                if client_drive_folder_id:
                    # Find or create monthly subfolder inside client folder
                    monthly_drive_folder_id = self.find_or_create_drive_folder(current_month, client_drive_folder_id)
        
        # Generate and save individual content files
        generated_files = []
        uploaded_files = []
        
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
            
            # Upload to Google Drive if configured
            if self.drive_service and monthly_drive_folder_id:
                upload_link = self.upload_file_to_drive(file_path, filename, monthly_drive_folder_id)
                if upload_link:
                    uploaded_files.append({
                        'filename': filename,
                        'link': upload_link
                    })
        
        # Create summary with Google Drive information
        summary_file = os.path.join(monthly_folder, f"{current_month}_Upload_Summary.txt")
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(f"""CONTENT PACKAGE UPLOAD SUMMARY - {business_name}
{'='*70}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Month: {current_month}
Total Files: {len(generated_files)}

GOOGLE DRIVE UPLOAD STATUS:
===========================
Drive Location: My Drive/Social Media Business{"" if not test_mode else " - TEST"}/{drive_folder}/{current_month}
Client Folder: {drive_folder}
Monthly Subfolder: {current_month}
Upload Status: {'SUCCESS' if uploaded_files else 'LOCAL ONLY'}

""")
            
            if uploaded_files:
                f.write(f"UPLOADED FILES ({len(uploaded_files)}):\n")
                f.write("="*50 + "\n")
                for file_info in uploaded_files:
                    f.write(f"{file_info['filename']}\n")
                    f.write(f"  Link: {file_info['link']}\n\n")
            else:
                f.write("FILES GENERATED LOCALLY:\n")
                f.write("="*30 + "\n")
                for file_info in generated_files:
                    f.write(f"{file_info['filename']}\n")
                    f.write(f"  Path: {file_info['path']}\n\n")
            
            f.write(f"""
NAMING CONVENTION:
=================
Format: {current_month}_##_Type_Topic.txt
- {current_month}: Current month folder
- ##: Sequential number (01-12)
- Type: Content type (Educational, Promotional, etc.)
- Topic: Shortened topic name

CONTENT FEATURES:
================
Each file includes:
- Safety disclaimer about checking AI content
- Contact information for changes (admin@kevinrmiddleton.com)
- Both shortform and longform versions
- Platform usage guide for images

Generated by Content Factory Pro OAuth2 Upload System (Fixed)
Contact: admin@kevinrmiddleton.com
""")
        
        # Upload summary to Drive as well
        if self.drive_service and monthly_drive_folder_id:
            self.upload_file_to_drive(summary_file, f"{current_month}_Upload_Summary.txt", monthly_drive_folder_id)
        
        print(f"\n[SUCCESS] Content package generated for {business_name}")
        print(f"[LOCAL] Saved to: {monthly_folder}")
        
        if uploaded_files:
            print(f"[DRIVE] Uploaded {len(uploaded_files)} files to Google Drive")
            folder_path = f"Social Media Business{'- TEST' if test_mode else ''}/{drive_folder}/{current_month}"
            print(f"[DRIVE] Location: My Drive/{folder_path}")
        else:
            print(f"[INFO] Google Drive upload not configured - files saved locally")
        
        print(f"[FILES] 12 content files created with {current_month}_##_ naming")
        print(f"[SUMMARY] Upload summary saved")
    
    def generate_client_content_oauth_upload(self, business_name: str, test_mode: bool = False):
        """Generate complete content package with automatic Google Drive upload using OAuth2"""
        
        mode_text = "TEST MODE" if test_mode else "PRODUCTION MODE"
        print(f"[INFO] {mode_text} - Generating content with OAuth2 auto-upload for {business_name}...")
        
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
        
        # Generate content and upload to Drive
        self.generate_and_upload_content(business_name, ideas, config, test_mode)

def main():
    """Main function"""
    
    uploader = ContentDriveOAuthUploader()
    
    # Check if user wants test mode
    print("\n=== Content Factory Pro OAuth2 Upload (FIXED) ===")
    print("1. TEST MODE - Upload to 'Social Media Business - TEST' folder")
    print("2. PRODUCTION MODE - Upload to 'Social Media Business' folder")
    
    mode_choice = input("Choose mode (1 for TEST, 2 for PRODUCTION): ").strip()
    test_mode = mode_choice == "1"
    
    if test_mode:
        print("\n[TEST MODE] Files will be uploaded to test folder")
    else:
        print("\n[PRODUCTION MODE] Files will be uploaded to production folder")
    
    # Get business name
    business_name = input("Enter business name: ").strip()
    if not business_name:
        print("[ERROR] Business name is required")
        return
    
    uploader.generate_client_content_oauth_upload(business_name, test_mode)

if __name__ == "__main__":
    main()