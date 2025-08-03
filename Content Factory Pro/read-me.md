Features:

  - Reads any content-strategy.csv file from your business automation
  - Generates posts for 5 platforms: Facebook, Instagram, Twitter, LinkedIn, TikTok
  - Respects platform limits: Character counts, hashtag limits
  - Creates platform-specific content: Professional for LinkedIn, visual for Instagram, concise for Twitter
  - Outputs to organized markdown files

  How It Works:

  # From any business folder:
  python ../automation/social_media_generator.py content-strategy.csv

  # Or specify custom output folder:
  python ../automation/social_media_generator.py content-strategy.csv ./social_posts

  Output Structure:

  social_media_posts/
  ├── facebook_posts.md
  ├── instagram_posts.md
  ├── twitter_posts.md
  ├── linkedin_posts.md
  ├── tiktok_posts.md
  └── content_calendar.md

  What You Get:

  - Platform-specific posts optimized for each social network
  - Copy-paste ready content with proper formatting
  - Character count tracking to ensure posts fit platform limits
  - Intelligent hashtag generation based on content type and keywords
  - Content calendar overview showing distribution across platforms

  Content Types Supported:

  - Educational (40%) - Tips, insights, how-tos
  - Product Highlight (25%) - Service features, benefits
  - Problem & Solution (25%) - Address pain points
  - Community & Stories (10%) - Success stories, testimonials

  Each post type has unique templates and hooks optimized for engagement. The generator automatically creates 12 posts per
  business (matching your content strategy CSV) across all platforms.

  Would you like me to show you how to integrate this with your existing workflow or modify any specific aspects?

> Can you please show me, imagine there's a new business needing onboarding, what is the step-by-step process?

● Absolutely! Let me walk you through the complete step-by-step process for onboarding a new business from start to finish.

  Complete Business Onboarding Process

  Step 1: Create Business Folder Structure

  # Navigate to Clients folder
  cd "Content Factory Pro/Clients"

  # Create new business folder
  mkdir "New Business Name"
  cd "New Business Name"

  Step 2: Create submission.md File

  Create a submission.md file with the client's information:
  # Business Submission Form

  **Business Name:** New Business Name
  **Your Name:** John Smith
  **Phone:** (555) 123-4567
  **Email:** john@newbusiness.com
  **Website:** https://www.newbusiness.com

  **What Does Your Business Do:**
  We provide premium landscaping services for residential and commercial properties, specializing in sustainable garden design
  and maintenance.

  **Target Audience:**
  Homeowners aged 35-65 with household income $75k+, commercial property managers, and eco-conscious clients seeking sustainable
  landscaping solutions.

  **Brand Voice Guidelines:**
  Professional yet approachable, environmentally conscious, expertise-focused. We emphasize sustainability, quality
  craftsmanship, and long-term relationships.

  **Social Media:**
  Facebook, Instagram, LinkedIn

  **Content Brief:**
  Focus on seasonal landscaping tips, before/after transformations, sustainable gardening practices, and client success stories.
  Highlight our expertise and environmental commitment.

  **SEO Keywords:**
  landscaping services, sustainable gardening, landscape design, eco-friendly landscaping, commercial landscaping

  Step 3: Run Automated Processing

  # From the business folder, run the automation
  python ../../Code\ Files/Claude-Code-Configs/automation/content_factory_automation.py

  What happens automatically:
  - ✅ Parses the submission.md file
  - ✅ Conducts business research and competitive analysis
  - ✅ Generates business-config.csv with all business details
  - ✅ Creates content-strategy.csv with 12 monthly content pieces
  - ✅ Exports research-notes.md with market insights
  - ✅ Adds business to Notion database (or updates if exists)

  Step 4: Generate Social Media Posts

  # Generate social media content from the strategy CSV
  python ../../Code\ Files/Claude-Code-Configs/automation/social_media_generator.py content-strategy.csv

  This creates:
  New Business Name/
  ├── submission.md
  ├── business-config.csv
  ├── content-strategy.csv
  ├── research-notes.md
  └── social_media_posts/
      ├── facebook_posts.md
      ├── instagram_posts.md
      ├── twitter_posts.md
      ├── linkedin_posts.md
      ├── tiktok_posts.md
      └── content_calendar.md

  Step 5: Review Generated Content

  business-config.csv contains:
  - Business ID, category, contact details
  - Target audience and brand voice
  - Website and social platform info
  - All data formatted for Notion database

  content-strategy.csv contains:
  - 12 content pieces for the month
  - 5 Educational posts (40%)
  - 3 Product Highlight posts (25%)
  - 3 Problem & Solution posts (25%)
  - 1 Community & Stories post (10%)

  social_media_posts/ folder contains:
  - Platform-optimized posts for each content piece
  - Character count tracking
  - Copy-paste ready content
  - Hashtag suggestions

  Step 6: Verify Notion Integration

  Check your Notion database - the business should appear with:
  - Auto-assigned ID number
  - Categorized properly (e.g., "Home Services")
  - All contact and business details populated
  - Status set to "Active"

  Step 7: Quality Check & Customization

  1. Review generated content for accuracy
  2. Customize social media posts with specific business details
  3. Verify research notes align with business goals
  4. Update any placeholder content with real information

  Complete Folder Structure After Processing:

  Clients/New Business Name/
  ├── submission.md                    # Client input
  ├── business-config.csv              # Business data for systems
  ├── content-strategy.csv             # Monthly content plan
  ├── research-notes.md                # Market analysis
  └── social_media_posts/
      ├── facebook_posts.md            # 12 Facebook posts
      ├── instagram_posts.md           # 12 Instagram posts
      ├── twitter_posts.md             # 12 Twitter posts
      ├── linkedin_posts.md            # 12 LinkedIn posts
      ├── tiktok_posts.md              # 12 TikTok posts
      └── content_calendar.md          # Overview & calendar

  Total Time:

  - Manual work: ~5 minutes (create folder + submission.md)
  - Automated processing: ~30 seconds
  - Review & customization: ~10-15 minutes
