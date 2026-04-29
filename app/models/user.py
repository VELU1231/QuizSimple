from dataclasses import dataclass, field
from typing import Optional


@dataclass
class User:
    """
    Placeholder User model.
    Activate when auth is implemented (e.g., add SQLAlchemy columns here).
    """

    id: Optional[int] = None
    username: str = ""
    email: str = ""
    is_active: bool = False
    roles: list = field(default_factory=list)

    def is_authenticated(self) -> bool:
        return self.id is not None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_active": self.is_active,
        }
