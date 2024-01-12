from typing import List
from .debt import Debt

class AppUser:
    def __init__(self, telegram_id: int, username: str, first_name: str, last_name: str, debts: List[Debt], friends: List):
        self.telegram_id = telegram_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.debts = debts
        self.friends = friends

    def __str__(self):
        return self.username
    
    def __repr__(self) -> str:
        return self.username
