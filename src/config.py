from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    environment: str
    title: str = "user_management_service"
    debug: bool = False
    dc_ports: str
    db_port: str
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    database_url: str


settings = Settings()

