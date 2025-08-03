#!/usr/bin/env python3
"""
Content Quality Validator - Comprehensive quality assurance system
Validates content for engagement, authenticity, brand alignment, and technical quality
"""

import re
from typing import Dict, List
from datetime import datetime

class ContentQualityValidator:
    def __init__(self):
        # Quality thresholds
        self.quality_thresholds = {
            'excellent': 0.9,
            'very_good': 0.8,
            'good': 0.7,
            'fair': 0.6,
            'poor': 0.5
        }
        
        # British English patterns
        self.british_patterns = {
            'correct_spellings': ['colour', 'centre', 'realise', 'organise', 'specialise', 'programme', 'whilst'],
            'american_spellings': ['color', 'center', 'realize', 'organize', 'specialize', 'program', 'while'],
            'british_terms': ['queue', 'lift', 'boot', 'bonnet', 'lorry', 'coach', 'mate']
        }
        
        # Engagement indicators
        self.engagement_indicators = {
            'strong_hooks': [
                r'Why do \d+%',  # Statistical hook
                r'What if',      # Hypothetical hook
                r'How to',       # Practical hook
                r'[A-Z][^.!?]*\?$',  # Question hook
                r'This [a-z]+ (went|transformed|changed)'  # Story hook
            ],
            'value_propositions': [
                'evidence-based', 'proven', 'professional', 'expert', 'specialized',
                'confidence', 'results', 'success', 'transformation', 'improvement'
            ],
            'social_proof': [
                r'\d+\+?\s+(customers|clients|members|coaches|teams)',
                r'\d+\.?\d*\s+stars?',
                r'\d+%\s+(success|satisfaction|improvement)',
                'testimonial', 'review', 'rated', 'recommended'
            ]
        }
        
        # AI detection patterns (to avoid)
        self.ai_patterns = [
            'delve into', 'unlock the power', 'game-changer', 'revolutionary',
            'cutting-edge solutions', 'seamless integration', 'elevate your',
            'unparalleled', 'state-of-the-art', 'next level'
        ]
    
    def validate_content(self, content: str, business_config: Dict, platform: str = 'Facebook') -> Dict:
        """Comprehensive content quality validation"""
        
        # Calculate individual scores
        engagement_score = self._calculate_engagement_score(content)
        authenticity_score = self._calculate_authenticity_score(content)
        brand_alignment_score = self._calculate_brand_alignment_score(content, business_config)
        technical_score = self._calculate_technical_score(content, platform)
        
        # Calculate weighted overall score
        overall_score = (
            engagement_score * 0.3 +
            authenticity_score * 0.25 +
            brand_alignment_score * 0.25 +
            technical_score * 0.2
        )
        
        # Generate improvement suggestions
        suggestions = self._generate_improvement_suggestions(
            content, engagement_score, authenticity_score, 
            brand_alignment_score, technical_score, business_config
        )
        
        # Determine quality grade
        quality_grade = self._get_quality_grade(overall_score)
        
        return {
            'overall_score': overall_score,
            'engagement_score': engagement_score,
            'authenticity_score': authenticity_score,
            'brand_alignment_score': brand_alignment_score,
            'technical_score': technical_score,
            'quality_grade': quality_grade,
            'passes_threshold': overall_score >= self.quality_thresholds['good'],
            'improvement_suggestions': suggestions,
            'platform': platform,
            'validated_at': datetime.now().isoformat(),
            'character_count': len(content),
            'word_count': len(content.split())
        }
    
    def _calculate_engagement_score(self, content: str) -> float:
        """Calculate engagement potential score"""
        score = 0.5  # Base score
        
        # Check for strong hooks
        for hook_pattern in self.engagement_indicators['strong_hooks']:
            if re.search(hook_pattern, content, re.IGNORECASE):
                score += 0.15
                break
        
        # Check for value propositions
        value_prop_count = 0
        for value_term in self.engagement_indicators['value_propositions']:
            if value_term.lower() in content.lower():
                value_prop_count += 1
        score += min(value_prop_count * 0.05, 0.2)
        
        # Check for social proof
        for proof_pattern in self.engagement_indicators['social_proof']:
            if re.search(proof_pattern, content, re.IGNORECASE):
                score += 0.1
                break
        
        # Check for clear call-to-action
        cta_patterns = [r'Ready to', r'Want to', r'Join', r'Contact', r'Book', r'Call']
        for cta_pattern in cta_patterns:
            if re.search(cta_pattern, content, re.IGNORECASE):
                score += 0.1
                break
        
        # Bonus for question engagement
        if content.count('?') >= 1:
            score += 0.05
        
        return min(score, 1.0)
    
    def _calculate_authenticity_score(self, content: str) -> float:
        """Calculate content authenticity score"""
        score = 0.9  # Start high, deduct for issues
        
        # Penalize AI-typical phrases
        ai_phrase_count = 0
        for ai_phrase in self.ai_patterns:
            if ai_phrase.lower() in content.lower():
                ai_phrase_count += 1
        score -= ai_phrase_count * 0.1
        
        # Check for natural language flow
        sentences = content.split('.')
        if len(sentences) > 1:
            # Penalize overly complex sentences
            avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences)
            if avg_sentence_length > 25:
                score -= 0.1
            elif avg_sentence_length < 5:
                score -= 0.05
        
        # Bonus for conversational tone
        conversational_indicators = ["you'll", "we're", "that's", "it's", "don't", "can't"]
        conversational_count = sum(1 for indicator in conversational_indicators if indicator in content.lower())
        score += min(conversational_count * 0.02, 0.1)
        
        # Check for excessive jargon
        jargon_words = ['leverage', 'synergy', 'paradigm', 'holistic', 'optimization', 'streamline']
        jargon_count = sum(1 for word in jargon_words if word.lower() in content.lower())
        score -= jargon_count * 0.05
        
        return max(score, 0.0)
    
    def _calculate_brand_alignment_score(self, content: str, business_config: Dict) -> float:
        """Calculate brand voice alignment score"""
        score = 0.6  # Base score
        
        business_name = business_config.get('business_name', '')
        brand_voice = business_config.get('brand_voice', '').lower()
        key_themes = business_config.get('key_themes', [])
        
        # Check for business name mention
        if business_name.lower() in content.lower():
            score += 0.1
        
        # Check for key themes
        theme_matches = 0
        for theme in key_themes:
            if theme.lower() in content.lower():
                theme_matches += 1
        score += min(theme_matches * 0.1, 0.2)
        
        # Brand voice alignment
        voice_keywords = {
            'encouraging': ['confidence', 'support', 'help', 'guide', 'empower'],
            'professional': ['expertise', 'quality', 'standards', 'certified', 'professional'],
            'trustworthy': ['honest', 'reliable', 'trusted', 'transparent', 'proven'],
            'accessible': ['simple', 'easy', 'straightforward', 'clear', 'affordable'],
            'authoritative': ['expert', 'leading', 'proven', 'established', 'recognized']
        }
        
        for voice_type, keywords in voice_keywords.items():
            if voice_type in brand_voice:
                keyword_matches = sum(1 for keyword in keywords if keyword in content.lower())
                score += min(keyword_matches * 0.02, 0.1)
        
        return min(score, 1.0)
    
    def _calculate_technical_score(self, content: str, platform: str) -> float:
        """Calculate technical quality score"""
        score = 0.8  # Base score
        
        # Platform-specific character limits
        platform_limits = {
            'Facebook': (80, 250),
            'Instagram': (125, 150),
            'LinkedIn': (150, 300),
            'Twitter': (71, 100)
        }
        
        char_count = len(content)
        if platform in platform_limits:
            min_chars, max_chars = platform_limits[platform]
            if min_chars <= char_count <= max_chars:
                score += 0.1  # Bonus for optimal length
            elif char_count < min_chars:
                score -= 0.1  # Penalty for too short
            elif char_count > max_chars * 1.2:
                score -= 0.2  # Penalty for too long
        
        # Check for British English
        american_spelling_count = 0
        for american_word in self.british_patterns['american_spellings']:
            if american_word in content.lower():
                american_spelling_count += 1
        score -= american_spelling_count * 0.05
        
        # Grammar and punctuation check
        if not content.strip().endswith(('.', '!', '?')):
            score -= 0.1
        
        # Check for proper capitalization
        sentences = re.split(r'[.!?]+', content)
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and not sentence[0].isupper():
                score -= 0.05
                break
        
        # Check for excessive punctuation
        if content.count('!') > 2 or content.count('?') > 3:
            score -= 0.1
        
        return max(score, 0.0)
    
    def _generate_improvement_suggestions(self, content: str, engagement_score: float, 
                                        authenticity_score: float, brand_alignment_score: float, 
                                        technical_score: float, business_config: Dict) -> List[str]:
        """Generate specific improvement suggestions"""
        suggestions = []
        
        # Engagement improvements
        if engagement_score < 0.7:
            if not any(re.search(pattern, content, re.IGNORECASE) for pattern in self.engagement_indicators['strong_hooks']):
                suggestions.append("Add a stronger hook (question, statistic, or compelling statement)")
            
            if not any(proof in content.lower() for proof in ['stars', 'customers', 'reviews', '%']):
                suggestions.append("Include social proof (customer numbers, ratings, or testimonials)")
            
            if not re.search(r'Ready to|Want to|Join|Contact', content, re.IGNORECASE):
                suggestions.append("Add a clear call-to-action")
        
        # Authenticity improvements
        if authenticity_score < 0.7:
            ai_phrases_found = [phrase for phrase in self.ai_patterns if phrase.lower() in content.lower()]
            if ai_phrases_found:
                suggestions.append(f"Remove AI-typical phrases: {', '.join(ai_phrases_found[:2])}")
            
            if content.count('.') == 0:
                suggestions.append("Break into shorter, more natural sentences")
            
            if not any(contraction in content.lower() for contraction in ["you'll", "we're", "that's", "don't"]):
                suggestions.append("Use more conversational language with contractions")
        
        # Brand alignment improvements
        if brand_alignment_score < 0.7:
            business_name = business_config.get('business_name', '')
            if business_name.lower() not in content.lower():
                suggestions.append(f"Include the business name '{business_name}'")
            
            key_themes = business_config.get('key_themes', [])
            missing_themes = [theme for theme in key_themes if theme.lower() not in content.lower()]
            if missing_themes:
                suggestions.append(f"Incorporate key themes: {', '.join(missing_themes[:2])}")
        
        # Technical improvements
        if technical_score < 0.7:
            # Check for American spellings
            american_found = [word for word in self.british_patterns['american_spellings'] if word in content.lower()]
            if american_found:
                british_replacements = dict(zip(self.british_patterns['american_spellings'], self.british_patterns['correct_spellings']))
                suggestions.append(f"Use British spelling: {' → '.join([f'{word} → {british_replacements.get(word, word)}' for word in american_found[:2]])}")
            
            if not content.strip().endswith(('.', '!', '?')):
                suggestions.append("End with proper punctuation")
            
            if content.count('!') > 2:
                suggestions.append("Reduce excessive exclamation marks")
        
        return suggestions[:5]  # Limit to top 5 suggestions
    
    def _get_quality_grade(self, score: float) -> str:
        """Convert numeric score to quality grade"""
        if score >= 0.9:
            return "A+ (Excellent)"
        elif score >= 0.8:
            return "A (Very Good)"
        elif score >= 0.7:
            return "B (Good)"
        elif score >= 0.6:
            return "C (Fair)"
        else:
            return "D (Needs Improvement)"

if __name__ == "__main__":
    validator = ContentQualityValidator()
    
    # Test validation
    sample_content = "Why do 70% of young goalkeepers quit by age 14? Every young goalkeeper needs proper guidance to build confidence. Our evidence-based approach has helped hundreds of goalkeepers across Scotland. Ready to build unshakeable confidence?"
    
    sample_config = {
        'business_name': 'BGK Goalkeeping',
        'brand_voice': 'encouraging, confident, evidence-based',
        'key_themes': ['confidence building', 'evidence-based training', 'youth development']
    }
    
    result = validator.validate_content(sample_content, sample_config, 'Facebook')
    
    print("Quality Validation Results:")
    print(f"Overall Score: {result['overall_score']:.2f}")
    print(f"Quality Grade: {result['quality_grade']}")
    print(f"Engagement: {result['engagement_score']:.2f}")
    print(f"Authenticity: {result['authenticity_score']:.2f}")
    print(f"Brand Alignment: {result['brand_alignment_score']:.2f}")
    print(f"Technical: {result['technical_score']:.2f}")
    print("\nSuggestions:")
    for suggestion in result['improvement_suggestions']:
        print(f"- {suggestion}")