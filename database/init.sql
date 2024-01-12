CREATE TABLE "users" (
    telegram_id INTEGER PRIMARY KEY NOT NULL,
    username VARCHAR(30) UNIQUE,
    first_name VARCHAR(15),
    last_name VARCHAR(15)
);

CREATE TABLE "debts" (
    id SERIAL PRIMARY KEY,
    borrower_id INTEGER,
    debtor_id INTEGER,
    amount INTEGER,
    deadline DATE
);

ALTER TABLE "debts" ADD FOREIGN KEY (borrower_id) REFERENCES "users"(telegram_id);
ALTER TABLE "debts" ADD FOREIGN KEY (debtor_id) REFERENCES "users"(telegram_id);
