from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class User:
    _id: str
    email: str
    password: str
    confirmed: bool
    confirmed_on: datetime
    books: list[dict] = field(default_factory=list)
    pages: list[dict] = field(default_factory=list)
