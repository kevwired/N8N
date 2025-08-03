#!/usr/bin/env python3
"""
Content Factory Pro - Complete Content Generation System
Replaces N8N workflow with Python automation
Generates short-form and long-form content for all platforms
"""

import os
import json
import csv
import requests
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import anthropic
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Configuration
NOTION_API_KEY = os.getenv('NOTION_API_KEY')
NOTION_DATABASE_ID = os.getenv('NOTION_DATABASE_ID')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Content type definitions
CONTENT_TYPES = {
    'Educational': {
        'description': 'Teaching valuable information',
        'tone': 'informative and helpful',
        'structure': 'problem-solution or how-to format'
    },
    'Promotional': {
        'description': 'Highlighting services or offers',
        'tone': 'persuasive but not pushy',
        'structure': 'benefit-focused with clear CTA'
    },
    'Behind-the-Scenes': {
        'description': 'Showing business personality',
        'tone': 'casual and authentic',
        'structure': 'story-driven or process-focused'
    },
    'Success Story': {
        'description': 'Customer testimonials or case studies',
        'tone': 'celebratory and inspiring',
        'structure': 'narrative with results focus'
    },
    'Industry News': {
        'description': 'Commenting on trends or updates',
        'tone': 'authoritative and current',
        'structure': 'news commentary with business perspective'
    }
}

# Platform specifications
PLATFORM_SPECS = {
    'facebook': {
        'type': 'short',
        'word_count': 80,
        'char_limit': 500,
        'features': ['emoji_moderate', 'hashtags_minimal', 'conversational']
    },
    'instagram': {
        'type': 'short',
        'word_count': 50,
        'char_limit': 300,
        'features': ['emoji_moderate', 'hashtags_heavy', 'visual_focus']
    },
    'twitter': {
        'type': 'short',
        'word_count': 40,
        'char_limit': 280,
        'features': ['concise', 'hashtags_moderate', 'thread_potential']
    },
    'linkedin_post': {
        'type': 'short',
        'word_count': 100,
        'char_limit': 600,
        'features': ['professional', 'emoji_minimal', 'thought_leadership']
    },
    'linkedin_article': {
        'type': 'long',
        'word_count': 800,
        'features': ['professional', 'structured', 'seo_optimized']
    },
    'blog': {
        'type': 'long',
        'word_count': 1000,
        'features': ['seo_heavy', 'structured', 'comprehensive']
    },
    'newsletter': {
        'type': 'long',
        'word_count': 600,
        'features': ['personal_tone', 'value_focused', 'action_oriented']
    }
}

