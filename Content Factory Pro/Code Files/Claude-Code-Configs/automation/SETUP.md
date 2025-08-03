# Content Factory Pro - Business Automation

Secure automation system for uploading businesses to Notion database.

## 🔒 Security Setup

This system uses environment variables to keep API keys secure and out of version control.

### First Time Setup:

1. **Copy the environment template:**
   ```bash
   cp .env.example .env
   ```

2. **Edit .env with your actual credentials:**
   ```bash
   NOTION_API_KEY=your_actual_notion_api_key
   NOTION_DATABASE_ID=your_actual_database_id
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage

### Single Business Upload (Interactive):
```bash
python business_uploader.py
```

### Single Business Upload (JSON):
```bash
python business_uploader.py --json business_data.json
```

### Batch Upload:
```bash
python batch_uploader.py --csv businesses.csv
python batch_uploader.py --json businesses.json
```

### Create Templates:
```bash
python business_uploader.py --template
python batch_uploader.py --csv-template
python batch_uploader.py --json-template
```

## 📋 Complete Schema Support

The system supports all 29 columns required by Content Factory Pro:
- Basic business information
- Target audience and brand voice
- Content strategy fields
- SEO and social media settings
- System messages for automation
- All workflow-required fields

## 🔐 Security Features

- ✅ No hardcoded API keys in code
- ✅ Environment variables for credentials
- ✅ .gitignore prevents accidental commits
- ✅ Configuration validation
- ✅ Secure error handling

## 📁 Files Explained

- `business_uploader.py` - Main interactive uploader
- `batch_uploader.py` - Batch processing for multiple businesses
- `notion_client.py` - Notion API interface
- `config.py` - Secure configuration management
- `.env` - Your actual credentials (NOT committed to git)
- `.env.example` - Template for credentials
- `requirements.txt` - Python dependencies

## ⚠️ Important

**Never commit the `.env` file to git!** It contains your actual API keys.
Always use the `.env.example` as a template for new environments.