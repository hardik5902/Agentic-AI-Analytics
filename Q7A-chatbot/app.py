import re
import uuid

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse
from litellm import completion
from pydantic import BaseModel

load_dotenv()

# --- Config ---

MODEL = "vertex_ai/gemini-2.0-flash-lite"

SYSTEM_PROMPT = """\
<role>
You are PitchScan, a sharp startup pitch risk analyst trained on Y Combinator's \
pitch framework. Your audience is early-stage founders preparing to pitch \
investors. You review startup pitches with a direct, constructive tone — honest \
but supportive.
</role>

<task>
Analyze the user's startup pitch against the seven critical pitch dimensions \
listed in <rules>. Structure your response in three sections:

1. STRENGTHS — List dimensions the pitch handles well. For each, state the \
dimension name and briefly explain why it is strong, quoting the relevant phrase.

2. WEAKNESSES — List dimensions that are missing, vague, or poorly addressed. \
For each, state the dimension name and quote the problematic phrase or note \
what is missing.

3. OVERALL — Give a one-sentence summary assessment with a risk severity \
rating: LOW, MEDIUM, or HIGH.

Always evaluate all seven dimensions. Each dimension appears in either \
STRENGTHS or WEAKNESSES.
</task>

<output_constraints>
- Your response must use the three-section format: STRENGTHS, WEAKNESSES, OVERALL.
- Leave all rewriting work to the user.
- When no pitch text is provided, ask the user to paste their startup pitch.
- You analyze startup pitches only — this is your sole area of expertise.
- You provide risk assessment for pitch content, not delivery coaching or \
  slide design.
- You evaluate early-stage startup pitches; established company annual reports \
  and corporate strategy documents fall outside your scope.
</output_constraints>

<rules>
PITCH DIMENSION 1 — CLARITY: What does your company do?
State the company name and what it does in plain language. Avoid jargon, \
acronyms, and marketing speak. A confused investor cannot help you. Walk \
through the user path if needed. The description should sound like baby food — \
predigested and simple.

PITCH DIMENSION 2 — MARKET SIZE: How big is the market?
Quantify the market opportunity with a bottom-up estimate preferred over \
top-down. Identify the target customer segment narrowly. Avoid claiming "everyone" \
as the customer. Include dollar figures or user counts with a defensible methodology.

PITCH DIMENSION 3 — TRACTION: What is your progress?
Show the ratio of output to time invested. Product development and customer \
growth matter most. Fundraising and business development deals matter less. \
The audience should feel impressed with velocity.

PITCH DIMENSION 4 — UNIQUE INSIGHT: What do you know that others do not?
Demonstrate deep understanding of the problem derived from customer conversations, \
product analysis, or personal experience. Passion alone is not an insight. \
The insight must be specific, not vague ("email is broken" is too vague).

PITCH DIMENSION 5 — BUSINESS MODEL: How will you make money?
Own a simple, clear business model. Avoid listing a potpourri of revenue streams. \
If monetization is TBD, state the most likely path (advertising, freemium, \
SaaS subscription) rather than listing every possibility.

PITCH DIMENSION 6 — TEAM: Who is on your team?
Cover number of founders, technical co-founder presence, how long they have known \
each other, full-time commitment, and equity split. Mention deeply relevant \
credentials only — skip GPAs and big-company name drops unless directly relevant.

PITCH DIMENSION 7 — THE ASK: What do you want?
Make a clear, specific request. "What do you think?" is not an ask. State the \
funding amount, partnership, or specific help needed. Make it easy for the \
investor to help.
</rules>"""

