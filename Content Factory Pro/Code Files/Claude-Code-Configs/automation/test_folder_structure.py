#!/usr/bin/env python3
"""
Test the correct Google Drive folder structure
My Drive/Social Media Business/[Client Folder]/[Month]
"""

import os
import json
from dotenv import load_dotenv
from googleapiclient.discovery import build
from google.oauth2 import service_account

# Load environment variables
load_dotenv()

GOOGLE_DRIVE_SERVICE_ACCOUNT_JSON = os.getenv('GOOGLE_DRIVE_SERVICE_ACCOUNT_JSON')

def test_folder_structure():
    """Test the correct Google Drive folder structure"""
    
    try:
        # Parse credentials
        credentials_info = json.loads(GOOGLE_DRIVE_SERVICE_ACCOUNT_JSON)
        
        # Create credentials
        credentials = service_account.Credentials.from_service_account_info(
            credentials_info,
            scopes=['https://www.googleapis.com/auth/drive.file']
        )
        
        # Build Drive service
        drive_service = build('drive', 'v3', credentials=credentials)
        
        print("[SUCCESS] Google Drive API initialized")
        print(f"[INFO] Service Account: {credentials_info['client_email']}")
        
        # Search for 'Social Media Business' folder
        query = "name='Social Media Business' and mimeType='application/vnd.google-apps.folder'"
        results = drive_service.files().list(q=query).execute()
        items = results.get('files', [])
        
        if items:
            social_media_id = items[0]['id']
            print(f"[FOUND] Social Media Business folder")
            print(f"[FOLDER ID] {social_media_id}")
            print(f"[LOCATION] My Drive/Social Media Business")
            
            # Test creating a client folder structure
            test_client_folder = "KF_Barbers"
            test_month = "Aug_25"
            
            # Create client folder
            client_metadata = {
                'name': test_client_folder,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [social_media_id]
            }
            
            client_folder = drive_service.files().create(body=client_metadata).execute()
            client_id = client_folder.get('id')
            
            print(f"[CREATED] Client folder: {test_client_folder}")
            print(f"[CLIENT ID] {client_id}")
            print(f"[LOCATION] My Drive/Social Media Business/{test_client_folder}")
            
            # Create month folder
            month_metadata = {
                'name': test_month,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [client_id]
            }
            
            month_folder = drive_service.files().create(body=month_metadata).execute()
            month_id = month_folder.get('id')
            
            print(f"[CREATED] Month folder: {test_month}")
            print(f"[MONTH ID] {month_id}")
            print(f"[FINAL LOCATION] My Drive/Social Media Business/{test_client_folder}/{test_month}")
            
            # Generate access URL
            print(f"[ACCESS URL] https://drive.google.com/drive/folders/{month_id}")
            
            return True
            
        else:
            print("[ERROR] 'Social Media Business' folder not found")
            print("[INFO] Please ensure the folder exists and is shared with the service account")
            print(f"[SHARE WITH] {credentials_info['client_email']}")
            return False
            
    except Exception as e:
        print(f"[ERROR] Test failed: {e}")
        return False

if __name__ == "__main__":
    test_folder_structure()