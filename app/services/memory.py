import os
from langchain_community.chat_message_histories import SQLChatMessageHistory

DB_DIR = "data"
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = f"sqlite:///{DB_DIR}/chat_history.db"

def get_session_history(session_id: str) -> SQLChatMessageHistory:
    """Retrieve or create persistent SQLite history for a session."""
    return SQLChatMessageHistory(
        session_id=session_id,
        connection=DB_PATH,
        table_name="message_store"
    )

def get_formatted_history(session_id: str) -> list[dict]:
    """Return serialized conversation history."""
    history = get_session_history(session_id)
    return [
        {"role": msg.type, "content": msg.content}
        for msg in history.messages
    ]