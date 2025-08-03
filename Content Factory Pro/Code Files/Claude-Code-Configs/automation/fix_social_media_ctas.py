#!/usr/bin/env python3
"""
Fix social media CTAs to be short, varied, and natural
"""

import os
import re
from pathlib import Path
import random

# Define varied CTAs for each business
BUSINESS_CTAS = {
    'BGK Goalkeeping': {
        'Educational': [
            "Learn more goalkeeper tips @BGKGoalkeeping 🥅",
            "Follow for daily goalkeeper training tips!",
            "DM us to improve your game",
            "More training tips at BGKGoalkeeping.com",
            "Tag a young goalkeeper who needs this!"
        ],
        'Promotional': [
            "Book your 1-to-1 session today!",
            "Spaces available - link in bio",
            "Join the #BGKUNION today",
            "Start your goalkeeper journey with us",
            "Limited spots - book now!"
        ],
        'Behind-the-Scenes': [
            "See more behind the scenes @BGKGoalkeeping",
            "Follow our goalkeeper journey!",
            "Join our goalkeeper community",
            "Be part of the BGK family",
            "Watch our keepers grow 🧤"
        ],
        'Success Story': [
            "Your success story starts here 💪",
            "Be our next goalkeeper success",
            "Ready to transform your game?",
            "Join these successful keepers",
            "Start your journey today"
        ]
    },
    '360TFT': {
        'Educational': [
            "Join 1,200+ coaches at 360TFT.com",
            "More coaching tips @360TFT",
            "Transform your coaching today",
            "Follow for daily coaching insights",
            "Level up your coaching game"
        ],
        'Promotional': [
            "Join our coaching community!",
            "Start for just £8/month",
            "1,200+ coaches can't be wrong",
            "Join the revolution today",
            "Limited time offer - join now"
        ],
        'Behind-the-Scenes': [
            "Follow Kevin's coaching journey",
            "See how we built 800+ players",
            "Behind every great team...",
            "Join our coaching story",
            "Be part of something bigger"
        ],
        'Success Story': [
            "Your coaching success awaits",
            "Join these successful coaches",
            "Ready to transform your club?",
            "Start your success story",
            "Next success story: yours"
        ]
    },
    'Kit-Mart': {
        'Educational': [
            "Get your kit sorted at Kit-Mart",
            "Follow for kit tips & deals",
            "Quality kit for every team",
            "More at Kit-Mart.com",
            "Tag your team! 👕"
        ],
        'Promotional': [
            "Order your team kit today!",
            "Bulk discounts available",
            "Get a quote - link in bio",
            "Outfit your team now",
            "Special offers this month"
        ],
        'Behind-the-Scenes': [
            "See how we kit 600+ teams",
            "Quality control matters",
            "Behind every great kit...",
            "Follow our kit journey",
            "Trusted by clubs nationwide"
        ],
        'Success Story': [
            "Your team could be next",
            "Join these happy clubs",
            "Transform your team's look",
            "Be our next success",
            "Start your kit journey"
        ]
    },
    'CD Copland Motors': {
        'Educational': [
            "Book your MOT at CD Copland",
            "Follow for car care tips",
            "Trust the experts",
            "More tips @CDCoplandMotors",
            "Tag someone who needs this!"
        ],
        'Promotional': [
            "Book your service today!",
            "MOTs available now",
            "Call 01234 567890",
            "5-star service guaranteed",
            "Book online - link in bio"
        ],
        'Behind-the-Scenes': [
            "See why we're 5-star rated",
            "Quality you can trust",
            "Behind every great service...",
            "Follow for garage insights",
            "Monifieth's trusted garage"
        ],
        'Success Story': [
            "Join our happy customers",
            "Your car deserves the best",
            "Experience 5-star service",
            "Be our next review",
            "Trust the professionals"
        ]
    },
    'KF Barbers': {
        'Educational': [
            "Book at KF Barbers today",
            "Follow for grooming tips",
            "Looking sharp starts here",
            "More tips @KFBarbers",
            "Tag a mate who needs a trim!"
        ],
        'Promotional': [
            "Book your cut today!",
            "Walk-ins welcome",
            "Call 07449 761659",
            "Gift vouchers available",
            "Book on Fresha app"
        ],
        'Behind-the-Scenes': [
            "See why we're 4.9 rated",
            "Traditional barbering at its best",
            "Follow our barber journey",
            "Arbroath's finest cuts",
            "Join the KF family"
        ],
        'Success Story': [
            "Your fresh cut awaits",
            "Join 215+ happy customers",
            "Experience the difference",
            "Be our next 5-star review",
            "Start looking sharp today"
        ]
    },
    'Athlete Recovery Zone': {
        'Educational': [
            "Recover like a champion",
            "Follow for recovery tips",
            "Book your session today",
            "More at AthleteRecoveryZone",
            "Tag an athlete who needs this!"
        ],
        'Promotional': [
            "Book your recovery session!",
            "Membership deals available",
            "Start recovering properly",
            "Limited spots - book now",
            "Walk-ins welcome"
        ],
        'Behind-the-Scenes': [
            "See our recovery tech",
            "Where champions recover",
            "Follow our athlete journeys",
            "State-of-the-art facilities",
            "Join the recovery revolution"
        ],
        'Success Story': [
            "Your recovery starts here",
            "Join elite athletes",
            "Transform your performance",
            "Be our next success",
            "Recover. Perform. Repeat."
        ]
    }
}

