from enum import Enum

from pydantic import BaseModel
from typing import Optional


class Severity(Enum):
    ISSUE_HIGH = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4


class TicketCreate(BaseModel):
    title: str
    description: Optional[str]
    severity: Severity
