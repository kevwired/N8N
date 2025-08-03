#!/usr/bin/env python3
"""
Generate 12 marketing content ideas and save to client folder
Each piece numbered sequentially (1-12) for posting order
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

class ClientContentGenerator:
    def __init__(self):
        self.notion_headers = {
            'Authorization': f'Bearer {NOTION_API_KEY}',
            'Content-Type': 'application/json',
            'Notion-Version': '2022-06-28'
        }
        # Base client directory - fixed absolute path
        self.base_client_dir = r"Z:\Main Drive\360TFT Resources\Workflows\N8N\Content Factory Pro\Clients"
    
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
        category = business_config['category'].lower()
        
        # Barber-specific content
        if 'barber' in business_name.lower() or 'barber' in category:
            return [
                {'type': 'Educational', 'topic': 'How Often Should You Get a Haircut?', 'brief': 'Explain ideal haircut frequency for different hair types and styles. Include maintenance tips.', 'hook': 'Looking sharp requires the right schedule'},
                {'type': 'Educational', 'topic': 'Beard Maintenance Between Visits', 'brief': 'Daily beard care routine, product recommendations, and trimming tips between professional visits.', 'hook': 'Your beard deserves daily attention'},
                {'type': 'Educational', 'topic': 'Choosing the Right Haircut for Your Face Shape', 'brief': 'Guide to selecting flattering cuts based on face shape with visual examples.', 'hook': 'The perfect cut starts with knowing your face shape'},
                {'type': 'Educational', 'topic': 'Kids Haircut Preparation Tips', 'brief': 'Help parents prepare children for stress-free haircut experiences.', 'hook': 'Make your child\'s haircut a happy experience'},
                {'type': 'Behind-the-Scenes', 'topic': 'Early Morning Prep at the Barbershop', 'brief': 'Show the daily routine, tool preparation, and dedication to service before opening.', 'hook': 'Ever wonder what happens before we open?'},
                {'type': 'Behind-the-Scenes', 'topic': 'The Art of Traditional Barbering', 'brief': 'Showcase traditional techniques, craftsmanship, and attention to detail.', 'hook': 'Where traditional craftsmanship meets modern service'},
                {'type': 'Promotional', 'topic': 'Walk-In Wednesday Special', 'brief': 'Highlight walk-in availability and convenience for busy schedules.', 'hook': 'No appointment? No problem!'},
                {'type': 'Promotional', 'topic': 'Father & Son Appointment Special', 'brief': 'Encourage booking father-son appointments for bonding experiences.', 'hook': 'Create memories that last longer than the haircut'},
                {'type': 'Promotional', 'topic': 'Early Bird Saturday Hours', 'brief': 'Promote early morning appointments and benefits of beating the rush.', 'hook': 'Start your weekend looking sharp'},
                {'type': 'Success Story', 'topic': 'Nervous Child Becomes Regular Customer', 'brief': 'Share story of transforming haircut fears into excitement for kids.', 'hook': 'How we turned haircut tears into cheers'},
                {'type': 'Success Story', 'topic': 'Three Generations Choose Us', 'brief': 'Highlight families who bring multiple generations for haircuts.', 'hook': 'When granddad, dad, and son all trust the same barber'},
                {'type': 'Success Story', 'topic': 'Customer Reviews Speak for Themselves', 'brief': 'Share authentic customer feedback and satisfaction stories.', 'hook': 'Real customers, real results, real satisfaction'}
            ]
        
        # Automotive-specific content
        elif 'automotive' in category or 'motor' in business_name.lower():
            return [
                {'type': 'Educational', 'topic': 'Essential Car Maintenance Tips', 'brief': 'Basic maintenance every car owner should know to extend vehicle life.', 'hook': 'Simple steps for a longer-lasting vehicle'},
                {'type': 'Educational', 'topic': 'When to Schedule Your MOT', 'brief': 'Understanding MOT requirements and optimal timing for testing.', 'hook': 'Stay legal and safe on the road'},
                {'type': 'Educational', 'topic': 'Electric Vehicle Charging Best Practices', 'brief': 'Guide to proper EV charging habits and battery care.', 'hook': 'Maximize your EV battery life'},
                {'type': 'Educational', 'topic': 'Warning Signs Your Car Needs Attention', 'brief': 'How to identify common car problems before they become expensive.', 'hook': 'Catch problems early, save money later'},
                {'type': 'Behind-the-Scenes', 'topic': 'Meet Our Certified Technicians', 'brief': 'Introduce the skilled team and their qualifications.', 'hook': 'The experts who keep you moving'},
                {'type': 'Behind-the-Scenes', 'topic': 'State-of-the-Art Diagnostic Equipment', 'brief': 'Show modern technology used for accurate vehicle diagnosis.', 'hook': 'Precision diagnostics for precise repairs'},
                {'type': 'Promotional', 'topic': 'New Customer Welcome Offer', 'brief': 'Special pricing or service package for first-time customers.', 'hook': 'Your first visit made special'},
                {'type': 'Promotional', 'topic': 'EV Service Specialist Booking', 'brief': 'Highlight specialized electric vehicle servicing capabilities.', 'hook': 'Expert EV care when you need it'},
                {'type': 'Promotional', 'topic': 'Multi-Vehicle Family Discount', 'brief': 'Special rates for families with multiple vehicles.', 'hook': 'Family fleet? Family savings!'},
                {'type': 'Success Story', 'topic': 'Saved Customer from Costly Repair', 'brief': 'How early diagnosis prevented major expense.', 'hook': 'When prevention saves thousands'},
                {'type': 'Success Story', 'topic': 'Emergency Breakdown Rescue', 'brief': 'Quick response story that got customer back on road.', 'hook': 'When you need us most, we\'re there'},
                {'type': 'Success Story', 'topic': 'Long-Term Customer Loyalty', 'brief': 'Celebrate customers who\'ve trusted us for years.', 'hook': 'Trusted partners for the long haul'}
            ]
        
        # Generic content for other business types
        else:
            return [
                {'type': 'Educational', 'topic': f'Top 5 {category.title()} Tips for Beginners', 'brief': f'Essential advice for those new to {category} services.', 'hook': 'Start your journey the right way'},
                {'type': 'Educational', 'topic': f'Common {category.title()} Mistakes to Avoid', 'brief': f'Help customers avoid typical pitfalls in {category}.', 'hook': 'Save time and money by avoiding these errors'},
                {'type': 'Educational', 'topic': f'Seasonal {category.title()} Considerations', 'brief': f'How seasons affect {category} needs and solutions.', 'hook': 'Prepare for the season ahead'},
                {'type': 'Educational', 'topic': 'Understanding Our Service Process', 'brief': 'Step-by-step explanation of what customers can expect.', 'hook': 'Know what to expect from start to finish'},
                {'type': 'Behind-the-Scenes', 'topic': 'Meet Our Expert Team', 'brief': 'Introduce team members and their expertise.', 'hook': 'The people who make it all happen'},
                {'type': 'Behind-the-Scenes', 'topic': 'Our Quality Standards', 'brief': 'Show commitment to excellence and attention to detail.', 'hook': 'Why we go the extra mile'},
                {'type': 'Promotional', 'topic': 'New Customer Welcome Offer', 'brief': 'Special introductory offer for first-time customers.', 'hook': 'Your first experience made special'},
                {'type': 'Promotional', 'topic': 'Refer a Friend Rewards', 'brief': 'Reward customers for bringing new business.', 'hook': 'Share the love, share the rewards'},
                {'type': 'Promotional', 'topic': 'Flexible Scheduling Options', 'brief': 'Highlight convenience and availability.', 'hook': 'We work around your schedule'},
                {'type': 'Success Story', 'topic': 'Customer Success Spotlight', 'brief': 'Feature a satisfied customer and their experience.', 'hook': 'Real results from real people'},
                {'type': 'Success Story', 'topic': 'Challenge Overcome Success', 'brief': 'How we solved a difficult customer problem.', 'hook': 'When others said it couldn\'t be done'},
                {'type': 'Success Story', 'topic': 'Long-Term Partnership Celebration', 'brief': 'Celebrate customers who have been with us for years.', 'hook': 'Partnerships that stand the test of time'}
            ]
    
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
            post += f"{' '.join(hashtags.split()[:3])}"  # Limited hashtags for FB
            
        elif idea['type'] == 'Behind-the-Scenes':
            post = f"{idea['hook']} 👀\n\n"
            post += f"Take a peek behind the curtain at {config['business_name']}! "
            post += f"{idea['brief'][:80]}...\n\n"
            post += f"We're more than just a business - we're your neighbors. "
            post += f"{cta}\n\n"
            post += f"{' '.join(hashtags.split()[:2])}"
            
        elif idea['type'] == 'Promotional':
            post = f"🎉 {idea['topic']} 🎉\n\n"
            post += f"{idea['hook']}! "
            post += f"At {config['business_name']}, {idea['brief'][:60]}...\n\n"
            post += f"Don't miss out! {cta}\n\n"
            post += f"{' '.join(hashtags.split()[:3])}"
            
        else:  # Success Story
            post = f"❤️ Customer Success Story ❤️\n\n"
            post += f"{idea['hook']}. "
            post += f"{idea['brief'][:70]}...\n\n"
            post += f"Thank you for trusting {config['business_name']}! "
            post += f"Ready for your success story? {cta}\n\n"
            post += f"{' '.join(hashtags.split()[:2])}"
        
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
    
    def _create_monthly_folders(self, client_folder: str):
        """Create monthly folders for content organization"""
        
        # Define the months to create
        months = ['Aug_25', 'Sep_25', 'Oct_25', 'Nov_25', 'Dec_25']
        
        for month in months:
            month_folder = os.path.join(client_folder, month)
            os.makedirs(month_folder, exist_ok=True)
        
        print(f"[INFO] Created monthly folders: {', '.join(months)}")
    
    def save_client_content(self, business_name: str, ideas: List[Dict], business_config: Dict):
        """Save content to client folder with sequential numbering in monthly folders"""
        
        # Determine client folder path
        client_folder = os.path.join(self.base_client_dir, business_name)
        
        if not os.path.exists(client_folder):
            print(f"[ERROR] Client folder not found: {client_folder}")
            print("Available client folders:")
            if os.path.exists(self.base_client_dir):
                for folder in os.listdir(self.base_client_dir):
                    if os.path.isdir(os.path.join(self.base_client_dir, folder)):
                        print(f"  - {folder}")
            return
        
        # Create monthly folders structure
        self._create_monthly_folders(client_folder)
        
        # Determine current month folder
        current_month = datetime.now().strftime('%b_25')  # Aug_25, Sep_25, etc.
        monthly_folder = os.path.join(client_folder, current_month)
        
        # Create content timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Create main content summary file in monthly folder
        summary_file = os.path.join(monthly_folder, f'Content_Package_{timestamp}.txt')
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(f"""CONTENT PACKAGE - {business_name}
{'='*50}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Business Category: {business_config['category']}
Total Content Pieces: 12

