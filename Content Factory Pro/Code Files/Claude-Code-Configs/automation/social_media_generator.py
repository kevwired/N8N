#!/usr/bin/env python3
"""
Social Media Post Generator for Content Factory Pro
Reads content-strategy.csv and generates formatted social media posts
"""

import os
import sys
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import re

class SocialMediaGenerator:
    def __init__(self):
        self.platforms = {
            'facebook': {'char_limit': 63206, 'hashtag_limit': 30},
            'instagram': {'char_limit': 2200, 'hashtag_limit': 30},
            'twitter': {'char_limit': 280, 'hashtag_limit': 10},
            'linkedin': {'char_limit': 3000, 'hashtag_limit': 20},
            'tiktok': {'char_limit': 2200, 'hashtag_limit': 100}
        }
        
        self.post_templates = {
            'Educational': {
                'hook': [
                    "Did you know that",
                    "Here's something most people don't realize:",
                    "Quick tip:",
                    "Pro tip from our experts:",
                    "Let's talk about"
                ],
                'structure': 'hook + educational_content + cta',
                'hashtags': ['#TipTuesday', '#DidYouKnow', '#Education', '#Tips']
            },
            'Product Highlight': {
                'hook': [
                    "Spotlight on:",
                    "Let us introduce you to",
                    "Why our clients love",
                    "Featured this month:",
                    "Check out"
                ],
                'structure': 'hook + product_benefits + cta',
                'hashtags': ['#Featured', '#ProductSpotlight', '#WhyChooseUs']
            },
            'Problem & Solution': {
                'hook': [
                    "Struggling with",
                    "Tired of dealing with",
                    "We solved this problem:",
                    "Here's how we help with",
                    "Common challenge:"
                ],
                'structure': 'problem + solution + result + cta',
                'hashtags': ['#ProblemSolved', '#Solution', '#Results']
            },
            'Community & Stories': {
                'hook': [
                    "Success story:",
                    "We're proud to share",
                    "Client spotlight:",
                    "Amazing results from",
                    "Meet one of our"
                ],
                'structure': 'story + outcome + community_message + cta',
                'hashtags': ['#SuccessStory', '#ClientSpotlight', '#Community', '#Results']
            }
        }

    def generate_posts_from_csv(self, csv_file_path, output_folder=None):
        """Generate social media posts from content strategy CSV"""
        
        if output_folder is None:
            output_folder = Path(csv_file_path).parent / "social_media_posts"
        else:
            output_folder = Path(output_folder)
        
        # Create output folder if it doesn't exist
        output_folder.mkdir(exist_ok=True)
        
        try:
            # Read content strategy CSV
            df = pd.read_csv(csv_file_path)
            print(f"📊 Loaded {len(df)} content pieces from CSV")
            
            # Generate posts for each platform
            all_posts = {}
            
            for platform in self.platforms.keys():
                platform_posts = []
                
                for _, row in df.iterrows():
                    post = self.create_post_for_platform(row, platform)
                    if post:
                        platform_posts.append(post)
                
                all_posts[platform] = platform_posts
                
                # Save platform-specific markdown file
                self.save_posts_to_markdown(platform_posts, output_folder / f"{platform}_posts.md", platform)
            
            # Create master calendar file
            self.create_content_calendar(all_posts, output_folder / "content_calendar.md")
            
            print(f"✅ Generated social media posts for {len(self.platforms)} platforms")
            print(f"📁 Output saved to: {output_folder}")
            
            return all_posts
            
        except Exception as e:
            print(f"❌ Error generating social media posts: {e}")
            return None

    def create_post_for_platform(self, content_row, platform):
        """Create a social media post for specific platform"""
        
        try:
            business_name = content_row.get('Business Name', 'Business')
            content_type = content_row.get('Social Content Type', 'Educational')
            topic = content_row.get('Specific Topic', 'Topic')
            brief = content_row.get('Content Brief', '')
            keywords = content_row.get('SEO Keywords', '').split(',')
            keywords = [kw.strip() for kw in keywords if kw.strip()]
            
            # Get platform constraints
            char_limit = self.platforms[platform]['char_limit']
            hashtag_limit = self.platforms[platform]['hashtag_limit']
            
            # Generate post content
            post_content = self.generate_post_content(
                business_name, content_type, topic, brief, platform
            )
            
            # Generate hashtags
            hashtags = self.generate_hashtags(content_type, keywords, business_name, hashtag_limit)
            
            # Combine content and hashtags
            full_post = f"{post_content}\n\n{hashtags}"
            
            # Trim if necessary
            if len(full_post) > char_limit:
                available_chars = char_limit - len(hashtags) - 10  # Buffer
                post_content = post_content[:available_chars] + "..."
                full_post = f"{post_content}\n\n{hashtags}"
            
            return {
                'platform': platform,
                'business_name': business_name,
                'content_type': content_type,
                'topic': topic,
                'post_content': post_content,
                'hashtags': hashtags,
                'full_post': full_post,
                'char_count': len(full_post),
                'char_limit': char_limit
            }
            
        except Exception as e:
            print(f"⚠️ Error creating post for {platform}: {e}")
            return None

    def generate_post_content(self, business_name, content_type, topic, brief, platform):
        """Generate the main post content based on type and platform"""
        
        template = self.post_templates.get(content_type, self.post_templates['Educational'])
        
        # Select appropriate hook
        import random
        hook = random.choice(template['hook'])
        
        # Platform-specific content generation
        if platform in ['twitter']:
            return self.generate_short_post(business_name, content_type, topic, hook)
        elif platform in ['instagram', 'tiktok']:
            return self.generate_visual_post(business_name, content_type, topic, hook)
        elif platform in ['linkedin']:
            return self.generate_professional_post(business_name, content_type, topic, hook, brief)
        else:  # Facebook and others
            return self.generate_standard_post(business_name, content_type, topic, hook, brief)

    def generate_short_post(self, business_name, content_type, topic, hook):
        """Generate short-form content for Twitter"""
        
        if content_type == 'Educational':
            return f"{hook} {topic.lower().replace(business_name, 'we')}! Quick tip: [Insert specific tip here] 💡"
        elif content_type == 'Product Highlight':
            return f"{hook} {topic}! Here's why clients choose us: [Insert key benefit] ✨"
        elif content_type == 'Problem & Solution':
            return f"{hook} [common problem]? We've got the solution: [Insert solution] 🎯"
        else:  # Community & Stories
            return f"{hook} Amazing results from one of our clients! [Insert brief success story] 🎉"

    def generate_visual_post(self, business_name, content_type, topic, hook):
        """Generate visual-focused content for Instagram/TikTok"""
        
        visual_cues = {
            'Educational': "📚 SWIPE for tips ➡️",
            'Product Highlight': "✨ See it in action ✨",
            'Problem & Solution': "🔧 Problem solved! 🎯",
            'Community & Stories': "📸 Real results 📈"
        }
        
        visual_cue = visual_cues.get(content_type, "👀 Check this out!")
        
        content = f"{visual_cue}\n\n{hook} {topic}!\n\n"
        
        if content_type == 'Educational':
            content += "[Insert educational content with emojis]\n\n💡 Key takeaway: [Insert main point]"
        elif content_type == 'Product Highlight':
            content += "[Highlight key features/benefits]\n\n🌟 What makes us different: [Insert differentiator]"
        elif content_type == 'Problem & Solution':
            content += "❌ The problem: [Insert problem]\n✅ Our solution: [Insert solution]\n📈 The result: [Insert outcome]"
        else:
            content += "[Share success story with specific details]\n\n🎉 Results speak for themselves!"
        
        content += f"\n\n👇 Tell us about your experience with {business_name}!"
        
        return content

    def generate_professional_post(self, business_name, content_type, topic, hook, brief):
        """Generate professional content for LinkedIn"""
        
        content = f"{hook} {topic}\n\n"
        
        if content_type == 'Educational':
            content += f"In our experience at {business_name}, we've learned that [insert educational insight].\n\n"
            content += "Here are the key points:\n• [Point 1]\n• [Point 2]\n• [Point 3]\n\n"
            content += "What's your experience with this? Share your thoughts in the comments."
        elif content_type == 'Product Highlight':
            content += f"At {business_name}, we're proud to offer [service/product feature].\n\n"
            content += "This has helped our clients:\n✓ [Benefit 1]\n✓ [Benefit 2]\n✓ [Benefit 3]\n\n"
            content += "Interested in learning more? Let's connect."
        elif content_type == 'Problem & Solution':
            content += "Many businesses face [common problem]. We see this challenge regularly.\n\n"
            content += f"Our approach at {business_name}:\n1. [Step 1]\n2. [Step 2]\n3. [Step 3]\n\n"
            content += "The result? [Insert typical outcome]. How do you handle this challenge?"
        else:
            content += f"We're excited to share a recent success story from {business_name}.\n\n"
            content += "[Insert detailed case study/story]\n\n"
            content += "Success stories like this remind us why we do what we do. What's your latest win?"
        
        return content

    def generate_standard_post(self, business_name, content_type, topic, hook, brief):
        """Generate standard content for Facebook and general use"""
        
        content = f"{hook} {topic}! 🎯\n\n"
        
        if content_type == 'Educational':
            content += f"Here at {business_name}, we believe in sharing knowledge that makes a difference.\n\n"
            content += "[Insert educational content - 2-3 paragraphs with specific tips/insights]\n\n"
            content += "💡 Pro tip: [Insert actionable advice]\n\n"
            content += "What questions do you have about this topic? Drop them in the comments!"
        elif content_type == 'Product Highlight':
            content += f"We're excited to showcase what makes {business_name} special! ✨\n\n"
            content += "[Describe service/product with specific benefits and features]\n\n"
            content += "🌟 Why our clients love this:\n• [Benefit 1]\n• [Benefit 2]\n• [Benefit 3]\n\n"
            content += "Ready to experience the difference? Get in touch today!"
        elif content_type == 'Problem & Solution':
            content += "We hear this concern a lot: '[Insert common problem]' 🤔\n\n"
            content += f"Good news! At {business_name}, we've developed a proven approach:\n\n"
            content += "[Explain solution process in detail]\n\n"
            content += "📈 The results speak for themselves: [Insert typical outcomes]\n\n"
            content += "Dealing with something similar? We're here to help!"
        else:
            content += f"We love celebrating our clients' success! 🎉\n\n"
            content += "[Share detailed success story with specific metrics/outcomes]\n\n"
            content += f"Stories like this are exactly why the {business_name} team is passionate about what we do.\n\n"
            content += "What's your success story? We'd love to hear about it!"
        
        return content

    def generate_hashtags(self, content_type, keywords, business_name, limit):
        """Generate relevant hashtags for the post"""
        
        # Base hashtags from templates
        base_hashtags = self.post_templates.get(content_type, {}).get('hashtags', [])
        
        # Add business-related hashtags
        business_hashtags = [f"#{business_name.replace(' ', '').replace('-', '').replace('&', 'And')}"]
        
        # Add keyword-based hashtags
        keyword_hashtags = [f"#{kw.replace(' ', '').replace('-', '').title()}" for kw in keywords[:3]]
        
        # Combine all hashtags
        all_hashtags = base_hashtags + business_hashtags + keyword_hashtags
        
        # Remove duplicates and limit
        unique_hashtags = list(dict.fromkeys(all_hashtags))[:limit]
        
        return ' '.join(unique_hashtags)

    def save_posts_to_markdown(self, posts, output_file, platform):
        """Save posts to a markdown file"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# {platform.title()} Social Media Posts\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Posts: {len(posts)}\n\n")
            f.write("---\n\n")
            
            for i, post in enumerate(posts, 1):
                f.write(f"## Post {i}: {post['content_type']}\n\n")
                f.write(f"**Topic:** {post['topic']}\n\n")
                f.write(f"**Business:** {post['business_name']}\n\n")
                f.write(f"**Character Count:** {post['char_count']}/{post['char_limit']}\n\n")
                f.write("### Content:\n")
                f.write("```\n")
                f.write(post['full_post'])
                f.write("\n```\n\n")
                f.write("### Copy-Paste Version:\n")
                f.write(f"{post['full_post']}\n\n")
                f.write("---\n\n")

    def create_content_calendar(self, all_posts, output_file):
        """Create a content calendar markdown file"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# Social Media Content Calendar\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Summary table
            f.write("## Platform Summary\n\n")
            f.write("| Platform | Total Posts | Character Limits |\n")
            f.write("|----------|-------------|------------------|\n")
            
            for platform, posts in all_posts.items():
                char_limit = self.platforms[platform]['char_limit']
                f.write(f"| {platform.title()} | {len(posts)} | {char_limit} chars |\n")
            
            f.write("\n## Content Distribution\n\n")
            
            # Content type breakdown
            content_types = {}
            for platform, posts in all_posts.items():
                for post in posts:
                    content_type = post['content_type']
                    if content_type not in content_types:
                        content_types[content_type] = 0
                    content_types[content_type] += 1
            
            for content_type, count in content_types.items():
                f.write(f"- **{content_type}**: {count} posts\n")
            
            f.write("\n## Platform-Specific Files\n\n")
            for platform in all_posts.keys():
                f.write(f"- [{platform.title()} Posts](./{platform}_posts.md)\n")

def main():
    """Main function to run the social media generator"""
    
    if len(sys.argv) < 2:
        print("Usage: python social_media_generator.py <content_strategy.csv> [output_folder]")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    output_folder = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not Path(csv_file).exists():
        print(f"❌ CSV file not found: {csv_file}")
        sys.exit(1)
    
    generator = SocialMediaGenerator()
    result = generator.generate_posts_from_csv(csv_file, output_folder)
    
    if result:
        print("🎉 Social media posts generated successfully!")
    else:
        print("❌ Failed to generate social media posts")
        sys.exit(1)

if __name__ == "__main__":
    main()