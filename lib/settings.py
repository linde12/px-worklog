from pydantic_settings import BaseSettings

class PxSettings(BaseSettings):
    base_url: str
    username: str
    password: str
    server: str
    database: str
    project: str
    activity: str
