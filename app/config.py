from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Google Gemini API key
    gemini_api_key: str = ""

    # Gemini model
    gemini_model: str = "gemini-3.8-flash"

    # Application settings
    debug: bool = True

    # Optional local explanation model
    local_explanation: bool = False

    # Maximum input size
    max_input_chars: int = 20000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


# Create the settings object
settings = Settings()
def get_settings():
    return settings