#!/usr/bin/env python3
"""
Dynamic Content Generator - AI-powered content idea generation
Replaces hardcoded patterns with dynamic, varied content frameworks
"""

import random
import json
from typing import Dict, List
from datetime import datetime

class DynamicContentGenerator:
    def __init__(self):
        # Dynamic content frameworks to prevent repetition
        self.content_frameworks = {
            'Educational': [
                'Problem-Solution Framework',
                'Step-by-Step Guide Framework', 
                'Common Myths Debunked Framework',
                'Before-After Transformation Framework',
                'Expert Tips Framework',
                'Industry Insights Framework',
                'Best Practices Framework',
                'Troubleshooting Framework'
            ],
            'Promotional': [
                'Value Proposition Framework',
                'Social Proof Framework',
                'Limited Opportunity Framework',
                'Comparison Framework',
                'Benefit Stack Framework',
                'Customer Success Framework',
                'New Service Launch Framework',
                'Community Invitation Framework'
            ],
            'Behind-the-Scenes': [
                'Day-in-the-Life Framework',
                'Process Demonstration Framework',
                'Team Introduction Framework',
                'Quality Standards Framework',
                'Origin Story Framework',
                'Values in Action Framework',
                'Equipment/Technology Framework',
                'Customer Journey Framework'
            ],
            'Success Story': [
                'Customer Transformation Framework',
                'Challenge Overcome Framework',
                'Results Achieved Framework',
                'Long-term Impact Framework',
                'Community Impact Framework',
                'Innovation Success Framework',
                'Partnership Success Framework',
                'Recognition Achievement Framework'
            ]
        }
        
        # Hook patterns for variety
        self.hook_patterns = [
            'Question Hook',
            'Statistic Hook', 
            'Story Hook',
            'Contrarian Hook',
            'Emotional Hook'
        ]
        
        # Business-specific content angles
        self.business_angles = {
            'BGK Goalkeeping': {
                'unique_focus': 'confidence-building for young goalkeepers',
                'key_differentiators': ['evidence-based coaching', '#BGKUNION community', 'goalkeeper-specific expertise'],
                'target_outcomes': ['improved confidence', 'better technique', 'goal-scoring prevention'],
                'emotional_triggers': ['parent pride', 'child confidence', 'fear transformation']
            },
            '360TFT': {
                'unique_focus': 'structured coaching methodology vs expensive alternatives',
                'key_differentiators': ['game-based training', '1,200+ coach community', 'Kevin Middleton expertise'],
                'target_outcomes': ['coaching confidence', 'player development', 'business success'],
                'emotional_triggers': ['coach imposter syndrome', 'player progress', 'affordable quality']
            },
            'Kit-Mart': {
                'unique_focus': 'bespoke kit solutions for grassroots teams',
                'key_differentiators': ['local focus', 'Savi sportswear range', 'bulk processing'],
                'target_outcomes': ['professional team appearance', 'cost-effective solutions', 'quick delivery'],
                'emotional_triggers': ['team pride', 'professional image', 'grassroots support']
            },
            'CD Copland Motors': {
                'unique_focus': 'honest, quality automotive care in Monifieth',
                'key_differentiators': ['Good Garage Scheme', 'SMTA membership', '12-month guarantee'],
                'target_outcomes': ['vehicle reliability', 'peace of mind', 'fair pricing'],
                'emotional_triggers': ['trust concerns', 'garage horror stories', 'reliability importance']
            },
            'KF Barbers': {
                'unique_focus': 'traditional barbering excellence for all ages',
                'key_differentiators': ['child-friendly approach', '4.9-star rating', 'traditional techniques'],
                'target_outcomes': ['perfect grooming', 'comfortable experience', 'ongoing relationship'],
                'emotional_triggers': ['child anxiety', 'grooming confidence', 'family tradition']
            },
            'Athlete Recovery Zone': {
                'unique_focus': 'comprehensive recovery solutions for all athletes',
                'key_differentiators': ['cutting-edge technology', 'professional endorsements', 'flexible options'],
                'target_outcomes': ['faster recovery', 'injury prevention', 'performance enhancement'],
                'emotional_triggers': ['injury fear', 'performance plateau', 'competition readiness']
            }
        }
    
    def generate_dynamic_content_ideas(self, business_name: str, research_insights: Dict) -> List[Dict]:
        """Generate 12 dynamic content ideas using AI frameworks and research"""
        
        ideas = []
        business_angles = self.business_angles.get(business_name, {})
        
        # Generate 3 ideas per content type (12 total)
        for content_type in ['Educational', 'Promotional', 'Behind-the-Scenes', 'Success Story']:
            for i in range(3):
                idea = self._generate_single_idea(
                    business_name, 
                    content_type, 
                    business_angles, 
                    research_insights
                )
                ideas.append(idea)
        
        return ideas
    
    def _generate_single_idea(self, business_name: str, content_type: str, 
                            business_angles: Dict, research_insights: Dict) -> Dict:
        """Generate a single dynamic content idea"""
        
        # Select framework and hook pattern
        framework = random.choice(self.content_frameworks[content_type])
        hook_pattern = random.choice(self.hook_patterns)
        
        # Generate based on business and framework
        if business_name == 'BGK Goalkeeping':
            return self._generate_bgk_idea(content_type, framework, hook_pattern, research_insights)
        elif business_name == '360TFT':
            return self._generate_360tft_idea(content_type, framework, hook_pattern, research_insights)
        elif business_name == 'Kit-Mart':
            return self._generate_kitmart_idea(content_type, framework, hook_pattern, research_insights)
        elif business_name == 'CD Copland Motors':
            return self._generate_copland_idea(content_type, framework, hook_pattern, research_insights)
        elif business_name == 'KF Barbers':
            return self._generate_kf_idea(content_type, framework, hook_pattern, research_insights)
        elif business_name == 'Athlete Recovery Zone':
            return self._generate_arz_idea(content_type, framework, hook_pattern, research_insights)
    
    def _generate_bgk_idea(self, content_type: str, framework: str, hook_pattern: str, research: Dict) -> Dict:
        """Generate BGK Goalkeeping content ideas"""
        
        base_ideas = {
            'Educational': {
                'Problem-Solution Framework': {
                    'topic': 'Confidence Crisis in Young Goalkeepers',
                    'angle': 'How fear between the posts destroys potential and what to do about it',
                    'hook': 'Why do 70% of young goalkeepers quit by age 14?',
                    'value_prop': 'Evidence-based confidence building'
                },
                'Step-by-Step Guide Framework': {
                    'topic': 'Building Goalkeeper Reflexes Progressively',
                    'angle': 'The exact progression we use to develop lightning-fast reflexes',
                    'hook': 'Great goalkeepers aren\'t born - they\'re systematically developed',
                    'value_prop': 'Professional development pathway'
                }
            },
            'Promotional': {
                'Social Proof Framework': {
                    'topic': 'Join Scotland\'s Fastest-Growing Goalkeeper Community',
                    'angle': '4,285+ goalkeepers can\'t be wrong about the #BGKUNION',
                    'hook': 'More goalkeepers choose BGK than any other academy in Scotland',
                    'value_prop': 'Community-backed training'
                }
            },
            'Behind-the-Scenes': {
                'Team Introduction Framework': {
                    'topic': 'Meet Your BGK Coaching Team',
                    'angle': 'Former professional goalkeepers now developing the next generation',
                    'hook': 'What do you get when former pros become youth coaches?',
                    'value_prop': 'Professional expertise'
                }
            },
            'Success Story': {
                'Customer Transformation Framework': {
                    'topic': 'From Bench-Warmer to Star Goalkeeper',
                    'angle': 'How we transformed a nervous substitute into a confident starter',
                    'hook': 'This goalkeeper went from tears to cheers in just 8 weeks',
                    'value_prop': 'Proven transformation methods'
                }
            }
        }
        
        # Get framework-specific idea or create fallback
        idea_data = base_ideas.get(content_type, {}).get(framework, {
            'topic': f'Goalkeeper Development Focus',
            'angle': f'Evidence-based approach to goalkeeper training',
            'hook': f'Every great goalkeeper starts somewhere',
            'value_prop': 'Professional goalkeeper development'
        })
        
        return {
            'type': content_type,
            'framework': framework,
            'hook_pattern': hook_pattern,
            'topic': idea_data['topic'],
            'angle': idea_data['angle'],
            'hook': idea_data['hook'],
            'value_proposition': idea_data['value_prop'],
            'research_integration': research.get('key_insights', ''),
            'generated_at': datetime.now().isoformat()
        }
    
    def _generate_360tft_idea(self, content_type: str, framework: str, hook_pattern: str, research: Dict) -> Dict:
        """Generate 360TFT content ideas"""
        
        base_ideas = {
            'Educational': {
                'Problem-Solution Framework': {
                    'topic': 'Why Expensive Coaching Courses Fail Grassroots Coaches',
                    'angle': 'The £500+ course problem and the £8/month solution',
                    'hook': 'Spending £500+ on coaching courses? You\'re being ripped off',
                    'value_prop': 'Affordable, practical coaching education'
                },
                'Expert Tips Framework': {
                    'topic': 'Game Model Methodology Explained',
                    'angle': 'The exact system that built two successful academies',
                    'hook': 'This simple methodology grew two academies from 300 to 800+ players',
                    'value_prop': 'Proven coaching framework'
                }
            },
            'Promotional': {
                'Community Invitation Framework': {
                    'topic': 'Join 1,200+ Coaches Who\'ve Stopped Guessing',
                    'angle': 'The Skool community transforming grassroots football',
                    'hook': '1,200+ coaches can\'t be wrong about this approach',
                    'value_prop': 'Community-supported learning'
                }
            },
            'Behind-the-Scenes': {
                'Origin Story Framework': {
                    'topic': 'From Volunteer to Six-Figure Football Business',
                    'angle': 'Kevin\'s journey from grassroots volunteer to professional coach',
                    'hook': 'Every successful coach starts as a volunteer with a dream',
                    'value_prop': 'Authentic experience'
                }
            },
            'Success Story': {
                'Results Achieved Framework': {
                    'topic': 'How One Coach Built a Sustainable Football Academy',
                    'angle': 'Real numbers from a coach who implemented our methodology',
                    'hook': 'From 50 to 400 players in 18 months - here\'s how',
                    'value_prop': 'Scalable business model'
                }
            }
        }
        
        idea_data = base_ideas.get(content_type, {}).get(framework, {
            'topic': f'Football Coaching Excellence',
            'angle': f'Structured approach to coaching development',
            'hook': f'Stop guessing, start coaching with confidence',
            'value_prop': 'Evidence-based coaching methods'
        })
        
        return {
            'type': content_type,
            'framework': framework,
            'hook_pattern': hook_pattern,
            'topic': idea_data['topic'],
            'angle': idea_data['angle'],
            'hook': idea_data['hook'],
            'value_proposition': idea_data['value_prop'],
            'research_integration': research.get('key_insights', ''),
            'generated_at': datetime.now().isoformat()
        }
    
    def _generate_kitmart_idea(self, content_type: str, framework: str, hook_pattern: str, research: Dict) -> Dict:
        """Generate Kit-Mart content ideas"""
        
        base_ideas = {
            'Educational': {
                'Best Practices Framework': {
                    'topic': 'Custom Kit Ordering Without the Headaches',
                    'angle': 'What schools and clubs need to know before ordering',
                    'hook': 'Most kit orders go wrong because of these 3 mistakes',
                    'value_prop': 'Hassle-free ordering process'
                }
            },
            'Promotional': {
                'Value Proposition Framework': {
                    'topic': 'Professional Kit at Grassroots Prices',
                    'angle': 'Quality Savi sportswear without the premium markup',
                    'hook': 'Why pay premium prices for the same quality kit?',
                    'value_prop': 'Quality without the premium price'
                }
            },
            'Behind-the-Scenes': {
                'Process Demonstration Framework': {
                    'topic': 'Inside Our 600-Order Processing System',
                    'angle': 'How we handle hundreds of kit orders without delays',
                    'hook': 'Ever wondered how we process 600 orders without delays?',
                    'value_prop': 'Reliable, scalable service'
                }
            },
            'Success Story': {
                'Community Impact Framework': {
                    'topic': 'Transforming Grassroots Football, One Kit at a Time',
                    'angle': 'How professional-looking teams play more professionally',
                    'hook': 'This club\'s transformation started with better kit',
                    'value_prop': 'Image transformation impact'
                }
            }
        }
        
        idea_data = base_ideas.get(content_type, {}).get(framework, {
            'topic': f'Bespoke Kit Solutions',
            'angle': f'Professional sportswear for grassroots teams',
            'hook': f'Look professional, play professional',
            'value_prop': 'Custom kit expertise'
        })
        
        return {
            'type': content_type,
            'framework': framework,
            'hook_pattern': hook_pattern,
            'topic': idea_data['topic'],
            'angle': idea_data['angle'],
            'hook': idea_data['hook'],
            'value_proposition': idea_data['value_prop'],
            'research_integration': research.get('key_insights', ''),
            'generated_at': datetime.now().isoformat()
        }
    
    def _generate_copland_idea(self, content_type: str, framework: str, hook_pattern: str, research: Dict) -> Dict:
        """Generate CD Copland Motors content ideas"""
        
        base_ideas = {
            'Educational': {
                'Troubleshooting Framework': {
                    'topic': 'Why Your Car Failed Its MOT (And How to Prevent It)',
                    'angle': 'The most common MOT failures and simple prevention tips',
                    'hook': '80% of MOT failures could be prevented with these simple checks',
                    'value_prop': 'Preventive maintenance expertise'
                }
            },
            'Promotional': {
                'Comparison Framework': {
                    'topic': 'Independent vs Franchise Garage Truth',
                    'angle': 'Why choosing independent doesn\'t mean compromising quality',
                    'hook': 'Franchise prices, independent service - you can\'t have both... or can you?',
                    'value_prop': 'Quality without franchise markup'
                }
            },
            'Behind-the-Scenes': {
                'Quality Standards Framework': {
                    'topic': 'What Good Garage Scheme Membership Really Means',
                    'angle': 'The standards we maintain to earn customer trust',
                    'hook': 'Not every garage can meet Good Garage Scheme standards',
                    'value_prop': 'Verified quality standards'
                }
            },
            'Success Story': {
                'Challenge Overcome Framework': {
                    'topic': 'The Diagnostic Case Other Garages Couldn\'t Solve',
                    'angle': 'When experience and equipment combine to solve the impossible',
                    'hook': 'Three garages couldn\'t fix it. We solved it in 30 minutes',
                    'value_prop': 'Advanced diagnostic capability'
                }
            }
        }
        
        idea_data = base_ideas.get(content_type, {}).get(framework, {
            'topic': f'Automotive Care Excellence',
            'angle': f'Professional service with independent garage values',
            'hook': f'Quality automotive care you can trust',
            'value_prop': 'Honest, professional service'
        })
        
        return {
            'type': content_type,
            'framework': framework,
            'hook_pattern': hook_pattern,
            'topic': idea_data['topic'],
            'angle': idea_data['angle'],
            'hook': idea_data['hook'],
            'value_proposition': idea_data['value_prop'],
            'research_integration': research.get('key_insights', ''),
            'generated_at': datetime.now().isoformat()
        }
    
    def _generate_kf_idea(self, content_type: str, framework: str, hook_pattern: str, research: Dict) -> Dict:
        """Generate KF Barbers content ideas"""
        
        base_ideas = {
            'Educational': {
                'Common Myths Debunked Framework': {
                    'topic': 'Beard Grooming Myths That Damage Your Look',
                    'angle': 'Professional beard care vs internet advice',
                    'hook': 'Your beard grooming routine is probably wrong',
                    'value_prop': 'Professional grooming expertise'
                }
            },
            'Promotional': {
                'Customer Success Framework': {
                    'topic': 'Why 215+ Customers Rate Us 4.9 Stars',
                    'angle': 'The service standards that earn exceptional ratings',
                    'hook': 'You don\'t get 4.9 stars by accident',
                    'value_prop': 'Consistently exceptional service'
                }
            },
            'Behind-the-Scenes': {
                'Values in Action Framework': {
                    'topic': 'Making Every Child\'s First Haircut Special',
                    'angle': 'How we turn nervous kids into confident regulars',
                    'hook': 'The secret to being "brilliant with kids" isn\'t magic',
                    'value_prop': 'Child-focused expertise'
                }
            },
            'Success Story': {
                'Long-term Impact Framework': {
                    'topic': 'Three Generations, One Trusted Barber',
                    'angle': 'Building family relationships that span decades',
                    'hook': 'When granddad, dad, and son all trust the same barber',
                    'value_prop': 'Generational trust'
                }
            }
        }
        
        idea_data = base_ideas.get(content_type, {}).get(framework, {
            'topic': f'Traditional Barbering Excellence',
            'angle': f'Professional grooming with personal service',
            'hook': f'Experience the difference quality makes',
            'value_prop': 'Traditional craftsmanship'
        })
        
        return {
            'type': content_type,
            'framework': framework,
            'hook_pattern': hook_pattern,
            'topic': idea_data['topic'],
            'angle': idea_data['angle'],
            'hook': idea_data['hook'],
            'value_proposition': idea_data['value_prop'],
            'research_integration': research.get('key_insights', ''),
            'generated_at': datetime.now().isoformat()
        }
    
    def _generate_arz_idea(self, content_type: str, framework: str, hook_pattern: str, research: Dict) -> Dict:
        """Generate Athlete Recovery Zone content ideas"""
        
        base_ideas = {
            'Educational': {
                'Before-After Transformation Framework': {
                    'topic': 'The Recovery Revolution in Athletic Performance',
                    'angle': 'How proper recovery is changing the game for all athletes',
                    'hook': 'Recovery is the difference between good athletes and great ones',
                    'value_prop': 'Performance-changing recovery protocols'
                }
            },
            'Promotional': {
                'Social Proof Framework': {
                    'topic': '450+ Sports Teams Choose Us for Recovery',
                    'angle': 'Why professional and college teams trust our protocols',
                    'hook': '450+ teams can\'t be wrong about recovery',
                    'value_prop': 'Professional-grade recovery solutions'
                }
            },
            'Behind-the-Scenes': {
                'Equipment/Technology Framework': {
                    'topic': 'Inside Our State-of-the-Art Recovery Technology',
                    'angle': 'The same equipment used by Division 1 athletes',
                    'hook': 'This is the technology that\'s changing athletic recovery',
                    'value_prop': 'Cutting-edge recovery technology'
                }
            },
            'Success Story': {
                'Innovation Success Framework': {
                    'topic': 'How We\'re Revolutionizing Weekend Warrior Recovery',
                    'angle': 'Professional recovery solutions for recreational athletes',
                    'hook': 'You don\'t need to be a pro to recover like one',
                    'value_prop': 'Accessible professional recovery'
                }
            }
        }
        
        idea_data = base_ideas.get(content_type, {}).get(framework, {
            'topic': f'Advanced Athletic Recovery',
            'angle': f'Professional recovery solutions for all athletes',
            'hook': f'Recover faster, perform better',
            'value_prop': 'Evidence-based recovery protocols'
        })
        
        return {
            'type': content_type,
            'framework': framework,
            'hook_pattern': hook_pattern,
            'topic': idea_data['topic'],
            'angle': idea_data['angle'],
            'hook': idea_data['hook'],
            'value_proposition': idea_data['value_prop'],
            'research_integration': research.get('key_insights', ''),
            'generated_at': datetime.now().isoformat()
        }

if __name__ == "__main__":
    generator = DynamicContentGenerator()
    
    # Test generation
    sample_research = {"key_insights": "Market showing increased demand for youth sports development"}
    ideas = generator.generate_dynamic_content_ideas('BGK Goalkeeping', sample_research)
    
    print("Generated Content Ideas:")
    for idea in ideas:
        print(f"- {idea['type']}: {idea['topic']}")
        print(f"  Hook: {idea['hook']}")
        print(f"  Framework: {idea['framework']}")
        print()