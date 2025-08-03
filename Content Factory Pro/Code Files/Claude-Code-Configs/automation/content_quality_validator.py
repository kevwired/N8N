#!/usr/bin/env python3
"""
Content Quality Validator
=========================

Advanced content quality assurance system that:
1. Validates content quality, engagement potential, and brand alignment
2. Checks for AI detection patterns and ensures natural language flow
3. Verifies British English consistency and grammar
4. Ensures compliance with platform guidelines and best practices
5. Provides quality scores and improvement recommendations

Author: Claude Code
Version: 2.0
"""

import re
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from engaging_content_writer import ContentPiece
from platform_optimizer import PlatformContent

@dataclass
class QualityReport:
    """Comprehensive quality assessment report"""
    overall_score: float
    engagement_score: float
    authenticity_score: float
    brand_alignment_score: float
    technical_score: float
    
    passed_checks: List[str]
    failed_checks: List[str]
    warnings: List[str]
    recommendations: List[str]
    
    detailed_analysis: Dict[str, Union[float, str, List[str]]]
    validation_timestamp: datetime

class ContentQualityValidator:
    """Comprehensive content quality validation system"""
    
    def __init__(self):
        # AI detection patterns to avoid
        self.ai_detection_patterns = [
            # Overly formal structures
            r'\b(furthermore|moreover|additionally|consequently)\b',
            r'\b(in conclusion|to summarize|in summary)\b',
            r'\b(it is important to note|it should be noted)\b',
            
            # Repetitive patterns
            r'\b(\w+)\s+\1\b',  # Word repetition
            r'(the\s+\w+\s+of\s+the\s+\w+){2,}',  # Repetitive 'the X of the Y' patterns
            
            # Unnatural transitions
            r'\b(what\'s more|what is more)\b',
            r'\b(on the other hand|on one hand)\b',
            
            # Generic business language
            r'\b(leverage|utilize|facilitate)\b',
            r'\b(innovative solutions|cutting-edge|state-of-the-art)\b',
            
            # Overly promotional language
            r'\b(amazing|incredible|outstanding|exceptional)\s+(results|service|experience)\b',
            r'\b(don\'t miss out|act now|limited time)\b'
        ]
        
        # Brand voice guidelines for each business
        self.brand_voice_guidelines = {
            'BGK Goalkeeping': {
                'tone': ['confident', 'supportive', 'encouraging', 'expert'],
                'avoid': ['pushy', 'aggressive', 'intimidating'],
                'key_terms': ['confidence', 'evidence-based', 'specialist', '#BGKUNION'],
                'british_elements': True,
                'target_audience_voice': 'parent-friendly'
            },
            '360TFT': {
                'tone': ['practical', 'no-nonsense', 'empowering', 'authentic'],
                'avoid': ['theoretical', 'academic', 'pretentious'],
                'key_terms': ['stop guessing', 'proven', 'game-based', 'community'],
                'british_elements': True,
                'target_audience_voice': 'coach-to-coach'
            },
            'Kit-Mart': {
                'tone': ['reliable', 'professional', 'community-focused', 'quality-driven'],
                'avoid': ['cheap', 'mass-market', 'impersonal'],
                'key_terms': ['bespoke', 'quality', 'local', 'grassroots'],
                'british_elements': True,
                'target_audience_voice': 'team-focused'
            },
            'CD Copland Motors': {
                'tone': ['trustworthy', 'honest', 'professional', 'local'],
                'avoid': ['salesy', 'corporate', 'intimidating'],
                'key_terms': ['honest', 'trusted', 'local', 'quality'],
                'british_elements': True,
                'target_audience_voice': 'customer-care'
            },
            'KF Barbers': {
                'tone': ['traditional', 'welcoming', 'professional', 'family-friendly'],
                'avoid': ['trendy', 'flashy', 'commercial'],
                'key_terms': ['traditional', 'family', 'craft', 'quality'],
                'british_elements': True,
                'target_audience_voice': 'family-welcoming'
            },
            'Athlete Recovery Zone': {
                'tone': ['scientific', 'professional', 'results-focused', 'inclusive'],
                'avoid': ['exclusive', 'intimidating', 'overly-technical'],
                'key_terms': ['evidence-based', 'performance', 'recovery', 'professional'],
                'british_elements': True,
                'target_audience_voice': 'athlete-focused'
            }
        }
        
        # British English patterns and requirements
        self.british_english_requirements = {
            'spelling': {
                'ise_ize': ['realise', 'recognise', 'specialise', 'organise'],
                'our_or': ['colour', 'favour', 'behaviour', 'honour'],
                're_er': ['centre', 'theatre', 'metre'],
                'specific_words': {
                    'mom': 'mum',
                    'soccer': 'football',
                    'awesome': 'brilliant',
                    'guys': 'everyone'
                }
            },
            'expressions': [
                'brilliant', 'spot on', 'proper', 'chuffed', 'keen',
                'reckon', 'sorted', 'fair enough', 'right then'
            ],
            'avoid_americanisms': [
                'awesome', 'amazing', 'guys', 'mom', 'soccer', 'gotten',
                'super', 'totally', 'like totally', 'for sure'
            ]
        }
        
        # Engagement quality indicators
        self.engagement_indicators = {
            'positive': [
                'questions',
                'personal_stories',
                'community_references',
                'specific_benefits',
                'social_proof',
                'clear_call_to_action',
                'emotional_connection',
                'curiosity_gaps'
            ],
            'negative': [
                'generic_statements',
                'corporate_speak',
                'no_clear_purpose',
                'weak_call_to_action',
                'boring_facts_only',
                'too_salesy',
                'confusing_message'
            ]
        }
        
        # Platform compliance requirements
        self.platform_requirements = {
            'Facebook': {
                'max_length': 63206,
                'optimal_length': (80, 250),
                'required_elements': ['clear_message', 'call_to_action'],
                'avoid': ['too_many_hashtags', 'spam_language']
            },
            'Instagram': {
                'max_length': 2200,
                'optimal_length': (138, 150),
                'required_elements': ['visual_appeal', 'hashtags'],
                'avoid': ['link_spam', 'excessive_text']
            },
            'LinkedIn': {
                'max_length': 3000,
                'optimal_length': (150, 300),
                'required_elements': ['professional_tone', 'industry_relevance'],
                'avoid': ['overly_casual', 'inappropriate_content']
            },
            'Twitter': {
                'max_length': 280,
                'optimal_length': (71, 100),
                'required_elements': ['concise_message', 'engagement_hook'],
                'avoid': ['thread_abuse', 'hashtag_stuffing']
            }
        }

    def validate_content_quality(self, content_piece: ContentPiece, business_name: str, 
                               platform_contents: Dict[str, PlatformContent] = None) -> QualityReport:
        """Perform comprehensive content quality validation"""
        
        # Initialize scoring
        scores = {
            'overall': 0.0,
            'engagement': 0.0,
            'authenticity': 0.0,
            'brand_alignment': 0.0,
            'technical': 0.0
        }
        
        passed_checks = []
        failed_checks = []
        warnings = []
        recommendations = []
        detailed_analysis = {}
        
        # 1. Engagement Quality Assessment
        engagement_result = self._assess_engagement_quality(content_piece)
        scores['engagement'] = engagement_result['score']
        passed_checks.extend(engagement_result['passed'])
        failed_checks.extend(engagement_result['failed'])
        warnings.extend(engagement_result['warnings'])
        recommendations.extend(engagement_result['recommendations'])
        detailed_analysis['engagement'] = engagement_result['details']
        
        # 2. Authenticity and AI Detection Assessment
        authenticity_result = self._assess_authenticity(content_piece)
        scores['authenticity'] = authenticity_result['score']
        passed_checks.extend(authenticity_result['passed'])
        failed_checks.extend(authenticity_result['failed'])
        warnings.extend(authenticity_result['warnings'])
        recommendations.extend(authenticity_result['recommendations'])
        detailed_analysis['authenticity'] = authenticity_result['details']
        
        # 3. Brand Alignment Assessment
        brand_result = self._assess_brand_alignment(content_piece, business_name)
        scores['brand_alignment'] = brand_result['score']
        passed_checks.extend(brand_result['passed'])
        failed_checks.extend(brand_result['failed'])
        warnings.extend(brand_result['warnings'])
        recommendations.extend(brand_result['recommendations'])
        detailed_analysis['brand_alignment'] = brand_result['details']
        
        # 4. Technical Quality Assessment
        technical_result = self._assess_technical_quality(content_piece, business_name)
        scores['technical'] = technical_result['score']
        passed_checks.extend(technical_result['passed'])
        failed_checks.extend(technical_result['failed'])
        warnings.extend(technical_result['warnings'])
        recommendations.extend(technical_result['recommendations'])
        detailed_analysis['technical'] = technical_result['details']
        
        # 5. Platform Compliance Assessment (if platform contents provided)
        if platform_contents:
            platform_result = self._assess_platform_compliance(platform_contents)
            detailed_analysis['platform_compliance'] = platform_result['details']
            warnings.extend(platform_result['warnings'])
            recommendations.extend(platform_result['recommendations'])
        
        # Calculate overall score
        scores['overall'] = (
            scores['engagement'] * 0.35 +
            scores['authenticity'] * 0.25 +
            scores['brand_alignment'] * 0.25 +
            scores['technical'] * 0.15
        )
        
        return QualityReport(
            overall_score=scores['overall'],
            engagement_score=scores['engagement'],
            authenticity_score=scores['authenticity'],
            brand_alignment_score=scores['brand_alignment'],
            technical_score=scores['technical'],
            passed_checks=passed_checks,
            failed_checks=failed_checks,
            warnings=warnings,
            recommendations=recommendations,
            detailed_analysis=detailed_analysis,
            validation_timestamp=datetime.now()
        )

    def _assess_engagement_quality(self, content_piece: ContentPiece) -> Dict:
        """Assess content engagement potential"""
        
        score = 0.0
        passed = []
        failed = []
        warnings = []
        recommendations = []
        details = {}
        
        shortform = content_piece.shortform_content
        longform = content_piece.longform_content
        
        # Check for engaging hook
        hook_quality = self._assess_hook_quality(shortform)
        if hook_quality['score'] >= 0.7:
            passed.append("Strong engaging hook")
            score += 0.2
        else:
            failed.append("Weak or missing hook")
            recommendations.append("Improve opening hook to grab attention immediately")
        
        details['hook_analysis'] = hook_quality
        
        # Check for clear value proposition
        value_prop_score = self._assess_value_proposition(shortform, longform)
        if value_prop_score >= 0.7:
            passed.append("Clear value proposition")
            score += 0.15
        else:
            failed.append("Unclear value proposition")
            recommendations.append("Make the benefit to the audience clearer")
        
        details['value_proposition_score'] = value_prop_score
        
        # Check for social proof elements
        social_proof_score = self._assess_social_proof(shortform, longform)
        if social_proof_score >= 0.5:
            passed.append("Includes social proof")
            score += 0.1
        else:
            warnings.append("Could benefit from more social proof")
            recommendations.append("Add testimonials, statistics, or community references")
        
        details['social_proof_score'] = social_proof_score
        
        # Check for emotional connection
        emotional_score = self._assess_emotional_connection(shortform, longform)
        if emotional_score >= 0.6:
            passed.append("Creates emotional connection")
            score += 0.15
        else:
            warnings.append("Limited emotional connection")
            recommendations.append("Add more emotional elements or personal stories")
        
        details['emotional_connection_score'] = emotional_score
        
        # Check for clear call-to-action
        cta_quality = self._assess_cta_quality(content_piece.call_to_action)
        if cta_quality['score'] >= 0.7:
            passed.append("Strong call-to-action")
            score += 0.2
        else:
            failed.append("Weak call-to-action")
            recommendations.append("Create a clearer, more compelling call-to-action")
        
        details['cta_analysis'] = cta_quality
        
        # Check for engagement elements
        engagement_elements_score = len(content_piece.engagement_elements) / 5.0  # Normalize to max 5 elements
        if engagement_elements_score >= 0.4:
            passed.append("Good use of engagement elements")
            score += 0.1
        else:
            warnings.append("Could use more engagement elements")
            recommendations.append("Add questions, stories, or interactive elements")
        
        details['engagement_elements'] = content_piece.engagement_elements
        
        # Check content flow and readability
        flow_score = self._assess_content_flow(shortform, longform)
        if flow_score >= 0.7:
            passed.append("Good content flow")
            score += 0.1
        else:
            warnings.append("Content flow could be improved")
            recommendations.append("Improve logical flow and transitions")
        
        details['flow_score'] = flow_score
        
        return {
            'score': min(score, 1.0),
            'passed': passed,
            'failed': failed,
            'warnings': warnings,
            'recommendations': recommendations,
            'details': details
        }

    def _assess_authenticity(self, content_piece: ContentPiece) -> Dict:
        """Assess content authenticity and detect AI patterns"""
        
        score = 1.0  # Start with perfect score, deduct for issues
        passed = []
        failed = []
        warnings = []
        recommendations = []
        details = {}
        
        content_to_check = content_piece.shortform_content + " " + content_piece.longform_content
        
        # Check for AI detection patterns
        ai_pattern_count = 0
        detected_patterns = []
        
        for pattern in self.ai_detection_patterns:
            matches = re.findall(pattern, content_to_check, re.IGNORECASE)
            if matches:
                ai_pattern_count += len(matches)
                detected_patterns.extend(matches)
        
        if ai_pattern_count == 0:
            passed.append("No AI detection patterns found")
        elif ai_pattern_count <= 2:
            warnings.append(f"Minor AI patterns detected: {detected_patterns}")
            score -= 0.1
            recommendations.append("Replace overly formal language with more natural expressions")
        else:
            failed.append(f"Multiple AI patterns detected: {detected_patterns}")
            score -= 0.3
            recommendations.append("Significantly revise to sound more natural and human")
        
        details['ai_patterns_detected'] = detected_patterns
        details['ai_pattern_count'] = ai_pattern_count
        
        # Check for natural language flow
        natural_flow_score = self._assess_natural_flow(content_to_check)
        if natural_flow_score >= 0.8:
            passed.append("Natural language flow")
        elif natural_flow_score >= 0.6:
            warnings.append("Some unnatural language patterns")
            score -= 0.1
            recommendations.append("Make language more conversational and natural")
        else:
            failed.append("Unnatural language flow")
            score -= 0.2
            recommendations.append("Rewrite to sound more human and conversational")
        
        details['natural_flow_score'] = natural_flow_score
        
        # Check for repetitive patterns
        repetition_score = self._assess_repetition(content_to_check)
        if repetition_score >= 0.8:
            passed.append("Good content variety")
        elif repetition_score >= 0.6:
            warnings.append("Some repetitive patterns")
            score -= 0.05
        else:
            failed.append("Too much repetition")
            score -= 0.15
            recommendations.append("Reduce repetitive language and add variety")
        
        details['repetition_score'] = repetition_score
        
        # Check for personal touch
        personal_touch_score = self._assess_personal_touch(content_to_check)
        if personal_touch_score >= 0.6:
            passed.append("Includes personal elements")
        else:
            warnings.append("Could be more personal")
            recommendations.append("Add more personal stories or specific examples")
        
        details['personal_touch_score'] = personal_touch_score
        
        return {
            'score': max(score, 0.0),
            'passed': passed,
            'failed': failed,
            'warnings': warnings,
            'recommendations': recommendations,
            'details': details
        }

    def _assess_brand_alignment(self, content_piece: ContentPiece, business_name: str) -> Dict:
        """Assess alignment with brand voice and guidelines"""
        
        score = 0.0
        passed = []
        failed = []
        warnings = []
        recommendations = []
        details = {}
        
        brand_guidelines = self.brand_voice_guidelines.get(business_name, {})
        if not brand_guidelines:
            warnings.append(f"No brand guidelines defined for {business_name}")
            return {
                'score': 0.5,
                'passed': passed,
                'failed': failed,
                'warnings': warnings,
                'recommendations': ['Define brand voice guidelines'],
                'details': {}
            }
        
        content_to_check = content_piece.shortform_content + " " + content_piece.longform_content
        content_lower = content_to_check.lower()
        
        # Check tone alignment
        required_tones = brand_guidelines.get('tone', [])
        avoid_tones = brand_guidelines.get('avoid', [])
        
        tone_score = self._assess_tone_alignment(content_to_check, required_tones, avoid_tones)
        if tone_score >= 0.7:
            passed.append("Good tone alignment")
            score += 0.3
        elif tone_score >= 0.5:
            warnings.append("Some tone misalignment")
            score += 0.15
            recommendations.append("Better align with brand tone guidelines")
        else:
            failed.append("Poor tone alignment")
            recommendations.append("Significantly revise to match brand voice")
        
        details['tone_score'] = tone_score
        details['required_tones'] = required_tones
        details['avoid_tones'] = avoid_tones
        
        # Check for key terms
        key_terms = brand_guidelines.get('key_terms', [])
        key_terms_found = [term for term in key_terms if term.lower() in content_lower]
        key_terms_score = len(key_terms_found) / max(len(key_terms), 1)
        
        if key_terms_score >= 0.5:
            passed.append(f"Uses brand key terms: {key_terms_found}")
            score += 0.2
        else:
            warnings.append("Could include more brand key terms")
            recommendations.append(f"Consider including terms like: {', '.join(key_terms)}")
        
        details['key_terms_score'] = key_terms_score
        details['key_terms_found'] = key_terms_found
        
        # Check target audience voice
        target_voice = brand_guidelines.get('target_audience_voice', '')
        voice_alignment_score = self._assess_audience_voice_alignment(content_to_check, target_voice)
        
        if voice_alignment_score >= 0.7:
            passed.append("Good audience voice alignment")
            score += 0.25
        elif voice_alignment_score >= 0.5:
            warnings.append("Some audience voice misalignment")
            score += 0.1
        else:
            failed.append("Poor audience voice alignment")
            recommendations.append(f"Better align with {target_voice} voice")
        
        details['audience_voice_score'] = voice_alignment_score
        
        # Check British English elements (if required)
        if brand_guidelines.get('british_elements', False):
            british_score = self._assess_british_english(content_to_check)
            if british_score >= 0.8:
                passed.append("Good British English usage")
                score += 0.25
            elif british_score >= 0.6:
                warnings.append("Some British English issues")
                score += 0.1
                recommendations.append("Improve British English consistency")
            else:
                failed.append("Poor British English usage")
                recommendations.append("Convert to proper British English")
            
            details['british_english_score'] = british_score
        
        return {
            'score': min(score, 1.0),
            'passed': passed,
            'failed': failed,
            'warnings': warnings,
            'recommendations': recommendations,
            'details': details
        }

    def _assess_technical_quality(self, content_piece: ContentPiece, business_name: str) -> Dict:
        """Assess technical quality including grammar, spelling, and structure"""
        
        score = 0.0
        passed = []
        failed = []
        warnings = []
        recommendations = []
        details = {}
        
        content_to_check = content_piece.shortform_content + " " + content_piece.longform_content
        
        # Check grammar and spelling
        grammar_score = self._assess_grammar_quality(content_to_check)
        if grammar_score >= 0.9:
            passed.append("Excellent grammar and spelling")
            score += 0.3
        elif grammar_score >= 0.7:
            warnings.append("Minor grammar/spelling issues")
            score += 0.2
            recommendations.append("Review for minor grammar and spelling corrections")
        else:
            failed.append("Significant grammar/spelling issues")
            score += 0.1
            recommendations.append("Comprehensive grammar and spelling review needed")
        
        details['grammar_score'] = grammar_score
        
        # Check content structure
        structure_score = self._assess_content_structure(content_piece)
        if structure_score >= 0.8:
            passed.append("Well-structured content")
            score += 0.25
        elif structure_score >= 0.6:
            warnings.append("Structure could be improved")
            score += 0.15
        else:
            failed.append("Poor content structure")
            recommendations.append("Improve content organization and flow")
        
        details['structure_score'] = structure_score
        
        # Check consistency across content formats
        consistency_score = self._assess_format_consistency(content_piece)
        if consistency_score >= 0.8:
            passed.append("Good format consistency")
            score += 0.2
        else:
            warnings.append("Format consistency issues")
            recommendations.append("Ensure consistency across short and long form content")
        
        details['consistency_score'] = consistency_score
        
        # Check for proper CTAs and metadata
        metadata_score = self._assess_metadata_quality(content_piece)
        if metadata_score >= 0.7:
            passed.append("Complete metadata")
            score += 0.15
        else:
            warnings.append("Incomplete metadata")
            recommendations.append("Ensure all required metadata is complete")
        
        details['metadata_score'] = metadata_score
        
        # Check character limits and formatting
        formatting_score = self._assess_formatting_quality(content_piece)
        if formatting_score >= 0.8:
            passed.append("Good formatting")
            score += 0.1
        else:
            warnings.append("Formatting issues")
            recommendations.append("Improve content formatting and structure")
        
        details['formatting_score'] = formatting_score
        
        return {
            'score': min(score, 1.0),
            'passed': passed,
            'failed': failed,
            'warnings': warnings,
            'recommendations': recommendations,
            'details': details
        }

    def _assess_platform_compliance(self, platform_contents: Dict[str, PlatformContent]) -> Dict:
        """Assess compliance with platform requirements"""
        
        warnings = []
        recommendations = []
        details = {}
        
        for platform, platform_content in platform_contents.items():
            platform_reqs = self.platform_requirements.get(platform, {})
            platform_details = {}
            
            # Check length requirements
            content_length = len(platform_content.content)
            max_length = platform_reqs.get('max_length', 1000)
            optimal_range = platform_reqs.get('optimal_length', (50, 200))
            
            if content_length > max_length:
                warnings.append(f"{platform}: Content exceeds maximum length ({content_length} > {max_length})")
                recommendations.append(f"Trim {platform} content to under {max_length} characters")
            elif content_length < optimal_range[0] or content_length > optimal_range[1]:
                warnings.append(f"{platform}: Content outside optimal range ({content_length} chars)")
                recommendations.append(f"Adjust {platform} content to {optimal_range[0]}-{optimal_range[1]} characters")
            
            platform_details['content_length'] = content_length
            platform_details['optimal_range'] = optimal_range
            platform_details['within_optimal'] = optimal_range[0] <= content_length <= optimal_range[1]
            
            # Check required elements
            required_elements = platform_reqs.get('required_elements', [])
            missing_elements = []
            
            for element in required_elements:
                if not self._check_platform_element(platform_content, element):
                    missing_elements.append(element)
            
            if missing_elements:
                warnings.append(f"{platform}: Missing elements: {', '.join(missing_elements)}")
                recommendations.append(f"Add missing elements to {platform} content: {', '.join(missing_elements)}")
            
            platform_details['missing_elements'] = missing_elements
            
            details[platform] = platform_details
        
        return {
            'warnings': warnings,
            'recommendations': recommendations,
            'details': details
        }

    # Helper methods for specific assessments
    def _assess_hook_quality(self, content: str) -> Dict:
        """Assess the quality of the opening hook"""
        
        score = 0.0
        first_sentence = content.split('.')[0].strip()
        
        # Check for question hooks
        if first_sentence.endswith('?'):
            score += 0.3
        
        # Check for surprising statements
        if any(word in first_sentence.lower() for word in ['what if', 'imagine', 'surprising', 'secret']):
            score += 0.2
        
        # Check for emotional words
        emotional_words = ['love', 'hate', 'fear', 'excited', 'worried', 'confident', 'frustrated']
        if any(word in first_sentence.lower() for word in emotional_words):
            score += 0.2
        
        # Check for specificity
        if any(char.isdigit() for char in first_sentence):
            score += 0.1
        
        # Check for personal pronouns
        if any(pronoun in first_sentence.lower() for pronoun in ['you', 'your', 'we', 'our']):
            score += 0.2
        
        return {
            'score': min(score, 1.0),
            'first_sentence': first_sentence,
            'hook_type': self._identify_hook_type(first_sentence)
        }

    def _identify_hook_type(self, sentence: str) -> str:
        """Identify the type of hook used"""
        
        if sentence.endswith('?'):
            return 'question'
        elif 'what if' in sentence.lower():
            return 'hypothetical'
        elif any(char.isdigit() for char in sentence):
            return 'statistic'
        elif any(word in sentence.lower() for word in ['story', 'remember', 'imagine']):
            return 'story'
        else:
            return 'statement'

    def _assess_value_proposition(self, shortform: str, longform: str) -> float:
        """Assess clarity of value proposition"""
        
        score = 0.0
        combined_content = shortform + " " + longform
        
        # Check for benefit-focused language
        benefit_words = ['help', 'improve', 'better', 'save', 'gain', 'achieve', 'transform', 'build']
        benefit_count = sum(1 for word in benefit_words if word in combined_content.lower())
        score += min(benefit_count * 0.1, 0.4)
        
        # Check for specific outcomes
        outcome_words = ['results', 'success', 'growth', 'confidence', 'skills', 'performance']
        outcome_count = sum(1 for word in outcome_words if word in combined_content.lower())
        score += min(outcome_count * 0.1, 0.3)
        
        # Check for clear problem-solution structure
        problem_words = ['problem', 'challenge', 'struggle', 'difficulty', 'issue']
        solution_words = ['solution', 'answer', 'fix', 'solve', 'help']
        
        has_problem = any(word in combined_content.lower() for word in problem_words)
        has_solution = any(word in combined_content.lower() for word in solution_words)
        
        if has_problem and has_solution:
            score += 0.3
        
        return min(score, 1.0)

    def _assess_social_proof(self, shortform: str, longform: str) -> float:
        """Assess presence of social proof elements"""
        
        score = 0.0
        combined_content = shortform + " " + longform
        
        # Check for testimonials or reviews
        social_proof_indicators = ['reviews', 'customers', 'testimonial', 'stars', 'rated', 'recommend']
        for indicator in social_proof_indicators:
            if indicator in combined_content.lower():
                score += 0.2
        
        # Check for numbers/statistics
        if any(char.isdigit() for char in combined_content):
            score += 0.3
        
        # Check for community references
        community_words = ['community', 'members', 'join', 'others', 'everyone']
        for word in community_words:
            if word in combined_content.lower():
                score += 0.1
        
        return min(score, 1.0)

    def _assess_emotional_connection(self, shortform: str, longform: str) -> float:
        """Assess emotional connection strength"""
        
        score = 0.0
        combined_content = shortform + " " + longform
        
        # Check for emotional words
        emotional_words = [
            'love', 'confidence', 'trust', 'worry', 'fear', 'excited', 'proud',
            'frustrated', 'happy', 'sad', 'anxious', 'relieved', 'grateful'
        ]
        
        for word in emotional_words:
            if word in combined_content.lower():
                score += 0.1
        
        # Check for personal stories
        story_indicators = ['remember', 'story', 'experience', 'happened', 'told me']
        for indicator in story_indicators:
            if indicator in combined_content.lower():
                score += 0.2
        
        # Check for "you" focus
        you_count = combined_content.lower().count('you')
        score += min(you_count * 0.05, 0.3)
        
        return min(score, 1.0)

    def _assess_cta_quality(self, cta: str) -> Dict:
        """Assess call-to-action quality"""
        
        score = 0.0
        
        if not cta or len(cta.strip()) < 10:
            return {'score': 0.0, 'issue': 'Missing or too short'}
        
        # Check for action words
        action_words = ['get', 'join', 'start', 'book', 'call', 'contact', 'visit', 'learn', 'discover']
        has_action = any(word in cta.lower() for word in action_words)
        if has_action:
            score += 0.4
        
        # Check for urgency or value
        urgency_words = ['today', 'now', 'ready', 'start']
        has_urgency = any(word in cta.lower() for word in urgency_words)
        if has_urgency:
            score += 0.2
        
        # Check for clarity
        if '?' in cta:
            score += 0.2
        
        # Check for specificity
        if any(word in cta.lower() for word in ['contact', 'call', 'visit', 'email']):
            score += 0.2
        
        return {
            'score': min(score, 1.0),
            'has_action': has_action,
            'has_urgency': has_urgency
        }

    def _assess_content_flow(self, shortform: str, longform: str) -> float:
        """Assess logical flow of content"""
        
        score = 0.8  # Start high, deduct for issues
        
        # Check for logical sentence progression in shortform
        shortform_sentences = [s.strip() for s in shortform.split('.') if s.strip()]
        
        if len(shortform_sentences) < 2:
            score -= 0.2
        
        # Check for transition words
        transition_words = ['but', 'however', 'because', 'so', 'therefore', 'that\'s why']
        has_transitions = any(word in shortform.lower() for word in transition_words)
        if not has_transitions and len(shortform_sentences) > 2:
            score -= 0.1
        
        return max(score, 0.0)

    def _assess_natural_flow(self, content: str) -> float:
        """Assess natural language flow"""
        
        score = 0.8  # Start high
        
        # Check for overly long sentences
        sentences = [s.strip() for s in content.split('.') if s.strip()]
        avg_sentence_length = sum(len(s.split()) for s in sentences) / max(len(sentences), 1)
        
        if avg_sentence_length > 25:
            score -= 0.2
        elif avg_sentence_length < 8:
            score -= 0.1
        
        # Check for varied sentence structure
        sentence_starts = [s.split()[0].lower() if s.split() else '' for s in sentences]
        unique_starts = len(set(sentence_starts))
        if unique_starts < len(sentences) * 0.7:
            score -= 0.1
        
        return max(score, 0.0)

    def _assess_repetition(self, content: str) -> float:
        """Assess content for repetitive patterns"""
        
        words = content.lower().split()
        word_count = len(words)
        unique_words = len(set(words))
        
        if word_count == 0:
            return 0.0
        
        # Calculate lexical diversity
        lexical_diversity = unique_words / word_count
        
        # Convert to score (higher diversity = higher score)
        return min(lexical_diversity * 2, 1.0)

    def _assess_personal_touch(self, content: str) -> float:
        """Assess personal elements in content"""
        
        score = 0.0
        
        # Check for personal pronouns
        personal_pronouns = ['i', 'we', 'our', 'my', 'us']
        for pronoun in personal_pronouns:
            if f' {pronoun} ' in f' {content.lower()} ':
                score += 0.2
        
        # Check for personal experiences
        experience_words = ['experience', 'learned', 'discovered', 'found', 'realized']
        for word in experience_words:
            if word in content.lower():
                score += 0.1
        
        return min(score, 1.0)

    def _assess_tone_alignment(self, content: str, required_tones: List[str], avoid_tones: List[str]) -> float:
        """Assess tone alignment with brand guidelines"""
        
        score = 0.5  # Start neutral
        
        # Tone indicators
        tone_indicators = {
            'confident': ['proven', 'expert', 'specialist', 'professional', 'experienced'],
            'supportive': ['help', 'support', 'guide', 'care', 'understand'],
            'encouraging': ['can', 'will', 'possible', 'achieve', 'success'],
            'practical': ['how', 'step', 'method', 'approach', 'technique'],
            'authentic': ['real', 'genuine', 'honest', 'truth', 'actually'],
            'professional': ['service', 'quality', 'standards', 'excellence'],
            'friendly': ['welcome', 'happy', 'pleased', 'glad'],
            'trustworthy': ['trust', 'honest', 'reliable', 'dependable']
        }
        
        content_lower = content.lower()
        
        # Check for required tones
        for tone in required_tones:
            indicators = tone_indicators.get(tone, [])
            tone_present = any(indicator in content_lower for indicator in indicators)
            if tone_present:
                score += 0.1
        
        # Check for avoided tones
        for tone in avoid_tones:
            indicators = tone_indicators.get(tone, [])
            tone_present = any(indicator in content_lower for indicator in indicators)
            if tone_present:
                score -= 0.2
        
        return max(min(score, 1.0), 0.0)

    def _assess_audience_voice_alignment(self, content: str, target_voice: str) -> float:
        """Assess alignment with target audience voice"""
        
        voice_indicators = {
            'parent-friendly': ['child', 'children', 'kids', 'family', 'parent'],
            'coach-to-coach': ['coaches', 'training', 'players', 'team', 'session'],
            'team-focused': ['team', 'club', 'players', 'together', 'group'],
            'customer-care': ['service', 'care', 'help', 'support', 'customer'],
            'family-welcoming': ['family', 'welcome', 'everyone', 'children', 'generations'],
            'athlete-focused': ['athletes', 'performance', 'training', 'recovery', 'sports']
        }
        
        indicators = voice_indicators.get(target_voice, [])
        if not indicators:
            return 0.5
        
        content_lower = content.lower()
        matches = sum(1 for indicator in indicators if indicator in content_lower)
        
        return min(matches / len(indicators), 1.0)

    def _assess_british_english(self, content: str) -> float:
        """Assess British English usage"""
        
        score = 1.0  # Start perfect, deduct for issues
        
        # Check for American spellings
        american_patterns = {
            r'\bcolor\b': 'colour',
            r'\bfavor\b': 'favour',
            r'\bcenter\b': 'centre',
            r'\brealize\b': 'realise',
            r'\borganize\b': 'organise'
        }
        
        for american, british in american_patterns.items():
            if re.search(american, content, re.IGNORECASE):
                score -= 0.1
        
        # Check for American expressions
        avoid_americanisms = self.british_english_requirements['avoid_americanisms']
        for americanism in avoid_americanisms:
            if americanism.lower() in content.lower():
                score -= 0.1
        
        return max(score, 0.0)

    def _assess_grammar_quality(self, content: str) -> float:
        """Basic grammar assessment"""
        
        score = 0.9  # Start high
        
        # Check for basic punctuation
        sentences = content.split('.')
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and not sentence[0].isupper():
                score -= 0.05
        
        # Check for spell-check patterns (basic)
        # This is a simplified check - in production, you'd use a proper spell checker
        common_errors = ['teh', 'recieve', 'seperate', 'occured', 'acheive']
        for error in common_errors:
            if error in content.lower():
                score -= 0.1
        
        return max(score, 0.0)

    def _assess_content_structure(self, content_piece: ContentPiece) -> float:
        """Assess overall content structure"""
        
        score = 0.0
        
        # Check if shortform has clear structure
        if content_piece.shortform_content:
            score += 0.3
        
        # Check if longform has headers/sections
        if '##' in content_piece.longform_content or '#' in content_piece.longform_content:
            score += 0.3
        
        # Check if CTA is present and clear
        if content_piece.call_to_action and len(content_piece.call_to_action) > 10:
            score += 0.2
        
        # Check for hashtags
        if content_piece.hashtags:
            score += 0.1
        
        # Check for engagement elements
        if content_piece.engagement_elements:
            score += 0.1
        
        return min(score, 1.0)

    def _assess_format_consistency(self, content_piece: ContentPiece) -> float:
        """Assess consistency across content formats"""
        
        score = 0.5  # Start neutral
        
        # Check if shortform and longform have consistent messaging
        shortform_words = set(content_piece.shortform_content.lower().split())
        longform_words = set(content_piece.longform_content.lower().split())
        
        # Calculate overlap
        overlap = len(shortform_words.intersection(longform_words))
        total_unique = len(shortform_words.union(longform_words))
        
        if total_unique > 0:
            consistency_ratio = overlap / total_unique
            score = consistency_ratio
        
        return min(score, 1.0)

    def _assess_metadata_quality(self, content_piece: ContentPiece) -> float:
        """Assess completeness of metadata"""
        
        score = 0.0
        
        required_fields = [
            content_piece.title,
            content_piece.shortform_content,
            content_piece.longform_content,
            content_piece.call_to_action,
            content_piece.hashtags
        ]
        
        completed_fields = sum(1 for field in required_fields if field and len(str(field).strip()) > 0)
        score = completed_fields / len(required_fields)
        
        return score

    def _assess_formatting_quality(self, content_piece: ContentPiece) -> float:
        """Assess formatting quality"""
        
        score = 0.8  # Start high
        
        # Check for proper sentence ending
        if not content_piece.shortform_content.rstrip().endswith(('.', '!', '?')):
            score -= 0.2
        
        # Check for proper capitalization
        if content_piece.shortform_content and not content_piece.shortform_content[0].isupper():
            score -= 0.1
        
        # Check for excessive punctuation
        if '!!!' in content_piece.shortform_content or '???' in content_piece.shortform_content:
            score -= 0.1
        
        return max(score, 0.0)

    def _check_platform_element(self, platform_content: PlatformContent, element: str) -> bool:
        """Check if platform content includes required element"""
        
        content = platform_content.content.lower()
        
        element_checks = {
            'clear_message': len(content) > 20,
            'call_to_action': any(word in content for word in ['contact', 'join', 'get', 'book', 'visit']),
            'visual_appeal': len(content) < 300,  # Assume shorter is more visual-friendly
            'hashtags': bool(platform_content.hashtags),
            'professional_tone': not any(word in content for word in ['awesome', 'amazing', 'super']),
            'industry_relevance': True,  # Simplified check
            'concise_message': len(content) <= 280,
            'engagement_hook': content.endswith('?') or 'what' in content
        }
        
        return element_checks.get(element, True)

