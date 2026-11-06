from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from app.services.llm import llm_service, StructuredAnalysis
from app.services.memory import get_formatted_history

app = FastAPI(
    title="LLM Powered AI Assistant (OpenRouter)",
    description="Conversational AI backend with SQLite persistence, structured outputs, and Web UI.",
    version="1.2.0"
)

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=10000)
    session_id: str = Field(default="default_session")

class ChatResponse(BaseModel):
    session_id: str
    response: str

class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=5, max_length=10000)

class MessageItem(BaseModel):
    role: str
    content: str

class HistoryResponse(BaseModel):
    session_id: str
    messages: list[MessageItem]

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        reply = llm_service.generate_response(request.message, request.session_id)
        return ChatResponse(session_id=request.session_id, response=reply)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"OpenRouter API error: {str(exc)}")

@app.post("/chat/structured", response_model=StructuredAnalysis)
def analyze(request: AnalyzeRequest):
    try:
        return llm_service.analyze_text(request.text)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Structured extraction error: {str(exc)}")

@app.get("/history/{session_id}", response_model=HistoryResponse)
def get_history(session_id: str):
    history = get_formatted_history(session_id)
    return HistoryResponse(session_id=session_id, messages=history)

@app.get("/", response_class=HTMLResponse)
def serve_ui():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI Assistant</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-900 text-slate-100 flex flex-col h-screen font-sans">
        <header class="p-4 bg-slate-800 border-b border-slate-700 flex justify-between items-center">
            <h1 class="text-lg font-bold text-sky-400">LLM AI Assistant</h1>
            <div class="flex items-center gap-2">
                <span class="text-xs text-slate-400">Session:</span>
                <input id="sessionId" type="text" value="session-1" class="bg-slate-700 text-xs px-2 py-1 rounded text-white border border-slate-600 focus:outline-none">
            </div>
        </header>

        <main id="chatWindow" class="flex-1 overflow-y-auto p-4 space-y-4 max-w-3xl mx-auto w-full">
            <div class="bg-slate-800 p-3 rounded-lg border border-slate-700 max-w-md text-sm">
                Hello! I am your AI assistant. How can I help you today?
            </div>
        </main>

        <footer class="p-4 bg-slate-800 border-t border-slate-700">
            <form id="chatForm" class="max-w-3xl mx-auto flex gap-2">
                <input id="userInput" type="text" placeholder="Type a message..." autocomplete="off" class="flex-1 bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-sm focus:outline-none focus:border-sky-500">
                <button type="submit" class="bg-sky-500 hover:bg-sky-600 text-white px-4 py-2 rounded-lg text-sm font-medium transition">Send</button>
            </form>
        </footer>

        <script>
            const form = document.getElementById('chatForm');
            const input = document.getElementById('userInput');
            const sessionInput = document.getElementById('sessionId');
            const chatWindow = document.getElementById('chatWindow');

            function appendMessage(role, text) {
                const bubble = document.createElement('div');
                bubble.className = role === 'user' 
                    ? 'bg-sky-600 text-white p-3 rounded-lg max-w-md ml-auto text-sm'
                    : 'bg-slate-800 text-slate-100 p-3 rounded-lg border border-slate-700 max-w-md text-sm';
                bubble.innerText = text;
                chatWindow.appendChild(bubble);
                chatWindow.scrollTop = chatWindow.scrollHeight;
            }

            form.addEventListener('submit', async (e) => {
                e.preventDefault();
                const msg = input.value.trim();
                const session = sessionInput.value.trim() || 'default';
                if (!msg) return;

                appendMessage('user', msg);
                input.value = '';

                try {
    const res = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: msg, session_id: session })
    });
    const data = await res.json();
    if (!res.ok) {
        appendMessage('ai', `Error (${res.status}): ${data.detail || 'Request failed'}`);
    } else {
        appendMessage('ai', data.response || '[Empty response received]');
    }
} catch (err) {
    appendMessage('ai', `Network Error: ${err.message}`);
}
            });
        </script>
    </body>
    </html>
    """