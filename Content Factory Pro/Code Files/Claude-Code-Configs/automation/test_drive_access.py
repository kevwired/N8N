#!/usr/bin/env python3
"""
Test what folders the service account can access
"""

import os
import json
from dotenv import load_dotenv
from googleapiclient.discovery import build
from google.oauth2 import service_account

# Load environment variables
load_dotenv()

GOOGLE_DRIVE_SERVICE_ACCOUNT_JSON = os.getenv('GOOGLE_DRIVE_SERVICE_ACCOUNT_JSON')

def test_drive_access():
    """Test what the service account can access"""
    
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
        
        # List all folders accessible to the service account
        print("\n[SEARCHING] All accessible folders...")
        
        query = "mimeType='application/vnd.google-apps.folder'"
        results = drive_service.files().list(q=query, pageSize=50, fields="files(id, name, parents)").execute()
        items = results.get('files', [])
        
        print(f"[FOUND] {len(items)} accessible folders:")
        
        for item in items:
            print(f"  • {item['name']} (ID: {item['id']})")
            if 'parents' in item:
                print(f"    Parents: {item['parents']}")
        
        # Search specifically for folders with "Social" in the name
        print("\n[SEARCHING] Folders containing 'Social'...")
        
        query = "mimeType='application/vnd.google-apps.folder' and name contains 'Social'"
        results = drive_service.files().list(q=query, fields="files(id, name, parents)").execute()
        items = results.get('files', [])
        
        if items:
            print(f"[FOUND] {len(items)} folders with 'Social':")
            for item in items:
                print(f"  • {item['name']} (ID: {item['id']})")
        else:
            print("[NOT FOUND] No folders containing 'Social'")
        
        # Search for folders with "Media" in the name
        print("\n[SEARCHING] Folders containing 'Media'...")
        
        query = "mimeType='application/vnd.google-apps.folder' and name contains 'Media'"
        results = drive_service.files().list(q=query, fields="files(id, name, parents)").execute()
        items = results.get('files', [])
        
        if items:
            print(f"[FOUND] {len(items)} folders with 'Media':")
            for item in items:
                print(f"  • {item['name']} (ID: {item['id']})")
        else:
            print("[NOT FOUND] No folders containing 'Media'")
        
        # Search for folders with "Business" in the name
        print("\n[SEARCHING] Folders containing 'Business'...")
        
        query = "mimeType='application/vnd.google-apps.folder' and name contains 'Business'"
        results = drive_service.files().list(q=query, fields="files(id, name, parents)").execute()
        items = results.get('files', [])
        
        if items:
            print(f"[FOUND] {len(items)} folders with 'Business':")
            for item in items:
                print(f"  • {item['name']} (ID: {item['id']})")
        else:
            print("[NOT FOUND] No folders containing 'Business'")
            
    except Exception as e:
        print(f"[ERROR] Test failed: {e}")

if __name__ == "__main__":
    test_drive_access()