#!/usr/bin/env python3
"""
Upload KF Barbers data directly to Notion database
"""

import os
import sys
from pathlib import Path

# Add the automation directory to Python path
sys.path.append(str(Path(__file__).parent))

from notion_client import NotionClient

def main():
    """Upload KF Barbers data to Notion database"""
    
    # KF Barbers business data based on research
    kf_barbers_data = {
        'id': 31,
        'name': 'KF Barbers',
        'contact_name': '',  # Not provided in research
        'phone': '07449 761659',
        'email': '',  # Not provided in research
        'website': 'https://www.fresha.com/lvp/kf-barbers-high-street-NoL3Xx',
        'description': 'Professional men\'s barbershop in Arbroath, Scotland specializing in traditional haircuts, beard trimming, hot shaves, and head shaves. Known for exceptional skill with both adults and children.',
        'target_audience': 'Primary Target Audience: Local men aged 25-55 in Arbroath and surrounding areas seeking professional barbering services. This includes working professionals, fathers, and traditional gentlemen who value quality craftsmanship and reliable service. Secondary Audience: Parents with young boys (ages 3-16) looking for a patient, child-friendly barber who can handle first haircuts and nervous children with skill and care. Tertiary Audience: Men seeking traditional services like hot shaves and beard grooming, including older gentlemen who appreciate classic barbering techniques. Geographic Focus: Primarily Arbroath locals, but customers willing to travel for quality service. Customer Demographics: Middle-income families, working professionals, and retirees who prioritize quality over low prices. Decision Drivers: Consistency in service quality, friendly professional atmosphere, accommodation of walk-ins, and exceptional skill with children. Pain Points: Finding reliable barbers who can handle both adult precision cuts and patient child services, consistent availability, and maintaining traditional barbering standards.',
        'brand_voice': 'Professional, confident, and community-focused with a warm, welcoming tone. KF Barbers communicates with the expertise of traditional craftsmanship while maintaining modern accessibility. The voice should reflect pride in barbering skills, patience with all customers (especially children), and genuine care for the Arbroath community. Avoid overly casual language but remain approachable. Emphasize quality, reliability, and the personal touch that sets apart a skilled barber from generic hair salons. Use terminology that respects traditional barbering while being inclusive to modern customers.',
        'social_platforms': 'Facebook: emilbelukf, Instagram: kf-barbers-arbroath, Fresha booking platform',
        'content_brief': 'You are creating content for KF Barbers, a respected traditional barbershop in Arbroath, Scotland. The business has built a strong reputation over the years for quality men\'s haircuts, beard trimming, and hot shaves, with particular expertise in handling children\'s haircuts. Content should reflect professional barbering skills, community connection, and the welcoming atmosphere that has earned them a 4.9/5 customer rating. Emphasize traditional craftsmanship, family-friendly service, and local community pride.',
        'seo_keywords': 'barber Arbroath, men\'s haircut Arbroath, beard trim Arbroath, kids haircut Arbroath, traditional barber Scotland, hot shave Arbroath',
        'business_category': 'Health & Fitness',
        'active_status': 'Active',
        'location': '109 High Street, Arbroath DD11 1DP, Scotland',
        'rating': '4.9/5 (215+ reviews)',
        'hours': 'Mon-Fri: 8:00am-6:00pm, Sat: 7:30am-5:00pm, Sun: Closed'
    }
    
    try:
        # Initialize Notion client with credentials from config
        print("Initializing Notion client...")
        from config import Config
        
        try:
            config = Config.get_notion_config()
            client = NotionClient(api_key=config['api_key'], database_id=config['database_id'])
        except ValueError as e:
            print(f"Configuration Error: {e}")
            print("Please create a .env file with your API credentials.")
            print("See .env.example for the required format.")
            return False
        
        # Test connection
        print("Testing Notion connection...")
        if not client.test_connection():
            print("Failed to connect to Notion. Please check your API key and database ID.")
            return False
        
        # Check if business already exists
        print("Checking for existing KF Barbers record...")
        existing_business = client.find_business_by_name('KF Barbers')
        
        if existing_business:
            print("KF Barbers already exists in database. Updating existing record...")
            page_id = existing_business['id']
            result = client.update_business_record(page_id, kf_barbers_data)
            print(f"Successfully updated KF Barbers record: {page_id}")
        else:
            print("Adding KF Barbers to Notion database...")
            result = client.add_business_to_database(kf_barbers_data)
            print(f"Successfully added KF Barbers to database")
        
        # Print result summary
        print("\nUpload Summary:")
        print(f"   Business Name: {kf_barbers_data['name']}")
        print(f"   Category: {kf_barbers_data['business_category']}")
        print(f"   Phone: {kf_barbers_data['phone']}")
        print(f"   Location: {kf_barbers_data['location']}")
        print(f"   Rating: {kf_barbers_data['rating']}")
        
        return True
        
    except Exception as e:
        print(f"Error uploading to Notion: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\nKF Barbers successfully uploaded to Notion database!")
        print("You can now skip the CSV step and work directly with Notion for future businesses.")
    else:
        print("\nUpload failed. Check your Notion API configuration.")