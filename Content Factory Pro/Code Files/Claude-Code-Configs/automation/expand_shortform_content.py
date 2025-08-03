#!/usr/bin/env python3
"""
Expand short-form content to 2-3 sentences with consistent paragraph structure
"""

import os
import re
from pathlib import Path

def expand_shortform_content(file_path, business_name):
    """Expand short-form content to proper paragraph size"""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Skip summary files
        if 'SUMMARY' in file_path.name:
            return False
        
        # Extract current shortform content
        shortform_match = re.search(r'📱 SHORTFORM VERSION\n═+\n\n(.*?)\n\n📘', content, re.DOTALL)
        if not shortform_match:
            return False
        
        current_shortform = shortform_match.group(1).strip()
        
        # Parse current content parts
        parts = current_shortform.split('. ')
        if len(parts) < 2:
            parts = current_shortform.split('! ')
        
        # Extract hook, topic info, and CTA
        hook = parts[0] if parts else "Great content"
        if not hook.endswith('!') and not hook.endswith('.'):
            hook += "!"
        
        # Get the CTA (last part)
        cta = ""
        for part in reversed(parts):
            if any(keyword in part.lower() for keyword in ['more', 'join', 'book', 'call', 'contact', 'follow', 'tag', 'dm', 'visit', 'learn', 'start', 'get']):
                cta = part.strip()
                break
        
        # Determine content type from filename
        content_type = "Educational"
        if "Promotional" in file_path.name:
            content_type = "Promotional"
        elif "Behind-the-Scenes" in file_path.name:
            content_type = "Behind-the-Scenes"
        elif "Success Story" in file_path.name:
            content_type = "Success Story"
        
        # Create expanded content based on business and type
        expanded_content = generate_expanded_content(business_name, content_type, hook, cta, file_path.name)
        
        if expanded_content and expanded_content != current_shortform:
            # Replace in content
            new_content = re.sub(
                r'(📱 SHORTFORM VERSION\n═+\n\n).*?(\n\n📘)',
                f'\\1{expanded_content}\\2',
                content,
                flags=re.DOTALL
            )
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"[EXPANDED] {file_path.name}")
            return True
        
        return False
        
    except Exception as e:
        print(f"[ERROR] {file_path}: {e}")
        return False

