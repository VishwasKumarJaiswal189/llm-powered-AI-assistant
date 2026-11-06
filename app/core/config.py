from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    OPENROUTER_API_KEY: str
    OPENROUTER_MODEL: str = "openrouter/free"
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    APP_NAME: str = "LLM-Powered-AI-Assistant"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()