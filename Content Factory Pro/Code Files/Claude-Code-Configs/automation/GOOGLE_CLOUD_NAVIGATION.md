# Google Cloud Console Navigation Guide

## Can't Find OAuth Settings? Follow These Exact Steps:

### Step 1: Get to the Right Place
1. **Go to**: https://console.cloud.google.com/
2. **Look at the top left** - make sure it shows your project: `n8n-skool-automation`
3. **If wrong project**: Click the project name dropdown and select `n8n-skool-automation`

### Step 2: Navigate to APIs & Services
1. **Click the hamburger menu** (☰) in the top left corner
2. **Scroll down** to find **"APIs & Services"**
3. **Click "APIs & Services"**
4. **You'll see a submenu appear**

### Step 3: Find OAuth Consent Screen
In the APIs & Services submenu, you should see:
- Overview
- Library
- **Credentials** ← Click this first
- **OAuth consent screen** ← This is what we need
- Domain verification
- Usage

**Click "OAuth consent screen"**

### Step 4: What You Should See
If this is your first time, you'll see:
- **"Configure Consent Screen"** button
- **OR** an existing consent screen configuration

## Alternative Navigation Method

### Method 2: Direct Link
1. **Copy this exact URL**: 
   ```
   https://console.cloud.google.com/apis/credentials/consent?project=n8n-skool-automation
   ```
2. **Paste it in your browser**
3. **This takes you directly to OAuth consent screen**

### Method 3: Search Box
1. **At the top of Google Cloud Console**, there's a search box
2. **Type**: "OAuth consent screen"
3. **Click the search result**

## What If You Still Can't Find It?

### Check These Things:
1. **Project Selection**: Make sure `n8n-skool-automation` is selected
2. **Permissions**: You need to be an owner/editor of the project
3. **APIs Enabled**: Google Drive API needs to be enabled first

### Enable Google Drive API First:
1. **Go to**: https://console.cloud.google.com/apis/library
2. **Search for**: "Google Drive API"
3. **Click on it** and press **"ENABLE"**
4. **Then try finding OAuth consent screen again**

## Screenshots Reference

### What the Left Menu Should Look Like:
```
☰ Navigation menu
├── Home
├── Compute Engine
├── Kubernetes Engine
├── App Engine
├── Cloud Functions
├── APIs & Services          ← Click here
│   ├── Overview
│   ├── Library
│   ├── Credentials
│   ├── OAuth consent screen ← Then click here
│   ├── Domain verification
│   └── Usage
└── IAM & Admin
```

### What OAuth Consent Screen Looks Like:
```
OAuth consent screen
════════════════════════════════════════

User Type
○ Internal    ● External

[CREATE] or [EDIT APP]
```

## Still Can't Find It?

**Send me a screenshot** of what you see when you:
1. Go to https://console.cloud.google.com/
2. Click the hamburger menu (☰)
3. Look for "APIs & Services"

I'll help you navigate from there!