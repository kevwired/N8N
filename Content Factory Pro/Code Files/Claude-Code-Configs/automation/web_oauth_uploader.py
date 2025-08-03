#!/usr/bin/env python3
"""
Google Drive uploader using web OAuth2 credentials
Works with your existing web application credentials
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
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import webbrowser
import urllib.parse

# Load environment variables
load_dotenv()

NOTION_API_KEY = os.getenv('NOTION_API_KEY')
NOTION_DATABASE_ID = os.getenv('NOTION_DATABASE_ID')

# OAuth2 configuration
SCOPES = ['https://www.googleapis.com/auth/drive.file']
CREDENTIALS_FILE = 'oauth_credentials.json'
TOKEN_FILE = 'token.pickle'

class WebOAuthUploader:
    def __init__(self):
        self.notion_headers = {
            'Authorization': f'Bearer {NOTION_API_KEY}',
            'Content-Type': 'application/json',
            'Notion-Version': '2022-06-28'
        }
        self.base_client_dir = r"Z:\Main Drive\360TFT Resources\Workflows\N8N\Content Factory Pro\Clients"
        self.drive_service = None
        self._initialize_drive_service()
    
    def _get_web_credentials(self):
        """Load web application credentials"""
        with open(CREDENTIALS_FILE, 'r') as f:
            creds_data = json.load(f)
        
        if 'web' in creds_data:
            return creds_data['web']
        else:
            raise Exception("Web credentials not found in oauth_credentials.json")
    
    def _initialize_drive_service(self):
        """Initialize Google Drive using web OAuth2 flow"""
        
        creds = None
        
        # Check if we have stored credentials
        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, 'rb') as token:
                creds = pickle.load(token)
        
        # If there are no valid credentials available, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                    print("[SUCCESS] Refreshed existing OAuth2 credentials")
                except Exception as e:
                    print(f"[WARNING] Failed to refresh credentials: {e}")
                    creds = None
            
            if not creds:
                print("[INFO] Starting web OAuth2 authentication...")
                creds = self._get_new_credentials()
                
                if creds:
                    # Save credentials for future runs
                    with open(TOKEN_FILE, 'wb') as token:
                        pickle.dump(creds, token)
                    print("[SAVED] Credentials saved for future use")
                else:
                    print("[ERROR] Failed to get credentials")
                    return
        
        try:
            # Build the Drive service
            self.drive_service = build('drive', 'v3', credentials=creds)
            print("[SUCCESS] Google Drive API initialized")
            
            # Test the connection
            about = self.drive_service.about().get(fields='user').execute()
            user_email = about.get('user', {}).get('emailAddress', 'Unknown')
            print(f"[AUTHENTICATED] Connected as: {user_email}")
            
        except Exception as e:
            print(f"[ERROR] Failed to initialize Google Drive: {e}")
    
    def _get_new_credentials(self):
        """Get new credentials using web OAuth2 flow"""
        
        try:
            web_creds = self._get_web_credentials()
            
            # Build authorization URL
            auth_url = "https://accounts.google.com/o/oauth2/auth?" + urllib.parse.urlencode({
                'client_id': web_creds['client_id'],
                'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob',  # Use OOB flow for web credentials
                'scope': ' '.join(SCOPES),
                'response_type': 'code',
                'access_type': 'offline',
                'prompt': 'consent'
            })
            
            print("\n" + "="*70)
            print("GOOGLE OAUTH2 AUTHORIZATION")
            print("="*70)
            print("1. Click the link below or copy and paste it into your browser:")
            print(auth_url)
            print("\n2. Sign in to your Google account")
            print("3. Grant permissions to 'Content Factory Pro'")
            print("4. Copy the authorization code that appears")
            print("5. Paste it below")
            print("="*70)
            
            # Optionally open browser
            try:
                webbrowser.open(auth_url)
                print("[INFO] Browser opened automatically")
            except:
                print("[INFO] Please open the URL manually")
            
            # Get authorization code from user
            auth_code = input("\nEnter the authorization code: ").strip()
            
            if not auth_code:
                print("[ERROR] No authorization code provided")
                return None
            
            # Exchange code for tokens
            token_url = "https://oauth2.googleapis.com/token"
            token_data = {
                'client_id': web_creds['client_id'],
                'client_secret': web_creds['client_secret'],
                'code': auth_code,
                'grant_type': 'authorization_code',
                'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob'
            }
            
            response = requests.post(token_url, data=token_data)
            
            if response.status_code == 200:
                token_info = response.json()
                
                # Create credentials object
                creds = Credentials(
                    token=token_info['access_token'],
                    refresh_token=token_info.get('refresh_token'),
                    id_token=token_info.get('id_token'),
                    token_uri=token_url,
                    client_id=web_creds['client_id'],
                    client_secret=web_creds['client_secret'],
                    scopes=SCOPES
                )
                
                print("[SUCCESS] OAuth2 authorization completed!")
                return creds
            else:
                print(f"[ERROR] Token exchange failed: {response.status_code}")
                print(f"[ERROR] Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"[ERROR] OAuth2 flow failed: {e}")
            return None
    
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
    
    def generate_and_upload_test(self, business_name: str):
        """Generate test content and upload to Google Drive"""
        
        print(f"[INFO] TEST MODE - Generating content for {business_name}...")
        
        # Get business config
        config = self.get_business_config(business_name)
        if not config:
            print(f"[ERROR] Business '{business_name}' not found")
            return
        
        print(f"[SUCCESS] Found configuration for {config['business_name']}")
        
        # Generate ideas
        ideas = self.generate_marketing_ideas(config)
        
        # Create test folder structure
        test_folder = os.path.join(self.base_client_dir, f"{business_name}_TEST")
        current_month = datetime.now().strftime('%b_25')
        monthly_folder = os.path.join(test_folder, current_month)
        os.makedirs(monthly_folder, exist_ok=True)
        
        # Set up Google Drive folder
        drive_folder_name = f"{config.get('google_drive_folder', business_name)}_TEST"
        
        if self.drive_service:
            # Find or create Social Media Business - TEST folder
            test_parent = self.find_or_create_drive_folder('Social Media Business - TEST')
            
            if test_parent:
                # Create client folder
                client_drive_folder = self.find_or_create_drive_folder(drive_folder_name, test_parent)
                
                if client_drive_folder:
                    # Create monthly folder  
                    monthly_drive_folder = self.find_or_create_drive_folder(current_month, client_drive_folder)
        
        # Generate content files
        uploaded_files = []
        
        for idx, idea in enumerate(ideas, 1):
            clean_topic = idea['topic'].replace('?', '').replace(':', '').replace(' ', '_')[:25]
            filename = f"{current_month}_{idx:02d}_{idea['type']}_{clean_topic}.txt"
            
            content = self.generate_content_with_disclaimer(idea, config, idx, current_month)
            
            # Save locally
            file_path = os.path.join(monthly_folder, filename)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"[{idx:02d}/12] Generated: {filename}")
            
            # Upload to Drive
            if self.drive_service and 'monthly_drive_folder' in locals():
                upload_link = self.upload_file_to_drive(file_path, filename, monthly_drive_folder)
                if upload_link:
                    uploaded_files.append({'filename': filename, 'link': upload_link})
        
        print(f"\n[SUCCESS] Generated {len(ideas)} content files")
        print(f"[LOCAL] Saved to: {monthly_folder}")
        
        if uploaded_files:
            print(f"[DRIVE] Uploaded {len(uploaded_files)} files to Google Drive")
            print(f"[DRIVE] Location: Social Media Business - TEST/{drive_folder_name}/{current_month}")
        else:
            print("[INFO] Google Drive upload not available")

def main():
    """Main function"""
    
    print("="*60)
    print("    Content Factory Pro - Web OAuth2 Uploader")
    print("="*60)
    
    uploader = WebOAuthUploader()
    
    business_name = input("Enter business name for testing: ").strip()
    if not business_name:
        print("[ERROR] Business name required")
        return
    
    uploader.generate_and_upload_test(business_name)

if __name__ == "__main__":
    main()