def get_content_type(filename):
    """Determine content type from filename"""
    if 'Educational' in filename:
        return 'Educational'
    elif 'Promotional' in filename:
        return 'Promotional'
    elif 'Behind-the-Scenes' in filename:
        return 'Behind-the-Scenes'
    elif 'Success Story' in filename:
        return 'Success Story'
    return 'Educational'  # default

def fix_social_cta(file_path, business_name):
    """Replace long CTA with short, appropriate one"""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Skip summary files
        if 'SUMMARY' in file_path.name:
            return False
        
        # Get content type
        content_type = get_content_type(file_path.name)
        
        # Get appropriate CTAs for this business and type
        if business_name in BUSINESS_CTAS and content_type in BUSINESS_CTAS[business_name]:
            cta_options = BUSINESS_CTAS[business_name][content_type]
            # Use filename hash to consistently select same CTA for same file
            cta_index = hash(file_path.name) % len(cta_options)
            new_cta = cta_options[cta_index]
        else:
            new_cta = f"Learn more at {business_name}"
        
        # Find and replace the long CTA in shortform section
        shortform_pattern = r'(📱 SHORTFORM VERSION\n═+\n\n.*?)(Ready to.*?$)'
        
        def replace_cta(match):
            content_part = match.group(1)
            # Remove any trailing space/period and add new CTA
            content_part = content_part.rstrip('. ')
            return f"{content_part}. {new_cta}"
        
        fixed_content = re.sub(shortform_pattern, replace_cta, content, flags=re.MULTILINE | re.DOTALL)
        
        # Only write if we made changes
        if fixed_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            print(f"[FIXED] {file_path.name} -> {new_cta}")
            return True
        
        return False
        
    except Exception as e:
        print(f"[ERROR] {file_path}: {e}")
        return False

def main():
    """Fix all social media CTAs"""
    
    print("=" * 60)
    print("    SOCIAL MEDIA CTA FIXER")
    print("    Making CTAs Short, Varied, and Natural")
    print("=" * 60)
    
    base_dir = Path("Z:/Main Drive/360TFT Resources/Workflows/N8N/Content Factory Pro/Clients")
    
    total_fixed = 0
    
    for business_name in BUSINESS_CTAS.keys():
        business_dir = base_dir / business_name / "Aug_25"
        
        if not business_dir.exists():
            continue
        
        print(f"\nFixing {business_name}...")
        
        for txt_file in business_dir.glob("Aug_25_*.txt"):
            if fix_social_cta(txt_file, business_name):
                total_fixed += 1
    
    print(f"\n{'='*60}")
    print(f"COMPLETE! Fixed {total_fixed} files")
    print(f"All CTAs now short, varied, and natural for social media")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()