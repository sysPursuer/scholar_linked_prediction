import sqlite3

class ScholarDB(object):
    """
    sqlite3 backed scholar storage
    """
    def __init__(self,db_path="./processed/scholars.db"):
        super().__init__()
        self.path = db_path