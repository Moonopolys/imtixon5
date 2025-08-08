import sqlite3


class Database:
    def __init__(self, db_name: str = "main.db"):
        self.database = db_name

    def execute(self, sql, *args, commit: bool = False, fetchone: bool = False, fetchall: bool = False):
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