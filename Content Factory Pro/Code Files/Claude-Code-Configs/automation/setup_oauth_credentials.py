#!/usr/bin/env python3
"""
Setup script to help create OAuth2 credentials for Google Drive
"""

import json
import os

def create_oauth_credentials_template():
    """Create a template for OAuth2 credentials"""
    
    template = {
        "installed": {
            "client_id": "YOUR_CLIENT_ID.apps.googleusercontent.com",
            "project_id": "your-project-id",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_secret": "YOUR_CLIENT_SECRET",
            "redirect_uris": ["http://localhost:8080/callback"]
        }
    }
    
    template_file = "oauth_credentials_template.json"
    
    with open(template_file, 'w') as f:
        json.dump(template, f, indent=2)
    
    print(f"[CREATED] OAuth2 credentials template: {template_file}")
    return template_file

def show_oauth_setup_instructions():
    """Show detailed instructions for setting up OAuth2 credentials"""
    
    print("""
═══════════════════════════════════════════════════════════════
            GOOGLE DRIVE OAUTH2 SETUP INSTRUCTIONS
═══════════════════════════════════════════════════════════════

STEP 1: CREATE GOOGLE CLOUD PROJECT
-----------------------------------
1. Go to: https://console.cloud.google.com/
2. Click "New Project" or select existing project
3. Note your Project ID

STEP 2: ENABLE GOOGLE DRIVE API
-------------------------------
1. In Google Cloud Console, go to "APIs & Services" > "Library"
2. Search for "Google Drive API"
3. Click on it and press "ENABLE"

STEP 3: CREATE OAUTH2 CREDENTIALS
---------------------------------
1. Go to "APIs & Services" > "Credentials"
2. Click "CREATE CREDENTIALS" > "OAuth client ID"
3. If prompted, configure OAuth consent screen:
   - User Type: External (for personal use)
   - App name: "Content Factory Pro"
   - User support email: Your email
   - Developer contact: Your email
   - Add scope: https://www.googleapis.com/auth/drive.file
4. Application type: "Desktop application"
5. Name: "Content Factory Pro Desktop"
6. Click "CREATE"

STEP 4: DOWNLOAD CREDENTIALS
---------------------------
1. Click "DOWNLOAD JSON" button
2. Save the file as "oauth_credentials.json" in this folder:
   Z:\\Main Drive\\360TFT Resources\\Workflows\\N8N\\Content Factory Pro\\Code Files\\Claude-Code-Configs\\automation\\

STEP 5: REQUIRED FILE STRUCTURE
-------------------------------
Your oauth_credentials.json should look like this:
{
  "installed": {
    "client_id": "123456789.apps.googleusercontent.com",
    "project_id": "your-project-name",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "GOCSPX-your_client_secret",
    "redirect_uris": ["http://localhost"]
  }
}

STEP 6: FIRST RUN AUTHENTICATION
--------------------------------
1. Run: py auto_upload_oauth.py
2. Follow the authentication prompts
3. Grant permissions in your browser
4. Copy the callback URL back to the script

STEP 7: TEST THE UPLOAD
----------------------
1. Enter a business name (e.g., "KF Barbers")
2. The script will authenticate and upload files automatically
3. Check your Google Drive: My Drive/Social Media Business/[Client]/Aug_25

═══════════════════════════════════════════════════════════════
                        IMPORTANT NOTES
═══════════════════════════════════════════════════════════════

• OAuth2 requires one-time browser authentication
• Credentials are saved locally for future use
• Much more reliable than Service Account for regular Drive
• Uploads work to your personal Google Drive account
• No storage quota limitations

TROUBLESHOOTING:
- If authentication fails, delete token.pickle and try again
- Ensure oauth_credentials.json is in the automation folder
- Check that Google Drive API is enabled in your project

═══════════════════════════════════════════════════════════════
""")

def check_oauth_setup():
    """Check if OAuth2 credentials are properly configured"""
    
    credentials_file = "oauth_credentials.json"
    
    if os.path.exists(credentials_file):
        try:
            with open(credentials_file, 'r') as f:
                creds = json.load(f)
            
            if 'installed' in creds:
                client_id = creds['installed'].get('client_id', '')
                client_secret = creds['installed'].get('client_secret', '')
                
                if client_id.startswith('YOUR_') or client_secret.startswith('YOUR_'):
                    print(f"[WARNING] {credentials_file} contains template values")
                    print("[ACTION] Please replace with actual credentials from Google Cloud Console")
                    return False
                else:
                    print(f"[SUCCESS] OAuth2 credentials file configured: {credentials_file}")
                    print(f"[CLIENT] {client_id[:20]}...")
                    return True
            else:
                print(f"[ERROR] Invalid OAuth2 credentials format in {credentials_file}")
                return False
                
        except json.JSONDecodeError:
            print(f"[ERROR] Invalid JSON in {credentials_file}")
            return False
    else:
        print(f"[MISSING] OAuth2 credentials file not found: {credentials_file}")
        print("[ACTION] Please create oauth_credentials.json from Google Cloud Console")
        return False

def main():
    """Main setup function"""
    
    print("[SETUP] Google Drive OAuth2 Configuration")
    print("="*60)
    
    # Check current setup
    is_configured = check_oauth_setup()
    
    if not is_configured:
        print("\n[CREATING] OAuth2 credentials template...")
        create_oauth_credentials_template()
        
        print("\n[INSTRUCTIONS] Follow these steps to set up OAuth2:")
        show_oauth_setup_instructions()
    else:
        print("\n[READY] OAuth2 credentials are configured!")
        print("[NEXT] Run: py auto_upload_oauth.py")

if __name__ == "__main__":
    main()