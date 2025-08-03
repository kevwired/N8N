#!/usr/bin/env python3
"""
Debug OAuth2 authentication issues
"""

import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow

# Allow insecure transport for localhost
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

SCOPES = ['https://www.googleapis.com/auth/drive.file']
CREDENTIALS_FILE = 'oauth_credentials.json'

def debug_oauth_credentials():
    """Debug the OAuth2 credentials file"""
    
    print("=== DEBUGGING OAUTH2 CREDENTIALS ===")
    
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"[ERROR] {CREDENTIALS_FILE} not found")
        return False
    
    try:
        with open(CREDENTIALS_FILE, 'r') as f:
            creds = json.load(f)
        
        print(f"[SUCCESS] Credentials file loaded")
        print(f"[INFO] Keys in file: {list(creds.keys())}")
        
        if 'web' in creds:
            web_creds = creds['web']
            print(f"[INFO] Web credentials found")
            print(f"[INFO] Client ID: {web_creds.get('client_id', 'MISSING')}")
            print(f"[INFO] Project ID: {web_creds.get('project_id', 'MISSING')}")
            print(f"[INFO] Redirect URIs: {web_creds.get('redirect_uris', 'MISSING')}")
            
            # Check if we can create a flow
            try:
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
                print(f"[SUCCESS] Can create OAuth2 flow")
                return True
            except Exception as e:
                print(f"[ERROR] Cannot create OAuth2 flow: {e}")
                return False
                
        elif 'installed' in creds:
            installed_creds = creds['installed']
            print(f"[INFO] Installed app credentials found")
            print(f"[INFO] Client ID: {installed_creds.get('client_id', 'MISSING')}")
            print(f"[INFO] Project ID: {installed_creds.get('project_id', 'MISSING')}")
            
            try:
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
                print(f"[SUCCESS] Can create OAuth2 flow")
                return True
            except Exception as e:
                print(f"[ERROR] Cannot create OAuth2 flow: {e}")
                return False
        else:
            print(f"[ERROR] No 'web' or 'installed' section found")
            return False
            
    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return False

def test_simple_oauth():
    """Test a simple OAuth2 flow"""
    
    print("\n=== TESTING SIMPLE OAUTH2 FLOW ===")
    
    try:
        # Use InstalledAppFlow which handles redirects better
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
        
        print("[INFO] Starting OAuth2 flow...")
        print("[INFO] This will open a browser window")
        print("[INFO] Please authorize the application")
        
        # Run local server - this should handle the callback automatically
        creds = flow.run_local_server(port=8080)
        
        if creds:
            print("[SUCCESS] OAuth2 authentication successful!")
            print(f"[INFO] Token: {creds.token[:20]}...")
            
            # Save token for future use
            with open('token.pickle', 'wb') as token:
                import pickle
                pickle.dump(creds, token)
            print("[SAVED] Token saved to token.pickle")
            
            return creds
        else:
            print("[ERROR] No credentials returned")
            return None
            
    except Exception as e:
        print(f"[ERROR] OAuth2 flow failed: {e}")
        return None

if __name__ == "__main__":
    print("OAuth2 Debug Tool")
    print("=" * 50)
    
    # Debug credentials
    creds_ok = debug_oauth_credentials()
    
    if creds_ok:
        # Test OAuth flow
        creds = test_simple_oauth()
        
        if creds:
            print("\n[SUCCESS] OAuth2 setup is working!")
            print("[NEXT] You can now run the upload scripts")
        else:
            print("\n[FAILED] OAuth2 authentication failed")
    else:
        print("\n[FAILED] Credentials file has issues")