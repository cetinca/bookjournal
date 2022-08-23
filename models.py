from dataclasses import dataclass, field


@dataclass
class User:
    _id: str
    email: str
    password: str
    books: list[dict] = field(default_factory=list)
    pages: list[dict] = field(default_factory=list)
