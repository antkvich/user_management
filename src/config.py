from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    postgres_password: str
    postgres_user: str
    environment: str
    title: str = "user_management_service"
    debug: bool = False
    dc_ports: str
    db_port: str
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    database_url: str
    jwt_access_token: str
    jwt_refresh_token: str
    alembic_ip: str
    alembic_port: str
    access_token_expire_minutes: int
    refresh_token_expire_minutes: int
    token_algorithm: str


settings = Settings()

