import sqlite3

def init_db():
    with sqlite3.connect('subscriptions.db') as db:
        db.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, subscribed INTEGER DEFAULT 0)''')

if __name__ == '__main__':
    init_db()
