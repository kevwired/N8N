#!/usr/bin/env python3
"""
Research-based content generator for 5 businesses
Combines online research with Notion database configurations
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

class ResearchBasedContentGenerator:
    def __init__(self):
        self.notion_headers = {
            'Authorization': f'Bearer {NOTION_API_KEY}',
            'Content-Type': 'application/json',
            'Notion-Version': '2022-06-28'
        }
        self.base_client_dir = r"Z:\Main Drive\360TFT Resources\Workflows\N8N\Content Factory Pro\Clients"
        
        # Research data from online investigation
        self.research_data = {
            'BGK Goalkeeping': {
                'services': 'Goalkeeper training and coaching across Scotland, 1-to-1 and group classes, performance camps',
                'unique_selling_points': 'Evidence-based coaching, #BGKUNION community, 4,285 Instagram followers, specialized goalkeeper equipment',
                'target_market': 'Young goalkeepers of all ages, grass-roots clubs',
                'social_proof': 'Strong social media presence with engaged community, professional training programs'
            },
            '360TFT': {
                'services': 'Football coaching platform with 328+ training sessions, UEFA C Licence guidance, digital coaching tools',
                'unique_selling_points': 'Founded by Kevin Middleton, 1,200+ coaches in Skool Community, "Stop Guessing. Start Coaching With Confidence"',
                'target_market': 'Football coaches, academy owners, grassroots coaches',
                'social_proof': '800+ players trained across two academies, coaching roles at Arbroath FC and Hamilton Women FC'
            },
            'Kit-Mart': {
                'services': 'Bespoke football kit supplier to local clubs, schools and local authorities, Savi sportswear range',
                'unique_selling_points': 'Leading supplier of custom clothing, ships 600 parcels regularly, focus on local/grassroots market',
                'target_market': 'Local football clubs, schools, local authorities across UK',
                'social_proof': 'Established supplier with regular high-volume shipping, trusted by educational institutions'
            },
            'CD Copland Motors': {
                'services': 'MOT testing, general repairs, servicing, diagnostics, welding, Unipart Car Care Centre',
                'unique_selling_points': '12,000 mile/12 month nationwide guarantee, Good Garage Scheme member, SMTA member',
                'target_market': 'Vehicle owners in Monifieth/Dundee/Angus area, EV owners',
                'social_proof': '5/5 stars (21 reviews), 100% recommend (31 Facebook reviews), established independent garage'
            },
            'KF Barbers': {
                'services': 'Haircuts, hot shaves, beard trims, walk-ins welcome, gift vouchers available',
                'unique_selling_points': 'Excellent with children, professional service, affordable prices, accommodating walk-ins',
                'target_market': 'Local men, parents with young boys, traditional gentlemen in Arbroath',
                'social_proof': '4.9/5 rating, 215+ reviews, "Best barbers in town", "Brilliant with kids"'
            },
            'Athlete Recovery Zone': {
                'services': 'Whole Body Cryotherapy, NormaTec Compression therapy, Infrared Sauna, Red Light Therapy, Sports Massage, Assisted Stretching, Myofascial Release, Cupping Therapy',
                'unique_selling_points': 'Comprehensive recovery approach, professional athletic background staff, cutting-edge technology, evidence-based treatments, flexible membership and walk-in options',
                'target_market': 'Professional athletes, college sports participants, weekend warriors, fitness enthusiasts, individuals recovering from sports injuries',
                'social_proof': 'Professional athlete endorsements, Division 1 athlete testimonials, partnerships with 450+ sports teams and colleges, immediate results customer feedback'
            }
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
            'email': get_text(props.get('Email', {})),
            'google_drive_folder': get_text(props.get('Google Drive Parent Folder', {}))
        }
    
    def generate_content_ideas_with_research(self, business_name: str, business_config: Dict, research_data: Dict) -> List[Dict]:
        """Generate 12 content ideas based on research and configuration"""
        
        category = business_config['category'].lower()
        research_info = research_data
        
        if business_name == 'BGK Goalkeeping':
            return [
                {'type': 'Educational', 'topic': 'Essential Goalkeeper Training Drills', 'brief': f'Share proven goalkeeper training techniques that develop reflexes and positioning. Based on BGK\'s evidence-based coaching approach.', 'hook': 'Transform your goalkeeping with professional techniques', 'research_tie_in': 'BGK\'s specialized goalkeeper training across Scotland'},
                {'type': 'Educational', 'topic': 'Building Confidence in Young Goalkeepers', 'brief': f'How parents and coaches can help young goalkeepers overcome fear and build confidence between the posts.', 'hook': 'Every great goalkeeper started with confidence', 'research_tie_in': 'BGK\'s focus on confidence-building for young goalkeepers'},
                {'type': 'Educational', 'topic': 'Goalkeeper Equipment Essentials', 'brief': f'What every goalkeeper needs to train and play effectively, from gloves to training aids.', 'hook': 'The right gear makes all the difference', 'research_tie_in': 'BGK\'s specialized goalkeeper equipment range'},
                {'type': 'Educational', 'topic': 'The Mental Game of Goalkeeping', 'brief': f'How to develop the mental toughness and focus required for successful goalkeeping.', 'hook': 'Goalkeeping is 80% mental', 'research_tie_in': 'BGK\'s evidence-based coaching methodology'},
                {'type': 'Behind-the-Scenes', 'topic': 'Inside a BGK Performance Camp', 'brief': f'Take a look at what happens during our intensive goalkeeper training camps.', 'hook': 'Where goalkeeper dreams become reality', 'research_tie_in': 'BGK\'s performance camps for all ages'},
                {'type': 'Behind-the-Scenes', 'topic': 'Meet the BGK Coaching Team', 'brief': f'Get to know the experienced coaches who make up the BGK academy.', 'hook': 'Goalkeeper-to-goalkeeper expertise', 'research_tie_in': 'BGK\'s professional coaching team'},
                {'type': 'Promotional', 'topic': 'Join the #BGKUNION', 'brief': f'Become part of Scotland\'s premier goalkeeper community and training network.', 'hook': 'More goalkeepers are joining the #BGKUNION', 'research_tie_in': 'BGK\'s 4,285+ Instagram community'},
                {'type': 'Promotional', 'topic': '1-to-1 Training Available', 'brief': f'Personalized goalkeeper coaching sessions tailored to individual development needs.', 'hook': 'Elite coaching, just for you', 'research_tie_in': 'BGK\'s 1-to-1 and group training options'},
                {'type': 'Promotional', 'topic': 'Small Group Training Sessions', 'brief': f'Join our small group sessions for intensive goalkeeper development in a supportive environment.', 'hook': 'Learn together, grow together', 'research_tie_in': 'BGK\'s small group training classes'},
                {'type': 'Success Story', 'topic': 'From Grassroots to Confidence', 'brief': f'How BGK training transformed a nervous young goalkeeper into a confident shot-stopper.', 'hook': 'Watch confidence grow with every save', 'research_tie_in': 'BGK\'s work with grassroots clubs'},
                {'type': 'Success Story', 'topic': 'Academy Success Stories', 'brief': f'Celebrating the achievements of goalkeepers who\'ve progressed through BGK training.', 'hook': 'BGK goalkeepers achieving their dreams', 'research_tie_in': 'BGK\'s training program success'},
                {'type': 'Success Story', 'topic': 'Parent Testimonials', 'brief': f'What parents say about the impact of BGK training on their young goalkeepers.', 'hook': 'Parents see the difference BGK makes', 'research_tie_in': 'BGK\'s positive impact on young goalkeepers'}
            ]
        
        elif business_name == '360TFT':
            return [
                {'type': 'Educational', 'topic': 'Stop Guessing, Start Coaching', 'brief': f'How structured, game-based training replaces guesswork with proven coaching methods.', 'hook': 'Confidence comes from knowing what works', 'research_tie_in': '360TFT\'s "Stop Guessing. Start Coaching With Confidence" philosophy'},
                {'type': 'Educational', 'topic': 'UEFA C Licence Guidance', 'brief': f'Essential tips and resources for coaches pursuing their UEFA C Licence qualification.', 'hook': 'Your pathway to professional coaching', 'research_tie_in': '360TFT\'s UEFA C Licence guidance materials'},
                {'type': 'Educational', 'topic': '328+ Training Sessions at Your Fingertips', 'brief': f'Access ready-to-use training sessions covering ball mastery, rondos, and tactical scenarios.', 'hook': 'Never run out of training ideas again', 'research_tie_in': '360TFT\'s comprehensive session library'},
                {'type': 'Educational', 'topic': 'Grassroots Football Revolution', 'brief': f'How to challenge expensive football establishment while delivering quality coaching.', 'hook': 'Quality coaching shouldn\'t cost a fortune', 'research_tie_in': '360TFT\'s mission to make coaching accessible'},
                {'type': 'Behind-the-Scenes', 'topic': 'From Volunteer to Academy Owner', 'brief': f'Kevin Middleton\'s journey from grassroots volunteer to training 800+ players.', 'hook': 'Every coach starts somewhere', 'research_tie_in': 'Kevin\'s journey with two successful academies'},
                {'type': 'Behind-the-Scenes', 'topic': 'Coaching at Arbroath FC', 'brief': f'Insights from Kevin\'s experience coaching at professional and semi-professional level.', 'hook': 'Professional insights for grassroots coaches', 'research_tie_in': 'Kevin\'s roles at Arbroath FC and Hamilton Women FC'},
                {'type': 'Promotional', 'topic': 'Join 1,200+ Coaches', 'brief': f'Become part of the fastest-growing football coaching community for just $10/month.', 'hook': '1,200+ coaches can\'t be wrong', 'research_tie_in': '360TFT\'s 1,200+ Skool Community members'},
                {'type': 'Promotional', 'topic': '360@HOME Training App', 'brief': f'Digital training tools that bring professional coaching methods to your fingertips.', 'hook': 'Professional coaching, anywhere, anytime', 'research_tie_in': '360TFT\'s digital coaching tools'},
                {'type': 'Promotional', 'topic': 'Webinar Replays Available', 'brief': f'Access recorded coaching webinars covering advanced techniques and methodologies.', 'hook': 'Learn from the experts, on demand', 'research_tie_in': '360TFT\'s educational webinar content'},
                {'type': 'Success Story', 'topic': 'From 300 to 800+ Players', 'brief': f'How 360TFT methodologies helped build two successful football academies.', 'hook': 'Proven methods, proven results', 'research_tie_in': 'Growth from 300 to 800+ players across academies'},
                {'type': 'Success Story', 'topic': 'Coach Transformation Stories', 'brief': f'How grassroots coaches gained confidence and improved their coaching through 360TFT.', 'hook': 'Watch coaches transform their approach', 'research_tie_in': '360TFT community success stories'},
                {'type': 'Success Story', 'topic': 'Six-Figure Success', 'brief': f'How structured coaching methods and business acumen led to sustainable football businesses.', 'hook': 'Building successful football enterprises', 'research_tie_in': 'Kevin\'s six-figure business achievements'}
            ]
        
        elif business_name == 'Kit-Mart':
            return [
                {'type': 'Educational', 'topic': 'Bespoke Kit Ordering Made Simple', 'brief': f'How local clubs can access professional-quality custom kit without the complexity.', 'hook': 'Professional kits for grassroots clubs', 'research_tie_in': 'Kit-Mart\'s bespoke clothing for local clubs'},
                {'type': 'Educational', 'topic': 'School Sports Kit Solutions', 'brief': f'Complete guide to ordering custom sports kit for schools and educational institutions.', 'hook': 'Equipping tomorrow\'s athletes today', 'research_tie_in': 'Kit-Mart\'s work with schools and local authorities'},
                {'type': 'Educational', 'topic': 'Savi Sportswear Range Explained', 'brief': f'Everything you need to know about our comprehensive Savi sportswear collection.', 'hook': 'Quality sportswear for every team', 'research_tie_in': 'Kit-Mart\'s complete Savi range'},
                {'type': 'Educational', 'topic': 'Training Kit Essentials', 'brief': f'The complete range of training products and accessories every team needs.', 'hook': 'From training ground to match day', 'research_tie_in': 'Kit-Mart\'s training products and accessories'},
                {'type': 'Behind-the-Scenes', 'topic': 'Processing 600 Orders', 'brief': f'A look inside our facility as we process hundreds of kit orders for clubs across the UK.', 'hook': 'The busiest kit supplier in grassroots football', 'research_tie_in': 'Kit-Mart\'s 600 parcels leaving regularly'},
                {'type': 'Behind-the-Scenes', 'topic': 'Quality Control Process', 'brief': f'How we ensure every piece of custom kit meets our high standards before shipping.', 'hook': 'Quality is never an accident', 'research_tie_in': 'Kit-Mart\'s commitment to bespoke quality'},
                {'type': 'Promotional', 'topic': 'Local Authority Partnerships', 'brief': f'Reliable kit supply partnerships with local councils and government organizations.', 'hook': 'Trusted by local authorities nationwide', 'research_tie_in': 'Kit-Mart\'s work with local authorities'},
                {'type': 'Promotional', 'topic': 'Club Bulk Ordering', 'brief': f'Special rates and streamlined processes for clubs ordering complete team kits.', 'hook': 'Better rates for team orders', 'research_tie_in': 'Kit-Mart\'s focus on club orders'},
                {'type': 'Promotional', 'topic': 'Custom Hoodies & Tracksuits', 'brief': f'Complete your team\'s look with custom hoodies, tracksuits, and training wear.', 'hook': 'Look professional, feel professional', 'research_tie_in': 'Kit-Mart\'s range including hoodies and tracksuits'},
                {'type': 'Success Story', 'topic': 'School Success Partnership', 'brief': f'How we helped a local school transform their sports program with quality kit.', 'hook': 'Transforming school sports, one kit at a time', 'research_tie_in': 'Kit-Mart\'s educational institution partnerships'},
                {'type': 'Success Story', 'topic': 'Club Kit Transformation', 'brief': f'From basic kit to professional appearance - a grassroots club\'s transformation story.', 'hook': 'When clubs look professional, they play professional', 'research_tie_in': 'Kit-Mart\'s impact on local club presentation'},
                {'type': 'Success Story', 'topic': 'High-Volume Success', 'brief': f'How our efficient systems help us consistently deliver hundreds of orders on time.', 'hook': 'Reliability at scale', 'research_tie_in': 'Kit-Mart\'s high-volume shipping success'}
            ]
        
        elif business_name == 'CD Copland Motors':
            return [
                {'type': 'Educational', 'topic': 'MOT Testing Explained', 'brief': f'Everything you need to know about MOT tests for cars, motorcycles, vans, and commercial vehicles.', 'hook': 'Stay legal, stay safe on the road', 'research_tie_in': 'CD Copland\'s comprehensive MOT testing services'},
                {'type': 'Educational', 'topic': 'Electric Vehicle Servicing', 'brief': f'What EV owners need to know about maintaining their electric vehicles properly.', 'hook': 'The future of automotive care is electric', 'research_tie_in': 'CD Copland\'s progressive EV services'},
                {'type': 'Educational', 'topic': 'Unipart 12-Month Guarantee', 'brief': f'Understanding your nationwide 12,000 mile or 12-month parts guarantee coverage.', 'hook': 'Peace of mind, guaranteed nationwide', 'research_tie_in': 'CD Copland\'s Unipart Car Care Centre status'},
                {'type': 'Educational', 'topic': 'Independent vs Franchise Garages', 'brief': f'Why independent garages offer better value without compromising on quality or service.', 'hook': 'All the skills, without the inflated prices', 'research_tie_in': 'CD Copland\'s independent garage advantages'},
                {'type': 'Behind-the-Scenes', 'topic': 'Good Garage Scheme Standards', 'brief': f'What it means to be a Good Garage Scheme member and how it protects customers.', 'hook': 'Quality standards you can trust', 'research_tie_in': 'CD Copland\'s Good Garage Scheme membership'},
                {'type': 'Behind-the-Scenes', 'topic': 'SMTA Code of Conduct', 'brief': f'Our commitment to the Scottish Motor Trade Association\'s professional standards.', 'hook': 'Professional standards, Scottish values', 'research_tie_in': 'CD Copland\'s SMTA membership'},
                {'type': 'Promotional', 'topic': 'Monifieth\'s Trusted Garage', 'brief': f'Serving the Monifieth, Dundee, and Angus communities with professional automotive care.', 'hook': 'Your local garage, your trusted partner', 'research_tie_in': 'CD Copland\'s local Monifieth/Dundee focus'},
                {'type': 'Promotional', 'topic': 'Diagnostic Specialists', 'brief': f'Advanced diagnostic equipment and expertise for complex automotive problems.', 'hook': 'When others can\'t find the problem, we can', 'research_tie_in': 'CD Copland\'s diagnostic capabilities'},
                {'type': 'Promotional', 'topic': 'Three Wheeler & Trike MOTs', 'brief': f'Specialized MOT testing for motorcycles, three-wheelers, and trikes.', 'hook': 'Specialized testing for specialized vehicles', 'research_tie_in': 'CD Copland\'s diverse MOT testing capabilities'},
                {'type': 'Success Story', 'topic': '5-Star Customer Reviews', 'brief': f'What our customers say about their experience with CD Copland Motors.', 'hook': '5 stars, 21 reviews, 100% recommended', 'research_tie_in': 'CD Copland\'s excellent review scores'},
                {'type': 'Success Story', 'topic': 'Facebook Community Love', 'brief': f'Why 31 Facebook reviewers give us 100% recommendation rating.', 'hook': 'When customers love you, they tell everyone', 'research_tie_in': 'CD Copland\'s 100% Facebook recommendation rate'},
                {'type': 'Success Story', 'topic': 'Solved the Unsolvable', 'brief': f'Case study of a complex diagnostic problem other garages couldn\'t solve.', 'hook': 'Experience finds solutions others miss', 'research_tie_in': 'CD Copland\'s diagnostic expertise and problem-solving'}
            ]
        
        elif business_name == 'KF Barbers':
            return [
                {'type': 'Educational', 'topic': 'Perfect Haircut Frequency Guide', 'brief': f'How often different hair types and styles need cutting to maintain their best appearance.', 'hook': 'Looking sharp requires the right schedule', 'research_tie_in': 'KF Barbers\' professional grooming expertise'},
                {'type': 'Educational', 'topic': 'Preparing Kids for Haircuts', 'brief': f'Tips for parents to make their child\'s barber visit stress-free and enjoyable.', 'hook': 'Making every child\'s haircut a happy experience', 'research_tie_in': 'KF Barbers\' reputation for being "brilliant with kids"'},
                {'type': 'Educational', 'topic': 'Traditional Hot Shave Benefits', 'brief': f'The art and benefits of traditional hot shaves for the modern gentleman.', 'hook': 'Experience the luxury of traditional grooming', 'research_tie_in': 'KF Barbers\' hot shave services'},
                {'type': 'Educational', 'topic': 'Beard Trimming Techniques', 'brief': f'Professional beard shaping and maintenance techniques for the perfect look.', 'hook': 'A well-groomed beard speaks volumes', 'research_tie_in': 'KF Barbers\' beard trimming expertise'},
                {'type': 'Behind-the-Scenes', 'topic': '4.9-Star Service Standards', 'brief': f'What goes into delivering the consistently excellent service that earns 4.9/5 ratings.', 'hook': 'Excellence isn\'t an accident, it\'s a habit', 'research_tie_in': 'KF Barbers\' exceptional 4.9/5 rating'},
                {'type': 'Behind-the-Scenes', 'topic': 'The Art of Barbering', 'brief': f'Traditional barbering skills combined with modern techniques and customer service.', 'hook': 'Where traditional craftsmanship meets modern service', 'research_tie_in': 'KF Barbers\' professional barbering approach'},
                {'type': 'Promotional', 'topic': 'Walk-Ins Welcome', 'brief': f'No appointment needed - quality cuts available for walk-in customers throughout the day.', 'hook': 'Great haircuts, no waiting around', 'research_tie_in': 'KF Barbers\' accommodating walk-in policy'},
                {'type': 'Promotional', 'topic': 'Gift Vouchers Available', 'brief': f'The perfect gift for the well-groomed man in your life - professional grooming vouchers.', 'hook': 'Give the gift of looking sharp', 'research_tie_in': 'KF Barbers\' gift voucher service'},
                {'type': 'Promotional', 'topic': 'Arbroath\'s Premier Barbers', 'brief': f'Why locals and visitors choose KF Barbers for their grooming needs in Arbroath.', 'hook': 'Best barbers in town, according to our customers', 'research_tie_in': 'KF Barbers\' reputation as "best barbers in town"'},
                {'type': 'Success Story', 'topic': '215+ Happy Customers', 'brief': f'What over 215 customer reviews tell us about the KF Barbers experience.', 'hook': 'Real customers, real results, real satisfaction', 'research_tie_in': 'KF Barbers\' 215+ positive reviews'},
                {'type': 'Success Story', 'topic': 'Father and Son Tradition', 'brief': f'Creating multi-generational customers who trust KF Barbers for family grooming.', 'hook': 'When granddad, dad, and son all trust the same barber', 'research_tie_in': 'KF Barbers\' family-friendly reputation'},
                {'type': 'Success Story', 'topic': 'Professional Service Excellence', 'brief': f'Customer testimonials highlighting the professional, classy service at KF Barbers.', 'hook': 'Superb service, very classy interior, always professional', 'research_tie_in': 'Customer praise for KF Barbers\' professional standards'}
            ]
        
        elif business_name == 'Athlete Recovery Zone':
            return [
                {'type': 'Educational', 'topic': 'Complete Recovery Guide', 'brief': f'Everything athletes need to know about proper recovery between training sessions and competitions.', 'hook': 'Recovery is where champions are made', 'research_tie_in': 'Athlete Recovery Zone\'s comprehensive recovery approach'},
                {'type': 'Educational', 'topic': 'Cryotherapy Benefits Explained', 'brief': f'The science behind whole body cryotherapy and how it accelerates athletic recovery.', 'hook': 'Cold therapy, hot performance results', 'research_tie_in': 'Athlete Recovery Zone\'s cutting-edge cryotherapy technology'},
                {'type': 'Educational', 'topic': 'NormaTec Compression Therapy', 'brief': f'How pneumatic compression helps flush metabolic waste and improve circulation for faster recovery.', 'hook': 'Compression that works as hard as you do', 'research_tie_in': 'Athlete Recovery Zone\'s professional-grade NormaTec systems'},
                {'type': 'Educational', 'topic': 'Injury Prevention Strategies', 'brief': f'Proactive recovery techniques that prevent injuries before they happen, keeping athletes in the game.', 'hook': 'Prevention is the best performance strategy', 'research_tie_in': 'Athlete Recovery Zone\'s evidence-based prevention protocols'},
                {'type': 'Behind-the-Scenes', 'topic': 'Professional Athlete Endorsements', 'brief': f'Why Division 1 athletes and professionals choose our facility as their recovery headquarters.', 'hook': 'Where elite athletes come to recover', 'research_tie_in': 'Division 1 athlete testimonials and professional endorsements'},
                {'type': 'Behind-the-Scenes', 'topic': 'Cutting-Edge Recovery Technology', 'brief': f'A tour of our state-of-the-art recovery equipment and how each modality serves athletic performance.', 'hook': 'Technology that keeps you ahead of the game', 'research_tie_in': 'Athlete Recovery Zone\'s professional-grade equipment investment'},
                {'type': 'Promotional', 'topic': 'Flexible Membership Options', 'brief': f'Recovery plans that fit every athlete\'s schedule and budget, from walk-ins to unlimited memberships.', 'hook': 'Recovery solutions as unique as your training', 'research_tie_in': 'Athlete Recovery Zone\'s flexible membership and walk-in options'},
                {'type': 'Promotional', 'topic': 'Sports Team Partnerships', 'brief': f'Comprehensive recovery programs designed for teams, clubs, and athletic organizations.', 'hook': 'Team recovery for championship results', 'research_tie_in': 'Partnerships with 450+ sports teams and colleges'},
                {'type': 'Promotional', 'topic': 'Red Light Therapy Sessions', 'brief': f'Advanced photobiomodulation therapy for enhanced muscle recovery and pain reduction.', 'hook': 'Healing at the speed of light', 'research_tie_in': 'Athlete Recovery Zone\'s advanced red light therapy technology'},
                {'type': 'Success Story', 'topic': 'Immediate Recovery Results', 'brief': f'Real athlete testimonials about experiencing instant relief and improved performance after sessions.', 'hook': 'Results you can feel immediately', 'research_tie_in': 'Customer feedback about immediate recovery benefits'},
                {'type': 'Success Story', 'topic': 'Weekend Warrior Transformations', 'brief': f'How recreational athletes dramatically improved their performance and reduced injury rates with consistent recovery.', 'hook': 'From weekend warrior to weekend champion', 'research_tie_in': 'Success stories from fitness enthusiasts and recreational athletes'},
                {'type': 'Success Story', 'topic': 'Professional Athletic Success', 'brief': f'Case studies of professional athletes who credit our recovery protocols for their competitive edge.', 'hook': 'The edge that separates good from great', 'research_tie_in': 'Professional athlete success stories and performance improvements'}
            ]
        
        else:
            # Fallback for any other business
            return []
    
    def _get_clean_cta(self, business_config: Dict, content_type: str) -> str:
        """Extract a single, clean CTA from business configuration"""
        
        cta_template = business_config.get('cta_template', '')
        
        # Handle businesses with multiple CTA options (like BGK Goalkeeping)
        if 'PRIMARY CTA OPTIONS:' in cta_template or 'FOR TRAINING INQUIRIES:' in cta_template:
            # Extract the first clean CTA option
            lines = cta_template.split('\n')
            for line in lines:
                if line.startswith('"') and line.endswith('"'):
                    return line.strip('"')
            
            # Fallback: create a generic CTA based on business name
            business_name = business_config.get('business_name', 'us')
            return f"Ready to experience the difference? Contact {business_name} today to learn more."
        
        # For businesses with clean CTAs (like Athlete Recovery Zone)
        return cta_template.strip()
    
    def generate_content_with_disclaimer(self, idea: Dict, business_config: Dict, content_number: int, month: str) -> str:
        """Generate content with disclaimer and research integration"""
        
        # Enhanced content generation using research data
        business_name = business_config['business_name']
        research_info = self.research_data.get(business_name, {})
        
        # Create clean, complete shortform content with proper CTA
        clean_cta = self._get_clean_cta(business_config, idea['type'])
        shortform_content = f"{idea['hook']}! {idea['brief']} {clean_cta}"
        
        # Enhanced longform content with research integration
        longform_content = f"""# {idea['topic']}

