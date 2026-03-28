from pydantic import BaseModel
from typing import List, Optional


class Project(BaseModel):
    id: str
    title: str
    description: str
    technologies: List[str]
    features: List[str]
    year: int
    github: Optional[str] = None
    demo: Optional[str] = None


class Skill(BaseModel):
    name: str
    level: int
    category: str


class Experience(BaseModel):
    title: str
    company: str
    location: str
    period: str
    current: bool
    responsibilities: List[str]
    technologies: List[str]
