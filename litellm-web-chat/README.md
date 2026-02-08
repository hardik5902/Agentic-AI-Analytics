# LiteLLM Web Chat

Build a web chatbot powered by Gemini on Vertex AI using LiteLLM.

## Prerequisites

Before starting this exercise, complete the **Google Cloud & Vertex AI Setup Guide** to:

1. Access Google Cloud with your Columbia account
2. Create a GCP project and enable the Vertex AI API
3. Install and configure the `gcloud` CLI with your project
4. Set up Application Default Credentials

No additional configuration needed - the app will use your gcloud settings automatically.

## Background

In the previous exercise, you built a web chatbot using a local TinyLlama model. Now you'll connect to a hosted model (Gemini) through Vertex AI using LiteLLM.

LiteLLM provides a unified interface to 100+ LLM providers. You write OpenAI-style code, and LiteLLM translates it to whatever format the provider expects.

## What's Provided

- `index.html` - Complete frontend (no changes needed)
- `app.py` - FastAPI server with session management (you complete the TODOs)
- `pyproject.toml` - Dependencies (includes `litellm[google]` with Vertex AI support)

## Your Task

Complete the TODOs in `app.py`:

1. **Import**: Add `from litellm import completion`
2. **Model**: Set `MODEL = "vertex_ai/gemini-2.0-flash-lite"`
3. **Generate**: Call `completion(model=MODEL, messages=messages)` and return the response

## The OpenAI Message Format

LiteLLM (and most hosted APIs) use a list of message dictionaries:

```python
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"},
    {"role": "assistant", "content": "Hi there! How can I help?"},
    {"role": "user", "content": "What's 2+2?"},
]
```

This replaces the raw prompt string format we used with TinyLlama. The session management in `app.py` already builds this list for you.

## Run It

```bash
uv run python app.py
```

Open http://localhost:8000. The first request may take a few seconds as it authenticates with Vertex AI.

## Troubleshooting

**"Your default credentials were not found"**

Run `gcloud auth application-default login` and complete the browser authentication. Make sure to check ALL permission boxes.

**"Could not find project" or project-related errors**

Make sure your project is set in gcloud:

```bash
gcloud config set project YOUR-PROJECT-ID
```

Verify it's set correctly:

```bash
gcloud config get-value project
```

**"Permission denied" or "API not enabled"**

Verify the Vertex AI API is enabled in your GCP project.
