from datetime import date

class Debt:
    def __init__(self, borrower, debtor, ammount: int, deadline: date):
        self.borrower = borrower
        self.debtor = debtor
        self.amount = ammount
        self.deadline = deadline

    def __repr__(self) -> str:
        deadline = f"{self.deadline.day}-{self.deadline.month}-{self.deadline.year}"
        return f"{self.debtor} занял у {self.borrower} {self.amount} рублей до {self.deadline.isoformat()}"