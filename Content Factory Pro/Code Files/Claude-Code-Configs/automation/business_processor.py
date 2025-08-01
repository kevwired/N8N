"""
Business processing logic for Content Factory Pro
"""

import re
import json
import pandas as pd
from datetime import datetime
from pathlib import Path

def parse_submission(submission_file):
    """Parse standardized submission.md file"""
    
    with open(submission_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract business data using regex patterns
    business_data = {
        'name': extract_field(content, 'Business Name'),
        'contact_name': extract_field(content, 'Your Name'),
        'phone': extract_field(content, 'Phone'),
        'email': extract_field(content, 'Email'),
        'website': extract_field(content, 'Website'),
        'description': extract_field(content, 'What Does Your Business Do'),
        'target_audience': extract_field(content, 'Target Audience'),
        'brand_voice': extract_field(content, 'Brand Voice Guidelines'),
        'social_platforms': extract_field(content, 'Social Media'),
        'content_brief': extract_field(content, 'Content Brief'),
        'seo_keywords': extract_field(content, 'SEO Keywords'),
        'submission_date': datetime.now().strftime('%Y-%m-%d')
    }
    
    return business_data

def extract_field(content, field_name):
    """Extract field value from markdown content"""
    pattern = rf"{field_name}:\s*(.+?)(?=\n[A-Z][^:]*:|$)"
    match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else ""

def generate_business_config(business_data, research_data):
    """Generate business configuration CSV data"""
    
    config_data = {
        'ID': [get_next_id()],
        'Title': [business_data['name']],
        'Business Category': [determine_category(business_data)],
        'Active Status': ['Yes'],
        'Target Audience': [business_data['target_audience']],
        'Brand Voice Guidelines': [business_data['brand_voice']],
        'Website URLs': [business_data['website']],
        'Business Owner': [business_data['contact_name']],
        'Email': [business_data['email']],
        'Phone': [business_data['phone']],
        'Created Date': [business_data['submission_date']],
        'Last Modified': [business_data['submission_date']]
        # Add other required fields based on your schema
    }
    
    return pd.DataFrame(config_data)

def generate_content_strategy(business_data, config_data):
    """Generate 12-piece monthly content strategy"""
    
    content_pieces = []
    
    # Content distribution strategy
    content_types = [
        ('Educational', 5),      # 40%
        ('Product Highlight', 3), # 25%  
        ('Problem & Solution', 3), # 25%
        ('Community & Stories', 1) # 10%
    ]
    
    for content_type, count in content_types:
        for i in range(count):
            piece = {
                'Business Name': business_data['name'],
                'Social Content Type': content_type,
                'Specific Topic': generate_topic(business_data, content_type, i),
                'Content Brief': generate_brief(business_data, content_type),
                'Word Count Target': get_word_count(content_type),
                'Product Focus URL': business_data['website'],
                'CTA URL': business_data['website'],
                'SEO Keywords': select_keywords(business_data, content_type)
            }
            content_pieces.append(piece)
    
    return pd.DataFrame(content_pieces)

def get_next_id():
    """Get next available business ID from existing data"""
    try:
        # Check if there's a central database CSV to get the next ID
        database_path = Path("../../Database/Business_Configurations 20ed14ad2042804194a1d732d174e720.csv")
        if database_path.exists():
            df = pd.read_csv(database_path)
            if not df.empty and 'ID' in df.columns:
                return df['ID'].max() + 1
        return 1
    except Exception:
        return 1

def determine_category(business_data):
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

def generate_topic(business_data, content_type, index):
    """Generate specific topic for content piece"""
    business_name = business_data.get('name', 'Business')
    
    topics = {
        'Educational': [
            f"How {business_name} Can Help You Achieve Your Goals",
            f"Top 5 Tips from {business_name} Experts",
            f"The Ultimate Guide to {business_data.get('description', 'Our Services')}",
            f"Common Mistakes to Avoid - {business_name} Advice",
            f"Industry Insights from {business_name}"
        ],
        'Product Highlight': [
            f"Spotlight: {business_name}'s Featured Service",
            f"Why Customers Choose {business_name}",
            f"Behind the Scenes at {business_name}"
        ],
        'Problem & Solution': [
            f"Solving Your Biggest Challenge with {business_name}",
            f"Case Study: How {business_name} Transformed a Client",
            f"Before & After: {business_name} Success Story"
        ],
        'Community & Stories': [
            f"Customer Spotlight: {business_name} Success",
            f"Meet the Team: {business_name} Story",
            f"Community Impact: {business_name}'s Mission"
        ]
    }
    
    topic_list = topics.get(content_type, [f"{business_name} Content"])
    return topic_list[index % len(topic_list)]

def generate_brief(business_data, content_type):
    """Generate content brief for specific content type"""
    briefs = {
        'Educational': f"Create educational content that positions {business_data.get('name', 'your business')} as an industry expert. Focus on providing valuable insights and actionable tips related to {business_data.get('description', 'your services')}.",
        'Product Highlight': f"Showcase the unique features and benefits of {business_data.get('name', 'your business')} services. Highlight what sets you apart from competitors.",
        'Problem & Solution': f"Address common pain points your target audience faces and demonstrate how {business_data.get('name', 'your business')} provides effective solutions.",
        'Community & Stories': f"Share authentic stories about {business_data.get('name', 'your business')} impact on customers and community. Build emotional connection and trust."
    }
    
    return briefs.get(content_type, f"Create engaging content for {business_data.get('name', 'your business')}")

def get_word_count(content_type):
    """Get target word count for content type"""
    word_counts = {
        'Educational': 800,
        'Product Highlight': 600,
        'Problem & Solution': 700,
        'Community & Stories': 500
    }
    
    return word_counts.get(content_type, 600)

def select_keywords(business_data, content_type):
    """Select relevant SEO keywords for content type"""
    base_keywords = business_data.get('seo_keywords', '').split(',')
    base_keywords = [kw.strip() for kw in base_keywords if kw.strip()]
    
    if not base_keywords:
        # Generate basic keywords from business info
        business_name = business_data.get('name', '')
        description = business_data.get('description', '')
        base_keywords = [business_name, description.split()[0] if description else 'business']
    
    # Select 2-3 keywords for this content piece
    selected = base_keywords[:3] if len(base_keywords) >= 3 else base_keywords
    return ', '.join(selected)