POSTING ORDER GUIDE:
===================
Post these in numerical order (1-12) for optimal engagement and variety.
Each piece includes Facebook, Instagram, Twitter, and LinkedIn versions.

CONTENT MIX:
- Educational: 4 posts (33%)
- Behind-the-Scenes: 2 posts (17%)  
- Promotional: 3 posts (25%)
- Success Stories: 3 posts (25%)

INDIVIDUAL CONTENT FILES:
========================
""")
            
            # Generate individual content files and add to summary
            for idx, idea in enumerate(ideas, 1):
                posts = self.generate_social_posts(idea, business_config)
                
                # Create individual content file in monthly folder
                content_file = os.path.join(monthly_folder, f'{idx:02d}_{idea["type"]}_{idea["topic"][:30].replace(" ", "_").replace("?", "").replace(":", "")}.txt')
                
                with open(content_file, 'w', encoding='utf-8') as cf:
                    cf.write(f"""CONTENT PIECE #{idx}
{'='*30}

Type: {idea['type']}
Topic: {idea['topic']}
Hook: {idea['hook']}
Brief: {idea['brief']}

SOCIAL MEDIA POSTS:
==================

FACEBOOK:
---------
{posts['facebook']}

INSTAGRAM:
----------
{posts['instagram']}

TWITTER:
--------
{posts['twitter']}