{idea['hook']} - and at {business_name}, this isn't just a motto, it's how we operate every day.

## The Challenge

{idea['brief']} This is where many people struggle, but it's exactly where {business_name} excels.

## Our Research-Backed Approach

Based on real customer feedback and our proven track record, {business_name} has developed a methodology that works. {idea.get('research_tie_in', '')}

{research_info.get('social_proof', 'Our customers consistently praise our approach and results.')}

## What Sets Us Apart

{research_info.get('unique_selling_points', 'We combine expertise with genuine care for our customers.')}

## Why Choose {business_name}

{business_config.get('business_notes', 'We are committed to delivering exceptional results and building lasting relationships.')[:200]}

## Ready to Experience the Difference?

{clean_cta}

---
*{research_info.get('services', 'Professional services tailored to your needs.')}*"""
        
        # Create the content with exact disclaimer format
        content = f"""❗ DISCLAIMER
═══════════════════════════════════════
Please check all content carefully before you post it. AI can make mistakes. Check and correct important info.

Images can also be incorrect and are only provided as an alternative to your own images.

If you require any changes in how your content and images are produced, contact Kevin via admin@kevinrmiddleton.com or WhatsApp 07926676298
═══════════════════════════════════════

{idea['topic']}

📱 SHORTFORM VERSION
═══════════════════════════════════════

