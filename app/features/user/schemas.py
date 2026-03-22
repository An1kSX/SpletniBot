from dataclasses import dataclass
from typing import Optional
from aiogram.types import InlineKeyboardMarkup
from enum import Enum



@dataclass
class UserAccessResult:
    access: bool
    text: Optional[str] = None
    markup: Optional[InlineKeyboardMarkup] = None

class MenuOption(Enum):
    HELP = "Помощь"
    RECOGNITION = "Признание"
    RULES = "Правила"
    CHANGE_NICKNAME = "Смена никнейма"

    def equals(self, text: str) -> bool:
        return self.value.lower() == text.lower()