from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    environment: str
    db_url: str
    title: str = "user_management_service"
    debug: bool = False
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    
