#!/usr/bin/env python3
"""
Platform-Specific Content Optimizer
===================================

Advanced platform optimization system that:
1. Tailors content for each social media platform's algorithm and audience
2. Optimizes content length, format, and engagement features
3. Adds platform-specific elements (hashtags, mentions, formatting)
4. Ensures compliance with platform best practices
5. Maximizes engagement potential for each platform

Author: Claude Code
Version: 2.0
"""

import re
import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from engaging_content_writer import ContentPiece

@dataclass
class PlatformContent:
    """Platform-optimized content with metadata"""
    platform: str
    content: str
    optimal_length: int
    hashtags: str
    mentions: str
    posting_tips: List[str]
    engagement_features: List[str]
    best_posting_times: List[str]
    content_format: str

class PlatformOptimizer:
    """AI-powered platform-specific content optimization"""
    
    def __init__(self):
        # Platform specifications and requirements
        self.platform_specs = {
            'Facebook': {
                'character_limits': {
                    'post': 63206,
                    'optimal': 100-250,
                    'headline': 25,
                    'description': 30
                },
                'content_features': {
                    'supports_hashtags': True,
                    'hashtag_limit': 30,
                    'optimal_hashtags': 3-5,
                    'supports_mentions': True,
                    'supports_links': True,
                    'supports_images': True,
                    'supports_video': True
                },
                'algorithm_preferences': {
                    'engagement_types': ['comments', 'shares', 'reactions'],
                    'content_types': ['storytelling', 'community_questions', 'local_content'],
                    'posting_frequency': '1-2 times daily',
                    'peak_times': ['12-15:00', '19-21:00']
                },
                'tone': 'conversational',
                'formatting': {
                    'line_breaks': True,
                    'emojis': 'moderate',
                    'capitalization': 'sentence_case'
                }
            },
            
            'Instagram': {
                'character_limits': {
                    'post': 2200,
                    'optimal': 138-150,
                    'story': 2200,
                    'bio': 150
                },
                'content_features': {
                    'supports_hashtags': True,
                    'hashtag_limit': 30,
                    'optimal_hashtags': 20-30,
                    'supports_mentions': True,
                    'supports_links': False,  # Only in bio/stories
                    'supports_images': True,
                    'supports_video': True
                },
                'algorithm_preferences': {
                    'engagement_types': ['likes', 'comments', 'shares', 'saves'],
                    'content_types': ['visual_storytelling', 'behind_scenes', 'user_generated'],
                    'posting_frequency': '1-3 times daily',
                    'peak_times': ['11-13:00', '17-19:00']
                },
                'tone': 'visual_focused',
                'formatting': {
                    'line_breaks': True,
                    'emojis': 'heavy',
                    'capitalization': 'sentence_case'
                }
            },
            
            'LinkedIn': {
                'character_limits': {
                    'post': 3000,
                    'optimal': 150-300,
                    'headline': 120,
                    'article': 125000
                },
                'content_features': {
                    'supports_hashtags': True,
                    'hashtag_limit': 30,
                    'optimal_hashtags': 3-10,
                    'supports_mentions': True,
                    'supports_links': True,
                    'supports_images': True,
                    'supports_video': True
                },
                'algorithm_preferences': {
                    'engagement_types': ['comments', 'shares', 'reactions'],
                    'content_types': ['thought_leadership', 'industry_insights', 'professional_stories'],
                    'posting_frequency': '1 time daily max',
                    'peak_times': ['08-10:00', '12-14:00', '17-18:00']
                },
                'tone': 'professional',
                'formatting': {
                    'line_breaks': True,
                    'emojis': 'minimal',
                    'capitalization': 'title_case_headers'
                }
            },
            
            'Twitter': {
                'character_limits': {
                    'post': 280,
                    'optimal': 71-100,
                    'thread': 280,  # per tweet
                    'bio': 160
                },
                'content_features': {
                    'supports_hashtags': True,
                    'hashtag_limit': 280,  # within character limit
                    'optimal_hashtags': 1-2,
                    'supports_mentions': True,
                    'supports_links': True,
                    'supports_images': True,
                    'supports_video': True
                },
                'algorithm_preferences': {
                    'engagement_types': ['retweets', 'likes', 'comments', 'clicks'],
                    'content_types': ['quick_tips', 'trending_topics', 'real_time'],
                    'posting_frequency': '3-5 times daily',
                    'peak_times': ['09:00', '12:00', '15:00', '18:00']
                },
                'tone': 'concise',
                'formatting': {
                    'line_breaks': False,
                    'emojis': 'moderate',
                    'capitalization': 'sentence_case'
                }
            },
            
            'YouTube': {
                'character_limits': {
                    'title': 100,
                    'description': 5000,
                    'optimal_title': 60,
                    'optimal_description': 125
                },
                'content_features': {
                    'supports_hashtags': True,
                    'hashtag_limit': 15,
                    'optimal_hashtags': 10-15,
                    'supports_mentions': True,
                    'supports_links': True,
                    'supports_images': True,
                    'supports_video': True
                },
                'algorithm_preferences': {
                    'engagement_types': ['watch_time', 'likes', 'comments', 'subscribes'],
                    'content_types': ['educational', 'entertainment', 'tutorials'],
                    'posting_frequency': '1-3 times weekly',
                    'peak_times': ['14-16:00', '20-22:00']
                },
                'tone': 'educational',
                'formatting': {
                    'line_breaks': True,
                    'emojis': 'minimal',
                    'capitalization': 'title_case'
                }
            }
        }
        
        # Business-specific platform strategies
        self.business_platform_strategies = {
            'BGK Goalkeeping': {
                'Facebook': {
                    'focus': 'parent_community',
                    'content_angles': ['confidence_building', 'parent_education', 'success_stories'],
                    'engagement_tactics': ['parent_questions', 'training_tips', 'community_highlights']
                },
                'Instagram': {
                    'focus': 'visual_training',
                    'content_angles': ['training_moments', 'technique_videos', 'community_spirit'],
                    'engagement_tactics': ['training_clips', 'before_after', 'goalkeeper_spotlight']
                },
                'LinkedIn': {
                    'focus': 'coaching_expertise',
                    'content_angles': ['youth_sports_insights', 'coaching_methodology', 'industry_trends'],
                    'engagement_tactics': ['professional_insights', 'coaching_education', 'sports_psychology']
                },
                'Twitter': {
                    'focus': 'quick_tips',
                    'content_angles': ['training_tips', 'confidence_quotes', 'community_updates'],
                    'engagement_tactics': ['tip_threads', 'motivational_quotes', 'live_updates']
                }
            },
            
            '360TFT': {
                'Facebook': {
                    'focus': 'coach_community',
                    'content_angles': ['coaching_education', 'session_planning', 'coach_development'],
                    'engagement_tactics': ['coach_questions', 'session_ideas', 'community_discussions']
                },
                'Instagram': {
                    'focus': 'training_visuals',
                    'content_angles': ['session_highlights', 'coaching_moments', 'player_development'],
                    'engagement_tactics': ['training_videos', 'coach_stories', 'session_breakdowns']
                },
                'LinkedIn': {
                    'focus': 'professional_development',
                    'content_angles': ['coaching_business', 'education_insights', 'industry_leadership'],
                    'engagement_tactics': ['thought_leadership', 'business_advice', 'industry_analysis']
                },
                'Twitter': {
                    'focus': 'coaching_tips',
                    'content_angles': ['quick_session_ideas', 'coaching_quotes', 'community_growth'],
                    'engagement_tactics': ['tip_threads', 'session_snippets', 'coach_chats']
                }
            },
            
            'Kit-Mart': {
                'Facebook': {
                    'focus': 'team_community',
                    'content_angles': ['team_identity', 'kit_showcases', 'club_partnerships'],
                    'engagement_tactics': ['team_features', 'kit_reveals', 'community_support']
                },
                'Instagram': {
                    'focus': 'visual_products',
                    'content_angles': ['kit_designs', 'team_photos', 'production_process'],
                    'engagement_tactics': ['kit_galleries', 'team_showcases', 'behind_production']
                },
                'LinkedIn': {
                    'focus': 'business_partnerships',
                    'content_angles': ['supply_chain', 'business_solutions', 'partnership_success'],
                    'engagement_tactics': ['case_studies', 'business_insights', 'partnership_highlights']
                },
                'Twitter': {
                    'focus': 'quick_updates',
                    'content_angles': ['kit_news', 'team_updates', 'industry_trends'],
                    'engagement_tactics': ['kit_reveals', 'team_news', 'trend_commentary']
                }
            },
            
            'CD Copland Motors': {
                'Facebook': {
                    'focus': 'local_community',
                    'content_angles': ['automotive_education', 'local_service', 'customer_care'],
                    'engagement_tactics': ['maintenance_tips', 'local_focus', 'customer_stories']
                },
                'Instagram': {
                    'focus': 'workshop_life',
                    'content_angles': ['garage_work', 'team_expertise', 'quality_service'],
                    'engagement_tactics': ['workshop_photos', 'team_highlights', 'service_moments']
                },
                'LinkedIn': {
                    'focus': 'professional_service',
                    'content_angles': ['automotive_expertise', 'business_values', 'industry_insights'],
                    'engagement_tactics': ['professional_insights', 'service_excellence', 'industry_trends']
                },
                'Twitter': {
                    'focus': 'quick_tips',
                    'content_angles': ['car_maintenance', 'service_updates', 'automotive_news'],
                    'engagement_tactics': ['maintenance_tips', 'service_alerts', 'automotive_chat']
                }
            },
            
            'KF Barbers': {
                'Facebook': {
                    'focus': 'family_community',
                    'content_angles': ['family_service', 'traditional_craft', 'local_pride'],
                    'engagement_tactics': ['family_stories', 'traditional_techniques', 'community_connection']
                },
                'Instagram': {
                    'focus': 'craft_showcase',
                    'content_angles': ['barbering_art', 'transformation_photos', 'shop_atmosphere'],
                    'engagement_tactics': ['cut_videos', 'before_after', 'shop_life']
                },
                'LinkedIn': {
                    'focus': 'business_craft',
                    'content_angles': ['traditional_skills', 'service_excellence', 'local_business'],
                    'engagement_tactics': ['craft_expertise', 'business_insights', 'service_standards']
                },
                'Twitter': {
                    'focus': 'grooming_tips',
                    'content_angles': ['grooming_advice', 'style_tips', 'shop_updates'],
                    'engagement_tactics': ['grooming_tips', 'style_advice', 'quick_updates']
                }
            },
            
            'Athlete Recovery Zone': {
                'Facebook': {
                    'focus': 'athlete_community',
                    'content_angles': ['recovery_education', 'athlete_stories', 'performance_insights'],
                    'engagement_tactics': ['recovery_tips', 'athlete_features', 'education_posts']
                },
                'Instagram': {
                    'focus': 'recovery_visuals',
                    'content_angles': ['technology_showcase', 'athlete_sessions', 'facility_tours'],
                    'engagement_tactics': ['technology_videos', 'session_photos', 'facility_highlights']
                },
                'LinkedIn': {
                    'focus': 'sports_science',
                    'content_angles': ['recovery_research', 'performance_optimization', 'sports_medicine'],
                    'engagement_tactics': ['research_insights', 'performance_data', 'industry_leadership']
                },
                'Twitter': {
                    'focus': 'recovery_tips',
                    'content_angles': ['quick_recovery_tips', 'sports_science', 'athlete_updates'],
                    'engagement_tactics': ['tip_threads', 'science_facts', 'athlete_chat']
                }
            }
        }

    def optimize_for_platforms(self, content_piece: ContentPiece, business_name: str, 
                             target_platforms: List[str] = None) -> Dict[str, PlatformContent]:
        """Optimize content for specific platforms"""
        
        if target_platforms is None:
            target_platforms = ['Facebook', 'Instagram', 'LinkedIn', 'Twitter']
        
        optimized_content = {}
        
        for platform in target_platforms:
            if platform not in self.platform_specs:
                continue
            
            platform_content = self._optimize_for_platform(
                content_piece, business_name, platform
            )
            optimized_content[platform] = platform_content
        
        return optimized_content

    def _optimize_for_platform(self, content_piece: ContentPiece, business_name: str, 
                             platform: str) -> PlatformContent:
        """Optimize content for a specific platform"""
        
        platform_spec = self.platform_specs[platform]
        business_strategy = self.business_platform_strategies.get(business_name, {}).get(platform, {})
        
        # Start with base content
        base_content = content_piece.shortform_content
        
        # Apply platform-specific optimization
        optimized_content = self._apply_length_optimization(base_content, platform_spec)
        optimized_content = self._apply_tone_optimization(optimized_content, platform_spec, business_strategy)
        optimized_content = self._apply_formatting_optimization(optimized_content, platform_spec)
        optimized_content = self._apply_engagement_optimization(optimized_content, platform_spec, business_strategy)
        
        # Generate platform-specific hashtags
        platform_hashtags = self._generate_platform_hashtags(
            content_piece, business_name, platform, platform_spec
        )
        
        # Generate mentions
        platform_mentions = self._generate_platform_mentions(business_name, platform)
        
        # Generate posting tips
        posting_tips = self._generate_posting_tips(platform_spec, business_strategy)
        
        # Identify engagement features
        engagement_features = self._identify_engagement_features(platform_spec, business_strategy)
        
        # Get best posting times
        best_times = platform_spec['algorithm_preferences']['peak_times']
        
        # Determine content format
        content_format = self._determine_content_format(platform, content_piece.content_metadata)
        
        return PlatformContent(
            platform=platform,
            content=optimized_content,
            optimal_length=platform_spec['character_limits']['optimal'],
            hashtags=platform_hashtags,
            mentions=platform_mentions,
            posting_tips=posting_tips,
            engagement_features=engagement_features,
            best_posting_times=best_times,
            content_format=content_format
        )

    def _apply_length_optimization(self, content: str, platform_spec: Dict) -> str:
        """Optimize content length for platform"""
        
        optimal_length = platform_spec['character_limits']['optimal']
        
        if isinstance(optimal_length, int):
            max_length = optimal_length
        else:
            # Handle range like "100-250"
            if '-' in str(optimal_length):
                max_length = int(str(optimal_length).split('-')[1])
            else:
                max_length = int(optimal_length)
        
        if len(content) <= max_length:
            return content
        
        # Trim content intelligently
        sentences = content.split('. ')
        trimmed_content = sentences[0]  # Start with first sentence
        
        # Add sentences until we approach the limit
        for sentence in sentences[1:]:
            test_content = trimmed_content + '. ' + sentence
            if len(test_content) <= max_length - 20:  # Leave room for CTA
                trimmed_content = test_content
            else:
                break
        
        # Ensure it ends properly
        if not trimmed_content.endswith('.') and not trimmed_content.endswith('!') and not trimmed_content.endswith('?'):
            trimmed_content += '.'
        
        return trimmed_content

    def _apply_tone_optimization(self, content: str, platform_spec: Dict, business_strategy: Dict) -> str:
        """Apply platform-appropriate tone"""
        
        platform_tone = platform_spec['tone']
        
        if platform_tone == 'professional':
            # Make more professional
            content = content.replace(' great ', ' excellent ')
            content = content.replace(' amazing ', ' outstanding ')
            content = content.replace('!', '.')
            
        elif platform_tone == 'conversational':
            # Make more conversational
            if business_strategy.get('focus') == 'parent_community':
                content = self._add_parent_friendly_language(content)
            elif business_strategy.get('focus') == 'coach_community':
                content = self._add_coach_friendly_language(content)
            
        elif platform_tone == 'visual_focused':
            # Optimize for visual platforms
            content = self._add_visual_cues(content)
            
        elif platform_tone == 'concise':
            # Make more concise
            content = self._make_more_concise(content)
        
        return content

    def _apply_formatting_optimization(self, content: str, platform_spec: Dict) -> str:
        """Apply platform-specific formatting"""
        
        formatting = platform_spec['formatting']
        
        # Handle line breaks
        if formatting['line_breaks']:
            # Add line breaks for readability
            content = self._add_strategic_line_breaks(content)
        else:
            # Remove extra line breaks
            content = ' '.join(content.split())
        
        # Handle emojis
        emoji_level = formatting['emojis']
        if emoji_level == 'heavy':
            content = self._add_emojis(content, 'heavy')
        elif emoji_level == 'moderate':
            content = self._add_emojis(content, 'moderate')
        elif emoji_level == 'minimal':
            content = self._add_emojis(content, 'minimal')
        
        # Handle capitalization
        if formatting['capitalization'] == 'title_case_headers':
            content = self._apply_title_case_headers(content)
        
        return content

    def _apply_engagement_optimization(self, content: str, platform_spec: Dict, business_strategy: Dict) -> str:
        """Apply engagement-focused optimizations"""
        
        engagement_tactics = business_strategy.get('engagement_tactics', [])
        preferred_content_types = platform_spec['algorithm_preferences']['content_types']
        
        # Add engagement elements based on strategy
        if 'questions' in engagement_tactics and not content.endswith('?'):
            content = self._add_engagement_question(content, business_strategy)
        
        if 'community_focus' in engagement_tactics:
            content = self._add_community_elements(content)
        
        if 'local_relevance' in engagement_tactics:
            content = self._add_local_elements(content, business_strategy)
        
        return content

    def _generate_platform_hashtags(self, content_piece: ContentPiece, business_name: str, 
                                  platform: str, platform_spec: Dict) -> str:
        """Generate platform-optimized hashtags"""
        
        optimal_count = platform_spec['content_features']['optimal_hashtags']
        
        # Business-specific hashtag pools
        hashtag_pools = {
            'BGK Goalkeeping': {
                'core': ['#BGKGoalkeeping', '#BGKUNION'],
                'topical': ['#GoalkeeperTraining', '#YouthFootball', '#Confidence', '#Scotland'],
                'platform_specific': {
                    'Instagram': ['#GoalkeeperLife', '#YouthSports', '#TrainingDay', '#ConfidenceBuilding'],
                    'LinkedIn': ['#YouthSportsDevelopment', '#CoachingExcellence', '#SportsEducation'],
                    'Facebook': ['#LocalFootball', '#ParentSupport', '#YouthDevelopment'],
                    'Twitter': ['#Goalkeeping', '#YouthSports', '#Training']
                }
            },
            '360TFT': {
                'core': ['#360TFT', '#StopGuessing'],
                'topical': ['#FootballCoaching', '#CoachEducation', '#GameModel', '#CoachingCommunity'],
                'platform_specific': {
                    'Instagram': ['#CoachingLife', '#FootballTraining', '#CoachDevelopment'],
                    'LinkedIn': ['#CoachingEducation', '#ProfessionalDevelopment', '#FootballIndustry'],
                    'Facebook': ['#GrassrootsFootball', '#CoachSupport', '#FootballCommunity'],
                    'Twitter': ['#Coaching', '#Football', '#Education']
                }
            },
            'Kit-Mart': {
                'core': ['#KitMart', '#TeamKit'],
                'topical': ['#CustomKit', '#Football', '#SportswearUK', '#TeamIdentity'],
                'platform_specific': {
                    'Instagram': ['#TeamColors', '#KitDesign', '#FootballKit', '#TeamPride'],
                    'LinkedIn': ['#SportswearIndustry', '#TeamSolutions', '#CustomApparel'],
                    'Facebook': ['#LocalTeams', '#GrassrootsFootball', '#TeamSupport'],
                    'Twitter': ['#Football', '#TeamKit', '#Sports']
                }
            },
            'CD Copland Motors': {
                'core': ['#CDCoplandMotors', '#Monifieth'],
                'topical': ['#MOT', '#GoodGarageScheme', '#SMTA', '#TrustedGarage'],
                'platform_specific': {
                    'Instagram': ['#GarageLife', '#AutomotiveService', '#LocalBusiness'],
                    'LinkedIn': ['#AutomotiveIndustry', '#ServiceExcellence', '#LocalBusiness'],
                    'Facebook': ['#Dundee', '#LocalGarage', '#CarCare', '#AutomotiveService'],
                    'Twitter': ['#Automotive', '#MOT', '#CarCare']
                }
            },
            'KF Barbers': {
                'core': ['#KFBarbers', '#Arbroath'],
                'topical': ['#TraditionalBarber', '#MensGrooming', '#Barbershop', '#Scotland'],
                'platform_specific': {
                    'Instagram': ['#BarberLife', '#TraditionalCrafts', '#MensStyle', '#GroomingGoals'],
                    'LinkedIn': ['#TraditionalSkills', '#ServiceExcellence', '#LocalBusiness'],
                    'Facebook': ['#LocalBarber', '#FamilyBusiness', '#TraditionalService'],
                    'Twitter': ['#Barbering', '#MensGrooming', '#Traditional']
                }
            },
            'Athlete Recovery Zone': {
                'core': ['#AthleteRecoveryZone', '#SportsRecovery'],
                'topical': ['#Cryotherapy', '#AthletePerformance', '#NormaTec', '#RedLightTherapy'],
                'platform_specific': {
                    'Instagram': ['#RecoveryDay', '#AthleteLife', '#PerformanceRecovery', '#SportsScience'],
                    'LinkedIn': ['#SportsScience', '#AthletePerformance', '#RecoveryTechnology'],
                    'Facebook': ['#LocalAthletes', '#SportsWellness', '#RecoveryCenter'],
                    'Twitter': ['#Recovery', '#Sports', '#Performance']
                }
            }
        }
        
        business_hashtags = hashtag_pools.get(business_name, {})
        
        # Combine hashtags based on optimal count
        if isinstance(optimal_count, str) and '-' in optimal_count:
            # Handle range
            min_count, max_count = map(int, optimal_count.split('-'))
            target_count = random.randint(min_count, max_count)
        else:
            target_count = int(optimal_count) if isinstance(optimal_count, str) else optimal_count
        
        selected_hashtags = []
        
        # Always include core hashtags
        core_hashtags = business_hashtags.get('core', [])
        selected_hashtags.extend(core_hashtags)
        
        # Add platform-specific hashtags
        platform_hashtags = business_hashtags.get('platform_specific', {}).get(platform, [])
        selected_hashtags.extend(platform_hashtags[:max(0, target_count - len(selected_hashtags))])
        
        # Fill remaining with topical hashtags
        remaining_slots = target_count - len(selected_hashtags)
        if remaining_slots > 0:
            topical_hashtags = business_hashtags.get('topical', [])
            selected_hashtags.extend(topical_hashtags[:remaining_slots])
        
        return ' '.join(selected_hashtags[:target_count])

    def _generate_platform_mentions(self, business_name: str, platform: str) -> str:
        """Generate relevant mentions for platform"""
        
        # Business-specific mentions
        mentions = {
            'BGK Goalkeeping': {
                'Twitter': '@BGKGoalkeeping',
                'Instagram': '@bgkgoalkeeping',
                'Facebook': '@BGKGoalkeeping',
                'LinkedIn': 'BGK Goalkeeping'
            },
            '360TFT': {
                'Twitter': '@360TFT',
                'Instagram': '@360tft',
                'Facebook': '@360TFT',
                'LinkedIn': '360TFT'
            }
            # Add other businesses as needed
        }
        
        business_mentions = mentions.get(business_name, {})
        return business_mentions.get(platform, '')

    def _generate_posting_tips(self, platform_spec: Dict, business_strategy: Dict) -> List[str]:
        """Generate platform-specific posting tips"""
        
        tips = []
        
        # General platform tips
        posting_frequency = platform_spec['algorithm_preferences']['posting_frequency']
        tips.append(f"Optimal posting frequency: {posting_frequency}")
        
        peak_times = platform_spec['algorithm_preferences']['peak_times']
        tips.append(f"Best posting times: {', '.join(peak_times)}")
        
        preferred_engagement = platform_spec['algorithm_preferences']['engagement_types']
        tips.append(f"Focus on: {', '.join(preferred_engagement)}")
        
        # Business-specific tips
        if business_strategy.get('focus'):
            tips.append(f"Content focus: {business_strategy['focus'].replace('_', ' ')}")
        
        return tips

    def _identify_engagement_features(self, platform_spec: Dict, business_strategy: Dict) -> List[str]:
        """Identify available engagement features for platform"""
        
        features = []
        
        content_features = platform_spec['content_features']
        
        if content_features['supports_hashtags']:
            features.append('hashtags')
        
        if content_features['supports_mentions']:
            features.append('mentions')
        
        if content_features['supports_images']:
            features.append('images')
        
        if content_features['supports_video']:
            features.append('video')
        
        if content_features['supports_links']:
            features.append('links')
        
        # Add strategy-specific features
        engagement_tactics = business_strategy.get('engagement_tactics', [])
        features.extend(engagement_tactics)
        
        return list(set(features))  # Remove duplicates

    def _determine_content_format(self, platform: str, metadata: Dict) -> str:
        """Determine optimal content format for platform"""
        
        content_type = metadata.get('content_type', 'Educational')
        
        format_map = {
            'Facebook': {
                'Educational': 'text_post',
                'Promotional': 'text_with_image',
                'Behind-the-Scenes': 'photo_album',
                'Success Story': 'text_post'
            },
            'Instagram': {
                'Educational': 'carousel_post',
                'Promotional': 'single_image',
                'Behind-the-Scenes': 'story_highlight',
                'Success Story': 'single_image'
            },
            'LinkedIn': {
                'Educational': 'article',
                'Promotional': 'text_post',
                'Behind-the-Scenes': 'text_with_image',
                'Success Story': 'text_post'
            },
            'Twitter': {
                'Educational': 'thread',
                'Promotional': 'single_tweet',
                'Behind-the-Scenes': 'tweet_with_image',
                'Success Story': 'single_tweet'
            }
        }
        
        return format_map.get(platform, {}).get(content_type, 'text_post')

    # Helper methods for content modification
    def _add_parent_friendly_language(self, content: str) -> str:
        """Add parent-friendly language"""
        content = content.replace('players', 'children')
        content = content.replace('athletes', 'young people')
        return content

    def _add_coach_friendly_language(self, content: str) -> str:
        """Add coach-friendly language"""
        content = content.replace('people', 'coaches')
        content = content.replace('customers', 'fellow coaches')
        return content

    def _add_visual_cues(self, content: str) -> str:
        """Add visual cues for visual platforms"""
        if 'training' in content.lower():
            content = "🏃‍♂️ " + content
        elif 'goal' in content.lower():
            content = "⚽ " + content
        return content

    def _make_more_concise(self, content: str) -> str:
        """Make content more concise"""
        # Remove filler words
        filler_words = ['really', 'very', 'quite', 'actually', 'just']
        for word in filler_words:
            content = content.replace(f' {word} ', ' ')
        return content

    def _add_strategic_line_breaks(self, content: str) -> str:
        """Add strategic line breaks for readability"""
        # Add line breaks after sentences for better readability
        content = content.replace('. ', '.\n\n')
        return content

    def _add_emojis(self, content: str, level: str) -> str:
        """Add appropriate emojis based on level"""
        emoji_map = {
            'goal': '⚽',
            'training': '🏃‍♂️',
            'coach': '👨‍🏫',
            'car': '🚗',
            'barber': '✂️',
            'recovery': '💪',
            'kit': '👕'
        }
        
        if level == 'minimal':
            # Only add one relevant emoji
            for keyword, emoji in emoji_map.items():
                if keyword in content.lower():
                    content = emoji + " " + content
                    break
        
        elif level == 'moderate':
            # Add 1-2 relevant emojis
            emoji_count = 0
            for keyword, emoji in emoji_map.items():
                if keyword in content.lower() and emoji_count < 2:
                    content = content.replace(keyword, f"{emoji} {keyword}")
                    emoji_count += 1
        
        elif level == 'heavy':
            # Add multiple relevant emojis
            for keyword, emoji in emoji_map.items():
                if keyword in content.lower():
                    content = content.replace(keyword, f"{emoji} {keyword}")
        
        return content

    def _apply_title_case_headers(self, content: str) -> str:
        """Apply title case to headers"""
        # Simple title case application
        sentences = content.split('. ')
        if sentences:
            sentences[0] = sentences[0].title()
        return '. '.join(sentences)

    def _add_engagement_question(self, content: str, business_strategy: Dict) -> str:
        """Add engagement question based on business strategy"""
        
        questions = {
            'parent_community': "What's your experience with youth sports confidence?",
            'coach_community': "How do you handle session planning challenges?",
            'team_community': "What makes your team identity special?",
            'local_community': "What automotive questions can we help with?",
            'family_community': "What's your family grooming tradition?",
            'athlete_community': "How do you prioritize recovery in your training?"
        }
        
        focus = business_strategy.get('focus', '')
        question = questions.get(focus, "What's your experience?")
        
        return content + f" {question}"

    def _add_community_elements(self, content: str) -> str:
        """Add community-focused elements"""
        if 'join' not in content.lower():
            content += " Join our community!"
        return content

    def _add_local_elements(self, content: str, business_strategy: Dict) -> str:
        """Add local relevance elements"""
        focus = business_strategy.get('focus', '')
        if 'local' in focus:
            content = content.replace('customers', 'local community')
        return content

# Example usage and testing
if __name__ == "__main__":
    from engaging_content_writer import ContentPiece
    
    print("=== PLATFORM OPTIMIZER TEST ===")
    
    optimizer = PlatformOptimizer()
    
    # Mock content piece
    class MockContentPiece:
        def __init__(self):
            self.title = "Building Goalkeeper Confidence"
            self.shortform_content = "What if your child could love being in goal? At BGK Goalkeeping, we build confidence first, technique second. That's the #BGKUNION difference. Ready to transform your goalkeeper?"
            self.content_metadata = {'content_type': 'Educational'}
    
    content_piece = MockContentPiece()
    
    # Test optimization for multiple platforms
    optimized = optimizer.optimize_for_platforms(content_piece, 'BGK Goalkeeping')
    
    for platform, platform_content in optimized.items():
        print(f"\n{platform.upper()}:")
        print(f"Content: {platform_content.content[:100]}...")
        print(f"Hashtags: {platform_content.hashtags}")
        print(f"Format: {platform_content.content_format}")
        print(f"Best times: {platform_content.best_posting_times}")