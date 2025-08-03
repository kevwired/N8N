#!/usr/bin/env python3
"""
Content Factory Pro - Business Agnostic Automation
Processes any business folder with standardized file names
"""

import os
import sys
import json
import pandas as pd
from pathlib import Path
from datetime import datetime
from notion_client import NotionClient
from business_processor import *
from research_engine import *

def process_business_folder(folder_path=None):
    """Process business folder with standardized file structure"""
    
    if folder_path is None:
        folder_path = Path.cwd()
    else:
        folder_path = Path(folder_path)
    
    print(f"🚀 Processing business folder: {folder_path.name}")
    
    # Standard file paths (business agnostic)
    submission_file = folder_path / "submission.md"
    config_output = folder_path / "business-config.csv"
    content_output = folder_path / "content-strategy.csv"
    research_output = folder_path / "research-notes.md"
    
    # Validate input files exist
    if not submission_file.exists():
        print(f"❌ Error: submission.md not found in {folder_path}")
        return False
    
    try:
        # Step 1: Parse client submission
        print("📝 Parsing client submission...")
        business_data = parse_submission(submission_file)
        
        # Step 2: Conduct research
        print("🔍 Conducting business research...")
        research_data = conduct_business_research(business_data)
        
        # Step 3: Generate business configuration CSV
        print("⚙️ Generating business configuration...")
        config_csv = generate_business_config(business_data, research_data)
        
        # Step 4: Generate content strategy CSV
        print("📊 Generating content strategy...")
        content_csv = generate_content_strategy(business_data, config_csv)
        
        # Step 5: Export files
        print("💾 Exporting files...")
        config_csv.to_csv(config_output, index=False)
        content_csv.to_csv(content_output, index=False)
        export_research_notes(research_data, research_output)
        
        # Step 6: Add to Notion database
        print("🔗 Adding to Notion database...")
        try:
            notion_client = NotionClient()
            
            # Check if business already exists
            existing_business = notion_client.find_business_by_name(business_data['name'])
            
            if existing_business:
                print(f"⚠️ Business '{business_data['name']}' already exists in database, updating...")
                notion_client.update_business_record(existing_business['id'], business_data)
            else:
                notion_client.add_business_to_database(business_data)
                
        except Exception as e:
            print(f"⚠️ Failed to add to Notion database: {e}")
            print("   Continuing with local file generation...")
        
        print(f"✅ Successfully processed {business_data['name']}")
        print(f"   📄 Generated: {config_output.name}")
        print(f"   📄 Generated: {content_output.name}")
        print(f"   📄 Generated: {research_output.name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error processing {folder_path.name}: {str(e)}")
        return False

if __name__ == "__main__":
    # Can be run from any business folder or specify path
    folder_path = sys.argv[1] if len(sys.argv) > 1 else None
    success = process_business_folder(folder_path)
    sys.exit(0 if success else 1)