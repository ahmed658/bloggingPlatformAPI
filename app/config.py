from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    
    database_hostname: str
    database_name: str
    database_port: str
    database_username:str
    database_password: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    root_pass: str
    
    model_config = SettingsConfigDict(env_file=".env")
    
settings = Settings()