LINKEDIN:
---------
{posts['linkedin']}

POSTING NOTES:
=============
- Post #{idx} in your content sequence
- Best times: Check your analytics for optimal posting times
- Add relevant images or videos
- Engage with comments promptly
- Track performance for future optimization

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
""")
                
                # Add to summary
                f.write(f"{idx:02d}. {idea['type']}: {idea['topic']}\n")
                f.write(f"    File: {os.path.basename(content_file)}\n")
                f.write(f"    Hook: {idea['hook']}\n\n")
            
            f.write(f"""
USAGE INSTRUCTIONS:
==================

1. POSTING ORDER:
   - Follow the numerical sequence (01, 02, 03... 12)
   - Each file contains all platform versions
   - Space posts 2-3 days apart for optimal engagement

2. PLATFORM SELECTION:
   - Facebook: Conversational, community-focused
   - Instagram: Visual content with full hashtags
   - Twitter: Quick updates, news, tips
   - LinkedIn: Professional insights, thought leadership

3. CUSTOMIZATION:
   - Add your own images/videos
   - Adjust timing based on your audience analytics
   - Modify CTAs if needed for specific campaigns
   - Track which content types perform best

4. NEXT STEPS:
   - Review all content before posting
   - Schedule posts in your social media management tool
   - Monitor engagement and adjust future content
   - Request new content package when needed

Contact: admin@kevinrmiddleton.com for content updates or questions.
""")
        
        print(f"\n[SUCCESS] Content saved to monthly folder: {monthly_folder}")
        print(f"[SUMMARY] Main file: Content_Package_{timestamp}.txt")
        print(f"[INDIVIDUAL] 12 numbered content files created (01-12)")
        print(f"[MONTHLY] Organized in {current_month} folder")
        print(f"[ORDER] Content ready for sequential posting")
    
    def generate_client_content(self, business_name: str):
        """Generate complete content package for client"""
        
        print(f"[INFO] Generating content for {business_name}...")
        
        # Get business config
        config = self.get_business_config(business_name)
        if not config:
            print(f"[ERROR] Business '{business_name}' not found or inactive in Notion database")
            return
        
        print(f"[SUCCESS] Found configuration for {config['business_name']}")
        print(f"[INFO] Category: {config['category']}")
        
        # Generate marketing ideas
        ideas = self.generate_marketing_ideas(config)
        print(f"[INFO] Generated {len(ideas)} content ideas")
        
        # Save to client folder
        self.save_client_content(business_name, ideas, config)

def main():
    """Main function"""
    
    generator = ClientContentGenerator()
    
    # Get business name
    business_name = input("Enter business name: ").strip()
    if not business_name:
        print("[ERROR] Business name is required")
        return
    
    generator.generate_client_content(business_name)

if __name__ == "__main__":
    main()