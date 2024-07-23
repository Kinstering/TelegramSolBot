import sqlite3
from datetime import datetime, timedelta

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
    
    # USERS TABLE
    
    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)).fetchall()
            return bool(len(result))
    
    def add_user(self, user_id, private_key, public_key):
        with self.connection:
            return self.cursor.execute("INSERT INTO users (user_id, private_key, public_key) VALUES (?, ?, ?)", (user_id, private_key, public_key,))

    