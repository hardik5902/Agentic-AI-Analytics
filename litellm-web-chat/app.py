import uuid

import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

# TODO: Import the completion function from litellm

# --- Config ---

# TODO: Set the model name for Vertex AI Gemini
# Format: "vertex_ai/<model-name>"
# Use: gemini-2.0-flash-lite
MODEL = "TODO"

SYSTEM_PROMPT = "You are a helpful assistant. Be concise and friendly."


# --- LLM Call ---


def generate_response(messages: list[dict]) -> str:
    """Generate a response using LiteLLM.

    Args:
        messages: List of message dicts with 'role' and 'content' keys.
                  Example: [{"role": "user", "content": "Hello!"}]

    Returns:
        The assistant's response text.
    """
    # TODO: Call litellm.completion() with:
    #   - model=MODEL
    #   - messages=messages
    # Then extract and return the response text from:
    #   response.choices[0].message.content

    return "I AM A DUMB CHATBOT. Please implement generate_response()!"


# --- Session Management ---

# Each session stores a list of messages in OpenAI format:
# [
#     {"role": "system", "content": "You are a helpful assistant."},
#     {"role": "user", "content": "Hello!"},
#     {"role": "assistant", "content": "Hi there!"},
#     ...
# ]
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
    # Get or create session
    session_id = request.session_id or str(uuid.uuid4())
    if session_id not in sessions:
        # Start with the system prompt
        sessions[session_id] = [{"role": "system", "content": SYSTEM_PROMPT}]

    # Add user message to conversation
    sessions[session_id].append({"role": "user", "content": request.message})

    # Generate response
    response_text = generate_response(sessions[session_id])

    # Add assistant response to conversation history
    sessions[session_id].append({"role": "assistant", "content": response_text})

    return ChatResponse(response=response_text, session_id=session_id)


@app.post("/clear")
def clear(session_id: str | None = None):
    if session_id and session_id in sessions:
        del sessions[session_id]
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