{shortform_content}

📘 LINKEDIN/BLOG/NEWSLETTER VERSION
═══════════════════════════════════════

{longform_content}

🖼️ IMAGE USAGE GUIDE
═══════════════════════════════════════

💡 Quick Platform Guide:
   • Instagram → Use Original or Square (if available)
   • Facebook → Use Universal (if available) or Original
   • LinkedIn → Use Universal (if available) or Original
   • Twitter → Use Universal (if available) or Original
   • YouTube → Use Universal (if available) or Original
═══════════════════════════════════════"""
        
        return content
    
    def create_monthly_folders(self, client_folder: str):
        """Create monthly folders"""
        months = ['Aug_25', 'Sep_25', 'Oct_25', 'Nov_25', 'Dec_25']
        for month in months:
            month_folder = os.path.join(client_folder, month)
            os.makedirs(month_folder, exist_ok=True)
    
    def generate_business_content(self, business_name: str):
        """Generate content for a specific business"""
        
        print(f"\n{'='*60}")
        print(f"GENERATING CONTENT FOR: {business_name}")
        print(f"{'='*60}")
        
        # Get business config
        config = self.get_business_config(business_name)
        if not config:
            print(f"[ERROR] Business '{business_name}' not found in Notion database")
            return
        
        print(f"[SUCCESS] Found configuration for {config['business_name']}")
        print(f"[INFO] Category: {config['category']}")
        
        # Get research data
        research_data = self.research_data.get(business_name, {})
        print(f"[INFO] Research data: {len(research_data)} key insights")
        
        # Generate content ideas
        ideas = self.generate_content_ideas_with_research(business_name, config, research_data)
        print(f"[INFO] Generated {len(ideas)} research-based content ideas")
        
        # Create local folder structure
        client_folder = os.path.join(self.base_client_dir, business_name)
        
        if not os.path.exists(client_folder):
            os.makedirs(client_folder, exist_ok=True)
            print(f"[CREATED] Client folder: {client_folder}")
        
        # Create monthly folders
        self.create_monthly_folders(client_folder)
        
        # Current month folder (August 2025)
        current_month = datetime.now().strftime('%b_25')
        monthly_folder = os.path.join(client_folder, current_month)
        
        print(f"[INFO] Saving content to: {monthly_folder}")
        
        # Generate content files
        generated_files = []
        
        for idx, idea in enumerate(ideas, 1):
            clean_topic = idea['topic'].replace('?', '').replace(':', '').replace(' ', '_')[:25]
            filename = f"{current_month}_{idx:02d}_{idea['type']}_{clean_topic}.txt"
            
            content = self.generate_content_with_disclaimer(idea, config, idx, current_month)
            
            # Save to monthly folder
            file_path = os.path.join(monthly_folder, filename)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            generated_files.append({
                'filename': filename,
                'path': file_path,
                'type': idea['type'],
                'topic': idea['topic']
            })
            
            print(f"[{idx:02d}/12] Generated: {filename}")
        
        # Create summary file
        summary_content = f"""RESEARCH-BASED CONTENT SUMMARY - {business_name}
{'='*70}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Month: {current_month}
Total Files: {len(generated_files)}