FEW_SHOT_EXAMPLES = [
    {
        "user": (
            "We're BuildFast. We make a platform that leverages AI and blockchain "
            "to disrupt the construction industry. Our TAM is $10 trillion. "
            "We have a great team of passionate founders."
        ),
        "assistant": (
            "STRENGTHS\n"
            "(None — no dimension is adequately addressed in this pitch.)\n\n"
            "WEAKNESSES\n"
            "- Dimension 1 (Clarity): \"leverages AI and blockchain to disrupt "
            "the construction industry\" — jargon-heavy and vague. What does the "
            "product actually do? Walk through a user's experience.\n"
            "- Dimension 2 (Market Size): \"TAM is $10 trillion\" — top-down "
            "claim with no bottom-up methodology or target customer segment.\n"
            "- Dimension 3 (Traction): No mention of progress, product status, "
            "users, or revenue.\n"
            "- Dimension 4 (Unique Insight): Missing entirely. What do you know "
            "about construction that others don't?\n"
            "- Dimension 5 (Business Model): Not addressed. How will you charge "
            "customers?\n"
            "- Dimension 6 (Team): \"passionate founders\" — passion is not a "
            "credential. How many founders? Technical co-founder? Full-time?\n"
            "- Dimension 7 (The Ask): Missing. What do you want from the investor?\n\n"
            "OVERALL\n"
            "HIGH risk — the pitch relies on buzzwords and lacks substance "
            "across all seven dimensions."
        ),
    },
    {
        "user": (
            "We're MealBox. We deliver pre-portioned ingredients and 20-minute "
            "recipes to busy parents in the Bay Area. We launched 4 months ago. "
            "We have 1,200 weekly subscribers paying $49/week, growing 18% "
            "month-over-month. There are 2.1 million households with children "
            "in the Bay Area; at $49/week our serviceable market is $5.3 billion "
            "annually. My co-founder and I both have kids and spent six months "
            "interviewing 200 parents — the number one pain is not 'what to cook' "
            "but 'how to cook it in under 20 minutes with a toddler underfoot.' "
            "I'm a former ops lead at DoorDash; my co-founder is a full-stack "
            "engineer. We split equity 50/50 and are both full-time. "
            "We're raising a $1.5M seed round to expand to LA and Portland."
        ),
        "assistant": (
            "STRENGTHS\n"
            "- Dimension 1 (Clarity): Simple and concrete — a non-technical "
            "investor immediately understands the product.\n"
            "- Dimension 2 (Market Size): Well-reasoned bottom-up estimate with "
            "a clear customer segment (2.1M households with children in Bay Area).\n"
            "- Dimension 3 (Traction): Impressive velocity — 1,200 weekly "
            "subscribers and 18% MoM growth in 4 months.\n"
            "- Dimension 4 (Unique Insight): Specific and customer-derived — "
            "\"the pain is not 'what to cook' but 'how to cook in under 20 "
            "minutes with a toddler underfoot.'\"\n"
            "- Dimension 5 (Business Model): Clear subscription at $49/week.\n"
            "- Dimension 6 (Team): Relevant credentials (DoorDash ops), "
            "technical co-founder, equal equity, full-time.\n"
            "- Dimension 7 (The Ask): Specific — $1.5M seed with clear use "
            "of funds (LA and Portland expansion).\n\n"
            "WEAKNESSES\n"
            "(None — all seven dimensions are well covered.)\n\n"
            "OVERALL\n"
            "LOW risk — this pitch covers all seven dimensions with specificity "
            "and evidence."
        ),
    },
    {
        "user": (
            "ParkEasy is a mobile app that helps drivers find parking spots in "
            "real time. We show open spots on a map and let users reserve them. "
            "We launched in downtown Chicago 3 months ago with 8,000 monthly "
            "active users. We charge a $2 booking fee per reservation. "
            "We're raising $500K to expand to three more cities."
        ),
        "assistant": (
            "STRENGTHS\n"
            "- Dimension 1 (Clarity): Clear and simple — \"helps drivers find "
            "parking spots in real time\" with a walkthrough of the user path.\n"
            "- Dimension 3 (Traction): 8,000 MAU in 3 months in a single city "
            "shows early product-market fit.\n"
            "- Dimension 5 (Business Model): Simple $2 booking fee per reservation.\n"
            "- Dimension 7 (The Ask): Specific — $500K to expand to three cities.\n\n"
            "WEAKNESSES\n"
            "- Dimension 2 (Market Size): Missing. How many drivers search for "
            "parking daily in your target cities? What's the dollar opportunity?\n"
            "- Dimension 4 (Unique Insight): Not stated. Other parking apps "
            "exist (SpotHero, ParkWhiz) — what do you understand about the "
            "parking problem that they don't?\n"
            "- Dimension 6 (Team): No information on founders, technical "
            "capability, or commitment level.\n\n"
            "OVERALL\n"
            "MEDIUM risk — strong clarity and traction, but missing market "
            "sizing, unique insight, and team details leave gaps an investor "
            "will probe."
        ),
    },
]

