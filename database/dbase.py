import sqlite3

class Database:
    def __init__(self, db_name: str = "main.db"):
        self.database = db_name

    def execute(self, sql, *args, commit=False, fetchone=False, fetchall=False):
        with sqlite3.connect(self.database) as db:
            cursor = db.cursor()
            cursor.execute(sql, args)
            result = None
            if commit:
                db.commit()
            if fetchall:
                result = cursor.fetchall()
            if fetchone:
                result = cursor.fetchone()
        return result

    # --- USERS ---
    def create_table_users(self):
        sql = '''CREATE TABLE IF NOT EXISTS users(
            telegram_id INTEGER NOT NULL UNIQUE,
            full_name TEXT,
            phone_number VARCHAR(13)
        )'''
        self.execute(sql, commit=True)

    def insert_telegram_id(self, telegram_id):
        sql = '''INSERT INTO users(telegram_id) VALUES (?)'''
        self.execute(sql, telegram_id, commit=True)

    def get_user(self, telegram_id):
        sql = '''SELECT * FROM users WHERE telegram_id = ?'''
        return self.execute(sql, telegram_id, fetchone=True)

    def save_phone_number_and_full_name(self, full_name, phone_number, telegram_id):
        sql = '''UPDATE users SET full_name = ?, phone_number = ? WHERE telegram_id = ?'''
        self.execute(sql, full_name, phone_number, telegram_id, commit=True)

    # --- GENRES ---
    def create_table_genres(self):
        sql = '''CREATE TABLE IF NOT EXISTS genres(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )'''
        self.execute(sql, commit=True)

    def insert_genre(self, name):
        sql = '''INSERT INTO genres(name) VALUES (?)'''
        self.execute(sql, name, commit=True)

    def get_genres(self):
        sql = '''SELECT * FROM genres'''
        return self.execute(sql, fetchall=True)

    def get_genre(self, id):
        sql = '''SELECT * FROM genres WHERE id=?'''
        return self.execute(sql, id, fetchone=True)

    def update_genre(self, name, id):
        sql = '''UPDATE genres SET name=? WHERE id=?'''
        self.execute(sql, name, id, commit=True)

    def delete_genre(self, id):
        sql = '''DELETE FROM genres WHERE id=?'''
        self.execute(sql, id, commit=True)

    def get_genre_by_id(self, id):
        sql = '''SELECT * FROM genres WHERE id = ?'''
        return self.execute(sql, id, fetchone=True)

    def get_genre_id_by_name(self, genre_name):
        sql = "SELECT id FROM genres WHERE name = ?"
        return self.execute(sql, genre_name, fetchone=True)


    # --- BOOKS ---
    def create_table_books(self):
        sql = '''CREATE TABLE IF NOT EXISTS books(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            info TEXT,
            genre_id INTEGER REFERENCES genres(id)
        )'''
        self.execute(sql, commit=True)

    def insert_book(self, title, author, info, genre_id):
        sql = '''INSERT INTO books(title, author, info, genre_id) VALUES (?, ?, ?, ?)'''
        self.execute(sql, title, author, info, genre_id, commit=True)

    def get_books_by_genre(self, genre_id, offset=0, limit=10):
        sql = '''SELECT id, title, author FROM books 
                 WHERE genre_id = ? LIMIT ? OFFSET ?'''
        return self.execute(sql, genre_id, limit, offset, fetchall=True)

    def count_books_by_genre(self, genre_id):
        sql = '''SELECT COUNT(*) FROM books WHERE genre_id = ?'''
        result = self.execute(sql, genre_id, fetchone=True)
        return result[0] if result else 0

    def get_books(self, offset=0, limit=10):
        sql = '''SELECT id, title, author FROM books LIMIT ? OFFSET ?'''
        return self.execute(sql, limit, offset, fetchall=True)

    def count_books(self):
        sql = '''SELECT COUNT(*) FROM books'''
        result = self.execute(sql, fetchone=True)
        return result[0] if result else 0

    def get_book_details(self, book_id):
        sql = '''SELECT title, author, info FROM books WHERE id = ?'''
        return self.execute(sql, book_id, fetchone=True)

    def get_book_by_title_author(self, title, author):
        sql = "SELECT * FROM books WHERE title = ? AND author = ?"
        return self.execute(sql, title, author, fetchone=True)

    def update_book(self, book_id, title, author, info):
        sql = "UPDATE books SET title = ?, author = ?, info = ? WHERE id = ?"
        self.execute(sql, title, author, info, book_id, commit=True)

    def delete_book(self, id):
        sql = '''DELETE FROM books WHERE id=?'''
        self.execute(sql, id, commit=True)

    # --- IMAGES ---
    def create_table_image(self):
        sql = '''CREATE TABLE IF NOT EXISTS images(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image TEXT,
            book_id INTEGER REFERENCES books(id)
        )'''
        self.execute(sql, commit=True)

    def insert_image(self, image, book_id):
        sql = '''INSERT INTO images(image, book_id) VALUES (?, ?)'''
        self.execute(sql, image, book_id, commit=True)

    def count_images(self, book_id):
        sql  = '''SELECT count(id) FROM images WHERE book_id = ?'''
        return self.execute(sql, book_id, fetchone=True)[0]

    def select_image_by_pagination(self, book_id, offset, limit):
        sql = '''SELECT id, image FROM images WHERE book_id = ? LIMIT ? OFFSET ?'''
        return self.execute(sql, book_id, limit, offset, fetchone=True)

    def get_book_image(self, book_id):
        sql = '''SELECT image FROM images WHERE book_id = ? LIMIT 1'''
        return self.execute(sql, book_id, fetchone=True)