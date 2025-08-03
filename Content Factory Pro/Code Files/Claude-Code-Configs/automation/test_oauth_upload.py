#!/usr/bin/env python3
"""
Test script for OAuth2 Google Drive upload
Automatically runs in TEST MODE to avoid affecting production files
"""

from auto_upload_oauth import ContentDriveOAuthUploader

def main():
    """Test function - always runs in test mode"""
    
    print("="*60)
    print("         CONTENT FACTORY PRO - TEST MODE")
    print("="*60)
    print("This script runs in TEST MODE only.")
    print("Files will be uploaded to: 'Social Media Business - TEST'")
    print("Local files saved to: [Client]_TEST folders")
    print("="*60)
    
    uploader = ContentDriveOAuthUploader()
    
    # Get business name
    business_name = input("\nEnter business name for testing: ").strip()
    if not business_name:
        print("[ERROR] Business name is required")
        return
    
    print(f"\n[TEST] Running test upload for: {business_name}")
    print("[TEST] This will NOT affect your production files")
    
    # Always run in test mode
    uploader.generate_client_content_oauth_upload(business_name, test_mode=True)
    
    print("\n" + "="*60)
    print("TEST COMPLETE!")
    print("Check your Google Drive for:")
    print("  My Drive/Social Media Business - TEST/[Client]_TEST/Aug_25/")
    print("="*60)

if __name__ == "__main__":
    main()