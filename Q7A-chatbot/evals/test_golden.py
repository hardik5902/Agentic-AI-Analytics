"""Golden-example evals: judge the bot's output against reference answers.

Covers 10 in-domain cases with expected answers.
"""

from conftest import get_review, judge_with_golden

GOLDEN_EXAMPLES = [
    {
        "name": "all_buzzwords_no_substance",
        "input": (
            "We're NexaCore. We're building a next-gen, cloud-native platform "
            "that harnesses quantum computing and generative AI to revolutionize "
            "the logistics space. Our TAM is $8 trillion. We have an incredible "
            "team of visionary entrepreneurs who are deeply passionate about "
            "transforming supply chains."
        ),
        "reference": (
            "STRENGTHS\n"
            "(None — no dimension is adequately addressed in this pitch.)\n\n"
            "WEAKNESSES\n"
            "- Dimension 1 (Clarity): \"next-gen, cloud-native platform that "
            "harnesses quantum computing and generative AI\" — jargon-heavy "
            "and vague. What does the product actually do for a user?\n"
            "- Dimension 2 (Market Size): \"TAM is $8 trillion\" — top-down "
            "claim with no bottom-up methodology or customer segment.\n"
            "- Dimension 3 (Traction): No mention of progress, users, or "
            "timeline.\n"
            "- Dimension 4 (Unique Insight): Missing entirely.\n"
            "- Dimension 5 (Business Model): Not addressed.\n"
            "- Dimension 6 (Team): \"visionary entrepreneurs\" and \"deeply "
            "passionate\" give no detail on roles, count, or credentials.\n"
            "- Dimension 7 (The Ask): Missing.\n\n"
            "OVERALL\n"
            "HIGH risk — buzzwords without substance across all dimensions."
        ),
    },
    {
        "name": "strong_pitch_all_covered",
        "input": (
            "We're MealBox. We deliver pre-portioned ingredients and 20-minute "
            "recipes to busy parents in the Bay Area. We launched 4 months ago. "
            "We have 1,200 weekly subscribers paying $49/week, growing 18% MoM. "
            "There are 2.1M households with children in the Bay Area; at $49/week "
            "our serviceable market is $5.3B annually. My co-founder and I spent "
            "6 months interviewing 200 parents — the pain is not 'what to cook' "
            "but 'how to cook in under 20 minutes with a toddler underfoot.' "
            "I'm a former ops lead at DoorDash; my co-founder is a full-stack "
            "engineer. We split equity 50/50, both full-time. We're raising a "
            "$1.5M seed to expand to LA and Portland."
        ),
        "reference": (
            "STRENGTHS\n"
            "- Dimension 1 (Clarity): Simple, concrete product description.\n"
            "- Dimension 2 (Market Size): Well-reasoned bottom-up estimate "
            "with a clear customer segment.\n"
            "- Dimension 3 (Traction): 1,200 subs and 18% MoM in 4 months.\n"
            "- Dimension 4 (Unique Insight): Customer-derived and specific.\n"
            "- Dimension 5 (Business Model): Clear subscription at $49/week.\n"
            "- Dimension 6 (Team): Relevant credentials, technical co-founder, "
            "equal equity, full-time.\n"
            "- Dimension 7 (The Ask): $1.5M seed with stated use of funds.\n\n"
            "WEAKNESSES\n"
            "(None — all seven dimensions are well covered.)\n\n"
            "OVERALL\n"
            "LOW risk — covers all dimensions with specificity and evidence."
        ),
    },
    {
        "name": "missing_market_insight_team",
        "input": (
            "ParkEasy is a mobile app that helps drivers find parking spots in "
            "real time. We show open spots on a map and let users reserve them. "
            "We launched in downtown Chicago 3 months ago with 8,000 monthly "
            "active users. We charge a $2 booking fee per reservation. "
            "We're raising $500K to expand to three more cities."
        ),
        "reference": (
            "STRENGTHS\n"
            "- Dimension 1 (Clarity): Clear and simple product description.\n"
            "- Dimension 3 (Traction): 8,000 MAU in 3 months in a single city.\n"
            "- Dimension 5 (Business Model): Simple $2 booking fee.\n"
            "- Dimension 7 (The Ask): $500K to expand to three cities.\n\n"
            "WEAKNESSES\n"
            "- Dimension 2 (Market Size): Missing. No quantified market.\n"
            "- Dimension 4 (Unique Insight): Not stated.\n"
            "- Dimension 6 (Team): No information on founders.\n\n"
            "OVERALL\n"
            "MEDIUM risk — strong clarity and traction, but missing market "
            "sizing, unique insight, and team."
        ),
    },
    {
        "name": "vague_insight_weak_model",
        "input": (
            "We're HealthTrack, a wearable for seniors that monitors vitals. "
            "There are 54 million Americans over 65. We've been working on this "
            "for 2 years. Healthcare is broken and we're going to fix it. "
            "We'll make money through partnerships, subscriptions, data licensing, "
            "and maybe insurance co-pays. Our team is amazing. We want to raise $3M."
        ),
        "reference": (
            "STRENGTHS\n"
            "- Dimension 1 (Clarity): \"wearable for seniors that monitors "
            "vitals\" is clear and understandable.\n"
            "- Dimension 7 (The Ask): Specific — $3M raise.\n\n"
            "WEAKNESSES\n"
            "- Dimension 2 (Market Size): \"54 million Americans over 65\" is "
            "top-down with no narrowing.\n"
            "- Dimension 3 (Traction): 2 years with no product milestones or "
            "user metrics.\n"
            "- Dimension 4 (Unique Insight): \"Healthcare is broken\" is too "
            "vague.\n"
            "- Dimension 5 (Business Model): Potpourri of revenue streams.\n"
            "- Dimension 6 (Team): \"amazing\" is not a credential.\n\n"
            "OVERALL\n"
            "HIGH risk — weak insight, scattered business model, and no "
            "evidence of progress despite 2 years."
        ),
    },
    {
        "name": "no_ask",
        "input": (
            "We're CodeReview AI. We built an AI tool that reviews pull requests "
            "and suggests fixes in real time. We target engineering teams of "
            "10-100 developers at mid-size SaaS companies. There are roughly "
            "50,000 such companies in the US. We charge $20 per developer per "
            "month. We launched 6 weeks ago with 12 paying teams. I'm a former "
            "staff engineer at GitHub; my co-founder was an ML researcher at "
            "Meta. We've known each other for 8 years, both full-time, 50/50 split. "
            "Current code review tools miss context across files — we index the "
            "full repo graph to understand cross-file dependencies."
        ),
        "reference": (
            "STRENGTHS\n"
            "- Dimension 1 (Clarity): Clear product description with user path.\n"
            "- Dimension 2 (Market Size): 50,000 target companies identified.\n"
            "- Dimension 3 (Traction): 12 paying teams in 6 weeks.\n"
            "- Dimension 4 (Unique Insight): Specific — cross-file dependency "
            "indexing vs. single-file tools.\n"
            "- Dimension 5 (Business Model): $20/dev/month SaaS.\n"
            "- Dimension 6 (Team): Relevant credentials (GitHub, Meta ML), "
            "8-year relationship, full-time, 50/50.\n\n"
            "WEAKNESSES\n"
            "- Dimension 7 (The Ask): Missing. What do you want — funding "
            "amount, intro, advice?\n\n"
            "OVERALL\n"
            "LOW risk — strong across six dimensions; adding a clear ask "
            "would complete it."
        ),
    },
    {
        "name": "no_traction_no_team",
        "input": (
            "We're Vetly, an online marketplace connecting pet owners with "
            "vetted, verified veterinarians for telehealth consultations. "
            "The US pet healthcare market is $35B and 67% of households own a pet. "
            "Our unique insight: pet owners delay vet visits because of anxiety "
            "about cost uncertainty — we solve this with upfront transparent "
            "pricing before the consult. We charge a $30 flat fee per session. "
            "We're raising $750K pre-seed."
        ),
        "reference": (
            "STRENGTHS\n"
            "- Dimension 1 (Clarity): Clear marketplace description.\n"
            "- Dimension 4 (Unique Insight): Specific — cost uncertainty "
            "drives delayed vet visits.\n"
            "- Dimension 5 (Business Model): Simple $30 flat fee.\n"
            "- Dimension 7 (The Ask): $750K pre-seed.\n\n"
            "WEAKNESSES\n"
            "- Dimension 2 (Market Size): \"$35B\" is top-down. How many pet "
            "owners would use telehealth specifically?\n"
            "- Dimension 3 (Traction): No mention of launch status, users, "
            "or timeline.\n"
            "- Dimension 6 (Team): No information on founders or capabilities.\n\n"
            "OVERALL\n"
            "MEDIUM risk — good clarity, insight, and model, but no traction "
            "evidence and no team info."
        ),
    },
    {
        "name": "strong_technical_pitch",
        "input": (
            "We're Synthera. We build synthetic data generation APIs for ML "
            "teams. You give us a schema and privacy constraints, we return "
            "statistically accurate synthetic datasets. There are 120,000 ML "
            "teams at enterprises worldwide; at $500/month our SAM is $720M. "
            "We launched our beta 8 weeks ago — 45 teams are using it, 18 are "
            "paying. Our insight: ML teams spend 40% of their time on data "
            "compliance, not modeling — we eliminate the compliance bottleneck "
            "entirely. I have a PhD in differential privacy from Stanford; "
            "my co-founder ran data infra at Snowflake. Both full-time, 55/45 "
            "split. We're raising a $2M seed to hire 3 engineers and expand "
            "enterprise sales."
        ),
        "reference": (
            "STRENGTHS\n"
            "- Dimension 1 (Clarity): Clear user path — schema in, synthetic "
            "data out.\n"
            "- Dimension 2 (Market Size): Bottom-up SAM of $720M from 120K "
            "ML teams.\n"
            "- Dimension 3 (Traction): 45 beta teams, 18 paying in 8 weeks.\n"
            "- Dimension 4 (Unique Insight): Specific and quantified — 40% "
            "of time on compliance.\n"
            "- Dimension 5 (Business Model): $500/month SaaS.\n"
            "- Dimension 6 (Team): Deeply relevant (PhD differential privacy, "
            "Snowflake data infra), full-time.\n"
            "- Dimension 7 (The Ask): $2M seed with clear use of funds.\n\n"
            "WEAKNESSES\n"
            "(None — all seven dimensions are well covered.)\n\n"
            "OVERALL\n"
            "LOW risk — comprehensive, evidence-backed pitch."
        ),
    },
    {
        "name": "empty_pitch_no_text",
        "input": "",
        "reference": (
            "No pitch text provided. Please paste your startup pitch and I'll "
            "scan it for strengths and weaknesses across the seven key dimensions."
        ),
    },
    {
        "name": "ask_for_help_prompt",
        "input": "What should a good pitch include?",
        "reference": (
            "A strong pitch addresses seven dimensions: (1) Clarity — what your "
            "company does in plain language, (2) Market Size — a bottom-up estimate, "
            "(3) Traction — progress relative to time, (4) Unique Insight — "
            "specific knowledge others lack, (5) Business Model — how you make "
            "money, (6) Team — founders and credentials, (7) The Ask — what you "
            "want. Paste your pitch and I'll scan it for strengths and weaknesses."
        ),
    },
    {
        "name": "corporate_jargon_overload",
        "input": (
            "We're SynergyFlow. We deliver end-to-end, omnichannel, cloud-native "
            "digital transformation solutions for enterprise stakeholders "
            "looking to maximize ROI across verticals. Our platform synergizes "
            "big data, IoT, and next-gen AI to drive paradigm shifts in how "
            "businesses operationalize their core competencies."
        ),
        "reference": (
            "STRENGTHS\n"
            "(None — no dimension is adequately addressed.)\n\n"
            "WEAKNESSES\n"
            "- Dimension 1 (Clarity): The entire pitch is jargon — "
            "\"end-to-end, omnichannel, cloud-native digital transformation "
            "solutions\" tells me nothing about what the product does.\n"
            "- Dimension 2 (Market Size): Missing.\n"
            "- Dimension 3 (Traction): Missing.\n"
            "- Dimension 4 (Unique Insight): \"paradigm shifts\" and \"core "
            "competencies\" are marketing speak, not insight.\n"
            "- Dimension 5 (Business Model): Not addressed.\n"
            "- Dimension 6 (Team): Missing.\n"
            "- Dimension 7 (The Ask): Missing.\n\n"
            "OVERALL\n"
            "HIGH risk — the pitch reads like a corporate brochure."
        ),
    },
]


def test_golden_examples():
    """Each bot response should score >= 6/10 against its golden reference."""
    print()
    ratings = []
    for example in GOLDEN_EXAMPLES:
        response = get_review(example["input"])
        rating = judge_with_golden(
            prompt=example["input"],
            reference=example["reference"],
            response=response,
        )
        ratings.append(rating)
        print(f"  {example['name']}: {rating}/10")
        assert rating >= 6, (
            f"[{example['name']}] Rating {rating}/10 — response: {response[:200]}"
        )
    print(f"  average: {sum(ratings) / len(ratings):.1f}/10")
