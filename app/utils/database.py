import pyodbc
from app import db_path


class get_db:
    def __init__(self):
        return None

    def __enter__(self):
        self.conn = pyodbc.connect(
            r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + db_path + ";"
        )
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, _a, _b, _c):
        self.cursor.close()
        self.conn.close()
