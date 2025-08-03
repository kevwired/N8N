#!/usr/bin/env python3
"""
Test content generation for Athlete Recovery Zone only
"""

import os
import json
import requests
from datetime import datetime
from typing import Dict, List
from dotenv import load_dotenv
from research_based_content_generator import ResearchBasedContentGenerator

# Load environment variables
load_dotenv()

def main():
    """Test Athlete Recovery Zone content generation"""
    
    print("="*70)
    print("    TESTING ATHLETE RECOVERY ZONE CONTENT GENERATION")
    print("="*70)
    
    generator = ResearchBasedContentGenerator()
    
    try:
        files = generator.generate_business_content('Athlete Recovery Zone')
        if files:
            print(f"✅ SUCCESS: Generated {len(files)} files for Athlete Recovery Zone")
        else:
            print("❌ FAILED: No files generated")
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    main()