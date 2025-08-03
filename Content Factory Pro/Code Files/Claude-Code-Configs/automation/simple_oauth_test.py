#!/usr/bin/env python3
"""
Simple OAuth2 test - just provides URL for manual authorization
"""

import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow

# Allow insecure transport for localhost
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

SCOPES = ['https://www.googleapis.com/auth/drive.file']
CREDENTIALS_FILE = 'oauth_credentials.json'

def get_oauth_url():
    """Get OAuth2 authorization URL without automatic callback handling"""
    
    print("=== SIMPLE OAUTH2 URL GENERATOR ===")
    
    try:
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
        
        # Generate authorization URL
        auth_url, _ = flow.authorization_url(prompt='consent')
        
        print("\n" + "="*60)
        print("OAUTH2 AUTHORIZATION URL:")
        print("="*60)
        print(auth_url)
        print("="*60)
        
        print("\nINSTRUCTIONS:")
        print("1. Copy the URL above")
        print("2. Open it in your browser")
        print("3. Sign in to your Google account") 
        print("4. Authorize 'Content Factory Pro'")
        print("5. You'll see a success page or error")
        print("6. If successful, the token will be saved automatically")
        
        return auth_url
        
    except Exception as e:
        print(f"[ERROR] Failed to generate OAuth2 URL: {e}")
        return None

if __name__ == "__main__":
    get_oauth_url()