#!/usr/bin/env python3
"""
Simple test script to upload a file to Google Drive
"""

import os
import json
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account

# Load environment variables
load_dotenv()

GOOGLE_DRIVE_SERVICE_ACCOUNT_JSON = os.getenv('GOOGLE_DRIVE_SERVICE_ACCOUNT_JSON')

def test_drive_upload():
    """Test Google Drive upload functionality"""
    
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
        
        # Create test folder
        test_folder_metadata = {
            'name': 'Content_Factory_Test',
            'mimeType': 'application/vnd.google-apps.folder'
        }
        
        test_folder = drive_service.files().create(body=test_folder_metadata).execute()
        folder_id = test_folder.get('id')
        
        print(f"[CREATED] Test folder: Content_Factory_Test")
        print(f"[FOLDER ID] {folder_id}")
        
        # Upload test file
        test_file_path = "test_upload.txt"
        
        if not os.path.exists(test_file_path):
            print(f"[ERROR] Test file not found: {test_file_path}")
            return
        
        file_metadata = {
            'name': 'Content_Factory_Test_Upload.txt',
            'parents': [folder_id]
        }
        
        media = MediaFileUpload(test_file_path, resumable=True)
        
        uploaded_file = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id,name,webViewLink,parents'
        ).execute()
        
        print(f"[UPLOADED] File: {uploaded_file['name']}")
        print(f"[FILE ID] {uploaded_file['id']}")
        print(f"[VIEW LINK] {uploaded_file['webViewLink']}")
        print(f"[LOCATION] Google Drive > Content_Factory_Test > Content_Factory_Test_Upload.txt")
        
        # Share the folder publicly to test access
        permission = {
            'type': 'anyone',
            'role': 'reader'
        }
        
        drive_service.permissions().create(
            fileId=folder_id,
            body=permission
        ).execute()
        
        print(f"[SHARED] Folder shared publicly for testing")
        print(f"[ACCESS] https://drive.google.com/drive/folders/{folder_id}")
        
        return uploaded_file['webViewLink']
        
    except Exception as e:
        print(f"[ERROR] Upload failed: {e}")
        return None

if __name__ == "__main__":
    test_drive_upload()