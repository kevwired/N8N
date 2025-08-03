# Content Factory Pro Automation

Business-agnostic automation for generating business configurations and content strategies with Notion database integration.

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Environment Variables
Create a `.env` file in the automation folder:
```env
NOTION_API_KEY=your_notion_api_key_here
NOTION_DATABASE_ID=your_notion_database_id_here
```

### 3. Verify Notion Connection
```bash
python notion_client.py
```

## Usage

### Process Single Business
```bash
cd /path/to/business/folder/
python ../automation/content_factory_automation.py