#!/usr/bin/env python3
"""
Generate complete content package for KF Barbers
Creates short-form and long-form content for all platforms
"""

import os
from datetime import datetime
from content_factory_complete import ContentFactoryPro

# Content strategy for KF Barbers
CONTENT_STRATEGY = [
    {
        'type': 'Educational',
        'topic': 'How often should you get a haircut?',
        'brief': 'Explain the ideal haircut frequency for men based on hair type and style. Include maintenance tips between visits and why regular cuts matter for appearance.'
    },
    {
        'type': 'Educational',
        'topic': 'The benefits of a traditional hot shave',
        'brief': 'Detail the experience and benefits of traditional hot shave services. Cover the process, skin benefits, and why it\'s worth the investment.'
    },
    {
        'type': 'Educational',
        'topic': 'Kids first haircut tips',
        'brief': 'Guide for parents bringing children for their first haircut. Include preparation tips, what to expect, and how KF Barbers makes it a positive experience.'
    },
    {
        'type': 'Behind-the-Scenes',
        'topic': 'Early bird Saturday special',
        'brief': 'Highlight the 7:30am Saturday opening time and benefits of early appointments. Show the peaceful morning atmosphere and dedicated service.'
    },
    {
        'type': 'Promotional',
        'topic': 'Walk-ins welcome policy',
        'brief': 'Explain how KF Barbers accommodates walk-in customers while encouraging bookings. Emphasize flexibility and customer convenience.'
    },
    {
        'type': 'Success Story',
        'topic': '5-star service testimonials',
        'brief': 'Share customer success stories focusing on families and children who were nervous about haircuts. Use real review themes without fabricating.'
    }
]

def generate_all_content():
    """Generate complete content packages for KF Barbers"""
    
    # Check for API key
    if not os.getenv('ANTHROPIC_API_KEY') or os.getenv('ANTHROPIC_API_KEY') == 'your_anthropic_api_key_here':
        print("[ERROR] Please add your Anthropic API key to the .env file")
        print("Edit: Z:\\Main Drive\\360TFT Resources\\Workflows\\N8N\\Content Factory Pro\\Code Files\\Claude-Code-Configs\\automation\\.env")
        print("Replace 'your_anthropic_api_key_here' with your actual API key")
        return
    
    # Initialize factory
    factory = ContentFactoryPro()
    
    # Base output directory
    base_output_dir = os.path.join(
        os.path.dirname(__file__),
        'kf_barbers_complete_content',
        datetime.now().strftime('%Y%m%d')
    )
    
    print(f"[INFO] Starting content generation for KF Barbers")
    print(f"[INFO] Output directory: {base_output_dir}")
    
    # Generate content for each item in strategy
    for idx, content_item in enumerate(CONTENT_STRATEGY, 1):
        print(f"\n[{idx}/{len(CONTENT_STRATEGY)}] Generating: {content_item['topic']}")
        
        # SEO keywords based on content type
        seo_keywords = {
            'Educational': 'barber Arbroath, mens haircut, traditional barber, KF Barbers',
            'Behind-the-Scenes': 'Arbroath barber, local business, KF Barbers, Saturday barber',
            'Promotional': 'walk in barber Arbroath, KF Barbers, mens haircut Arbroath',
            'Success Story': 'barber reviews Arbroath, KF Barbers testimonials, 5 star barber'
        }.get(content_item['type'], 'KF Barbers, Arbroath barber')
        
        try:
            # Generate content package
            content_package = factory.generate_content_package(
                business_name="KF Barbers",
                content_type=content_item['type'],
                specific_topic=content_item['topic'],
                content_brief=content_item['brief'],
                seo_keywords=seo_keywords
            )
            
            if 'error' not in content_package:
                # Create subdirectory for this content
                content_dir = os.path.join(
                    base_output_dir,
                    f"{idx:02d}_{content_item['type']}_{content_item['topic'][:30].replace(' ', '_')}"
                )
                
                # Save the content
                factory.save_content_package(content_package, content_dir)
                print(f"[SUCCESS] Generated content for: {content_item['topic']}")
            else:
                print(f"[ERROR] Failed to generate: {content_package['error']}")
                
        except Exception as e:
            print(f"[ERROR] Exception generating content: {str(e)}")
    
    # Create master summary
    create_master_summary(base_output_dir, CONTENT_STRATEGY)
    
    print(f"\n[COMPLETE] All content generated successfully!")
    print(f"[LOCATION] {base_output_dir}")

def create_master_summary(output_dir: str, content_strategy: list):
    """Create a master summary of all generated content"""
    
    summary_file = os.path.join(output_dir, 'MASTER_SUMMARY.txt')
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("""KF BARBERS - COMPLETE CONTENT PACKAGE
=====================================

Generated: {date}
Business: KF Barbers
Location: 109 High Street, Arbroath DD11 1DP
Phone: 07449 761659

CONTENT OVERVIEW
================

This package contains {count} complete content sets, each including:
- Facebook post (80 words)
- Instagram post (50 words)  
- Twitter/X post (40 words)
- LinkedIn post (100 words)
- LinkedIn article (800 words)
- Blog post (1000 words)
- Newsletter content (600 words)
- AI-generated image prompt

CONTENT ITEMS
=============

""".format(date=datetime.now().strftime('%Y-%m-%d'), count=len(content_strategy)))
        
        for idx, item in enumerate(content_strategy, 1):
            f.write(f"{idx}. {item['type']}: {item['topic']}\n")
            f.write(f"   Brief: {item['brief'][:100]}...\n\n")
        
        f.write("""
USAGE INSTRUCTIONS
==================

1. SHORT-FORM CONTENT (Facebook, Instagram, Twitter, LinkedIn Posts):
   - Ready to copy and paste
   - Add relevant images from the generated image or your own
   - Hashtags and CTAs are included
   - Review before posting

2. LONG-FORM CONTENT (Blog, LinkedIn Articles, Newsletter):
   - Fully formatted with sections
   - SEO-optimized with keywords
   - May need light editing for your specific platform
   - Add images throughout for engagement

3. IMAGES:
   - Image prompts are provided for AI generation
   - Can be used with DALL-E, Midjourney, or similar
   - Always review generated images before use
   - Consider using your own photos when possible

4. CUSTOMIZATION:
   - All content follows KF Barbers brand voice
   - Includes local Arbroath references
   - Professional yet approachable tone
   - Family-friendly messaging

IMPORTANT DISCLAIMER
====================
Please review all content before publishing. AI can make mistakes.
Check facts, phone numbers, and opening hours are correct.
Contact admin@kevinrmiddleton.com for any adjustments needed.
""")

if __name__ == "__main__":
    generate_all_content()