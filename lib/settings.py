from pydantic import BaseModel

class PxSettings(BaseModel):
    base_url: str
    username: str
    password: str
    server: str
    database: str
    project: str
    activity: str
