#!/usr/bin/env python3
"""
Engaging Content Writer - High-quality short-form content generation
Replaces simple concatenation with proper hooks, flow, and CTAs
"""

import re
from typing import Dict, List
from datetime import datetime

class EngagingContentWriter:
    def __init__(self):
        # Platform-specific optimization rules
        self.platform_rules = {
            'Facebook': {
                'optimal_length': (80, 250),
                'tone': 'conversational',
                'focus': 'community and engagement',
                'emoji_limit': 2,
                'hashtag_limit': 3
            },
            'Instagram': {
                'optimal_length': (125, 150),  # Front-loaded for algorithm
                'tone': 'visual-focused',
                'focus': 'lifestyle and aspiration',
                'emoji_limit': 3,
                'hashtag_limit': 8
            },
            'LinkedIn': {
                'optimal_length': (150, 300),
                'tone': 'professional',
                'focus': 'industry insights and expertise',
                'emoji_limit': 1,
                'hashtag_limit': 3
            },
            'Twitter': {
                'optimal_length': (71, 100),  # Optimal engagement range
                'tone': 'concise and punchy',
                'focus': 'quick value and engagement',
                'emoji_limit': 2,
                'hashtag_limit': 2
            }
        }
        
        # Business-specific voice patterns
        self.voice_patterns = {
            'BGK Goalkeeping': {
                'tone': 'encouraging and confident',
                'key_phrases': ['confidence building', 'evidence-based', 'goalkeeper specific'],
                'avoid_phrases': ['fear', 'intimidating', 'difficult'],
                'community_terms': ['#BGKUNION', 'goalkeeper family', 'BGK community']
            },
            '360TFT': {
                'tone': 'authoritative but accessible',
                'key_phrases': ['stop guessing', 'coaching confidence', 'game-based'],
                'avoid_phrases': ['expensive', 'complex', 'overwhelming'],
                'community_terms': ['coach community', '1,200+ coaches', 'coaching family']
            },
            'Kit-Mart': {
                'tone': 'reliable and professional',
                'key_phrases': ['bespoke solutions', 'grassroots focused', 'quality kit'],
                'avoid_phrases': ['cheap', 'basic', 'standard'],
                'community_terms': ['team partners', 'kit family', 'grassroots community']
            },
            'CD Copland Motors': {
                'tone': 'trustworthy and honest',
                'key_phrases': ['honest service', 'quality care', 'trusted garage'],
                'avoid_phrases': ['expensive', 'complicated', 'pushy'],
                'community_terms': ['Monifieth family', 'trusted customers', 'local community']
            },
            'KF Barbers': {
                'tone': 'welcoming and professional',
                'key_phrases': ['traditional quality', 'family friendly', 'expert care'],
                'avoid_phrases': ['intimidating', 'rushed', 'impersonal'],
                'community_terms': ['barbershop family', 'Arbroath community', 'three generations']
            },
            'Athlete Recovery Zone': {
                'tone': 'performance-focused and scientific',
                'key_phrases': ['evidence-based', 'performance enhancement', 'professional grade'],
                'avoid_phrases': ['painful', 'experimental', 'unproven'],
                'community_terms': ['athlete family', 'recovery community', '450+ teams']
            }
        }
    
    def write_engaging_content(self, idea: Dict, business_config: Dict, platform: str = 'Facebook') -> Dict:
        """Write engaging content optimized for specific platform"""
        
        business_name = business_config.get('business_name', '')
        voice_pattern = self.voice_patterns.get(business_name, {})
        platform_rules = self.platform_rules.get(platform, self.platform_rules['Facebook'])
        
        # Generate platform-optimized content
        if platform == 'Instagram':
            content = self._write_instagram_content(idea, business_config, voice_pattern, platform_rules)
        elif platform == 'LinkedIn':
            content = self._write_linkedin_content(idea, business_config, voice_pattern, platform_rules)
        elif platform == 'Twitter':
            content = self._write_twitter_content(idea, business_config, voice_pattern, platform_rules)
        else:  # Facebook (default)
            content = self._write_facebook_content(idea, business_config, voice_pattern, platform_rules)
        
        return {
            'platform': platform,
            'content': content,
            'character_count': len(content),
            'word_count': len(content.split()),
            'optimal_range': platform_rules['optimal_length'],
            'within_optimal': platform_rules['optimal_length'][0] <= len(content) <= platform_rules['optimal_length'][1],
            'generated_at': datetime.now().isoformat()
        }
    
    def _write_facebook_content(self, idea: Dict, business_config: Dict, voice_pattern: Dict, rules: Dict) -> str:
        """Write Facebook-optimized content (community-focused, conversational)"""
        
        business_name = business_config.get('business_name', '')
        hook = idea.get('hook', '')
        value_prop = idea.get('value_proposition', '')
        
        # Facebook structure: Hook → Community connection → Value → CTA
        if business_name == 'BGK Goalkeeping':
            if idea['type'] == 'Educational':
                return f"{hook} Every young goalkeeper needs the right foundation to build lasting confidence. Our evidence-based approach has helped hundreds of goalkeepers across Scotland transform their game. Ready to see what confidence can do for your goalkeeper?"
            elif idea['type'] == 'Promotional':
                return f"{hook} Join the #BGKUNION community where confidence meets technique. Our specialized training programs are designed specifically for young goalkeepers who want to excel. Ready to build unshakeable confidence?"
            elif idea['type'] == 'Behind-the-Scenes':
                return f"{hook} Our coaching team brings professional experience directly to grassroots development. See how we're building the next generation of confident goalkeepers across Tayside. Want to be part of the journey?"
            else:  # Success Story
                return f"{hook} Real results from real goalkeepers who've transformed their game through our proven programs. These success stories show what's possible with the right guidance. Ready to write your own success story?"
        
        elif business_name == '360TFT':
            if idea['type'] == 'Educational':
                return f"{hook} Over 1,200 coaches have discovered that structured, game-based training eliminates guesswork and builds genuine coaching confidence. Our proven methodologies have helped build successful academies across Scotland. Ready to stop guessing and start coaching with confidence?"
            elif idea['type'] == 'Promotional':
                return f"{hook} Join a community of coaches who are revolutionizing grassroots football without breaking the bank. For just £8/month, access the same coaching education that's built multiple successful academies. Ready to transform your coaching?"
            elif idea['type'] == 'Behind-the-Scenes':
                return f"{hook} Follow Kevin Middleton's journey from grassroots volunteer to building academies with 800+ players. See the real story behind creating sustainable football coaching businesses. Ready to build your own coaching success?"
            else:  # Success Story
                return f"{hook} Real coaches sharing real results from implementing our Game Model methodology and business strategies. These transformations prove that quality coaching education works. Ready to be our next success story?"
        
        elif business_name == 'Kit-Mart':
            if idea['type'] == 'Educational':
                return f"{hook} From local clubs to schools and authorities, we've learned what makes kit ordering simple and stress-free. Our streamlined process has helped outfit over 600 teams with quality custom sportswear. Ready to simplify your kit ordering?"
            elif idea['type'] == 'Promotional':
                return f"{hook} We specialize in bespoke kit solutions for clubs, schools, and local authorities across the UK. With our Savi sportswear range and bulk ordering options, we make professional-quality kit accessible. Ready to transform your team's image?"
            elif idea['type'] == 'Behind-the-Scenes':
                return f"{hook} Watch how we process hundreds of kit orders weekly while maintaining the quality standards that teams depend on. Every piece is checked before shipping. Ready to experience our quality commitment?"
            else:  # Success Story
                return f"{hook} See how clubs and schools have transformed their team identity with our custom kit solutions. From grassroots teams to educational institutions, quality kit makes the difference. Ready for your transformation?"
        
        elif business_name == 'CD Copland Motors':
            if idea['type'] == 'Educational':
                return f"{hook} As a Good Garage Scheme member and SMTA-certified garage, we believe in educating customers about their vehicles. Our 12,000 mile/12 month nationwide guarantee reflects our commitment to quality. Ready for honest automotive advice?"
            elif idea['type'] == 'Promotional':
                return f"{hook} From MOTs to major repairs, our Unipart Car Care Centre offers comprehensive automotive services for the Monifieth and Dundee communities. With 5-star ratings and 100% recommendations, we've earned our reputation. Ready for trustworthy service?"
            elif idea['type'] == 'Behind-the-Scenes':
                return f"{hook} See why our customers consistently rate us 5 stars and recommend us to family and friends. Our commitment to professional standards and honest service shows in everything we do. Ready to experience the difference?"
            else:  # Success Story
                return f"{hook} Real customers sharing their experiences with our diagnostic expertise and honest service approach. These reviews reflect our commitment to solving problems other garages couldn't fix. Ready to become our next satisfied customer?"
        
        elif business_name == 'KF Barbers':
            if idea['type'] == 'Educational':
                return f"{hook} With 4.9 stars from 215+ customers, we've learned what makes the perfect barbering experience for men and children alike. Our traditional techniques combined with modern customer service create the atmosphere Arbroath trusts. Ready for the perfect cut?"
            elif idea['type'] == 'Promotional':
                return f"{hook} We welcome walk-ins throughout the week and offer gift vouchers for the special men in your life. From traditional hot shaves to children's cuts, everyone leaves looking their best. Ready to look sharp?"
            elif idea['type'] == 'Behind-the-Scenes':
                return f"{hook} See the craftsmanship and attention to detail that's earned us recognition as Arbroath's premier barbershop. Our commitment to traditional barbering standards shows in every interaction. Ready to experience true craftsmanship?"
            else:  # Success Story
                return f"{hook} Three generations of families trust us with their grooming needs, and our customer reviews speak to the lasting relationships we build. These stories show why we're consistently rated as the best. Ready to join the family?"
        
        elif business_name == 'Athlete Recovery Zone':
            if idea['type'] == 'Educational':
                return f"{hook} Professional athletes and weekend warriors alike need proper recovery protocols to perform at their peak and prevent injuries. Our evidence-based approach combines cutting-edge technology with proven methodologies. Ready to recover like a pro?"
            elif idea['type'] == 'Promotional':
                return f"{hook} Our comprehensive facility offers everything from cryotherapy and NormaTec compression to infrared saunas and red light therapy. With flexible membership options and walk-in availability, professional-grade recovery is accessible. Ready to elevate your recovery?"
            elif idea['type'] == 'Behind-the-Scenes':
                return f"{hook} See the state-of-the-art recovery technology and professional protocols that have made us the choice of Division 1 athletes and 450+ sports teams. Our commitment to excellence shows in every session. Ready to experience elite recovery?"
            else:  # Success Story
                return f"{hook} Real athletes sharing how our recovery protocols have transformed their training and performance outcomes. From immediate pain relief to long-term gains, these stories demonstrate the power of proper recovery. Ready to transform your performance?"
        
        # Fallback
        return f"{hook} {value_prop} Ready to experience the difference?"
    
    def _write_instagram_content(self, idea: Dict, business_config: Dict, voice_pattern: Dict, rules: Dict) -> str:
        """Write Instagram-optimized content (visual-focused, front-loaded)"""
        
        business_name = business_config.get('business_name', '')
        hook = idea.get('hook', '')
        
        # Instagram structure: Strong visual hook → Quick value → Visual CTA (front-loaded)
        if business_name == 'BGK Goalkeeping':
            return f"⚽ {hook} Transform your goalkeeper's confidence with evidence-based training that actually works. Join the #BGKUNION! 💪 #GoalkeeperTraining #YouthFootball #Scotland #Confidence"
        elif business_name == '360TFT':
            return f"⚽ {hook} Stop guessing, start coaching with confidence. Join 1,200+ coaches transforming grassroots football! 🚀 #CoachingEducation #FootballCoaches #GrassrootsFootball #GameModel"
        elif business_name == 'Kit-Mart':
            return f"👕 {hook} Professional-quality kit for grassroots teams. See the difference quality makes! ⚽ #CustomKit #GrassrootsFootball #TeamPride #SportswearUK"
        elif business_name == 'CD Copland Motors':
            return f"🔧 {hook} Honest service, quality results. Your trusted Monifieth garage! 🚗 #MOTTesting #CarService #Monifieth #TrustedGarage"
        elif business_name == 'KF Barbers':
            return f"✂️ {hook} Traditional barbering excellence in Arbroath. 4.9 stars, walk-ins welcome! 💇‍♂️ #TraditionalBarber #Arbroath #GreatWithKids #HotShave"
        elif business_name == 'Athlete Recovery Zone':
            return f"💪 {hook} Professional recovery technology for all athletes. Faster recovery, better performance! 🏃‍♂️ #AthleteRecovery #Cryotherapy #SportsRecovery #PerformanceTraining"
        
        return f"✨ {hook} Experience the difference! #Quality #Professional #Service"
    
    def _write_linkedin_content(self, idea: Dict, business_config: Dict, voice_pattern: Dict, rules: Dict) -> str:
        """Write LinkedIn-optimized content (professional, industry insights)"""
        
        business_name = business_config.get('business_name', '')
        hook = idea.get('hook', '')
        angle = idea.get('angle', '')
        
        # LinkedIn structure: Industry insight → Professional value → Professional CTA
        if business_name == 'BGK Goalkeeping':
            return f"Youth sports development increasingly recognizes the critical role of confidence in athletic performance. {hook} Our evidence-based approach to goalkeeper training has transformed hundreds of young athletes across Scotland, proving that technical skills and mental confidence must develop together for optimal results. #YouthSports #AthleteConfidence #GoalkeeperDevelopment"
        elif business_name == '360TFT':
            return f"The football coaching industry faces a significant challenge: expensive courses that don't translate to practical results. {hook} Our community of 1,200+ coaches proves that accessible, game-based methodologies can revolutionize grassroots football development while building sustainable coaching businesses. #FootballCoaching #SportsEducation #CoachingDevelopment"
        elif business_name == 'Kit-Mart':
            return f"Grassroots sports organizations often struggle with kit procurement challenges that impact team identity and budget constraints. {hook} Our bespoke solutions for schools, clubs, and local authorities demonstrate how streamlined processes and quality partnerships can transform team presentation and organizational efficiency. #SportsKit #TeamManagement #GrassrootsSports"
        elif business_name == 'CD Copland Motors':
            return f"The automotive service industry's reputation challenges stem from transparency and quality consistency issues. {hook} Our Good Garage Scheme membership and SMTA certification demonstrate how independent garages can deliver franchise-quality service while maintaining competitive pricing and personal customer relationships. #AutomotiveService #CustomerTrust #QualityStandards"
        elif business_name == 'KF Barbers':
            return f"Traditional service industries face modern challenges in maintaining craftsmanship while meeting contemporary customer expectations. {hook} Our 4.9-star rating from 215+ customers demonstrates how combining traditional barbering techniques with exceptional customer service creates lasting business relationships. #TraditionalCraftsmanship #CustomerService #SmallBusiness"
        elif business_name == 'Athlete Recovery Zone':
            return f"Athletic performance optimization increasingly relies on recovery protocols that were once exclusive to elite sports. {hook} Our evidence-based approach to recovery technology demonstrates how comprehensive wellness strategies can benefit athletes at every level, from weekend warriors to Division 1 competitors. #SportsScience #AthleteWellness #PerformanceOptimization"
        
        return f"Industry insights reveal important trends. {hook} Professional expertise makes the difference. #Industry #Professional #Expertise"
    
    def _write_twitter_content(self, idea: Dict, business_config: Dict, voice_pattern: Dict, rules: Dict) -> str:
        """Write Twitter-optimized content (concise, punchy, engagement-focused)"""
        
        business_name = business_config.get('business_name', '')
        hook = idea.get('hook', '')
        
        # Twitter structure: Punchy hook → Quick value → Engagement CTA
        if business_name == 'BGK Goalkeeping':
            return f"{hook} Build goalkeeper confidence with evidence-based training. Join #BGKUNION! ⚽"
        elif business_name == '360TFT':
            return f"{hook} Join 1,200+ coaches who stopped guessing. Game-based training that works! 🚀"
        elif business_name == 'Kit-Mart':
            return f"{hook} Professional kit for grassroots teams. Quality that shows! 👕⚽"
        elif business_name == 'CD Copland Motors':
            return f"{hook} Honest garage, quality service. Monifieth's trusted choice! 🔧"
        elif business_name == 'KF Barbers':
            return f"{hook} 4.9⭐ Arbroath's premier barbers. Walk-ins welcome! ✂️"
        elif business_name == 'Athlete Recovery Zone':
            return f"{hook} Pro recovery tech for all athletes. Recover faster! 💪"
        
        return f"{hook} Quality that speaks for itself! ✨"

if __name__ == "__main__":
    writer = EngagingContentWriter()
    
    # Test content generation
    sample_idea = {
        'type': 'Educational',
        'hook': 'Why do 70% of young goalkeepers quit by age 14?',
        'value_proposition': 'Evidence-based confidence building',
        'topic': 'Confidence Crisis in Young Goalkeepers'
    }
    
    sample_config = {
        'business_name': 'BGK Goalkeeping'
    }
    
    for platform in ['Facebook', 'Instagram', 'LinkedIn', 'Twitter']:
        result = writer.write_engaging_content(sample_idea, sample_config, platform)
        print(f"\n{platform}:")
        print(f"Content: {result['content']}")
        print(f"Characters: {result['character_count']} (Optimal: {result['optimal_range']})")
        print(f"Within Range: {result['within_optimal']}")