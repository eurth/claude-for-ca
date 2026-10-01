from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=(_ROOT / ".env", ".env"), extra="ignore")

    app_name: str = "for-ca"
    environment: str = "development"
    api_port: int = 8000
    web_origin: str = "http://localhost:3000"
    jwt_secret: str = "dev-only-change-me"
    jwt_hours: int = 12
    database_url: str = "sqlite:///./data/forca.db"
    data_dir: Path = Path("./data")
    packs_dir: Path = Path("./packs")

    seed_firm_name: str = "Gorantla Associates"
    seed_ca_name: str = "CA Butchi Babu"
    seed_partner_email: str = "partner@gorantla.local"
    seed_partner_password: str = "changeme"
    seed_hitl_threshold: int = 100_000

    llm_provider: str = "mock"
    anthropic_api_key: str = ""
    openai_api_key: str = ""
    gemini_api_key: str = ""
    openrouter_api_key: str = ""
    llm_model_low: str = ""
    llm_model_high: str = ""
    openrouter_site_url: str = "http://127.0.0.1:3000"
    openrouter_app_name: str = "for-ca"


settings = Settings()
settings.data_dir.mkdir(parents=True, exist_ok=True)
