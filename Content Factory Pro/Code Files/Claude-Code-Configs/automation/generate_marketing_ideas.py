#!/usr/bin/env python3
"""
Generate 12 marketing content ideas and social media posts
Based on business configuration from Notion database
"""

import os
import json
import requests
from datetime import datetime
from typing import Dict, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

NOTION_API_KEY = os.getenv('NOTION_API_KEY')
NOTION_DATABASE_ID = os.getenv('NOTION_DATABASE_ID')

class MarketingIdeaGenerator:
    def __init__(self):
        self.notion_headers = {
            'Authorization': f'Bearer {NOTION_API_KEY}',
            'Content-Type': 'application/json',
            'Notion-Version': '2022-06-28'
        }
    
    def get_business_config(self, business_name: str) -> Dict:
        """Fetch business configuration from Notion"""
        url = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query"
        
        payload = {
            "filter": {
                "and": [
                    {
                        "property": "Title",
                        "title": {"equals": business_name}
                    },
                    {
                        "property": "Active Status",  
                        "checkbox": {"equals": True}
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
        """Parse Notion page data"""
        props = notion_page.get('properties', {})
        
        def get_text(prop):
            if prop.get('rich_text'):
                return prop['rich_text'][0]['plain_text'] if prop['rich_text'] else ''
            elif prop.get('title'):
                return prop['title'][0]['plain_text'] if prop['title'] else ''
            return ''
        
        return {
            'business_name': get_text(props.get('Title', {})),
            'category': props.get('Business Category', {}).get('select', {}).get('name', ''),
            'target_audience': get_text(props.get('Target Audience', {})),
            'brand_voice': get_text(props.get('Brand Voice Guidelines', {})),
            'hashtag_strategy': get_text(props.get('Hashtag Strategy', {})),
            'cta_template': get_text(props.get('Call to Action Template', {})),
            'business_notes': get_text(props.get('Notes', {})),
            'website_urls': get_text(props.get('Website URLs', {})),
            'phone': get_text(props.get('Phone', {})),
            'email': get_text(props.get('Email', {}))
        }
    
    def generate_marketing_ideas(self, business_config: Dict) -> List[Dict]:
        """Generate 12 marketing content ideas based on business type"""
        
        business_name = business_config['business_name']
        category = business_config['category']
        
        # Base content mix (4 Educational, 2 Behind-the-Scenes, 3 Promotional, 3 Success Story)
        ideas = []
        
        # Category-specific content ideas
        if 'barber' in category.lower() or business_name == 'KF Barbers':
            ideas = [
                # Educational (4)
                {
                    'type': 'Educational',
                    'topic': 'How Often Should You Get a Haircut?',
                    'brief': 'Explain ideal haircut frequency for different hair types and styles. Include maintenance tips.',
                    'hook': 'Looking sharp requires the right schedule'
                },
                {
                    'type': 'Educational',
                    'topic': 'Beard Maintenance 101',
                    'brief': 'Daily beard care routine, product recommendations, and trimming tips between visits.',
                    'hook': 'Your beard deserves daily attention'
                },
                {
                    'type': 'Educational',
                    'topic': 'Choosing the Right Haircut for Your Face Shape',
                    'brief': 'Guide to selecting flattering cuts based on face shape with visual examples.',
                    'hook': 'The perfect cut starts with knowing your face shape'
                },
                {
                    'type': 'Educational',
                    'topic': 'Kids Haircut Preparation Tips',
                    'brief': 'Help parents prepare children for stress-free haircut experiences.',
                    'hook': 'Make your child\'s haircut a happy experience'
                },
                # Behind-the-Scenes (2)
                {
                    'type': 'Behind-the-Scenes',
                    'topic': 'A Day in the Life at Our Barbershop',
                    'brief': 'Show the daily routine, team preparation, and dedication to service.',
                    'hook': 'Ever wonder what happens before we open?'
                },
                {
                    'type': 'Behind-the-Scenes',
                    'topic': 'Meet Our Master Barbers',
                    'brief': 'Introduce team members, their experience, and specialties.',
                    'hook': 'The skilled hands behind every great cut'
                },
                # Promotional (3)
                {
                    'type': 'Promotional',
                    'topic': 'Early Bird Special Hours',
                    'brief': 'Promote early morning appointments and benefits of beating the rush.',
                    'hook': 'Start your day looking sharp'
                },
                {
                    'type': 'Promotional',
                    'topic': 'Father & Son Tradition',
                    'brief': 'Encourage booking father-son appointments for bonding experiences.',
                    'hook': 'Create memories that last longer than the haircut'
                },
                {
                    'type': 'Promotional',
                    'topic': 'Walk-In Wednesdays',
                    'brief': 'Highlight walk-in availability and convenience for busy schedules.',
                    'hook': 'No appointment? No problem!'
                },
                # Success Story (3)
                {
                    'type': 'Success Story',
                    'topic': 'Transforming First-Time Customers',
                    'brief': 'Share stories of nervous first-timers becoming regulars.',
                    'hook': 'From skeptical to satisfied'
                },
                {
                    'type': 'Success Story',
                    'topic': 'Three Generations of Trust',
                    'brief': 'Highlight families who bring multiple generations for haircuts.',
                    'hook': 'When granddad, dad, and son all trust the same barber'
                },
                {
                    'type': 'Success Story',
                    'topic': 'The Nervous Child Who Now Loves Haircuts',
                    'brief': 'Story of transforming haircut fears into excitement for kids.',
                    'hook': 'How we turned haircut tears into cheers'
                }
            ]
        else:
            # Generic content ideas for other business types
            ideas = [
                # Educational (4)
                {
                    'type': 'Educational',
                    'topic': f'Top 5 {category} Tips for Beginners',
                    'brief': f'Essential advice for those new to {category.lower()} services or products.',
                    'hook': 'Start your journey the right way'
                },
                {
                    'type': 'Educational',
                    'topic': f'Common {category} Mistakes to Avoid',
                    'brief': f'Help customers avoid typical pitfalls in {category.lower()}.',
                    'hook': 'Save time and money by avoiding these errors'
                },
                {
                    'type': 'Educational',
                    'topic': f'Seasonal {category} Guide',
                    'brief': f'How seasons affect {category.lower()} needs and solutions.',
                    'hook': 'Prepare for the season ahead'
                },
                {
                    'type': 'Educational',
                    'topic': 'Understanding Our Service Process',
                    'brief': 'Step-by-step explanation of what customers can expect.',
                    'hook': 'Know what to expect from start to finish'
                },
                # Behind-the-Scenes (2)
                {
                    'type': 'Behind-the-Scenes',
                    'topic': 'Meet Our Expert Team',
                    'brief': 'Introduce team members and their expertise.',
                    'hook': 'The people who make it all happen'
                },
                {
                    'type': 'Behind-the-Scenes',
                    'topic': 'Our Quality Standards',
                    'brief': 'Show commitment to excellence and attention to detail.',
                    'hook': 'Why we go the extra mile'
                },
                # Promotional (3)
                {
                    'type': 'Promotional',
                    'topic': 'New Customer Special',
                    'brief': 'Welcome offer for first-time customers.',
                    'hook': 'Your first experience with us made special'
                },
                {
                    'type': 'Promotional',
                    'topic': 'Refer a Friend Benefits',
                    'brief': 'Reward customers for bringing new business.',
                    'hook': 'Share the love, share the rewards'
                },
                {
                    'type': 'Promotional',
                    'topic': 'Flexible Scheduling Options',
                    'brief': 'Highlight convenience and availability.',
                    'hook': 'We work around your schedule'
                },
                # Success Story (3)
                {
                    'type': 'Success Story',
                    'topic': 'Customer Spotlight',
                    'brief': 'Feature a satisfied customer and their experience.',
                    'hook': 'Real results from real people'
                },
                {
                    'type': 'Success Story',
                    'topic': 'Problem Solved Success',
                    'brief': 'How we helped solve a challenging customer issue.',
                    'hook': 'When others said it couldn\'t be done'
                },
                {
                    'type': 'Success Story',
                    'topic': 'Long-Term Partnership',
                    'brief': 'Celebrate customers who have been with us for years.',
                    'hook': 'Trusted partners for the long haul'
                }
            ]
        
        return ideas
    
    def generate_social_posts(self, idea: Dict, business_config: Dict) -> Dict:
        """Generate social media posts for each platform"""
        
        posts = {}
        hashtags = business_config.get('hashtag_strategy', '#LocalBusiness')
        cta = business_config.get('cta_template', 'Contact us today!')
        
        # Facebook (conversational, 80 words)
        posts['facebook'] = self._generate_facebook_post(idea, business_config, hashtags, cta)
        
        # Instagram (visual focus, 50 words)
        posts['instagram'] = self._generate_instagram_post(idea, business_config, hashtags, cta)
        
        # Twitter (concise, 40 words/280 chars)
        posts['twitter'] = self._generate_twitter_post(idea, business_config, hashtags)
        
        # LinkedIn (professional, 100 words)
        posts['linkedin'] = self._generate_linkedin_post(idea, business_config, cta)
        
        return posts
    
    def _generate_facebook_post(self, idea: Dict, config: Dict, hashtags: str, cta: str) -> str:
        """Generate Facebook post (80 words, conversational)"""
        
        if idea['type'] == 'Educational':
            post = f"{idea['hook']}! 🎯\n\n{idea['topic']}\n\n"
            post += f"At {config['business_name']}, we believe in empowering our customers with knowledge. "
            post += f"{idea['brief'][:100]}...\n\n"
            post += f"Want to learn more? {cta}\n\n"
            post += f"{hashtags.split()[:3]}"  # Limited hashtags for FB
            
        elif idea['type'] == 'Behind-the-Scenes':
            post = f"{idea['hook']} 👀\n\n"
            post += f"Take a peek behind the curtain at {config['business_name']}! "
            post += f"{idea['brief'][:80]}...\n\n"
            post += f"We're more than just a business - we're your neighbors. "
            post += f"{cta}\n\n"
            post += f"{hashtags.split()[:2]}"
            
        elif idea['type'] == 'Promotional':
            post = f"🎉 {idea['topic']} 🎉\n\n"
            post += f"{idea['hook']}! "
            post += f"At {config['business_name']}, {idea['brief'][:60]}...\n\n"
            post += f"Don't miss out! {cta}\n\n"
            post += f"{hashtags.split()[:3]}"
            
        else:  # Success Story
            post = f"❤️ Customer Success Story ❤️\n\n"
            post += f"{idea['hook']}. "
            post += f"{idea['brief'][:70]}...\n\n"
            post += f"Thank you for trusting {config['business_name']}! "
            post += f"Ready for your success story? {cta}\n\n"
            post += f"{hashtags.split()[:2]}"
        
        return post
    
    def _generate_instagram_post(self, idea: Dict, config: Dict, hashtags: str, cta: str) -> str:
        """Generate Instagram post (50 words, visual focus)"""
        
        if idea['type'] == 'Educational':
            post = f"✨ {idea['hook']} ✨\n\n"
            post += f"{idea['topic']} - swipe for tips! ➡️\n\n"
            post += f"{cta}\n\n"
            post += hashtags  # Full hashtags for IG
            
        elif idea['type'] == 'Behind-the-Scenes':
            post = f"Behind the scenes at {config['business_name']} 📸\n\n"
            post += f"{idea['hook']}\n\n"
            post += f"Tap ❤️ if you love seeing how we work!\n\n"
            post += hashtags
            
        elif idea['type'] == 'Promotional':
            post = f"🔥 {idea['topic']} 🔥\n\n"
            post += f"{idea['hook']}\n"
            post += f"Link in bio for details 👆\n\n"
            post += hashtags
            
        else:  # Success Story
            post = f"SUCCESS STORY 🌟\n\n"
            post += f"{idea['hook']}\n\n"
            post += f"Your story could be next! {cta}\n\n"
            post += hashtags
        
        return post
    
    def _generate_twitter_post(self, idea: Dict, config: Dict, hashtags: str) -> str:
        """Generate Twitter post (280 chars max)"""
        
        main_hashtags = ' '.join(hashtags.split()[:2])  # 2 hashtags for Twitter
        
        if idea['type'] == 'Educational':
            post = f"{idea['hook']} 📚 {idea['topic']} - quick tips from {config['business_name']}! {main_hashtags}"
        elif idea['type'] == 'Behind-the-Scenes':
            post = f"{idea['hook']} 👀 Get an inside look at {config['business_name']}! {main_hashtags}"
        elif idea['type'] == 'Promotional':
            post = f"🎯 {idea['topic']} - {idea['hook']} Book now at {config['business_name']}! {main_hashtags}"
        else:  # Success Story
            post = f"⭐ {idea['hook']} Another happy customer at {config['business_name']}! {main_hashtags}"
        
        # Ensure under 280 chars
        if len(post) > 280:
            post = post[:277] + "..."
        
        return post
    
    def _generate_linkedin_post(self, idea: Dict, config: Dict, cta: str) -> str:
        """Generate LinkedIn post (100 words, professional)"""
        
        if idea['type'] == 'Educational':
            post = f"{idea['topic']}\n\n"
            post += f"{idea['hook']}. In our experience at {config['business_name']}, "
            post += f"we've found that {idea['brief'][:120]}.\n\n"
            post += f"Professional development in {config['category']} requires continuous learning. "
            post += f"We're committed to sharing our expertise with the community.\n\n"
            post += f"What's your experience with this topic? Let's discuss in the comments.\n\n"
            post += f"#{config['category'].replace(' ', '')} #ProfessionalDevelopment #LocalExpertise"
            
        elif idea['type'] == 'Behind-the-Scenes':
            post = f"Transparency in Business: {idea['topic']}\n\n"
            post += f"At {config['business_name']}, we believe in showing the real work behind our services. "
            post += f"{idea['brief'][:100]}.\n\n"
            post += f"Building trust through transparency is core to our business philosophy.\n\n"
            post += f"How does your business build trust? Share your thoughts below.\n\n"
            post += f"#{config['category'].replace(' ', '')} #BusinessTransparency #LocalBusiness"
            
        elif idea['type'] == 'Promotional':
            post = f"Exciting News from {config['business_name']}\n\n"
            post += f"{idea['topic']} - {idea['hook']}!\n\n"
            post += f"We're thrilled to offer {idea['brief'][:80]}. "
            post += f"This initiative reflects our commitment to customer convenience and satisfaction.\n\n"
            post += f"Ready to experience the difference? {cta}\n\n"
            post += f"#{config['category'].replace(' ', '')} #CustomerFirst #Innovation"
            
        else:  # Success Story
            post = f"Client Success Spotlight\n\n"
            post += f"{idea['hook']}. At {config['business_name']}, "
            post += f"these moments remind us why we do what we do.\n\n"
            post += f"{idea['brief'][:100]}.\n\n"
            post += f"Success stories like these drive our continued commitment to excellence.\n\n"
            post += f"#{config['category'].replace(' ', '')} #ClientSuccess #Excellence"
        
        return post
    
    def generate_complete_output(self, business_name: str):
        """Generate complete marketing package"""
        
        # Fetch business config
        print(f"[INFO] Fetching configuration for {business_name}...")
        config = self.get_business_config(business_name)
        
        if not config:
            print(f"[ERROR] Business '{business_name}' not found or inactive in Notion database")
            return
        
        print(f"[SUCCESS] Found configuration for {config['business_name']}")
        print(f"[INFO] Category: {config['category']}")
        print(f"[INFO] Target Audience: {config['target_audience'][:100]}...")
        
        # Generate marketing ideas
        print(f"\n[INFO] Generating 12 marketing content ideas...")
        ideas = self.generate_marketing_ideas(config)
        
        # Create output
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir = os.path.join(
            os.path.dirname(__file__),
            'marketing_ideas',
            f"{business_name.replace(' ', '_')}_{timestamp}"
        )
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate complete output document
        output_file = os.path.join(output_dir, 'marketing_content_ideas.txt')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"""MARKETING CONTENT IDEAS & SOCIAL MEDIA POSTS
============================================

Business: {config['business_name']}
Category: {config['category']}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

Target Audience: {config['target_audience']}
Brand Voice: {config['brand_voice']}

CONTENT STRATEGY OVERVIEW
========================
- 4 Educational Posts (33%)
- 2 Behind-the-Scenes Posts (17%)
- 3 Promotional Posts (25%)
- 3 Success Story Posts (25%)

""")
            
            # Generate posts for each idea
            for idx, idea in enumerate(ideas, 1):
                print(f"[{idx}/12] Generating posts for: {idea['topic']}")
                
                posts = self.generate_social_posts(idea, config)
                
                f.write(f"""
{'='*80}
CONTENT IDEA #{idx}: {idea['type'].upper()}
{'='*80}

TOPIC: {idea['topic']}
HOOK: {idea['hook']}
BRIEF: {idea['brief']}

SOCIAL MEDIA POSTS:
------------------

FACEBOOK (80 words):
{posts['facebook']}

INSTAGRAM (50 words):
{posts['instagram']}

TWITTER (280 chars):
{posts['twitter']}

LINKEDIN (100 words):
{posts['linkedin']}

""")
        
        # Create CSV for easy import
        csv_file = os.path.join(output_dir, 'content_calendar.csv')
        with open(csv_file, 'w', encoding='utf-8') as f:
            f.write('Number,Type,Topic,Hook,Facebook,Instagram,Twitter,LinkedIn\n')
            
            for idx, idea in enumerate(ideas, 1):
                posts = self.generate_social_posts(idea, config)
                f.write(f'{idx},"{idea["type"]}","{idea["topic"]}","{idea["hook"]}",')
                f.write(f'"{posts["facebook"]}","{posts["instagram"]}",')
                f.write(f'"{posts["twitter"]}","{posts["linkedin"]}"\n')
        
        print(f"\n[SUCCESS] Generated 12 marketing ideas with social media posts")
        print(f"[SAVED] Output saved to: {output_dir}")
        print(f"[FILES] Created:")
        print(f"  - marketing_content_ideas.txt (full details)")
        print(f"  - content_calendar.csv (for easy import)")

def main():
    """Run the marketing idea generator"""
    
    generator = MarketingIdeaGenerator()
    
    # Generate for KF Barbers by default
    business_name = input("Enter business name (default: KF Barbers): ").strip()
    if not business_name:
        business_name = "KF Barbers"
    
    generator.generate_complete_output(business_name)

if __name__ == "__main__":
    main()