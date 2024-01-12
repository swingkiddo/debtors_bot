from typing import List
from telegram import User
from models import AppUser
from database import conn


REGISTERED_USERS_FILE="registered_users"

class AppUserManager:
    def __init__(self, users: List[AppUser], db):
        self.users = users
        self.db = db
        if not self.users:
            self.init_users()

    def auth_user(self, user: User):
        registered_ids = [user.telegram_id for user in self.users]
        if user.id not in registered_ids:
            self.register_user(user)
            registered_ids.append(user.id)
        return self.users[registered_ids.index(user.id)]

    def register_user(self, user: User):
        with self.db.cursor() as cur:
            query = "INSERT INTO users (telegram_id, username, first_name, last_name) VALUES (%s, %s, %s, %s)"
            cur.execute(query, (user.id, user.username, user.first_name, user.last_name))
            conn.commit()
            self.add_user(user)
            print(f"User with telegram_id {user.id} registered succesfully")

    def init_users(self):
        with self.db.cursor() as cur:
            cur.execute("SELECT * FROM users;")
            users = cur.fetchall()
            for user in users:
                id, username, first_name,  last_name = user
                u = AppUser(
                    telegram_id=id, username=username, first_name=first_name, last_name=last_name, debts=[], friends=[]
                )
                self.users.append(u)
        print(f"REGISTERED USERS: {self.users}")

    def add_user(self, user: User):
        app_user = AppUser(
            telegram_id=user.id, 
            username=user.username, 
            first_name=user.first_name,
            last_name=user.last_name,
            debts=[], friends=[]
        )
        self.users.append(app_user)
    
    def get_user_by_id(self, id: int) -> AppUser|None:
        filtered = [user for user in self.users if user.telegram_id == id]
        return filtered[0] if filtered else None
    
app_users : List[AppUser] = []
user_manager = AppUserManager(users=app_users, db=conn)