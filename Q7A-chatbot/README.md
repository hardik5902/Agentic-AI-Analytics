# PitchScan — Startup Pitch Risk Scanner

A domain Q&A chatbot that scans startup pitches for risks and gaps against Y Combinator's seven-dimension pitch framework. Paste your pitch and the bot identifies missing elements, weak claims, and red flags — without rewriting your pitch for you.

**Live URL**: *(add after deployment)*

## Topic

Early-stage startup pitch analysis. The bot evaluates pitches across seven dimensions derived from [YC's "How to Pitch Your Company"](https://www.ycombinator.com/library/4b-how-to-pitch-your-company):

1. **Clarity** — Is the company description simple and jargon-free?
2. **Market Size** — Is there a bottom-up market estimate with a defined customer segment?
3. **Traction** — Does the pitch show impressive progress relative to time spent?
4. **Unique Insight** — Is there a specific, customer-derived insight?
5. **Business Model** — Is the revenue model clear and singular?
6. **Team** — Are founders, roles, equity, and commitment covered?
7. **The Ask** — Is there a specific, actionable request?

## Prerequisites

Google Cloud with Vertex AI enabled. Create a `.env` file in this directory:

```
VERTEXAI_PROJECT=your-project-id
VERTEXAI_LOCATION=us-central1
```

## Running Locally

```bash
uv run python app.py
```

Open http://localhost:8000 in your browser.

## API

- `GET /` — Serves the PitchScan UI
- `POST /chat` — Send a pitch for risk analysis, returns scan results
- `POST /clear` — Clear session history

## Evals

The `evals/` directory contains pytest-based evaluations:

- `test_golden.py` — Judge bot responses against 10 golden reference answers
- `test_rubric.py` — Judge bot responses against weighted rubric criteria (10 cases)
- `test_rules.py` — Deterministic checks that the bot flags correct pitch dimensions and handles out-of-scope/safety cases

```bash
uv run pytest evals/ -v
```

Note: evals make live LLM calls to both the bot and a judge model, so they require network access and will incur API costs.
