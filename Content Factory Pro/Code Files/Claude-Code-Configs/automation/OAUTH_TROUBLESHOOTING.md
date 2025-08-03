# OAuth2 Access Blocked - Troubleshooting Guide

## Error: "Access blocked: Authorization Error"

This error occurs when the OAuth2 app is not properly configured in Google Cloud Console.

## Quick Fix Steps

### 1. Configure OAuth Consent Screen

1. Go to: https://console.cloud.google.com/apis/credentials/consent
2. Select your project: `n8n-skool-automation`
3. **User Type**: Choose "External" (unless you have Google Workspace)
4. Click "CREATE"

### 2. Fill Out App Information

**App Information:**
- App name: `Content Factory Pro`
- User support email: Your email address
- Developer contact information: Your email address

**App Domain (Optional but recommended):**
- Leave blank for now or add your website

**Authorized domains:**
- Leave blank for testing

### 3. Add Scopes

**Add the following scope:**
- `https://www.googleapis.com/auth/drive.file`

Click "ADD OR REMOVE SCOPES"
Search for "Google Drive API"
Select: "See, edit, create, and delete only the specific Google Drive files you use with this app"

### 4. Add Test Users (IMPORTANT)

**For External apps, you MUST add test users:**
1. In the "Test users" section, click "ADD USERS"
2. Add your Gmail address (the one you'll use for authorization)
3. Save

### 5. Publish App (Optional)

If you want to skip the test user requirement:
1. Go back to OAuth consent screen
2. Click "PUBLISH APP"
3. Submit for verification (or use in testing mode)

## Alternative: Create New Desktop App Credentials

If you're still having issues, create proper desktop app credentials:

### 1. Create New Credentials
1. Go to: https://console.cloud.google.com/apis/credentials
2. Click "CREATE CREDENTIALS" > "OAuth client ID"
3. **Application type**: "Desktop application"
4. **Name**: "Content Factory Pro Desktop"
5. Click "CREATE"

### 2. Download New Credentials
1. Click the download button (JSON)
2. Save as `oauth_credentials.json` (replace the existing one)

## Test the Fix

After making these changes:

```bash
# Delete old token if exists
del token.pickle

# Test with fixed script
py auto_upload_fixed.py
```

## Still Having Issues?

If you're still getting access blocked:

1. **Check project**: Make sure you're in the right Google Cloud project
2. **Enable APIs**: Ensure Google Drive API is enabled
3. **Wait**: Sometimes changes take a few minutes to propagate
4. **Use incognito**: Try authorization in incognito/private browser window

## Verification Checklist

✅ OAuth consent screen configured  
✅ App name and contact email set  
✅ Google Drive scope added  
✅ Your email added as test user  
✅ Credentials downloaded as JSON  
✅ Google Drive API enabled  

## Quick Debug Command

```bash
py simple_oauth_test.py
```

This will show you the authorization URL to test if the basic OAuth flow works.