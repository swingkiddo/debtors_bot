import psycopg2

DB_NAME = "debtors"
DB_USER = "admin"
DB_PASSWORD = "admin"
DB_PORT = 5987
DB_HOST = "localhost"
REGISTERED_USERS_FILE = "registered_users"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)

def sync_data():
    with open(REGISTERED_USERS_FILE, "r") as registered_users:
        data = registered_users.readlines()
        if data:
            for line in data:
                with conn.cursor() as cur:
                    query = f"INSERT INTO users (telegram_id, username, first_name, last_name) VALUES (%s, %s, %s, %s)"
                    cur.execute(query, line.split(", "))
                    conn.commit()
                    print(f"User {line[1]} registered successfully")
