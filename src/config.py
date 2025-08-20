from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    DATABASE_URL: str = "postgres:///default.db"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )
    
Config =  Settings()