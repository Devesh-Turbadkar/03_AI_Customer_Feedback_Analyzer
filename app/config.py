from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Customer Feedback Analyzer"
    database_url: str = "sqlite:///./feedback_analyzer.db"

    gemini_api_key: str = ""

    # Primary Gemini model
    gemini_model: str = "gemini-3.8-flash"

    # Backup Gemini model
    gemini_fallback_model: str = "gemini-3.5-flash"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()