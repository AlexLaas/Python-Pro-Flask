
import sqlite3
from datetime import datetime

class Database():
    def __init__(self, db_path):
        self.connection = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def select_projects(self):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM projects").fetchall()
            if len(result) < 1:
                return False #Вернет False, если записи в таблице не найдены:
            return result

    def insert_projects(self, title, description, image_name):
        with self.connection:
            return self.cursor.execute("INSERT INTO projects VALUES (NULL, ?, ?, ?)", (title, description, image_name))

    def delete_project(self, id):
        with self.connection:
            return self.cursor.execute("DELETE FROM projects WHERE id=?", (id,))

    def select_reviews(self):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM reviews").fetchall()
            if len(result) < 1:
                return False #Вернет False, если записи в таблице не найдены:
            return result

    def insert_reviews(self, author, text, email):
        time_now = datetime.now().strftime("%d.%m.%Y")
        with self.connection:
            return self.cursor.execute("INSERT INTO reviews VALUES (NULL, ?, ?, ?, ?)", (text, author, email, time_now,))

    def delete_reviews(self, id):
        with self.connection:
            return self.cursor.execute("DELETE FROM reviews WHERE id=?", (id,))