class ContentFactoryPro:
    def __init__(self):
        """Initialize the Content Factory Pro system"""
        self.notion_headers = {
            'Authorization': f'Bearer {NOTION_API_KEY}',
            'Content-Type': 'application/json',
            'Notion-Version': '2022-06-28'
        }
        self.anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        
    def get_business_config(self, business_name: str) -> Optional[Dict]:
        """Fetch business configuration from Notion database"""
        url = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query"
        
        payload = {
            "filter": {
                "and": [
                    {
                        "property": "Title",
                        "title": {
                            "equals": business_name
                        }
                    },
                    {
                        "property": "Active Status",
                        "checkbox": {
                            "equals": True
                        }
                    }
                ]
            }
        }
        
        response = requests.post(url, headers=self.notion_headers, json=payload)
        
        if response.status_code == 200:
            results = response.json().get('results', [])
            if results:
                return self._parse_business_config(results[0])
        
        return None
    
    def _parse_business_config(self, notion_page: Dict) -> Dict:
        """Parse Notion page data into business configuration"""
        props = notion_page.get('properties', {})
        
        def get_text(prop):
            if prop.get('rich_text'):
                return prop['rich_text'][0]['plain_text'] if prop['rich_text'] else ''
            elif prop.get('title'):
                return prop['title'][0]['plain_text'] if prop['title'] else ''
            return ''
        
        return {
            'id': notion_page['id'],
            'business_name': get_text(props.get('Title', {})),
            'category': props.get('Business Category', {}).get('select', {}).get('name', ''),
            'target_audience': get_text(props.get('Target Audience', {})),
            'brand_voice': get_text(props.get('Brand Voice Guidelines', {})),
            'system_message': get_text(props.get('GENERATE TEXT - System Message', {})),
            'hashtag_strategy': get_text(props.get('Hashtag Strategy', {})),
            'cta_template': get_text(props.get('Call to Action Template', {})),
            'content_length': int(get_text(props.get('Content Length Limit', {})) or 150),
            'seo_strategy': get_text(props.get('SEO Strategy Template', {})),
            'business_notes': get_text(props.get('Notes', {})),
            'global_rules': get_text(props.get('Global Content Rules', {})),
            'image_style': get_text(props.get('Image Style Preferences', {})),
            'brand_colors': get_text(props.get('Brand Colors', {})),
            'website_urls': get_text(props.get('Website URLs', {})),
            'social_platforms': get_text(props.get('Social Platforms', {})),
            'email': get_text(props.get('Email', {})),
            'phone': get_text(props.get('Phone', {}))
        }
    
    def generate_content(self, 
                        business_config: Dict,
                        content_type: str,
                        specific_topic: str,
                        content_brief: str,
                        platform: str,
                        seo_keywords: Optional[str] = None,
                        product_url: Optional[str] = None,
                        cta_url: Optional[str] = None) -> str:
        """Generate content using Claude API"""
        
        platform_spec = PLATFORM_SPECS.get(platform, {})
        is_longform = platform_spec.get('type') == 'long'
        word_count = platform_spec.get('word_count', 100)
        
        # Build the system message
        system_message = self._build_system_message(
            business_config, 
            content_type, 
            platform, 
            word_count,
            is_longform
        )
        
        # Build the user prompt
        user_prompt = self._build_user_prompt(
            specific_topic,
            content_brief,
            content_type,
            seo_keywords,
            product_url,
            cta_url,
            word_count
        )
        
        # Generate content with Claude
        try:
            response = self.anthropic_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4000,
                temperature=0.7,
                system=system_message,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            return response.content[0].text
            
        except Exception as e:
            print(f"Error generating content: {e}")
            return ""
    
    def _build_system_message(self, 
                             business_config: Dict, 
                             content_type: str,
                             platform: str,
                             word_count: int,
                             is_longform: bool) -> str:
        """Build comprehensive system message for content generation"""
        
        platform_spec = PLATFORM_SPECS.get(platform, {})
        features = platform_spec.get('features', [])
        
        system_message = f"""You are creating {content_type} content for {business_config['business_name']}.

BUSINESS CONTEXT:
- Category: {business_config['category']}
- Target Audience: {business_config['target_audience']}
- Brand Voice: {business_config['brand_voice']}
- Business Notes: {business_config['business_notes']}

CONTENT REQUIREMENTS:
- Platform: {platform}
- Content Type: {content_type}
- Word Count: {word_count} words {'(long-form)' if is_longform else '(short-form)'}
- Features: {', '.join(features)}

CONTENT TYPE GUIDELINES:
- Description: {CONTENT_TYPES[content_type]['description']}
- Tone: {CONTENT_TYPES[content_type]['tone']}
- Structure: {CONTENT_TYPES[content_type]['structure']}

PLATFORM-SPECIFIC RULES:
"""
        
        # Add platform-specific rules
        if platform == 'facebook':
            system_message += """
- Conversational and engaging tone
- Include 1-2 relevant emojis
- Minimal hashtags (1-3 max)
- Clear call-to-action
"""
        elif platform == 'instagram':
            system_message += """
- Visual-first approach
- 5-10 relevant hashtags
- Emoji-friendly but not excessive
- Short paragraphs for readability
"""
        elif platform == 'twitter':
            system_message += """
- Ultra-concise and punchy
- 2-3 strategic hashtags
- Thread potential if needed
- Character limit: 280
"""
        elif platform == 'linkedin_post':
            system_message += """
- Professional tone
- Thought leadership angle
- Minimal emoji use
- Industry-relevant hashtags
"""
        elif platform in ['linkedin_article', 'blog']:
            system_message += """
- Structured with clear sections
- SEO-optimized headings
- Professional and authoritative
- Include introduction and conclusion
- Use subheadings for scannability
"""
        elif platform == 'newsletter':
            system_message += """
- Personal and conversational tone
- Value-focused content
- Clear action items
- Structured but friendly
"""
        
        # Add business-specific rules
        if business_config.get('global_rules'):
            system_message += f"\nCUSTOM BUSINESS RULES:\n{business_config['global_rules']}\n"
        
        # Add the base system message from business config
        if business_config.get('system_message'):
            system_message += f"\nADDITIONAL GUIDELINES:\n{business_config['system_message']}\n"
        
        system_message += """
IMPORTANT:
- Write exactly the specified word count
- Use British English spelling
- Never fabricate testimonials or statistics
- Do not include word count in your response
- Output pure content only
"""
        
        return system_message
    
    def _build_user_prompt(self,
                          specific_topic: str,
                          content_brief: str,
                          content_type: str,
                          seo_keywords: Optional[str],
                          product_url: Optional[str],
                          cta_url: Optional[str],
                          word_count: int) -> str:
        """Build user prompt for content generation"""
        
        prompt = f"""Create {content_type} content about: {specific_topic}

CONTENT BRIEF:
{content_brief}

REQUIREMENTS:
- Focus specifically on: {specific_topic}
- Content type: {content_type}
- Target length: {word_count} words exactly
"""
        
        if seo_keywords:
            prompt += f"\nSEO KEYWORDS TO INCLUDE: {seo_keywords}"
        
        if product_url:
            prompt += f"\nPRODUCT/REFERENCE URL: {product_url} (research and align content with this)"
        
        if cta_url:
            prompt += f"\nCALL-TO-ACTION URL: {cta_url} (direct readers here)"
        
        prompt += "\n\nGenerate the content now:"
        
        return prompt
    
    def generate_image_prompt(self,
                             business_config: Dict,
                             content_type: str,
                             specific_topic: str) -> str:
        """Generate image creation prompt"""
        
        prompt = f"""Create an image prompt for {business_config['business_name']} ({business_config['category']})
Topic: {specific_topic}
Content Type: {content_type}

Business Context: {business_config['business_notes']}
Image Style Preferences: {business_config.get('image_style', 'professional business imagery')}
Brand Colors: {business_config.get('brand_colors', 'neutral professional colors')}

Generate a specific, detailed image prompt that:
1. Visually represents "{specific_topic}"
2. Matches the {content_type} content style
3. Is appropriate for {business_config['category']} industry
4. Follows the brand's visual guidelines
5. Ends with ", no text or logos"
6. Is under 950 characters

Create the image prompt:"""
        
        # Generate image prompt with Claude
        try:
            response = self.anthropic_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=200,
                temperature=0.7,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return response.content[0].text
            
        except Exception as e:
            print(f"Error generating image prompt: {e}")
            return f"Professional image representing {specific_topic} for {business_config['business_name']}, no text or logos"
    
    def generate_image(self, prompt: str) -> Optional[bytes]:
        """Generate image using OpenAI DALL-E API"""
        
        if not OPENAI_API_KEY:
            print("OpenAI API key not configured")
            return None
        
        headers = {
            'Authorization': f'Bearer {OPENAI_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'model': 'dall-e-3',
            'prompt': prompt,
            'size': '1024x1024',
            'quality': 'standard',
            'n': 1
        }
        
        try:
            response = requests.post(
                'https://api.openai.com/v1/images/generations',
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                image_url = response.json()['data'][0]['url']
                # Download the image
                image_response = requests.get(image_url)
                if image_response.status_code == 200:
                    return image_response.content
            else:
                print(f"Error generating image: {response.text}")
                
        except Exception as e:
            print(f"Error with image generation: {e}")
        
        return None
    
    def generate_content_package(self,
                                business_name: str,
                                content_type: str,
                                specific_topic: str,
                                content_brief: str,
                                seo_keywords: Optional[str] = None,
                                product_url: Optional[str] = None,
                                cta_url: Optional[str] = None) -> Dict:
        """Generate complete content package for all platforms"""
        
        # Get business configuration
        business_config = self.get_business_config(business_name)
        if not business_config:
            return {'error': f'Business configuration not found for {business_name}'}
        
        print(f"\n[INFO] Generating content package for {business_name}")
        print(f"[INFO] Topic: {specific_topic}")
        print(f"[INFO] Type: {content_type}")
        
        content_package = {
            'business_name': business_name,
            'content_type': content_type,
            'specific_topic': specific_topic,
            'generated_at': datetime.now().isoformat(),
            'short_form': {},
            'long_form': {},
            'image_prompt': '',
            'hashtags': business_config.get('hashtag_strategy', ''),
            'cta': business_config.get('cta_template', '')
        }
        
        # Generate short-form content
        for platform in ['facebook', 'instagram', 'twitter', 'linkedin_post']:
            print(f"[INFO] Generating {platform} content...")
            content = self.generate_content(
                business_config,
                content_type,
                specific_topic,
                content_brief,
                platform,
                seo_keywords,
                product_url,
                cta_url
            )
            content_package['short_form'][platform] = content
            time.sleep(1)  # Rate limiting
        
        # Generate long-form content
        for platform in ['linkedin_article', 'blog', 'newsletter']:
            print(f"[INFO] Generating {platform} content...")
            content = self.generate_content(
                business_config,
                content_type,
                specific_topic,
                content_brief,
                platform,
                seo_keywords,
                product_url,
                cta_url
            )
            content_package['long_form'][platform] = content
            time.sleep(1)  # Rate limiting
        
        # Generate image prompt
        print("[INFO] Generating image prompt...")
        image_prompt = self.generate_image_prompt(
            business_config,
            content_type,
            specific_topic
        )
        content_package['image_prompt'] = image_prompt
        
        # Generate image if API key is available
        if OPENAI_API_KEY:
            print("[INFO] Generating image...")
            image_data = self.generate_image(image_prompt)
            if image_data:
                content_package['image_data'] = image_data
        
        return content_package
    
    def save_content_package(self, content_package: Dict, output_dir: str = None) -> str:
        """Save content package to files"""
        
        if not output_dir:
            output_dir = os.path.join(
                os.path.dirname(__file__),
                'generated_content',
                content_package['business_name'].replace(' ', '_'),
                datetime.now().strftime('%Y%m%d_%H%M%S')
            )
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Save main content file
        content_file = os.path.join(output_dir, 'content_package.json')
        with open(content_file, 'w', encoding='utf-8') as f:
            # Remove image data from JSON (save separately)
            package_copy = content_package.copy()
            if 'image_data' in package_copy:
                del package_copy['image_data']
            json.dump(package_copy, f, indent=2, ensure_ascii=False)
        
        # Save individual platform files
        for platform, content in content_package['short_form'].items():
            platform_file = os.path.join(output_dir, f'{platform}.txt')
            with open(platform_file, 'w', encoding='utf-8') as f:
                f.write(content)
        
        for platform, content in content_package['long_form'].items():
            platform_file = os.path.join(output_dir, f'{platform}.txt')
            with open(platform_file, 'w', encoding='utf-8') as f:
                f.write(content)
        
        # Save image if available
        if content_package.get('image_data'):
            image_file = os.path.join(output_dir, 'generated_image.png')
            with open(image_file, 'wb') as f:
                f.write(content_package['image_data'])
        
        # Create summary document
        summary_file = os.path.join(output_dir, 'content_summary.txt')
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(f"""Content Package Summary
======================

Business: {content_package['business_name']}
Topic: {content_package['specific_topic']}
Type: {content_package['content_type']}
Generated: {content_package['generated_at']}

Short-Form Content:
- Facebook: {len(content_package['short_form'].get('facebook', ''))} chars
- Instagram: {len(content_package['short_form'].get('instagram', ''))} chars
- Twitter: {len(content_package['short_form'].get('twitter', ''))} chars
- LinkedIn Post: {len(content_package['short_form'].get('linkedin_post', ''))} chars

Long-Form Content:
- LinkedIn Article: {len(content_package['long_form'].get('linkedin_article', '').split())} words
- Blog Post: {len(content_package['long_form'].get('blog', '').split())} words
- Newsletter: {len(content_package['long_form'].get('newsletter', '').split())} words

Hashtags: {content_package['hashtags']}
CTA: {content_package['cta']}

Files saved to: {output_dir}
""")
        
        print(f"\n[SUCCESS] Content package saved to: {output_dir}")
        return output_dir

def main():
    """Main function for testing"""
    
    # Check for required API keys
    if not ANTHROPIC_API_KEY:
        print("[ERROR] ANTHROPIC_API_KEY not found in .env file")
        return
    
    # Initialize Content Factory
    factory = ContentFactoryPro()
    
    # Example usage
    business_name = "KF Barbers"
    content_type = "Educational"
    specific_topic = "How to maintain your beard between barber visits"
    content_brief = """Create educational content teaching men how to maintain their beards at home 
    between professional barber visits. Include tips on daily care, trimming techniques, 
    and product recommendations. Make it practical and actionable."""
    
    seo_keywords = "beard maintenance, beard care tips, beard trimming, mens grooming"
    
    # Generate content package
    content_package = factory.generate_content_package(
        business_name=business_name,
        content_type=content_type,
        specific_topic=specific_topic,
        content_brief=content_brief,
        seo_keywords=seo_keywords
    )
    
    if 'error' not in content_package:
        # Save the content
        output_dir = factory.save_content_package(content_package)
        
        # Print sample outputs
        print("\n=== SAMPLE OUTPUTS ===")
        print("\nFacebook Post:")
        print(content_package['short_form']['facebook'][:200] + "...")
        print("\nInstagram Post:")
        print(content_package['short_form']['instagram'][:200] + "...")
        print("\nBlog Post Intro:")
        print(content_package['long_form']['blog'][:300] + "...")

if __name__ == "__main__":
    main()