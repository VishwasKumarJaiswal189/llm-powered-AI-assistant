from typing import List
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

from app.core.config import settings
from app.services.memory import get_session_history

# Schema for structured analysis
class StructuredAnalysis(BaseModel):
    summary: str = Field(description="A concise 1-sentence summary of the input.")
    key_points: List[str] = Field(description="List of key points or actionable takeaways.")
    sentiment: str = Field(description="Sentiment tone: positive, negative, or neutral.")
    confidence_score: float = Field(description="Model confidence score between 0.0 and 1.0.")

class LLMService:
    def __init__(self):
        # Base model initialization
        self.model = ChatOpenAI(
            model=settings.OPENROUTER_MODEL,
            api_key=settings.OPENROUTER_API_KEY,
            base_url=settings.OPENROUTER_BASE_URL,
            temperature=0.7,
            max_retries=2,
            timeout=30,
            default_headers={
                "HTTP-Referer": "http://localhost:8000",
                "X-Title": settings.APP_NAME,
            }
        )

        # Chat Prompt with history
        self.prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                "You are an intelligent, helpful AI assistant. "
                "Use the provided conversation history to maintain context and answer accurately."
            ),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])

        chain = self.prompt | self.model

        # Multi-turn history wrapper
        self.conversation = RunnableWithMessageHistory(
            chain,
            get_session_history,
            input_messages_key="input",
            history_messages_key="history",
        )

        # Structured Output Chain
        self.analysis_prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                "Analyze the provided text carefully and extract the requested structured fields."
            ),
            ("human", "{text}")
        ])
        structured_model = self.model.with_structured_output(StructuredAnalysis)
        self.structured_chain = self.analysis_prompt | structured_model

    def generate_response(self, message: str, session_id: str) -> str:
        response = self.conversation.invoke(
            {"input": message},
            config={"configurable": {"session_id": session_id}}
        )
        return response.content if isinstance(response.content, str) else str(response.content)

    def analyze_text(self, text: str) -> StructuredAnalysis:
        return self.structured_chain.invoke({"text": text})

llm_service = LLMService()