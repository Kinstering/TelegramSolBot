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
        # Ensure types are correct
        user_id = str(user_id)
        private_key = str(private_key)
        public_key = str(public_key)
        
        print(f"Adding user: user_id={user_id} (type: {type(user_id)}), private_key={private_key} (type: {type(private_key)}), public_key={public_key} (type: {type(public_key)})")
        
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO users (user_id, private_key, public_key) VALUES (?, ?, ?)", 
                (user_id, private_key, public_key)
            )


    def get_public_key(self, user_id):
        with self.connection:
            result = self.cursor.execute('SELECT public_key FROM users WHERE user_id = ?', (user_id,)).fetchone()
            return result[0] if result else None

    def get_private_key(self, user_id):
        with self.connection:
            result = self.cursor.execute('SELECT private_key FROM users WHERE user_id = ?', (user_id,)).fetchone()
            return result[0] if result else None