"""Rubric-based evals: judge the bot's output against weighted criteria.

Covers 10 cases with a pitch-analysis-specific rubric.
"""

import json

from conftest import get_review, judge_with_rubric

RUBRIC = json.dumps(
    [
        {
            "title": "Identifies missing pitch dimensions",
            "description": "Essential: correctly flags which of the 7 YC pitch dimensions are missing or weak, citing dimension names.",
            "weight": 5,
        },
        {
            "title": "Quotes or references specific phrases",
            "description": "Important: quotes the specific phrases from the pitch that are problematic or notes their absence.",
            "weight": 3,
        },
        {
            "title": "Analysis only — no rewriting",
            "description": "Essential: response contains only risk analysis and does not rewrite the user's pitch.",
            "weight": 5,
        },
        {
            "title": "Provides a risk severity rating",
            "description": "Important: includes an overall risk assessment with LOW, MEDIUM, or HIGH severity.",
            "weight": 3,
        },
        {
            "title": "Recognizes a strong pitch",
            "description": "Important: when a pitch covers all dimensions well, acknowledges strengths rather than inventing risks.",
            "weight": 3,
        },
        {
            "title": "Avoids false positives",
            "description": "Pitfall: does not flag dimensions that are adequately addressed in the pitch.",
            "weight": -3,
        },
    ]
)

INPUTS = [
    {
        "name": "heavy_jargon_pitch",
        "input": (
            "We leverage proprietary NLP to create a synergistic omnichannel "
            "platform that disrupts the B2B2C space for enterprise stakeholders."
        ),
    },
    {
        "name": "solid_all_dimensions",
        "input": (
            "We're FarmLink. We connect small organic farms directly with "
            "restaurants via a mobile ordering app. Launched 5 months ago in "
            "Portland with 85 farms and 120 restaurants. Revenue is $40K/month "
            "growing 22% MoM. We charge farms a 12% commission. There are "
            "18,000 organic farms within delivery range of major metro areas — "
            "our SAM is $180M. Our insight: farms lose 30% of produce to "
            "middlemen spoilage — direct routing cuts waste and improves margins "
            "for both sides. I managed supply chain at Whole Foods for 6 years; "
            "my CTO built logistics systems at Instacart. Both full-time, 50/50. "
            "We're raising $1M to expand to Seattle and Denver."
        ),
    },
    {
        "name": "no_business_model",
        "input": (
            "We're StudyBuddy, an AI tutor for high school students. We help "
            "students practice math by generating personalized problem sets. "
            "We have 15,000 monthly active users after 3 months. Our founders "
            "are both former math teachers with 20 years combined experience. "
            "We're raising $400K."
        ),
    },
    {
        "name": "passion_not_insight",
        "input": (
            "We're GreenRide. Electric scooter sharing is the future of urban "
            "mobility. We're so passionate about sustainability. The market is "
            "huge — everyone needs transportation. We know in our hearts this "
            "will work."
        ),
    },
    {
        "name": "potpourri_revenue",
        "input": (
            "We're EventFlow, an event management platform. We'll make money "
            "through ticket sales commissions, sponsorship matching, VIP "
            "upsells, merchandise, NFT tickets, data analytics licensing, "
            "and premium support tiers. We're 2 months old."
        ),
    },
    {
        "name": "strong_but_no_ask",
        "input": (
            "We're DataClean. We build a one-click data anonymization API for "
            "healthcare companies. HIPAA compliance takes healthcare startups "
            "an average of 6 months — we do it in 6 minutes. We have 28 paying "
            "customers at $200/month. There are 12,000 digital health startups "
            "in the US. My co-founder and I are both former compliance engineers "
            "at Epic Systems. Full-time, 50/50 equity."
        ),
    },
    {
        "name": "missing_clarity_and_insight",
        "input": (
            "We're disrupting the future of work with our platform. "
            "There are 60 million freelancers in the US. We charge $10/month. "
            "We launched 2 months ago with 500 users. Our 3 founders are all "
            "full-time, equal equity. We're raising $600K."
        ),
    },
    {
        "name": "top_down_market_only",
        "input": (
            "We're PetPal, a subscription box for dog toys. The US pet industry "
            "is $150 billion. We assume we can capture 0.1% of that. "
            "We launched last month."
        ),
    },
    {
        "name": "team_name_drops",
        "input": (
            "We're TalentAI. We use AI to match job candidates with employers. "
            "Our team includes graduates from Harvard, Stanford, and MIT. "
            "We have 4.0 GPAs and worked at Google, Meta, and Amazon. "
            "We're raising $2M."
        ),
    },
    {
        "name": "single_founder_risk",
        "input": (
            "I'm building FinBot, a personal finance chatbot. I'm working on "
            "this part-time while keeping my day job. I've been developing it "
            "for 18 months. I haven't launched yet but the idea is solid. "
            "I'm looking for a technical co-founder."
        ),
    },
]


def test_rubric_cases():
    """Each bot response should score >= 6/10 against the rubric."""
    print()
    ratings = []
    for case in INPUTS:
        response = get_review(case["input"])
        rating = judge_with_rubric(
            prompt=case["input"],
            response=response,
            rubric=RUBRIC,
        )
        ratings.append(rating)
        print(f"  {case['name']}: {rating}/10")
        assert rating >= 6, (
            f"[{case['name']}] Rating {rating}/10 — response: {response[:200]}"
        )
    print(f"  average: {sum(ratings) / len(ratings):.1f}/10")