RESEARCH INSIGHTS USED:
======================
Services: {research_data.get('services', 'N/A')[:100]}...
USPs: {research_data.get('unique_selling_points', 'N/A')[:100]}...
Social Proof: {research_data.get('social_proof', 'N/A')[:100]}...

CONTENT BREAKDOWN:
=================
"""
        
        # Add file breakdown
        content_types = {}
        for file_info in generated_files:
            content_type = file_info['type']
            if content_type not in content_types:
                content_types[content_type] = []
            content_types[content_type].append(file_info['filename'])
        
        for content_type, files in content_types.items():
            summary_content += f"\n{content_type.upper()} ({len(files)} files):\n"
            for filename in files:
                summary_content += f"  • {filename}\n"
        
        summary_content += f"""
RESEARCH-DRIVEN FEATURES:
========================
✅ Real customer reviews integrated
✅ Actual business services highlighted  
✅ Unique selling points emphasized
✅ Social proof incorporated
✅ Target audience alignment
✅ Brand voice consistency

LOCAL FOLDER: {monthly_folder}
GOOGLE DRIVE TARGET: Social Media Business/{config.get('google_drive_folder', business_name)}/{current_month}

Generated by Research-Based Content Factory Pro
Contact: admin@kevinrmiddleton.com
"""
        
        # Save summary
        summary_file = os.path.join(monthly_folder, f"{current_month}_RESEARCH_SUMMARY.txt")
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(summary_content)
        
        print(f"\n[SUCCESS] Content generation complete for {business_name}")
        print(f"[FILES] 12 research-based content files created")
        print(f"[SUMMARY] Research summary saved: {summary_file}")
        
        return generated_files

def main():
    """Generate content for all 6 businesses"""
    
    print("="*70)
    print("    RESEARCH-BASED CONTENT GENERATOR")
    print("    Combining Online Research + Notion Database")
    print("="*70)
    
    generator = ResearchBasedContentGenerator()
    
    # List of businesses to generate content for
    businesses = ['BGK Goalkeeping', '360TFT', 'Kit-Mart', 'CD Copland Motors', 'KF Barbers', 'Athlete Recovery Zone']
    
    total_generated = 0
    
    for business_name in businesses:
        try:
            files = generator.generate_business_content(business_name)
            if files:
                total_generated += len(files)
        except Exception as e:
            print(f"[ERROR] Failed to generate content for {business_name}: {e}")
    
    print(f"\n{'='*70}")
    print(f"✅ CONTENT GENERATION COMPLETE!")
    print(f"{'='*70}")
    print(f"📊 Total files generated: {total_generated}")
    print(f"📁 Businesses processed: {len(businesses)}")
    print(f"📅 Month folder: {datetime.now().strftime('%b_25')}")
    print(f"🔬 Research-driven content with real customer insights")
    print(f"{'='*70}")

if __name__ == "__main__":
    main()