# Example usage and testing
if __name__ == "__main__":
    from engaging_content_writer import ContentPiece
    
    print("=== CONTENT QUALITY VALIDATOR TEST ===")
    
    validator = ContentQualityValidator()
    
    # Mock content piece
    class MockContentPiece:
        def __init__(self):
            self.title = "Building Goalkeeper Confidence"
            self.shortform_content = "What if your child could love being in goal? At BGK Goalkeeping, we build confidence first, technique second. That's the #BGKUNION difference. Ready to transform your goalkeeper?"
            self.longform_content = "# Building Goalkeeper Confidence\n\nEvery young goalkeeper faces unique challenges..."
            self.call_to_action = "Ready to build confidence? Contact BGK today to learn more."
            self.hashtags = "#BGKGoalkeeping #BGKUNION #GoalkeeperTraining"
            self.engagement_elements = ["engaging_question", "personal_story"]
            self.content_metadata = {"content_type": "Educational"}
    
    content_piece = MockContentPiece()
    
    # Validate content
    quality_report = validator.validate_content_quality(content_piece, 'BGK Goalkeeping')
    
    print(f"Overall Score: {quality_report.overall_score:.2f}")
    print(f"Engagement Score: {quality_report.engagement_score:.2f}")
    print(f"Authenticity Score: {quality_report.authenticity_score:.2f}")
    print(f"Brand Alignment Score: {quality_report.brand_alignment_score:.2f}")
    print(f"Technical Score: {quality_report.technical_score:.2f}")
    
    print(f"\nPassed Checks: {len(quality_report.passed_checks)}")
    print(f"Failed Checks: {len(quality_report.failed_checks)}")
    print(f"Warnings: {len(quality_report.warnings)}")
    print(f"Recommendations: {len(quality_report.recommendations)}")
    
    if quality_report.recommendations:
        print("\nTop Recommendations:")
        for rec in quality_report.recommendations[:3]:
            print(f"- {rec}")