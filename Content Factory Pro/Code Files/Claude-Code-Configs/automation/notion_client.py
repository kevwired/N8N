#!/usr/bin/env python3
"""
Notion API client for Content Factory Pro
Handles database operations for business configurations
"""

import os
import json
import requests
from datetime import datetime
from typing import Dict, List, Optional, Any

class NotionClient:
    def __init__(self, api_key: str = None, database_id: str = None):
        """Initialize Notion client with API credentials"""
        self.api_key = api_key or os.getenv('NOTION_API_KEY')
        self.database_id = database_id or os.getenv('NOTION_DATABASE_ID')
        self.base_url = 'https://api.notion.com/v1'
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'Notion-Version': '2022-06-28'
        }
        
        if not self.api_key:
            raise ValueError("NOTION_API_KEY environment variable or api_key parameter required")
        if not self.database_id:
            raise ValueError("NOTION_DATABASE_ID environment variable or database_id parameter required")

    def add_business_to_database(self, business_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add new business to Notion database"""
        
        properties = self._format_business_properties(business_data)
        
        payload = {
            "parent": {"database_id": self.database_id},
            "properties": properties
        }
        
        response = self._make_request('POST', '/pages', payload)
        
        if response:
            print(f"Successfully added {business_data.get('name', 'Unknown')} to Notion database")
            return response
        else:
            raise Exception(f"Failed to add business to Notion database")

    def update_business_record(self, page_id: str, business_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update existing business record in Notion"""
        
        properties = self._format_business_properties(business_data)
        
        payload = {"properties": properties}
        
        response = self._make_request('PATCH', f'/pages/{page_id}', payload)
        
        if response:
            print(f"Successfully updated business record {page_id}")
            return response
        else:
            raise Exception(f"Failed to update business record {page_id}")

    def find_business_by_name(self, business_name: str) -> Optional[Dict[str, Any]]:
        """Search for existing business by name"""
        
        query = {
            "filter": {
                "property": "Title",
                "title": {
                    "equals": business_name
                }
            }
        }
        
        response = self._make_request('POST', f'/databases/{self.database_id}/query', query)
        
        if response and response.get('results'):
            return response['results'][0]
        return None

    def get_next_business_id(self) -> int:
        """Get next available business ID"""
        
        query = {
            "sorts": [
                {
                    "property": "ID",
                    "direction": "descending"
                }
            ],
            "page_size": 1
        }
        
        response = self._make_request('POST', f'/databases/{self.database_id}/query', query)
        
        if response and response.get('results'):
            last_id = response['results'][0]['properties']['ID']['number']
            return last_id + 1 if last_id else 1
        return 1

    def _format_business_properties(self, business_data: Dict[str, Any]) -> Dict[str, Any]:
        """Format business data for Notion properties"""
        
        properties = {}
        
        # Map business data to Notion properties - COMPLETE 29 COLUMN SCHEMA
        next_id = business_data.get('id', 31)
        field_mappings = {
            'ID': ('number', next_id),
            'Title': ('title', business_data.get('name', 'Untitled Business')),
            'Business Category': ('select', self._determine_category(business_data)),
            'Active Status': ('checkbox', True),
            'Target Audience': ('rich_text', business_data.get('target_audience', '')),
            'GENERATE TEXT - System Message': ('rich_text', business_data.get('system_message', '')),
            'Content Length Limit': ('number', business_data.get('content_length_limit', 150)),
            'Brand Voice Guidelines': ('rich_text', business_data.get('brand_voice', '')),
            'Hashtag Strategy': ('rich_text', business_data.get('hashtag_strategy', '')),
            'Call to Action Template': ('rich_text', business_data.get('cta_template', '')),
            'GENERATE PROMPT - User Message': ('rich_text', business_data.get('user_message', '')),
            'GENERATE PROMPT - System Message': ('rich_text', business_data.get('prompt_system_message', '')),
            'Image Style Preferences': ('rich_text', business_data.get('image_style', '')),
            'Brand Colors': ('rich_text', business_data.get('brand_colors', '')),
            'Google Drive Parent Folder': ('rich_text', business_data.get('drive_folder', business_data.get('name', '').replace(' ', '_'))),
            'Social Platforms': ('multi_select', business_data.get('social_platforms', '')),
            'SEO Strategy Template': ('rich_text', business_data.get('seo_strategy', '')),
            'Website URLs': ('rich_text', business_data.get('website', '')),
            'Business Owner': ('rich_text', business_data.get('contact_name', '')),
            'Social Handle': ('rich_text', business_data.get('social_handle', '')),
            'Created Date': ('date', business_data.get('submission_date', datetime.now().strftime('%Y-%m-%d'))),
            'Last Modified': ('date', datetime.now().strftime('%Y-%m-%d')),
            'Notes': ('rich_text', business_data.get('notes', '')),
            'Global Content Rules': ('rich_text', business_data.get('content_rules', '')),
            'Email': ('email', business_data.get('email', '')),
            'Phone': ('phone_number', business_data.get('phone', '')),
            # Additional ID fields that appear in your schema
            'ID 1': ('number', business_data.get('id_1', '')),
            'ID 2': ('number', business_data.get('id_2', '')),
            'ID 3': ('number', business_data.get('id_3', next_id))
        }
        
        for notion_field, (field_type, value) in field_mappings.items():
            if value:  # Only add fields with values
                properties[notion_field] = self._format_property(field_type, value)
        
        return properties

    def _format_property(self, property_type: str, value: Any) -> Dict[str, Any]:
        """Format individual property for Notion API"""
        
        if property_type == 'title':
            return {
                "title": [{"text": {"content": str(value)}}]
            }
        elif property_type == 'rich_text':
            return {
                "rich_text": [{"text": {"content": str(value)}}]
            }
        elif property_type == 'number':
            try:
                return {
                    "number": int(value) if isinstance(value, (int, float, str)) and str(value).isdigit() else 0
                }
            except Exception as e:
                print(f"Number formatting error for value '{value}': {e}")
                return {"number": 0}
        elif property_type == 'select':
            return {
                "select": {"name": str(value)}
            }
        elif property_type == 'checkbox':
            return {
                "checkbox": bool(value)
            }
        elif property_type == 'multi_select':
            # Handle multi_select by splitting string on commas
            if isinstance(value, str):
                options = [{"name": option.strip()} for option in value.split(',') if option.strip()]
                return {
                    "multi_select": options
                }
            return {
                "multi_select": []
            }
        elif property_type == 'email':
            return {
                "email": str(value) if self._is_valid_email(value) else None
            }
        elif property_type == 'phone_number':
            return {
                "phone_number": str(value)
            }
        elif property_type == 'url':
            return {
                "url": str(value) if self._is_valid_url(value) else None
            }
        elif property_type == 'date':
            return {
                "date": {"start": str(value)}
            }
        else:
            return {
                "rich_text": [{"text": {"content": str(value)}}]
            }

    def _determine_category(self, business_data: Dict[str, Any]) -> str:
        """Determine business category from business data"""
        
        description = business_data.get('description', '').lower()
        name = business_data.get('name', '').lower()
        
        # Category keywords mapping
        categories = {
            'Healthcare': ['health', 'medical', 'doctor', 'clinic', 'therapy', 'wellness'],
            'Fitness': ['gym', 'fitness', 'training', 'workout', 'exercise', 'recovery'],
            'Real Estate': ['real estate', 'property', 'mortgage', 'realtor', 'homes'],
            'Automotive': ['car', 'auto', 'vehicle', 'dealership', 'repair'],
            'Food & Beverage': ['restaurant', 'food', 'cafe', 'catering', 'dining'],
            'Professional Services': ['consulting', 'legal', 'accounting', 'marketing', 'agency'],
            'Retail': ['store', 'shop', 'retail', 'sales', 'products'],
            'Home Services': ['plumbing', 'heating', 'cleaning', 'maintenance', 'repair'],
            'Technology': ['tech', 'software', 'digital', 'IT', 'computer'],
            'Education': ['school', 'training', 'education', 'learning', 'academy']
        }
        
        text_to_check = f"{description} {name}"
        
        for category, keywords in categories.items():
            if any(keyword in text_to_check for keyword in keywords):
                return category
        
        return 'Other'

    def _is_valid_email(self, email: str) -> bool:
        """Basic email validation"""
        import re
        pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        return bool(re.match(pattern, str(email)))

    def _is_valid_url(self, url: str) -> bool:
        """Basic URL validation"""
        return str(url).startswith(('http://', 'https://'))

    def _make_request(self, method: str, endpoint: str, data: Dict = None) -> Optional[Dict[str, Any]]:
        """Make HTTP request to Notion API with retry logic"""
        
        url = f"{self.base_url}{endpoint}"
        
        for attempt in range(3):  # Retry up to 3 times
            try:
                if method == 'GET':
                    response = requests.get(url, headers=self.headers, params=data)
                elif method == 'POST':
                    response = requests.post(url, headers=self.headers, json=data)
                elif method == 'PATCH':
                    response = requests.patch(url, headers=self.headers, json=data)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 429:  # Rate limited
                    print(f"Rate limited, retrying in {2 ** attempt} seconds...")
                    import time
                    time.sleep(2 ** attempt)
                    continue
                else:
                    print(f"Notion API error {response.status_code}: {response.text}")
                    return None
                    
            except requests.exceptions.RequestException as e:
                print(f"Request failed (attempt {attempt + 1}): {e}")
                if attempt == 2:  # Last attempt
                    return None
                import time
                time.sleep(2 ** attempt)
        
        return None

    def test_connection(self) -> bool:
        """Test connection to Notion API and database"""
        
        try:
            # Test API connection
            response = self._make_request('GET', f'/databases/{self.database_id}')
            if response:
                print(f"Successfully connected to Notion database: {response.get('title', [{}])[0].get('text', {}).get('content', 'Unknown')}")
                return True
            else:
                print("Failed to connect to Notion database")
                return False
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False

if __name__ == "__main__":
    # Test the Notion client
    client = NotionClient()
    client.test_connection()