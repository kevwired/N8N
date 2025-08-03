# Google Drive OAuth2 Setup Guide

## Quick Setup Steps

### 1. Create Google Cloud Project
1. Go to: https://console.cloud.google.com/
2. Click "New Project" or select existing project
3. Note your Project ID

### 2. Enable Google Drive API
1. In Google Cloud Console, go to "APIs & Services" > "Library"
2. Search for "Google Drive API"
3. Click on it and press "ENABLE"

### 3. Create OAuth2 Credentials
1. Go to "APIs & Services" > "Credentials"
2. Click "CREATE CREDENTIALS" > "OAuth client ID"
3. If prompted, configure OAuth consent screen:
   - User Type: External (for personal use)
   - App name: "Content Factory Pro"
   - User support email: Your email
   - Developer contact: Your email
   - Add scope: `https://www.googleapis.com/auth/drive.file`
4. Application type: "Desktop application"
5. Name: "Content Factory Pro Desktop"
6. Click "CREATE"

### 4. Download Credentials
1. Click "DOWNLOAD JSON" button
2. Save the file as `oauth_credentials.json` in this folder

### 5. Run the OAuth2 Script

**For Testing (Recommended First):**
```bash
py test_oauth_upload.py
```

**For Production:**
```bash
py auto_upload_oauth.py
```

### 6. First Time Authentication
1. A browser window will open
2. Sign in to your Google account
3. Grant permissions to "Content Factory Pro"
4. Copy the callback URL back to the script
5. Authentication will be saved for future use

## Expected File Structure

Your `oauth_credentials.json` should look like this:
```json
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
```

## Benefits of OAuth2 vs Service Account

✅ **Works with personal Google Drive**  
✅ **No storage quota limitations**  
✅ **Full upload permissions**  
✅ **Can create folders automatically**  
✅ **One-time setup, then automatic**  

## Troubleshooting

- If authentication fails, delete `token.pickle` and try again
- Ensure `oauth_credentials.json` is in the automation folder
- Check that Google Drive API is enabled in your project
- Make sure you're signed into the correct Google account

## Upload Structure

**Test Mode** uploads to:
```
My Drive/
└── Social Media Business - TEST/
    └── [Client Name]_TEST/
        └── Aug_25/
            ├── Aug_25_01_Educational_How_Often_Should_You_Get_.txt
            ├── Aug_25_02_Educational_Beard_Maintenance_Between.txt
            └── ... (all 12 files)
```

**Production Mode** uploads to:
```
My Drive/
└── Social Media Business/
    └── [Client Name from Database]/
        └── Aug_25/
            ├── Aug_25_01_Educational_How_Often_Should_You_Get_.txt
            ├── Aug_25_02_Educational_Beard_Maintenance_Between.txt
            └── ... (all 12 files)
```

The client folder name comes from the "Google Drive Parent Folder" column in your Business_Configurations database.

## Test vs Production

- **Test Mode**: Safe testing without affecting real client folders
- **Production Mode**: Real uploads to client folders for actual use
- Always test first with `py test_oauth_upload.py`