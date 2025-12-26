from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Repo(BaseModel):
    id: int
    name: str
    full_name: str
    stargazers_count: int
    forks_count: int
    language: Optional[str]
    created_at: datetime
    updated_at: datetime
