#!/usr/bin/env python3
"""
Secure configuration management for Content Factory Pro
Loads settings from environment variables or .env file
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
env_path = Path(__file__).parent / '.env'
if env_path.exists():
    load_dotenv(env_path)

class Config:
    """Configuration class that loads from environment variables"""
    
    # Notion API Configuration
    NOTION_API_KEY = os.getenv('NOTION_API_KEY')
    NOTION_DATABASE_ID = os.getenv('NOTION_DATABASE_ID')
    
    # Optional API keys
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    @classmethod
    def validate(cls):
        """Validate that required configuration is present"""
        missing = []
        
        if not cls.NOTION_API_KEY:
            missing.append('NOTION_API_KEY')
        if not cls.NOTION_DATABASE_ID:
            missing.append('NOTION_DATABASE_ID')
            
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
        
        return True
    
    @classmethod
    def get_notion_config(cls):
        """Get Notion configuration as dict"""
        cls.validate()
        return {
            'api_key': cls.NOTION_API_KEY,
            'database_id': cls.NOTION_DATABASE_ID
        }