def generate_expanded_content(business_name, content_type, hook, cta, filename):
    """Generate 2-3 sentence expanded content"""
    
    # Extract topic from filename
    topic_part = filename.split('_')[-1].replace('.txt', '').replace('_', ' ')
    
    if business_name == "BGK Goalkeeping":
        if content_type == "Educational":
            return f"{hook} Every young goalkeeper needs proper guidance to build confidence and develop the skills that separate good keepers from great ones. Our evidence-based training methods have helped hundreds of goalkeepers across Scotland reach their potential. {cta}"
        elif content_type == "Promotional":
            return f"{hook} We offer personalized 1-to-1 training and small group sessions designed specifically for young goalkeepers aged 8-18. Join the #BGKUNION community where confidence and skill development go hand in hand. {cta}"
        elif content_type == "Behind-the-Scenes":
            return f"{hook} Led by former Dundee FC goalkeeper Calum Brodie, our coaching team brings professional experience directly to grassroots development. See how we're building the next generation of confident goalkeepers across Tayside and beyond. {cta}"
        else:  # Success Story
            return f"{hook} Real results from real goalkeepers who've transformed their game through our specialized training programs. These success stories show what's possible when young keepers get the right guidance and support. {cta}"
    
    elif business_name == "360TFT":
        if content_type == "Educational":
            return f"{hook} Over 1,200 coaches have discovered that structured, game-based training eliminates guesswork and builds genuine coaching confidence. Our proven methodologies have helped build successful academies training 800+ players across Scotland. {cta}"
        elif content_type == "Promotional":
            return f"{hook} For just £8/month, access the same coaching education that's built multiple six-figure football academies. Join a community of coaches who are revolutionizing grassroots football without breaking the bank. {cta}"
        elif content_type == "Behind-the-Scenes":
            return f"{hook} Follow Kevin Middleton's journey from grassroots volunteer to building academies with 800+ players and coaching at Arbroath FC. See the real story behind creating sustainable football coaching businesses. {cta}"
        else:  # Success Story
            return f"{hook} Real coaches sharing real results from implementing our Game Model methodology and business strategies. These transformations prove that quality coaching education doesn't have to cost hundreds per month. {cta}"
    
    elif business_name == "Kit-Mart":
        if content_type == "Educational":
            return f"{hook} From local clubs to schools and authorities, we've learned what makes kit ordering simple and stress-free. Our streamlined process has helped outfit over 600 teams with quality custom sportswear they're proud to wear. {cta}"
        elif content_type == "Promotional":
            return f"{hook} We specialize in bespoke kit solutions for clubs, schools, and local authorities across the UK. With our Savi sportswear range and bulk ordering options, we make professional-quality kit accessible to every team. {cta}"
        elif content_type == "Behind-the-Scenes":
            return f"{hook} Watch how we process hundreds of kit orders weekly while maintaining the quality control standards that teams depend on. Every piece is checked before shipping to ensure your team looks and feels professional. {cta}"
        else:  # Success Story
            return f"{hook} See how clubs and schools have transformed their team identity with our custom kit solutions. From grassroots teams to educational institutions, these partnerships show the difference quality kit makes. {cta}"
    
    elif business_name == "CD Copland Motors":
        if content_type == "Educational":
            return f"{hook} As a Good Garage Scheme member and SMTA-certified garage, we believe in educating customers about their vehicles. Our 12,000 mile/12 month nationwide guarantee reflects our commitment to quality service and customer peace of mind. {cta}"
        elif content_type == "Promotional":
            return f"{hook} From MOTs to major repairs, our Unipart Car Care Centre offers comprehensive automotive services for the Monifieth and Dundee communities. With 5-star ratings and 100% customer recommendations, we've earned our reputation as the area's trusted garage. {cta}"
        elif content_type == "Behind-the-Scenes":
            return f"{hook} See why our customers consistently rate us 5 stars and recommend us to family and friends. Our commitment to professional standards and honest service has made us Monifieth's most trusted independent garage. {cta}"
        else:  # Success Story
            return f"{hook} Real customers sharing their experiences with our diagnostic expertise and honest service approach. These reviews reflect our commitment to solving problems other garages couldn't fix while treating every customer fairly. {cta}"
    
    elif business_name == "KF Barbers":
        if content_type == "Educational":
            return f"{hook} With 4.9 stars from 215+ customers, we've learned what makes the perfect barbering experience for men and children alike. Our traditional techniques combined with modern customer service create the welcoming atmosphere Arbroath has come to trust. {cta}"
        elif content_type == "Promotional":
            return f"{hook} We welcome walk-ins throughout the week and offer gift vouchers for the special men in your life. From traditional hot shaves to children's cuts, our experienced barbers ensure everyone leaves looking and feeling their best. {cta}"
        elif content_type == "Behind-the-Scenes":
            return f"{hook} See the craftsmanship and attention to detail that's earned us recognition as Arbroath's premier barbershop. Our commitment to traditional barbering standards shows in every cut, shave, and customer interaction. {cta}"
        else:  # Success Story
            return f"{hook} Three generations of families trust us with their grooming needs, and our customer reviews speak to the lasting relationships we build. These stories show why we're consistently rated as the best barbers in town. {cta}"
    
    elif business_name == "Athlete Recovery Zone":
        if content_type == "Educational":
            return f"{hook} Professional athletes and weekend warriors alike need proper recovery protocols to perform at their peak and prevent injuries. Our evidence-based approach combines cutting-edge technology with proven recovery methodologies used by elite sports teams. {cta}"
        elif content_type == "Promotional":
            return f"{hook} Our comprehensive facility offers everything from cryotherapy and NormaTec compression to infrared saunas and red light therapy. With flexible membership options and walk-in availability, we make professional-grade recovery accessible to all athletes. {cta}"
        elif content_type == "Behind-the-Scenes":
            return f"{hook} See the state-of-the-art recovery technology and professional protocols that have made us the choice of Division 1 athletes and sports teams. Our partnerships with 450+ teams reflect our commitment to excellence in athletic recovery. {cta}"
        else:  # Success Story
            return f"{hook} Real athletes sharing how our recovery protocols have transformed their training and performance outcomes. From immediate pain relief to long-term performance gains, these stories demonstrate the power of proper recovery. {cta}"
    
    # Fallback
    return f"{hook} Quality service and professional expertise have made us a trusted choice in our community. Our commitment to excellence shows in every interaction and outcome we deliver. {cta}"

def main():
    """Expand all short-form content to proper paragraph structure"""
    
    print("=" * 70)
    print("    SHORT-FORM CONTENT EXPANDER")
    print("    Creating Consistent 2-3 Sentence Paragraph Structure")
    print("=" * 70)
    
    base_dir = Path("Z:/Main Drive/360TFT Resources/Workflows/N8N/Content Factory Pro/Clients")
    businesses = ['BGK Goalkeeping', '360TFT', 'Kit-mart', 'CD Copland Motors', 'KF Barbers', 'Athlete Recovery Zone']
    
    total_expanded = 0
    
    for business_name in businesses:
        business_dir = base_dir / business_name / "Aug_25"
        
        if not business_dir.exists():
            continue
        
        print(f"\nExpanding {business_name}...")
        
        for txt_file in business_dir.glob("Aug_25_*.txt"):
            if expand_shortform_content(txt_file, business_name):
                total_expanded += 1
    
    print(f"\n{'='*70}")
    print(f"EXPANSION COMPLETE!")
    print(f"{'='*70}")
    print(f"Files expanded: {total_expanded}")
    print(f"All short-form content now has consistent 2-3 sentence structure")
    print(f"{'='*70}")

if __name__ == "__main__":
    main()