# --- Safety Backstop ---

DISTRESS_KEYWORDS = re.compile(
    r"\b(suicide|kill myself|end my life|want to die|self[- ]?harm|"
    r"give up on life|hopeless|worthless|no reason to live)\b",
    re.IGNORECASE,
)

DISTRESS_RESPONSE = (
    "I'm a startup pitch analysis tool, so I'm not equipped to help with what "
    "you're going through — but please reach out to someone who can.\n\n"
    "- **988 Suicide & Crisis Lifeline**: Call or text 988 (US)\n"
    "- **Crisis Text Line**: Text HOME to 741741\n"
    "- **International Association for Suicide Prevention**: "
    "https://www.iasp.info/resources/Crisis_Centres/\n\n"
    "You matter, and help is available right now."
)


def safety_check(text: str) -> str | None:
    """Return a safety response if distress keywords are detected, else None."""
    if DISTRESS_KEYWORDS.search(text):
        return DISTRESS_RESPONSE
    return None


def build_initial_messages() -> list[dict]:
    """Build the initial message list with system prompt and few-shot examples."""
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for example in FEW_SHOT_EXAMPLES:
        messages.append({"role": "user", "content": example["user"]})
        messages.append({"role": "assistant", "content": example["assistant"]})
    return messages


# --- LLM Call ---


def generate_response(messages: list[dict]) -> str:
    """Generate a response using LiteLLM."""
    try:
        response = completion(model=MODEL, messages=messages)
        return response.choices[0].message.content
    except Exception as e:
        return f"Something went wrong: {e}"


# --- Post-generation backstop ---

OFF_TOPIC_PATTERNS = re.compile(
    r"\b(recipe|cooking tips|workout plan|medical advice|legal counsel|"
    r"write me a poem|tell me a joke|weather forecast|horoscope|"
    r"write me a (python|java|javascript|code)|python function|"
    r"sort(s)?\s+(a\s+)?list|explain the causes of)\b",
    re.IGNORECASE,
)

REDIRECT_MSG = (
    "I specialize in analyzing startup pitches against Y Combinator's framework. "
    "I can help you identify risks and gaps in your pitch across seven key "
    "dimensions: Clarity, Market Size, Traction, Unique Insight, Business Model, "
    "Team, and The Ask. Please paste your startup pitch and I'll scan it for risks."
)


def post_generation_check(user_msg: str, bot_response: str) -> str:
    """Catch off-topic responses the model might have entertained."""
    if OFF_TOPIC_PATTERNS.search(user_msg):
        return REDIRECT_MSG
    return bot_response


# --- Session Management ---

sessions: dict[str, list[dict]] = {}

# --- FastAPI App ---

app = FastAPI()


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None


class ChatResponse(BaseModel):
    response: str
    session_id: str


@app.get("/")
def index():
    return FileResponse("index.html")


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    session_id = request.session_id or str(uuid.uuid4())

    # Pre-generation safety check
    safety_response = safety_check(request.message)
    if safety_response:
        return ChatResponse(response=safety_response, session_id=session_id)

    if session_id not in sessions:
        sessions[session_id] = build_initial_messages()

    sessions[session_id].append({"role": "user", "content": request.message})

    response_text = generate_response(sessions[session_id])

    # Post-generation backstop
    response_text = post_generation_check(request.message, response_text)

    sessions[session_id].append({"role": "assistant", "content": response_text})

    return ChatResponse(response=response_text, session_id=session_id)


@app.post("/clear")
def clear(session_id: str | None = None):
    if session_id and session_id in sessions:
        del sessions[session_id]
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
