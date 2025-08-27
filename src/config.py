from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    DATABASE_URL: str = "postgres:///default.db"
    JWT_SECRET:str = "secret"
    JWT_ALGORITHM:str = "H256"
    REDIS_HOST:str = "localhost"
    REDIS_PORT:int = 6379
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )
    
Config =  Settings()