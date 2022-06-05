from pydantic import BaseSettings


class Settings(BaseSettings):
    # database config
    database_hostname: str
    database_port: str
    database_username: str
    database_password: str
    database_name: str

    # JWT auth config
    auth_secret_key: str
    auth_algorithm_type: str
    auth_expiration_in_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()
