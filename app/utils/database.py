import pyodbc
from app import db_path


class get_db:
    def __init__(self):
        self.conn = pyodbc.connect(
            r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + db_path + ";"
        )
        self.cursor = self.conn.cursor()

    def __enter__(self):
        return self

    def close(self):
        self.__exit__(None, None, None)

    def commit(self):
        self.conn.commit()

    def __exit__(self, _a, _b, _c):
        self.cursor.close()
        del self.cursor
        self.conn.close()
        del self.conn
